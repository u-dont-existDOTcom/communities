# Volume 33 Research Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Extend the verified *Communal Societies* source audit from volumes 1-32 through volume 33 without changing Joel's published article.

**Architecture:** Recover the 36 inventoried PDFs from the journal's primary publisher, require each PDF to match the pre-existing SHA-256 inventory, extract text, run the same discovery and dangerous-child searches used for volume 32, then update the cumulative report and ledgers only for materially distinct findings. Treat the repository as the durable home for plans, scripts, reports, and tabular checkpoints; exclude copyrighted source PDFs and generated extracted text.

**Tech Stack:** Python 3 standard library, Poppler (`pdftotext`, `pdfinfo`), `curl`, CSV/Markdown ledgers, Git, GitHub.

## Global Constraints

- Primary mode is **P0 research/source audit only**. Do not edit article prose.
- Do not repeat volumes 1-32; begin with `M-0798` and volume 33.
- Process all **36 PDFs**: 14 in issue 1 and 22 in issue 2.
- Preserve the existing article argument; new evidence may update the evidence ledger and gap bank but cannot silently change Joel's claims.
- Record source access exactly and separate facts, author interpretation, alternatives, process, outcome, transferability, and verification needs.
- A bounded dangerous-child null is not a historical claim of absence.
- Do not diagnose historical actors with ASPD or psychopathy without appropriate clinical evidence.
- Keep copyrighted PDFs and extracted text out of Git; commit only reusable workflow code and derived research artifacts.

---

### Task 1: Recover and authenticate the volume 33 corpus

**Files:**
- Create locally only: `recovered/corpus-v33/vol33/iss1/*.pdf`
- Create locally only: `recovered/corpus-v33/vol33/iss2/*.pdf`
- Modify: `recovered/COMMUNITIES-SOURCE-INVENTORY.csv`

**Interfaces:**
- Consumes: the 36 volume-33 inventory rows and publisher issue pages.
- Produces: one nonempty local PDF and one extracted text file for every `M-0798` through `M-0833`, with the inventoried SHA-256 unchanged.

- [x] **Step 1: Enumerate the expected source boundary**

Run:

```bash
python - <<'PY'
import csv
rows = [r for r in csv.DictReader(open('recovered/COMMUNITIES-SOURCE-INVENTORY.csv', encoding='utf-8')) if r['volume'] == '33']
assert len(rows) == 36
assert sum(r['issue'] == '1' for r in rows) == 14
assert sum(r['issue'] == '2' for r in rows) == 22
print('volume33 rows=36 issue1=14 issue2=22')
PY
```

- [x] **Step 2: Retrieve primary-publisher PDFs**

Download the issue-page PDF links from:

```text
https://scholarworks.gvsu.edu/communalsocieties/vol33/iss1/
https://scholarworks.gvsu.edu/communalsocieties/vol33/iss2/
```

Map publisher article IDs to inventory order, including front matter and back matter, and save each PDF at its inventoried `internal_filename` beneath `recovered/corpus-v33/`.

- [x] **Step 3: Verify every member hash before analysis**

Run:

```bash
python - <<'PY'
import csv, hashlib
from pathlib import Path
root = Path('recovered/corpus-v33')
rows = [r for r in csv.DictReader(open('recovered/COMMUNITIES-SOURCE-INVENTORY.csv', encoding='utf-8')) if r['volume'] == '33']
for row in rows:
    path = root / row['internal_filename']
    assert path.is_file() and path.stat().st_size > 0, row['record_id']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], row['record_id']
print('volume33 member hashes=36')
PY
```

- [x] **Step 4: Extract full text and page metadata**

Run `pdftotext -layout` for all 36 PDFs and retain form-feed page boundaries. Record nonempty text and `pdfinfo` page counts.

### Task 2: Build and prove the discovery workflow

**Files:**
- Create: `recovered/test_v33_workflow.py`
- Create: `recovered/discover_v33.py`
- Create: `recovered/V33-DISCOVERY-RANKING.csv`
- Create: `recovered/v33-keyword-contexts.txt`
- Create: `recovered/v33-child-danger-contexts.txt`

**Interfaces:**
- Consumes: all 36 extracted volume-33 texts and inventory metadata.
- Produces: a complete ranking, keyword-context file, and child-as-dangerous-actor candidate file.

- [x] **Step 1: Write the failing workflow test**

```python
def test_volume_33_discovery_outputs():
    rows = load_csv(ROOT / 'V33-DISCOVERY-RANKING.csv')
    assert len(rows) == 36
    assert {row['record_id'] for row in rows} == EXPECTED_VOLUME_33_IDS
    assert all((ROOT / row['file'].removeprefix('recovered/')).is_file() for row in rows)
```

- [x] **Step 2: Run the test and confirm RED**

Run:

```bash
python -m unittest recovered/test_v33_workflow.py -v
```

Expected: failure because `V33-DISCOVERY-RANKING.csv` and `discover_v33.py` do not yet exist.

- [x] **Step 3: Implement volume-33 discovery**

Adapt the locked volume-32 term families without weakening or broadening their meanings: danger, sanction, governance, child, exit, clinical, plus allegation, assessment, intervention, review, and outcome process families. Scores rank reading order only; they are never evidence weights.

- [x] **Step 4: Run discovery and confirm GREEN**

Run:

```bash
python recovered/discover_v33.py
python -m unittest recovered/test_v33_workflow.py -v
```

Expected: 36 ranking rows; every substantive source represented; child candidate count reported.

### Task 3: Complete source dispositions and finding analysis

**Files:**
- Create: `recovered/COMMUNITIES-V33-RESEARCH-REPORT.md`
- Modify: `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`

**Interfaces:**
- Consumes: ranking, contexts, all relevant full texts, and the cumulative evidence/gap ledgers.
- Produces: one defensible disposition for every PDF and sequential findings beginning at `F-112` only when materially distinct.

- [x] **Step 1: Metadata-triage front matter, contents, editorials, and back matter**

Record metadata items separately; do not inflate them into substantive close reads.

- [x] **Step 2: Close-read all sources that can affect the research question**

Prioritize admission, leader control, financial custody, discipline, coercion, expulsion, schism, exit, grievance, independent review, child conduct/protection, and later outcomes. Inspect every hit in context rather than promoting keyword co-occurrence.

- [x] **Step 3: Resolve the dangerous-child branch**

For every proximity candidate, classify the child as actor, victim, dependent, student, biographical subject, or unrelated mention. Promote a bounded negative finding only if no case supplies the requested actor-to-outcome sequence.

- [x] **Step 4: Draft findings with source limits**

For each proposed `F-112+` row, fill every ledger field, including `what_source_does_not_establish`, `alternative_interpretation`, `outcome`, `transferability`, and `external_verification_needed`.

### Task 4: Apply and verify the cumulative checkpoint

**Files:**
- Create: `recovered/update_v33.py`
- Create: `recovered/verify_v33.py`
- Modify: `recovered/COMMUNITIES-RESEARCH-STATE.md`
- Modify: `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`
- Modify: `recovered/COMMUNITIES-SOURCE-INVENTORY.csv`

**Interfaces:**
- Consumes: approved volume-33 dispositions and findings.
- Produces: idempotent durable ledgers and a fresh structural verification receipt.

- [x] **Step 1: Write the final checkpoint verifier before the updater**

The verifier must assert corpus hashes, nonempty text, exact disposition totals, sequential finding IDs, valid gap references, the volume-33 report table, and the next boundary at volume 34.

- [x] **Step 2: Run the verifier and confirm RED**

Run:

```bash
python recovered/verify_v33.py
```

Expected: failure because the cumulative files still stop at volume 32.

- [x] **Step 3: Implement and run the idempotent updater**

Run:

```bash
python recovered/update_v33.py
```

- [x] **Step 4: Run all final checks**

Run:

```bash
python -m py_compile recovered/discover_v33.py recovered/update_v33.py recovered/verify_v33.py
python -m unittest recovered/test_v33_workflow.py -v
python recovered/verify_v33.py
git diff --check
```

Expected: zero failures and a printed receipt for the complete volume-33 boundary.

### Task 5: Publish the reusable checkpoint

**Files:**
- Create: `README.md`
- Create: `.gitignore`
- Add: all cumulative Markdown/CSV reports and Python workflow scripts
- Exclude: source PDFs, ZIP archives, extracted text, temporary download files, and Python caches

**Interfaces:**
- Consumes: the freshly verified local checkpoint.
- Produces: a GitHub commit containing the reusable plan, workflow, reports, and ledgers.

- [x] **Step 1: Inspect the exact Git scope**

Run:

```bash
git status --short
git diff --check
```

- [x] **Step 2: Commit only derived artifacts**

Use commit message:

```text
Add verified volume 33 research checkpoint
```

- [x] **Step 3: Publish and read back**

Publish the commit to `u-dont-existDOTcom/communities`, then read back the repository tree and the checkpoint state file to confirm the remote contains the verified boundary.
