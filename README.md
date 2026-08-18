# Intentional Communities Evidence Audit

This repository preserves the reusable workflow and derived checkpoints for a source audit of *Communal Societies*. The active mode is **P0 research only**: the published article is not edited here.

## Current checkpoint

- Volumes **1-44** complete
- **969** journal PDFs triaged
- **432** relevant or contextual close reads
- **158** evidence findings (`F-001` through `F-158`)
- **18** reconciled article gaps: 8 partially present, 7 apparently missing, and 3 challenges
- Next unit: **volume 45, 15 PDFs** (all in issue 1)

The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-V44-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V44-RESEARCH-REPORT.md).

## Repository layout

- `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv` — finding-level evidence, source limits, alternative interpretations, outcomes, and verification needs
- `recovered/COMMUNITIES-SOURCE-INVENTORY.csv` — journal metadata, member hashes, extraction state, and dispositions; private Drive object IDs are redacted
- `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md` — reconciled implications for the article without changing its prose
- `recovered/COMMUNITIES-V*-RESEARCH-REPORT.md` — bounded checkpoint reports
- `recovered/V*-DISCOVERY-RANKING.csv` — reproducible reading-priority outputs; scores are not evidence weights
- `recovered/discover_*.py`, `update_*.py`, and `verify_*.py` — discovery, idempotent update, and regression workflow
- `docs/superpowers/plans/` — execution plans and scope constraints

## Verification

With the exact local source corpus restored beneath `recovered/corpus-v44/`, run:

```bash
python recovered/test_v44_workflow.py
python recovered/verify_v44.py
```

The verifier checks all 33 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-45 boundary. Source PDFs, ZIP containers, extracted full text, keyword contexts, and child-proximity contexts are intentionally excluded from Git.

## Evidence rules

- Keep source fact, author interpretation, alternative interpretation, process, outcome, and transferability separate.
- Promote only materially distinct findings; corroboration does not create a new gap by itself.
- Treat search scores as triage aids, never as evidence strength.
- Keep the dangerous-child branch bounded: a null within processed sources is not a claim of historical absence.
- Do not diagnose historical actors from conduct descriptions.
- Do not convert historical punishment, banishment, institutionalization, or state custody directly into modern recommendations.
