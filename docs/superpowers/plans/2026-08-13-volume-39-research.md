# Volume 39 Research Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the verified *Communal Societies* source audit from volumes 1-38 through volume 39 without changing Joel's published article.

**Architecture:** Recover the 23 inventoried volume-39 PDFs from the journal's primary publisher, identify every download by its saved SHA-256 rather than its browser filename, preserve page boundaries in extracted text, and reuse the locked volume-38 discovery families. Close-read every substantive source, promote only materially distinct findings, reconcile the existing 18-item gap bank, then update and independently verify every cumulative artifact. Git stores reusable workflow and research artifacts; copyrighted sources and full-text derivatives remain local.

**Tech Stack:** Python 3 standard library, Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`), browser-backed publisher downloads, CSV/Markdown ledgers, Git, GitHub.

## Global Constraints

- Primary mode is **P0 research/source audit only**. Do not edit article prose.
- Do not repeat volumes 1-38; begin with `M-0956` and volume 39.
- Process all **23 PDFs**: 11 in issue 1 and 12 in issue 2.
- Close-read 15 substantive sources and metadata-triage 8 sources: `M-0956`, `M-0957`, `M-0958`, `M-0966`, `M-0967`, `M-0968`, `M-0969`, and `M-0978`.
- Preserve Joel's argument. Evidence may update research ledgers but cannot silently weaken, replace, or expand article claims.
- Separate source fact, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, and external-verification needs.
- Treat discovery scores only as reading-order aids, never as evidence weights.
- A bounded dangerous-child null is not a historical claim of absence.
- Do not diagnose historical actors with ASPD or psychopathy without appropriate clinical evidence.
- Preserve the existing historical provenance for the shared `vol35-40.zip` archive row. This checkpoint verifies volume-39 publisher members; it must not pretend to reverify an absent archive container.
- Keep copyrighted PDFs, extracted full text, visual renders, and context dumps out of Git.
- Redact private Drive object identifiers in every public repository artifact.
- Base branch is `agent/volume-38-research`; publish the completed checkpoint on `agent/volume-39-research`.

---

### Task 1: Recover and authenticate the volume 39 corpus

**Files:**
- Create: `recovered/test_v39_workflow.py`
- Create: `recovered/recover_v39.py`
- Create locally only: `recovered/corpus-v39/vol39/iss1/*.pdf`
- Create locally only: `recovered/corpus-v39/vol39/iss2/*.pdf`

**Interfaces:**
- Consumes: volume-39 inventory rows and downloaded PDFs from the two ScholarWorks issue pages.
- Produces: an idempotent hash-routed corpus in which every `M-0956` through `M-0978` PDF exists at its inventoried path and matches its saved SHA-256.

- [x] **Step 1: Write the failing recovery test**

```python
def test_inventory_loader_maps_exact_volume_39_boundary():
    destinations = load_volume_39_destinations(INVENTORY, corpus)
    assert len(destinations) == 23
    assert sum("/iss1/" in path.as_posix() for path in destinations.values()) == 11
    assert sum("/iss2/" in path.as_posix() for path in destinations.values()) == 12
```

- [x] **Step 2: Run the test and confirm RED**

```bash
python -m unittest recovered/test_v39_workflow.py -v
```

Expected: import failure because `recover_v39.py` does not exist.

- [x] **Step 3: Implement minimal hash routing and corpus validation**

`recover_v39.py` reads the inventory, maps only volume-39 hashes, rejects unknown and duplicate downloads, creates only exact inventoried destinations, and exposes `load_volume_39_destinations()` plus the proven `route_downloads()` and command-line validation receipt.

- [x] **Step 4: Run the recovery tests and confirm GREEN**

```bash
python -m unittest recovered/test_v39_workflow.py -v
```

Expected: all recovery tests pass while an incomplete corpus remains explicitly reported by `--allow-incomplete`.

- [x] **Step 5: Retrieve all 23 primary-publisher PDFs**

Use the PDF links on:

```text
https://scholarworks.gvsu.edu/communalsocieties/vol39/iss1/
https://scholarworks.gvsu.edu/communalsocieties/vol39/iss2/
```

Compare publisher listings with the inventory before closing either issue. Rate-limit retrieval and retry transient WAF/rate-limit responses conservatively. Route every downloaded file through the saved-hash map; never infer identity from its browser filename.

- [x] **Step 6: Verify hashes, page counts, extraction, and visible first pages**

Run `recover_v39.py --verify`, compare `pdfinfo` page counts with inventory, extract page-preserving text, render first-page PNGs with `pdftoppm`, and inspect a contact sheet for title or identity failures before analysis.

### Task 2: Build and prove the volume 39 discovery boundary

**Files:**
- Modify: `recovered/test_v39_workflow.py`
- Create: `recovered/discover_v39.py`
- Create: `recovered/V39-DISCOVERY-RANKING.csv`
- Create locally only: `recovered/v39-keyword-contexts.txt`
- Create locally only: `recovered/v39-child-danger-contexts.txt`

**Interfaces:**
- Consumes: all 23 extracted volume-39 texts and inventory metadata.
- Produces: a complete ranking, contextual keyword excerpts, and bounded child-as-dangerous-actor candidates.

- [x] **Step 1: Add a failing discovery-output test**

```python
def test_volume_39_discovery_outputs_cover_every_inventory_row():
    rows = load_csv(RANKING)
    assert len(rows) == 23
    assert {row["record_id"] for row in rows} == EXPECTED_VOLUME_39_IDS
    assert KEYWORD_CONTEXTS.is_file()
    assert CHILD_CONTEXTS.is_file()
```

- [x] **Step 2: Run the test and confirm RED**

```bash
python -m unittest recovered/test_v39_workflow.py -v
```

Expected: failure because the volume-39 discovery outputs do not exist.

- [x] **Step 3: Implement discovery from the locked volume-38 families**

Copy the exact danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome regex families. Change only paths, record IDs, and the volume boundary. Preserve form-feed page boundaries and deterministic sorting.

- [x] **Step 4: Run discovery and confirm GREEN**

```bash
python recovered/discover_v39.py
python -m unittest recovered/test_v39_workflow.py -v
```

Expected: 23 ranking rows, 15 substantive sources, 8 functional metadata records, and an explicit child-candidate count.

### Task 3: Close-read and reconcile all volume 39 sources

**Files:**
- Create: `recovered/COMMUNITIES-V39-RESEARCH-REPORT.md`
- Modify: `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`
- Modify: `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`

**Interfaces:**
- Consumes: ranking, contexts, all substantive full texts, and cumulative ledgers.
- Produces: one traceable disposition per substantive PDF and sequential findings beginning at `F-139` only where a source supplies a materially distinct mechanism, outcome, challenge, or bounded negative result.

- [x] **Step 1: Metadata-triage the eight non-substantive records**

Record `M-0956`, `M-0957`, `M-0958`, `M-0966`, `M-0967`, `M-0968`, `M-0969`, and `M-0978` as metadata.

- [x] **Step 2: Close-read all 15 articles and reviews**

Inspect every substantive source for admission, governance, founder control, financial custody, discipline, coercion, expulsion, schism, grievance, protected dissent, exit, external review, transition support, child conduct or protection, and later outcomes. Record exact PDF and printed-page locators where a finding is proposed.

- [x] **Step 3: Resolve every child-danger proximity candidate**

Classify each candidate as child actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. Require actor, allegation, assessment, intervention, review, and later outcome before treating a case as responsive to the dangerous-child question.

- [x] **Step 4: Draft the source report and proposed findings**

For every promoted row, fill every ledger field and preserve unresolved alternatives. Distinguish direct source claims from participant allegations and verification leads. Give every substantive non-promotion an explicit reason.

- [x] **Step 5: Reconcile findings into the existing gap bank**

Retain the 18-row B/C/D architecture unless a genuinely new article gap is established. Add verification leads and explicit non-promotions without treating corroboration as a new finding or gap.

### Task 4: Apply and verify the cumulative checkpoint

**Files:**
- Create: `recovered/update_v39.py`
- Create: `recovered/verify_v39.py`
- Modify: `recovered/COMMUNITIES-RESEARCH-STATE.md`
- Modify: `recovered/COMMUNITIES-SOURCE-INVENTORY.csv`
- Modify: `README.md`

**Interfaces:**
- Consumes: completed volume-39 dispositions and findings.
- Produces: idempotent cumulative artifacts and a verifier that proves the complete volume-39 boundary and exact volume-40 handoff.

- [x] **Step 1: Write the checkpoint verifier before the updater**

The verifier asserts 23 member hashes, inventoried page counts, nonempty texts, exact dispositions, sequential finding IDs, valid gap references, report coverage, public-ID redaction, preservation of the shared archive row, and the next boundary at volume 40: 9 PDFs in issue 1, with 138 journal PDFs remaining.

- [x] **Step 2: Run the verifier and confirm RED**

```bash
python recovered/verify_v39.py
```

Expected: failure because cumulative artifacts still stop at volume 38.

- [x] **Step 3: Implement and run the idempotent updater**

```bash
python recovered/update_v39.py
python recovered/update_v39.py
```

The second run must produce no content change. The updater retains D-017's existing container provenance while marking only volume-39 member rows with their verified dispositions and current local corpus paths.

- [x] **Step 4: Run all final checks**

```bash
python -m py_compile recovered/recover_v39.py recovered/discover_v39.py recovered/update_v39.py recovered/verify_v39.py recovered/test_v39_workflow.py
python -m unittest recovered/test_v39_workflow.py -v
python recovered/verify_v39.py
git diff --check
```

Expected: zero failures, exact cumulative counts, and a printed volume-40 receipt.

### Task 5: Publish and read back the reusable checkpoint

**Files:**
- Add: the design, plan, volume-39 scripts, report, discovery ranking, and updated cumulative artifacts.
- Exclude: PDFs, ZIPs, extracted text, context dumps, PNG renders, partial downloads, and caches.

**Interfaces:**
- Consumes: the freshly verified local tree.
- Produces: a GitHub commit on `agent/volume-39-research` whose complete tree equals the verified local tree.

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
Add verified volume 39 research checkpoint
```

- [ ] **Step 3: Publish and read back**

Publish `agent/volume-39-research`, compare the remote tree SHA and complete file list with the local commit, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub before reporting completion.
