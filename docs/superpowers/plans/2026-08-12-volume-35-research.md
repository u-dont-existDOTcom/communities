# Volume 35 Research Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the verified *Communal Societies* source audit from volumes 1-34 through volume 35 without changing Joel's published article.

**Architecture:** Recover the 26 inventoried volume-35 PDFs from the journal's primary publisher, identify each download by its pre-existing SHA-256 rather than its browser filename, preserve page boundaries in extracted text, and reuse the locked volume-34 discovery families. Close-read every substantive source, promote only materially distinct findings, then update and verify all cumulative artifacts. Git stores plans, scripts, reports, and tabular checkpoints; copyrighted PDFs, extracted text, context dumps, and visual renders remain local.

**Tech Stack:** Python 3 standard library, Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`), browser-backed publisher downloads, CSV/Markdown ledgers, Git, GitHub.

## Global Constraints

- Primary mode is **P0 research/source audit only**. Do not edit article prose.
- Do not repeat volumes 1-34; begin with `M-0863` and volume 35.
- Process all **26 PDFs**: 12 in issue 1 and 14 in issue 2.
- The volume contains 22 substantive sources (8 articles and 14 reviews) plus 4 metadata sources (2 contents and 2 editorials).
- Preserve Joel's argument. Evidence may update research ledgers but cannot silently weaken, replace, or expand article claims.
- Separate source fact, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, and external-verification needs.
- Treat discovery scores only as reading-order aids, never as evidence weights.
- A bounded dangerous-child null is not a historical claim of absence.
- Do not diagnose historical actors with ASPD or psychopathy without appropriate clinical evidence.
- Preserve the existing historical provenance for the shared `vol35-40.zip` archive row. This checkpoint verifies volume-35 publisher members; it must not pretend to reverify the absent archive container.
- Keep copyrighted PDFs, extracted full text, visual renders, and context dumps out of Git.
- Redact private Drive object identifiers in every public repository artifact.
- Base branch is `agent/volume-34-research`; publish the completed checkpoint on `agent/volume-35-research`.

---

### Task 1: Recover and authenticate the volume 35 corpus

**Files:**
- Create: `recovered/test_v35_workflow.py`
- Create: `recovered/recover_v35.py`
- Create locally only: `recovered/corpus-v35/vol35/iss1/*.pdf`
- Create locally only: `recovered/corpus-v35/vol35/iss2/*.pdf`

**Interfaces:**
- Consumes: volume-35 inventory rows and downloaded PDFs from the two ScholarWorks issue pages.
- Produces: an idempotent hash-routed corpus in which each `M-0863` through `M-0888` PDF exists at its inventoried path and matches its saved SHA-256.

- [x] **Step 1: Write the failing recovery test**

```python
def test_route_downloads_uses_saved_hash_instead_of_browser_name():
    source = root / "arbitrary-browser-name.pdf"
    source.write_bytes(b"%PDF-test-member")
    expected_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    destination = root / "corpus" / "vol35" / "iss1" / "001-contents.pdf"
    routed = route_downloads([source], {expected_hash: destination})
    assert routed == [destination]
    assert destination.read_bytes() == b"%PDF-test-member"
    assert not source.exists()
```

- [x] **Step 2: Run the test and confirm RED**

Run:

```bash
python -m unittest recovered/test_v35_workflow.py -v
```

Expected: import failure because `recover_v35.py` does not exist.

- [x] **Step 3: Implement minimal hash routing and corpus validation**

`recover_v35.py` must read the inventory, map only volume-35 hashes, reject unknown and duplicate downloads, create only exact inventoried destinations, and expose `route_downloads()` plus a command-line validation receipt.

- [x] **Step 4: Retrieve all 26 primary-publisher PDFs**

Use the PDF links on:

```text
https://scholarworks.gvsu.edu/communalsocieties/vol35/iss1/
https://scholarworks.gvsu.edu/communalsocieties/vol35/iss2/
```

Compare publisher article listings with the inventory before calling the issue boundary complete. Rate-limit retrieval. Route browser filenames only through the saved-hash map; never infer identity from the download name.

- [x] **Step 5: Verify complete hashes, page counts, extraction, and visible first pages**

Run `recover_v35.py --verify`, compare `pdfinfo` page counts with inventory, extract page-preserving text, render first-page PNGs with `pdftoppm`, and inspect a contact sheet for title/identity failures before analysis.

### Task 2: Build and prove the volume 35 discovery boundary

**Files:**
- Modify: `recovered/test_v35_workflow.py`
- Create: `recovered/discover_v35.py`
- Create: `recovered/V35-DISCOVERY-RANKING.csv`
- Create locally only: `recovered/v35-keyword-contexts.txt`
- Create locally only: `recovered/v35-child-danger-contexts.txt`

**Interfaces:**
- Consumes: all 26 extracted volume-35 texts and inventory metadata.
- Produces: a complete ranking, contextual keyword excerpts, and bounded child-as-dangerous-actor candidates.

- [x] **Step 1: Add a failing discovery-output test**

```python
def test_volume_35_discovery_outputs_cover_every_inventory_row():
    rows = load_csv(RANKING)
    assert len(rows) == 26
    assert {row["record_id"] for row in rows} == EXPECTED_VOLUME_35_IDS
    assert KEYWORD_CONTEXTS.is_file()
    assert CHILD_CONTEXTS.is_file()
```

- [x] **Step 2: Run the test and confirm RED**

Run:

```bash
python -m unittest recovered/test_v35_workflow.py -v
```

Expected: failure because the volume-35 discovery outputs do not exist.

- [x] **Step 3: Implement discovery from the locked volume-34 families**

Copy the exact danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome regex families. Change only paths and volume boundary. Preserve form-feed page boundaries and deterministic sorting.

- [x] **Step 4: Run discovery and confirm GREEN**

```bash
python recovered/discover_v35.py
python -m unittest recovered/test_v35_workflow.py -v
```

Expected: 26 ranking rows, every substantive source represented, and an explicit child-candidate count.

### Task 3: Close-read and reconcile all volume 35 sources

**Files:**
- Create: `recovered/COMMUNITIES-V35-RESEARCH-REPORT.md`
- Modify: `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`
- Modify: `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`

**Interfaces:**
- Consumes: ranking, contexts, all relevant full texts, and cumulative ledgers.
- Produces: one traceable disposition per PDF and sequential findings beginning at `F-119` only where the source supplies a materially distinct mechanism, outcome, challenge, or bounded negative result.

- [x] **Step 1: Metadata-triage the four contents and editorial records**

Record these as metadata; do not inflate them into close reads or findings.

- [x] **Step 2: Close-read all 22 articles and reviews**

Inspect every substantive source for admission, governance, founder control, financial custody, discipline, coercion, expulsion, schism, grievance, protected dissent, exit, external review, transition support, child conduct/protection, and later outcomes. Record exact PDF and printed page locators where a finding is proposed.

- [x] **Step 3: Resolve every child-danger proximity candidate**

Classify each candidate as child actor, victim, dependent, student, biographical/theological/fictional figure, or unrelated mention. Require allegation, assessment, intervention, review, and later outcome before treating a case as responsive to the dangerous-child question.

- [x] **Step 4: Draft the source report and proposed findings**

For every promoted row, fill every ledger field and preserve unresolved alternatives. Distinguish direct source claims from participant allegations and verification leads. Give every substantive non-promotion an explicit reason.

### Task 4: Apply and verify the cumulative checkpoint

**Files:**
- Create: `recovered/update_v35.py`
- Create: `recovered/verify_v35.py`
- Modify: `recovered/COMMUNITIES-RESEARCH-STATE.md`
- Modify: `recovered/COMMUNITIES-SOURCE-INVENTORY.csv`
- Modify: `README.md`

**Interfaces:**
- Consumes: completed volume-35 dispositions and findings.
- Produces: idempotent cumulative artifacts and a verifier that proves the complete volume-35 boundary and exact volume-36 handoff.

- [x] **Step 1: Write the checkpoint verifier before the updater**

The verifier must assert 26 member hashes, inventoried page counts, nonempty texts, exact dispositions, sequential finding IDs, valid gap references, report coverage, public-ID redaction, preservation of the shared archive row, and the next boundary at volume 36: 21 PDFs, 10 in issue 1 and 11 in issue 2.

- [x] **Step 2: Run the verifier and confirm RED**

```bash
python recovered/verify_v35.py
```

Expected: failure because cumulative artifacts still stop at volume 34.

- [x] **Step 3: Implement and run the idempotent updater**

```bash
python recovered/update_v35.py
python recovered/update_v35.py
```

The second run must produce no content change. The updater must retain the existing D-017 container provenance while marking only volume-35 member rows with their verified dispositions and current local corpus paths.

- [x] **Step 4: Run all final checks**

```bash
python -m py_compile recovered/recover_v35.py recovered/discover_v35.py recovered/update_v35.py recovered/verify_v35.py recovered/test_v35_workflow.py
python -m unittest recovered/test_v35_workflow.py -v
python recovered/verify_v35.py
git diff --check
```

Expected: zero failures, exact cumulative counts, and a printed volume-36 receipt.

### Task 5: Publish and read back the reusable checkpoint

**Files:**
- Add: the plan, volume-35 scripts, report, discovery ranking, and updated cumulative artifacts.
- Exclude: PDFs, ZIPs, extracted text, context dumps, PNG renders, partial downloads, and caches.

**Interfaces:**
- Consumes: the freshly verified local tree.
- Produces: a GitHub commit on `agent/volume-35-research` whose complete tree equals the verified local tree.

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
Add verified volume 35 research checkpoint
```

- [x] **Step 3: Publish and read back**

Publish `agent/volume-35-research`, compare the remote tree SHA and file list with the local commit, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub before reporting completion.
