# Volume 34 Research Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the verified *Communal Societies* source audit from volumes 1-33 through volume 34 without changing Joel's published article.

**Architecture:** Recover the 29 inventoried PDFs from the journal's primary publisher, identify each download by its pre-existing SHA-256 rather than its browser filename, extract page-preserving text, and reuse the locked volume-33 discovery families. Close-read every substantive source that can affect the research question, promote only materially distinct findings, then update and verify all cumulative artifacts. Git stores plans, scripts, reports, and tabular checkpoints; copyrighted PDFs, extracted text, and context dumps remain local.

**Tech Stack:** Python 3 standard library, Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`), browser-backed publisher downloads, CSV/Markdown ledgers, Git, GitHub.

## Global Constraints

- Primary mode is **P0 research/source audit only**. Do not edit article prose.
- Do not repeat volumes 1-33; begin with `M-0834` and volume 34.
- Process all **29 PDFs**: 18 in issue 1 and 11 in issue 2.
- Preserve Joel's argument. Evidence may update research ledgers but cannot silently weaken, replace, or expand article claims.
- Separate source fact, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, and external-verification needs.
- Treat discovery scores only as reading-order aids, never as evidence weights.
- A bounded dangerous-child null is not a historical claim of absence.
- Do not diagnose historical actors with ASPD or psychopathy without appropriate clinical evidence.
- Keep copyrighted PDFs, extracted full text, visual renders, and context dumps out of Git.
- Redact private Drive object identifiers in every public repository artifact.
- Base branch is `agent/volume-33-research`; publish the completed checkpoint on `agent/volume-34-research`.

---

### Task 1: Recover and authenticate the volume 34 corpus

**Files:**
- Create: `recovered/test_v34_workflow.py`
- Create: `recovered/recover_v34.py`
- Create locally only: `recovered/corpus-v34/vol34/iss1/*.pdf`
- Create locally only: `recovered/corpus-v34/vol34/iss2/*.pdf`

**Interfaces:**
- Consumes: volume-34 inventory rows and downloaded PDFs from the two ScholarWorks issue pages.
- Produces: an idempotent hash-routed corpus in which each `M-0834` through `M-0862` PDF exists at its inventoried path and matches its saved SHA-256.

- [x] **Step 1: Write the failing recovery test**

```python
def test_recover_volume_34_routes_by_saved_hash(tmp_path):
    source = tmp_path / "arbitrary-browser-name.pdf"
    source.write_bytes(b"%PDF-test-member")
    expected = hashlib.sha256(source.read_bytes()).hexdigest()
    destination = tmp_path / "corpus" / "vol34" / "iss1" / "001-front-matter.pdf"
    route_downloads([source], {expected: destination})
    assert destination.read_bytes() == b"%PDF-test-member"
    assert not source.exists()
```

- [x] **Step 2: Run the test and confirm RED**

Run:

```bash
python -m unittest recovered/test_v34_workflow.py -v
```

Expected: import failure because `recover_v34.py` does not exist.

- [x] **Step 3: Implement minimal hash routing and corpus validation**

`recover_v34.py` must read the inventory, map only volume-34 hashes, reject unknown and duplicate downloads, create only exact inventoried destinations, and expose `route_downloads()` plus a command-line validation receipt.

- [x] **Step 4: Retrieve all 29 primary-publisher PDFs**

Use the PDF links on:

```text
https://scholarworks.gvsu.edu/communalsocieties/vol34/iss1/
https://scholarworks.gvsu.edu/communalsocieties/vol34/iss2/
```

Rate-limit retrieval. Route browser filenames only through the saved-hash map; never infer identity from the download name.

- [x] **Step 5: Verify complete hashes, page counts, and visible first pages**

Run `recover_v34.py --verify`, compare `pdfinfo` page counts with inventory, extract first-page PNGs with `pdftoppm`, and inspect a contact sheet for title/identity failures before analysis.

### Task 2: Build and prove the volume 34 discovery boundary

**Files:**
- Modify: `recovered/test_v34_workflow.py`
- Create: `recovered/discover_v34.py`
- Create: `recovered/V34-DISCOVERY-RANKING.csv`
- Create locally only: `recovered/v34-keyword-contexts.txt`
- Create locally only: `recovered/v34-child-danger-contexts.txt`

**Interfaces:**
- Consumes: all 29 extracted volume-34 texts and inventory metadata.
- Produces: a complete ranking, contextual keyword excerpts, and bounded child-as-dangerous-actor candidates.

- [x] **Step 1: Add a failing discovery-output test**

```python
def test_volume_34_discovery_outputs_cover_every_inventory_row():
    rows = load_csv(RANKING)
    assert len(rows) == 29
    assert {row["record_id"] for row in rows} == EXPECTED_VOLUME_34_IDS
    assert KEYWORD_CONTEXTS.is_file()
    assert CHILD_CONTEXTS.is_file()
```

- [x] **Step 2: Run the test and confirm RED**

Run:

```bash
python -m unittest recovered/test_v34_workflow.py -v
```

Expected: failure because the volume-34 discovery outputs do not exist.

- [x] **Step 3: Implement discovery from the locked volume-33 families**

Copy the exact danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome regex families. Change only paths and volume boundary. Preserve form-feed page boundaries and deterministic sorting.

- [x] **Step 4: Run discovery and confirm GREEN**

```bash
python recovered/discover_v34.py
python -m unittest recovered/test_v34_workflow.py -v
```

Expected: 29 ranking rows, every substantive source represented, and an explicit child-candidate count.

### Task 3: Close-read and reconcile all volume 34 sources

**Files:**
- Create: `recovered/COMMUNITIES-V34-RESEARCH-REPORT.md`
- Modify: `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`
- Modify: `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`

**Interfaces:**
- Consumes: ranking, contexts, all relevant full texts, and cumulative ledgers.
- Produces: one traceable disposition per PDF and sequential findings beginning at `F-116` only where the source supplies a materially distinct mechanism, outcome, challenge, or bounded negative result.

- [x] **Step 1: Metadata-triage the eight front-matter, contents, editorial, and back-matter records**

Record these as metadata; do not inflate them into close reads or findings.

- [x] **Step 2: Close-read every substantive candidate**

Inspect all 21 articles and reviews for admission, governance, founder control, financial custody, discipline, coercion, expulsion, schism, protected dissent, exit, external review, transition support, child conduct/protection, and later outcomes. Record exact PDF and printed page locators where a finding is proposed.

- [x] **Step 3: Resolve every child-danger proximity candidate**

Classify each candidate as child actor, victim, dependent, student, biographical/theological/fictional figure, or unrelated mention. Require allegation, assessment, intervention, review, and later outcome before treating a case as responsive to the dangerous-child question.

- [x] **Step 4: Draft the source report and proposed findings**

For every promoted row, fill every ledger field and preserve unresolved alternatives. Distinguish direct source claims from participant allegations and verification leads. Give all non-promotions an explicit reason.

### Task 4: Apply and verify the cumulative checkpoint

**Files:**
- Create: `recovered/update_v34.py`
- Create: `recovered/verify_v34.py`
- Modify: `recovered/COMMUNITIES-RESEARCH-STATE.md`
- Modify: `recovered/COMMUNITIES-SOURCE-INVENTORY.csv`
- Modify: `README.md`

**Interfaces:**
- Consumes: completed volume-34 dispositions and findings.
- Produces: idempotent cumulative artifacts and a verifier that proves the complete volume-34 boundary and exact volume-35 handoff.

- [x] **Step 1: Write the checkpoint verifier before the updater**

The verifier must assert 29 member hashes and nonempty texts, exact dispositions, sequential finding IDs, valid gap references, report coverage, public-ID redaction, and the next boundary at volume 35: 26 PDFs, 12 in issue 1 and 14 in issue 2.

- [x] **Step 2: Run the verifier and confirm RED**

```bash
python recovered/verify_v34.py
```

Expected: failure because cumulative artifacts still stop at volume 33.

- [x] **Step 3: Implement and run the idempotent updater**

```bash
python recovered/update_v34.py
python recovered/update_v34.py
```

The second run must produce no content change.

- [x] **Step 4: Run all final checks**

```bash
python -m py_compile recovered/recover_v34.py recovered/discover_v34.py recovered/update_v34.py recovered/verify_v34.py recovered/test_v34_workflow.py
python -m unittest recovered/test_v34_workflow.py -v
python recovered/verify_v34.py
git diff --check
```

Expected: zero failures, exact cumulative counts, and a printed volume-35 receipt.

### Task 5: Publish and read back the reusable checkpoint

**Files:**
- Add: the plan, volume-34 scripts, report, discovery ranking, and updated cumulative artifacts.
- Exclude: PDFs, ZIPs, extracted text, context dumps, PNG renders, partial downloads, and caches.

**Interfaces:**
- Consumes: the freshly verified local tree.
- Produces: a GitHub commit on `agent/volume-34-research` whose complete tree equals the verified local tree.

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
Add verified volume 34 research checkpoint
```

- [x] **Step 3: Publish and read back**

Publish `agent/volume-34-research`, compare the remote tree SHA and file list with the local commit, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub before reporting completion.
