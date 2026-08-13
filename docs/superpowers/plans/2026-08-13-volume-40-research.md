# Volume 40 Research Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the verified *Communal Societies* source audit from volumes 1-39 through volume 40 without changing Joel's published article.

**Architecture:** Recover the nine inventoried volume-40 PDFs from the journal's primary publisher, identify every download by its saved SHA-256 rather than its browser filename, preserve page boundaries in extracted text, and reuse the locked volume-39 discovery families. Close-read all five substantive sources, promote only materially distinct findings, reconcile the existing 18-item gap bank, then update and independently verify every cumulative artifact. Git stores reusable workflow and research artifacts; copyrighted sources and full-text derivatives remain local.

**Tech Stack:** Python 3 standard library, Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`), browser-backed publisher downloads, CSV/Markdown ledgers, Git, GitHub.

## Global Constraints

- Primary mode is **P0 research/source audit only**. Do not edit article prose.
- Do not repeat volumes 1-39; begin with `M-0979` and volume 40.
- Process all **9 PDFs**, all in issue 1.
- Close-read 5 substantive articles and metadata-triage `M-0979`, `M-0980`, `M-0981`, and `M-0987`.
- Preserve Joel's argument. Evidence may update research ledgers but cannot silently weaken, replace, or expand article claims.
- Separate source fact, participant allegation, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, and external-verification needs.
- Treat discovery scores only as reading-order aids, never as evidence weights.
- A bounded dangerous-child null is not a historical claim of absence.
- Do not diagnose historical actors with ASPD or psychopathy without appropriate clinical evidence.
- Preserve D-017's historical `vol35-40.zip` provenance. This checkpoint verifies volume-40 publisher members; it must not pretend to reverify an absent archive container.
- Keep copyrighted PDFs, extracted full text, visual renders, and context dumps out of Git.
- Redact private Drive object identifiers in every public repository artifact.
- Base branch is `agent/volume-39-research`; publish the completed checkpoint on `agent/volume-40-research`.

---

### Task 1: Recover and authenticate the volume 40 corpus

**Files:**
- Create: `recovered/test_v40_workflow.py`
- Create: `recovered/recover_v40.py`
- Create locally only: `recovered/corpus-v40/vol40/iss1/*.pdf`

**Interfaces:**
- Consumes: the nine volume-40 inventory rows and PDFs downloaded from the primary ScholarWorks issue page.
- Produces: an idempotent hash-routed corpus in which every `M-0979` through `M-0987` PDF exists at its inventoried path and matches its saved SHA-256.

- [x] **Step 1: Write the failing recovery test**

```python
def test_inventory_loader_maps_exact_volume_40_boundary():
    destinations = load_volume_40_destinations(INVENTORY, corpus)
    assert len(destinations) == 9
    assert all("/iss1/" in path.as_posix() for path in destinations.values())
```

- [x] **Step 2: Run the test and confirm RED**

```bash
python -m unittest recovered/test_v40_workflow.py -v
```

Expected: import failure because `recover_v40.py` does not exist.

- [x] **Step 3: Implement minimal hash routing and corpus validation**

`recover_v40.py` reads the inventory, maps only volume-40 hashes, rejects unknown and duplicate downloads, creates only exact inventoried destinations, and exposes `load_volume_40_destinations()`, `route_downloads()`, and a command-line validation receipt.

- [x] **Step 4: Run the recovery tests and confirm GREEN**

```bash
python -m unittest recovered/test_v40_workflow.py -v
```

Expected: all recovery tests pass while `--allow-incomplete` reports exactly nine missing members.

- [x] **Step 5: Retrieve all nine primary-publisher PDFs**

Use the PDF links on:

```text
https://scholarworks.gvsu.edu/communalsocieties/vol40/iss1/
```

Compare the live publisher listing with the nine inventory records. Rate-limit retrieval and retry transient WAF or skipped-download responses conservatively. Route every downloaded file through the saved-hash map; never infer identity from its browser filename.

- [x] **Step 6: Verify hashes, page counts, extraction, and visible first pages**

Run `recover_v40.py --verify`, compare `pdfinfo` page counts with inventory, extract page-preserving text, render first-page PNGs with `pdftoppm`, and inspect a contact sheet for title or identity failures before analysis.

### Task 2: Build and prove the volume 40 discovery boundary

**Files:**
- Modify: `recovered/test_v40_workflow.py`
- Create: `recovered/discover_v40.py`
- Create: `recovered/V40-DISCOVERY-RANKING.csv`
- Create locally only: `recovered/v40-keyword-contexts.txt`
- Create locally only: `recovered/v40-child-danger-contexts.txt`

**Interfaces:**
- Consumes: all nine extracted volume-40 texts and inventory metadata.
- Produces: a complete ranking, contextual keyword excerpts, and bounded child-as-dangerous-actor candidates.

- [x] **Step 1: Add a failing discovery-output test**

```python
def test_volume_40_discovery_outputs_cover_every_inventory_row():
    rows = load_csv(RANKING)
    assert len(rows) == 9
    assert {row["record_id"] for row in rows} == EXPECTED_VOLUME_40_IDS
    assert KEYWORD_CONTEXTS.is_file()
    assert CHILD_CONTEXTS.is_file()
```

- [x] **Step 2: Run the test and confirm RED**

```bash
python -m unittest recovered/test_v40_workflow.py -v
```

Expected: failure because the volume-40 discovery outputs do not exist.

- [x] **Step 3: Implement discovery from the locked volume-39 families**

Copy the exact danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome regex families. Change only paths, record IDs, and volume boundary. Preserve form-feed page boundaries and deterministic sorting.

- [x] **Step 4: Run discovery and confirm GREEN**

```bash
python recovered/discover_v40.py
python -m unittest recovered/test_v40_workflow.py -v
```

Expected: 9 ranking rows, 5 substantive sources, 4 functional metadata records, and an explicit child-candidate count.

### Task 3: Close-read and reconcile all volume 40 sources

**Files:**
- Create: `recovered/COMMUNITIES-V40-RESEARCH-REPORT.md`
- Modify: `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`
- Modify: `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`

**Interfaces:**
- Consumes: ranking, contexts, all five substantive full texts, and cumulative ledgers.
- Produces: one traceable disposition per substantive PDF and sequential findings beginning at `F-143` only where a source supplies a materially distinct mechanism, outcome, challenge, or bounded negative result.

- [x] **Step 1: Metadata-triage the four non-substantive records**

Record `M-0979`, `M-0980`, `M-0981`, and `M-0987` as functional metadata.

- [x] **Step 2: Close-read all five articles**

Inspect each source for admission, governance, founder or asset control, business power, discipline, coercion, dissent, expulsion, ostracism, schism, grievance, protected voice, usable exit, marriage or celibacy enforcement, external review, transition support, child conduct or protection, and later outcomes. Record exact PDF and printed-page locators where a finding is proposed.

- [x] **Step 3: Resolve every child-danger proximity candidate**

Classify each candidate as child actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. Require actor, allegation, assessment, intervention, review, and later outcome before treating a case as responsive to the dangerous-child question.

- [x] **Step 4: Draft the source report and proposed findings**

For every promoted row, fill every ledger field and preserve unresolved alternatives. Distinguish direct source claims from participant allegations and verification leads. Give every substantive non-promotion an explicit reason.

- [x] **Step 5: Reconcile findings into the existing gap bank**

Retain the 18-row B/C/D architecture unless a genuinely new article gap is established. Add verification leads and explicit non-promotions without treating corroboration as a new finding or gap.

### Task 4: Apply and verify the cumulative checkpoint

**Files:**
- Create: `recovered/update_v40.py`
- Create: `recovered/verify_v40.py`
- Modify: `recovered/COMMUNITIES-RESEARCH-STATE.md`
- Modify: `recovered/COMMUNITIES-SOURCE-INVENTORY.csv`
- Modify: `README.md`

**Interfaces:**
- Consumes: completed volume-40 dispositions and findings.
- Produces: idempotent cumulative artifacts and a verifier that proves the complete volume-40 boundary and exact volume-41 handoff.

- [x] **Step 1: Write the checkpoint verifier before the updater**

The verifier asserts nine member hashes, inventoried page counts, nonempty texts, exact dispositions, sequential finding IDs, valid gap references, report coverage, public-ID redaction, preservation of D-017's shared-archive row, and the next boundary at volume 41: 20 PDFs in issue 1, with 129 journal PDFs remaining.

- [x] **Step 2: Run the verifier and confirm RED**

```bash
python recovered/verify_v40.py
```

Expected: failure because cumulative artifacts still stop at volume 39.

- [x] **Step 3: Implement and run the idempotent updater**

```bash
python recovered/update_v40.py
python recovered/update_v40.py
```

The second run must produce no content change. The updater retains D-017's existing container provenance while marking only volume-40 member rows with their verified dispositions and current local corpus paths.

- [x] **Step 4: Run all final checks**

```bash
python -m py_compile recovered/recover_v40.py recovered/discover_v40.py recovered/update_v40.py recovered/verify_v40.py recovered/test_v40_workflow.py
python -m unittest recovered/test_v40_workflow.py -v
python recovered/verify_v40.py
git diff --check
```

Expected: zero failures, exact cumulative counts, and a printed volume-41 receipt.

### Task 5: Publish and read back the reusable checkpoint

**Files:**
- Add: the design, plan, volume-40 scripts, report, discovery ranking, and updated cumulative artifacts.
- Exclude: PDFs, ZIPs, extracted text, context dumps, PNG renders, partial downloads, and caches.

**Interfaces:**
- Consumes: the freshly verified local tree.
- Produces: a GitHub commit on `agent/volume-40-research` whose complete tree equals the verified local tree.

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
Add verified volume 40 research checkpoint
```

- [x] **Step 3: Publish and read back**

Publish `agent/volume-40-research`, compare the remote tree SHA and complete file list with the local commit, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub before reporting completion.
