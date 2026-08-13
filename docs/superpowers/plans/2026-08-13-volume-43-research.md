# Volume 43 Research Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the verified *Communal Societies* source audit from volumes 1-42 through volume 43 without changing Joel's published article.

**Architecture:** Recover the 37 inventoried volume-43 PDFs from the journal's two primary-publisher issue pages, identify every download by its saved SHA-256 rather than its browser filename, preserve page boundaries in extracted text, and reuse the locked volume-42 discovery families. Close-read all 29 nonmetadata sources, promote only materially distinct findings, reconcile the existing 18-item gap bank, then update and independently verify every cumulative artifact. Git stores reusable workflow and research artifacts; copyrighted sources and full-text derivatives remain local.

**Tech Stack:** Python 3 standard library, Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`), browser-backed publisher downloads, CSV/Markdown ledgers, Git, GitHub.

## Global Constraints

- Primary mode is **P0 research/source audit only**. Do not edit article prose.
- Do not repeat volumes 1-42; begin with `M-0046` and volume 43.
- Process all **37 PDFs**: 20 in issue 1 and 17 in issue 2.
- Close-read all 29 nonmetadata sources: 8 research articles, 18 book reviews, and 3 book notes. The inventory's broad `kind=article` label includes the three publication-designated book notes. Metadata-triage `M-0046`, `M-0047`, `M-0048`, `M-0065`, `M-0066`, `M-0067`, `M-0081`, and `M-0082`.
- Preserve Joel's argument. Evidence may update research ledgers but cannot silently weaken, replace, or expand article claims.
- Separate source fact, participant allegation, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, and external-verification needs.
- Treat discovery scores only as reading-order aids, never as evidence weights.
- A bounded dangerous-child null is not a historical claim of absence.
- Do not diagnose historical actors with ASPD or psychopathy without appropriate clinical evidence.
- Preserve D-003's historical `COMMUNAL-SOCIETIES-v41-v45.zip` provenance. This checkpoint verifies volume-43 publisher members; it must not pretend to reverify an absent archive container.
- A book review supports only the reviewer's direct report or evaluation unless the reviewed book itself is inspected.
- Keep copyrighted PDFs, extracted full text, visual renders, and context dumps out of Git.
- Redact private Drive object identifiers in every public repository artifact.
- Base branch is `agent/volume-42-research`; publish the completed checkpoint on `agent/volume-43-research`.

---

### Task 1: Recover and authenticate the volume 43 corpus

**Files:**
- Create: `recovered/test_v43_workflow.py`
- Create: `recovered/recover_v43.py`
- Create locally only: `recovered/corpus-v43/vol43/iss1/*.pdf`
- Create locally only: `recovered/corpus-v43/vol43/iss2/*.pdf`

**Interfaces:**
- Consumes: the 37 volume-43 inventory rows and PDFs downloaded from the two primary ScholarWorks issue pages.
- Produces: an idempotent hash-routed corpus in which every `M-0046` through `M-0082` PDF exists at its inventoried path and matches its saved SHA-256.

- [x] **Step 1: Write the failing recovery tests**

```python
def test_inventory_loader_maps_exact_volume_43_boundary():
    destinations = load_volume_43_destinations(INVENTORY, corpus)
    assert len(destinations) == 37
    assert sum("/iss1/" in path.as_posix() for path in destinations.values()) == 20
    assert sum("/iss2/" in path.as_posix() for path in destinations.values()) == 17
    assert all(path.is_relative_to(corpus / "vol43") for path in destinations.values())

def test_route_downloads_uses_saved_hash_instead_of_browser_name():
    routed = route_downloads([source], {expected_hash: destination})
    assert routed == [destination]
    assert destination.read_bytes() == payload
```

The first test catches loading the wrong volume, issue split, destination root, or a partial/duplicate boundary. The second catches any filename-based routing regression.

- [x] **Step 2: Run the tests and confirm RED**

```bash
python -m unittest recovered/test_v43_workflow.py -v
```

Expected: import failure because `recover_v43.py` does not exist.

- [x] **Step 3: Implement minimal hash routing and corpus validation**

Create `recover_v43.py` by reusing the proven generic routing helpers and adding this exact boundary loader:

```python
if __package__:
    from recovered.recover_v40 import route_downloads, sha256, verify_corpus
else:
    from recover_v40 import route_downloads, sha256, verify_corpus

def load_volume_43_destinations(inventory: Path = DEFAULT_INVENTORY,
                                corpus: Path = DEFAULT_CORPUS) -> dict[str, Path]:
    with inventory.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if row["volume"] == "43"]
    if len(rows) != 37:
        raise ValueError(f"expected 37 volume 43 inventory rows, found {len(rows)}")
    if Counter(row["issue"] for row in rows) != Counter({"1": 20, "2": 17}):
        raise ValueError("expected 20 volume 43 rows in issue 1 and 17 in issue 2")
    destinations = {
        row["sha256"]: corpus / Path(row["internal_filename"]).relative_to("archive")
        for row in rows
    }
    if len(destinations) != 37:
        raise ValueError("volume 43 inventory contains duplicate member hashes")
    return destinations
```

Expose `--downloads`, `--verify`, and `--allow-incomplete` command-line behavior.

- [x] **Step 4: Run the recovery tests and confirm GREEN**

```bash
python -m unittest recovered/test_v43_workflow.py -v
python recovered/recover_v43.py --allow-incomplete
```

Expected: all recovery tests pass while `--allow-incomplete` reports exactly 37 missing members.

- [x] **Step 5: Retrieve all 37 primary-publisher PDFs**

Use the PDF links on both verified issue pages:

```text
https://scholarworks.gvsu.edu/communalsocieties/vol43/iss1/
https://scholarworks.gvsu.edu/communalsocieties/vol43/iss2/
```

Compare the two live publisher listings with all 37 inventory records. Rate-limit retrieval and retry transient WAF or skipped-download responses conservatively. Route every downloaded file through the saved-hash map; never infer identity from its browser filename.

- [x] **Step 6: Verify hashes, page counts, extraction, and visible first pages**

Run `recover_v43.py --verify`, compare `pdfinfo` page counts with inventory, extract page-preserving text with `pdftotext -layout`, render first-page PNGs with `pdftoppm`, and inspect a contact sheet for title or identity failures before analysis.

### Task 2: Build and prove the volume 43 discovery boundary

**Files:**
- Modify: `recovered/test_v43_workflow.py`
- Create: `recovered/discover_v43.py`
- Create: `recovered/V43-DISCOVERY-RANKING.csv`
- Create locally only: `recovered/v43-keyword-contexts.txt`
- Create locally only: `recovered/v43-child-danger-contexts.txt`

**Interfaces:**
- Consumes: all 37 extracted volume-43 texts and inventory metadata.
- Produces: a complete ranking, contextual keyword excerpts, and bounded child-as-dangerous-actor candidates.

- [x] **Step 1: Add failing discovery-output and vocabulary-lock tests**

```python
def test_volume_43_discovery_outputs_cover_every_inventory_row():
    rows = load_csv(RANKING)
    assert len(rows) == 37
    assert {row["record_id"] for row in rows} == EXPECTED_VOLUME_43_IDS
    assert KEYWORD_CONTEXTS.is_file()
    assert CHILD_CONTEXTS.is_file()

def test_ranking_preserves_term_and_process_families():
    assert literal_assignment(ROOT / "discover_v43.py", "FAMILIES") == \
           literal_assignment(ROOT / "discover_v42.py", "FAMILIES")
    assert literal_assignment(ROOT / "discover_v43.py", "PROCESS_FAMILIES") == \
           literal_assignment(ROOT / "discover_v42.py", "PROCESS_FAMILIES")
```

These tests catch incomplete coverage and any silent widening or narrowing of the locked search vocabulary.

- [x] **Step 2: Run the tests and confirm RED**

```bash
python -m unittest recovered/test_v43_workflow.py -v
```

Expected: failure because the volume-43 discovery script and outputs do not exist.

- [x] **Step 3: Implement discovery from the locked volume-42 families**

Copy the exact danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome regex literals. Change only paths, record IDs, volume boundary, functional classification, and display labels. Preserve form-feed page boundaries and deterministic sorting.

- [x] **Step 4: Run discovery and confirm GREEN**

```bash
python recovered/discover_v43.py
python -m unittest recovered/test_v43_workflow.py -v
```

Expected: 37 ranking rows, 29 nonmetadata sources, 8 functional metadata records, and an explicit child-candidate count.

### Task 3: Close-read and reconcile all volume 43 sources

**Files:**
- Create: `recovered/COMMUNITIES-V43-RESEARCH-REPORT.md`
- Modify: `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`
- Modify: `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`

**Interfaces:**
- Consumes: ranking, contexts, all 29 nonmetadata full texts, and cumulative ledgers.
- Produces: one traceable disposition per nonmetadata PDF and sequential findings beginning at `F-152` only where a source supplies a materially distinct mechanism, outcome, challenge, or bounded negative result.

- [x] **Step 1: Metadata-triage the eight functional records**

Record `M-0046`, `M-0047`, `M-0048`, `M-0065`, `M-0066`, `M-0067`, `M-0081`, and `M-0082` as functional metadata.

- [x] **Step 2: Close-read all 8 research articles, 18 book reviews, and 3 book notes**

Inspect each source for admission, governance, founder or asset control, business power, discipline, coercion, dissent, expulsion, ostracism, schism, grievance, protected voice, usable exit, disability and care, external review, transition support, child conduct or protection, and later outcomes. Record exact PDF and printed-page locators where a finding is proposed. For reviews, distinguish the reviewer's direct evaluation from claims that require access to the reviewed book.

- [x] **Step 3: Resolve every child-danger proximity candidate**

Classify each candidate as child actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. Require actor, allegation, assessment, intervention, review, and later outcome before treating a case as responsive to the dangerous-child question.

- [x] **Step 4: Draft the source report and proposed findings**

For every promoted row, fill every ledger field and preserve unresolved alternatives. Distinguish direct source claims from participant allegations and verification leads. Give every nonmetadata non-promotion an explicit reason.

- [x] **Step 5: Reconcile findings into the existing gap bank**

Retain the 18-row B/C/D architecture unless a genuinely new article gap is established. Add verification leads and explicit non-promotions without treating corroboration as a new finding or gap.

### Task 4: Apply and verify the cumulative checkpoint

**Files:**
- Create: `recovered/update_v43.py`
- Create: `recovered/verify_v43.py`
- Modify: `recovered/COMMUNITIES-RESEARCH-STATE.md`
- Modify: `recovered/COMMUNITIES-SOURCE-INVENTORY.csv`
- Modify: `README.md`

**Interfaces:**
- Consumes: completed volume-43 dispositions and findings.
- Produces: idempotent cumulative artifacts and a verifier that proves the complete volume-43 boundary and exact volume-44 handoff.

- [x] **Step 1: Write a failing checkpoint contract before the updater**

The regression suite must first require the report, updater, verifier, sequential findings, statuses, and complete disposition table. The full verifier then asserts 37 member hashes, inventoried page counts, nonempty texts, exact dispositions, sequential finding IDs, valid gap references, report coverage, public-ID redaction, byte-for-byte preservation of D-003's archive row, and the next boundary at volume 44: 33 PDFs--20 in issue 1 and 13 in issue 2--with 48 journal PDFs remaining.

- [x] **Step 2: Run the checkpoint contract and confirm RED**

```bash
python -m unittest recovered.test_v43_workflow.Volume43WorkflowTest.test_completed_checkpoint_contract
```

Expected: failure because `update_v43.py`, `verify_v43.py`, and the completed checkpoint do not yet exist.

- [x] **Step 3: Implement and run the idempotent updater**

```bash
python recovered/update_v43.py
cp recovered/COMMUNITIES-SOURCE-INVENTORY.csv /tmp/v43-inventory-once.csv
cp recovered/COMMUNITIES-EVIDENCE-LEDGER.csv /tmp/v43-ledger-once.csv
cp recovered/COMMUNITIES-ARTICLE-GAP-BANK.md /tmp/v43-gaps-once.md
cp recovered/COMMUNITIES-RESEARCH-STATE.md /tmp/v43-state-once.md
cp README.md /tmp/v43-readme-once.md
python recovered/update_v43.py
cmp /tmp/v43-inventory-once.csv recovered/COMMUNITIES-SOURCE-INVENTORY.csv
cmp /tmp/v43-ledger-once.csv recovered/COMMUNITIES-EVIDENCE-LEDGER.csv
cmp /tmp/v43-gaps-once.md recovered/COMMUNITIES-ARTICLE-GAP-BANK.md
cmp /tmp/v43-state-once.md recovered/COMMUNITIES-RESEARCH-STATE.md
cmp /tmp/v43-readme-once.md README.md
```

The updater retains D-003's existing container provenance while marking only volume-43 member rows with verified dispositions and local corpus paths.

- [x] **Step 4: Run all final checks**

```bash
python -m py_compile recovered/recover_v43.py recovered/discover_v43.py recovered/update_v43.py recovered/verify_v43.py recovered/test_v43_workflow.py
python -m unittest recovered/test_v43_workflow.py -v
python recovered/recover_v43.py --verify
python recovered/verify_v43.py
git diff --check
```

Expected: zero failures, exact cumulative counts, and a printed volume-44 receipt.

### Task 5: Publish and read back the reusable checkpoint

**Files:**
- Add: the design, plan, volume-43 scripts, report, discovery ranking, and updated cumulative artifacts.
- Exclude: PDFs, ZIPs, extracted text, context dumps, PNG renders, partial downloads, and caches.

**Interfaces:**
- Consumes: the freshly verified local tree.
- Produces: a GitHub commit on `agent/volume-43-research` whose complete tree equals the verified local tree.

- [x] **Step 1: Inspect exact public scope and scan for private locators**

```bash
git status --short
git diff --check
git diff --cached --name-only
```

Assert that no PDF, ZIP, corpus path, context dump, visual render, credential, or non-redacted Drive object ID is staged.

- [x] **Step 2: Commit the verified checkpoint**

Use commit message:

```text
Add verified volume 43 research checkpoint
```

- [x] **Step 3: Publish and read back**

Publish `agent/volume-43-research`, compare the remote tree SHA and complete file list with the local commit, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub before reporting completion.
