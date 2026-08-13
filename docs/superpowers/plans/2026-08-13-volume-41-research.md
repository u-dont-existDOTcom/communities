# Volume 41 Research Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the verified *Communal Societies* source audit from volumes 1-40 through volume 41 without changing Joel's published article.

**Architecture:** Recover the 20 inventoried volume-41 PDFs from the journal's primary publisher, identify every download by its saved SHA-256 rather than its browser filename, preserve page boundaries in extracted text, and reuse the locked volume-40 discovery families. Close-read all 16 nonmetadata sources, promote only materially distinct findings, reconcile the existing 18-item gap bank, then update and independently verify every cumulative artifact. Git stores reusable workflow and research artifacts; copyrighted sources and full-text derivatives remain local.

**Tech Stack:** Python 3 standard library, Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`), browser-backed publisher downloads, CSV/Markdown ledgers, Git, GitHub.

## Global Constraints

- Primary mode is **P0 research/source audit only**. Do not edit article prose.
- Do not repeat volumes 1-40; begin with `M-0002` and volume 41.
- Process all **20 PDFs**, all in issue 1.
- Close-read all 16 nonmetadata sources: 8 articles and 8 book reviews. Metadata-triage `M-0004`, `M-0019`, `M-0020`, and `M-0021`.
- Preserve Joel's argument. Evidence may update research ledgers but cannot silently weaken, replace, or expand article claims.
- Separate source fact, participant allegation, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, and external-verification needs.
- Treat discovery scores only as reading-order aids, never as evidence weights.
- A bounded dangerous-child null is not a historical claim of absence.
- Do not diagnose historical actors with ASPD or psychopathy without appropriate clinical evidence.
- Preserve D-003's historical `COMMUNAL-SOCIETIES-v41-v45.zip` provenance. This checkpoint verifies volume-41 publisher members; it must not pretend to reverify an absent archive container.
- A book review supports only the reviewer's direct report or evaluation unless the reviewed book itself is inspected.
- Keep copyrighted PDFs, extracted full text, visual renders, and context dumps out of Git.
- Redact private Drive object identifiers in every public repository artifact.
- Base branch is `agent/volume-40-research`; publish the completed checkpoint on `agent/volume-41-research`.

---

### Task 1: Recover and authenticate the volume 41 corpus

**Files:**
- Create: `recovered/test_v41_workflow.py`
- Create: `recovered/recover_v41.py`
- Create locally only: `recovered/corpus-v41/vol41/iss1/*.pdf`

**Interfaces:**
- Consumes: the 20 volume-41 inventory rows and PDFs downloaded from the primary ScholarWorks issue page.
- Produces: an idempotent hash-routed corpus in which every `M-0002` through `M-0021` PDF exists at its inventoried path and matches its saved SHA-256.

- [x] **Step 1: Write the failing recovery test**

```python
def test_inventory_loader_maps_exact_volume_41_boundary():
    destinations = load_volume_41_destinations(INVENTORY, corpus)
    assert len(destinations) == 20
    assert all("/iss1/" in path.as_posix() for path in destinations.values())
    assert all(path.is_relative_to(corpus / "vol41") for path in destinations.values())
```

The production change this catches is loading the wrong volume, wrong issue, wrong destination root, or a partial/duplicate boundary.

- [x] **Step 2: Run the test and confirm RED**

```bash
python -m unittest recovered/test_v41_workflow.py -v
```

Expected: import failure because `recover_v41.py` does not exist.

- [x] **Step 3: Implement minimal hash routing and corpus validation**

Create `recover_v41.py` by reusing the proven generic routing helpers and adding this exact boundary loader:

```python
if __package__:
    from recovered.recover_v40 import route_downloads, sha256, verify_corpus
else:
    from recover_v40 import route_downloads, sha256, verify_corpus

def load_volume_41_destinations(inventory: Path = DEFAULT_INVENTORY,
                                corpus: Path = DEFAULT_CORPUS) -> dict[str, Path]:
    with inventory.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if row["volume"] == "41"]
    if len(rows) != 20:
        raise ValueError(f"expected 20 volume 41 inventory rows, found {len(rows)}")
    if any(row["issue"] != "1" for row in rows):
        raise ValueError("expected every volume 41 inventory row in issue 1")
    destinations = {
        row["sha256"]: corpus / Path(row["internal_filename"]).relative_to("archive")
        for row in rows
    }
    if len(destinations) != 20:
        raise ValueError("volume 41 inventory contains duplicate member hashes")
    return destinations
```

Read the inventory, select only volume 41, require 20 issue-1 rows, reject duplicate hashes, reuse the proven volume-40 routing implementation, and expose `--downloads`, `--verify`, and `--allow-incomplete` command-line behavior.

- [x] **Step 4: Run the recovery tests and confirm GREEN**

```bash
python -m unittest recovered/test_v41_workflow.py -v
```

Expected: all recovery tests pass while `--allow-incomplete` reports exactly 20 missing members.

- [x] **Step 5: Retrieve all 20 primary-publisher PDFs**

Use the 20 PDF links on the verified issue page:

```text
https://scholarworks.gvsu.edu/communalsocieties/vol41/iss1/
```

Compare the live publisher listing with all 20 inventory records. Rate-limit retrieval and retry transient WAF or skipped-download responses conservatively. Route every downloaded file through the saved-hash map; never infer identity from its browser filename.

- [x] **Step 6: Verify hashes, page counts, extraction, and visible first pages**

Run `recover_v41.py --verify`, compare `pdfinfo` page counts with inventory, extract page-preserving text with `pdftotext -layout`, render first-page PNGs with `pdftoppm`, and inspect a contact sheet for title or identity failures before analysis.

### Task 2: Build and prove the volume 41 discovery boundary

**Files:**
- Modify: `recovered/test_v41_workflow.py`
- Create: `recovered/discover_v41.py`
- Create: `recovered/V41-DISCOVERY-RANKING.csv`
- Create locally only: `recovered/v41-keyword-contexts.txt`
- Create locally only: `recovered/v41-child-danger-contexts.txt`

**Interfaces:**
- Consumes: all 20 extracted volume-41 texts and inventory metadata.
- Produces: a complete ranking, contextual keyword excerpts, and bounded child-as-dangerous-actor candidates.

- [x] **Step 1: Add failing discovery-output and vocabulary-lock tests**

```python
def test_volume_41_discovery_outputs_cover_every_inventory_row():
    rows = load_csv(RANKING)
    assert len(rows) == 20
    assert {row["record_id"] for row in rows} == EXPECTED_VOLUME_41_IDS
    assert KEYWORD_CONTEXTS.is_file()
    assert CHILD_CONTEXTS.is_file()

def test_ranking_preserves_term_and_process_families():
    assert literal_assignment(ROOT / "discover_v41.py", "FAMILIES") == \
           literal_assignment(ROOT / "discover_v40.py", "FAMILIES")
    assert literal_assignment(ROOT / "discover_v41.py", "PROCESS_FAMILIES") == \
           literal_assignment(ROOT / "discover_v40.py", "PROCESS_FAMILIES")
```

These tests catch incomplete coverage and any silent widening or narrowing of the locked search vocabulary.

- [x] **Step 2: Run the tests and confirm RED**

```bash
python -m unittest recovered/test_v41_workflow.py -v
```

Expected: failure because the volume-41 discovery script and outputs do not exist.

- [x] **Step 3: Implement discovery from the locked volume-40 families**

Copy the exact danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome regex literals. Change only paths, record IDs, volume boundary, functional classification, and display labels. Preserve form-feed page boundaries and deterministic sorting.

- [x] **Step 4: Run discovery and confirm GREEN**

```bash
python recovered/discover_v41.py
python -m unittest recovered/test_v41_workflow.py -v
```

Expected: 20 ranking rows, 16 nonmetadata sources, 4 functional metadata records, and an explicit child-candidate count.

### Task 3: Close-read and reconcile all volume 41 sources

**Files:**
- Create: `recovered/COMMUNITIES-V41-RESEARCH-REPORT.md`
- Modify: `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`
- Modify: `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`

**Interfaces:**
- Consumes: ranking, contexts, all 16 nonmetadata full texts, and cumulative ledgers.
- Produces: one traceable disposition per nonmetadata PDF and sequential findings beginning at `F-147` only where a source supplies a materially distinct mechanism, outcome, challenge, or bounded negative result.

- [x] **Step 1: Metadata-triage the four functional records**

Record `M-0004`, `M-0019`, `M-0020`, and `M-0021` as functional metadata.

- [x] **Step 2: Close-read all 8 articles and all 8 book reviews**

Inspect each source for admission, governance, founder or asset control, business power, discipline, coercion, dissent, expulsion, ostracism, schism, grievance, protected voice, usable exit, disability and care, external review, transition support, child conduct or protection, and later outcomes. Record exact PDF and printed-page locators where a finding is proposed. For reviews, distinguish the reviewer's direct evaluation from claims that require access to the reviewed book.

- [x] **Step 3: Resolve every child-danger proximity candidate**

Classify each candidate as child actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. Require actor, allegation, assessment, intervention, review, and later outcome before treating a case as responsive to the dangerous-child question.

- [x] **Step 4: Draft the source report and proposed findings**

For every promoted row, fill every ledger field and preserve unresolved alternatives. Distinguish direct source claims from participant allegations and verification leads. Give every nonmetadata non-promotion an explicit reason.

- [x] **Step 5: Reconcile findings into the existing gap bank**

Retain the 18-row B/C/D architecture unless a genuinely new article gap is established. Add verification leads and explicit non-promotions without treating corroboration as a new finding or gap.

### Task 4: Apply and verify the cumulative checkpoint

**Files:**
- Create: `recovered/update_v41.py`
- Create: `recovered/verify_v41.py`
- Modify: `recovered/COMMUNITIES-RESEARCH-STATE.md`
- Modify: `recovered/COMMUNITIES-SOURCE-INVENTORY.csv`
- Modify: `README.md`

**Interfaces:**
- Consumes: completed volume-41 dispositions and findings.
- Produces: idempotent cumulative artifacts and a verifier that proves the complete volume-41 boundary and exact volume-42 handoff.

- [x] **Step 1: Write the checkpoint verifier before the updater**

The verifier must assert 20 member hashes, inventoried page counts, nonempty texts, exact dispositions, sequential finding IDs, valid gap references, report coverage, public-ID redaction, byte-for-byte preservation of D-003's archive row, and the next boundary at volume 42: 24 PDFs across issues 1 and 2, with 109 journal PDFs remaining.

- [x] **Step 2: Run the verifier and confirm RED**

```bash
python recovered/verify_v41.py
```

Expected: failure because cumulative artifacts still stop at volume 40.

- [x] **Step 3: Implement and run the idempotent updater**

```bash
python recovered/update_v41.py
cp recovered/COMMUNITIES-SOURCE-INVENTORY.csv /tmp/v41-inventory-once.csv
cp recovered/COMMUNITIES-EVIDENCE-LEDGER.csv /tmp/v41-ledger-once.csv
cp recovered/COMMUNITIES-ARTICLE-GAP-BANK.md /tmp/v41-gaps-once.md
cp recovered/COMMUNITIES-RESEARCH-STATE.md /tmp/v41-state-once.md
cp README.md /tmp/v41-readme-once.md
python recovered/update_v41.py
cmp /tmp/v41-inventory-once.csv recovered/COMMUNITIES-SOURCE-INVENTORY.csv
cmp /tmp/v41-ledger-once.csv recovered/COMMUNITIES-EVIDENCE-LEDGER.csv
cmp /tmp/v41-gaps-once.md recovered/COMMUNITIES-ARTICLE-GAP-BANK.md
cmp /tmp/v41-state-once.md recovered/COMMUNITIES-RESEARCH-STATE.md
cmp /tmp/v41-readme-once.md README.md
```

The updater retains D-003's existing container provenance while marking only volume-41 member rows with verified dispositions and local corpus paths.

- [x] **Step 4: Run all final checks**

```bash
python -m py_compile recovered/recover_v41.py recovered/discover_v41.py recovered/update_v41.py recovered/verify_v41.py recovered/test_v41_workflow.py
python -m unittest recovered/test_v41_workflow.py -v
python recovered/verify_v41.py
git diff --check
```

Expected: zero failures, exact cumulative counts, and a printed volume-42 receipt.

### Task 5: Publish and read back the reusable checkpoint

**Files:**
- Add: the design, plan, volume-41 scripts, report, discovery ranking, and updated cumulative artifacts.
- Exclude: PDFs, ZIPs, extracted text, context dumps, PNG renders, partial downloads, and caches.

**Interfaces:**
- Consumes: the freshly verified local tree.
- Produces: a GitHub commit on `agent/volume-41-research` whose complete tree equals the verified local tree.

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
Add verified volume 41 research checkpoint
```

- [ ] **Step 3: Publish and read back**

Publish `agent/volume-41-research`, compare the remote tree SHA and complete file list with the local commit, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub before reporting completion.
