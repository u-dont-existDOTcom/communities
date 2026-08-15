# Intentional Communities Evidence Audit

This repository preserves the reusable workflow and derived checkpoints for a source audit of *Communal Societies*. The active mode is **P0 research only**: the published article is not edited here.

## Current checkpoint

- Volumes **1-45** complete
- **984** journal PDFs triaged
- **443** relevant or contextual close reads
- **179** evidence findings (`F-001` through `F-179`)
- **18** reconciled article gaps: 8 partially present, 7 apparently missing, and 3 challenges
- Primary assigned corpus: **complete, 984 journal PDFs plus 8 standalone sources**

The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).

## Repository layout

- `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv` — finding-level evidence, source limits, alternative interpretations, outcomes, and verification needs
- `recovered/COMMUNITIES-SOURCE-INVENTORY.csv` — journal metadata, member hashes, extraction state, and dispositions; private Drive object IDs are redacted
- `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md` — reconciled implications for the article without changing its prose
- `recovered/COMMUNITIES-V*-RESEARCH-REPORT.md` — bounded checkpoint reports
- `recovered/V*-DISCOVERY-RANKING.csv` — reproducible reading-priority outputs; scores are not evidence weights
- `recovered/discover_*.py`, `update_*.py`, and `verify_*.py` — discovery, idempotent update, and regression workflow
- `docs/superpowers/plans/` — execution plans and scope constraints

## Verification

With the exact local source corpora restored beneath `recovered/corpus-v45/` and `recovered/corpus-standalone/`, run:

```bash
python recovered/test_adjacent_durable_transition_workflow.py
python recovered/verify_adjacent_durable_transition.py
```

The current verifier checks sequential findings through F-179, the 13-record cumulative adjacent inventory, the four Unit C source dispositions, unchanged gap classes, durable-transition and report coverage, the Unit D handoff, and exclusion of source binaries outside known local-only corpus roots. Source PDFs, ZIP containers, extracted full text, keyword contexts, and child-proximity contexts are intentionally excluded from Git.

## Evidence rules

- Keep source fact, author interpretation, alternative interpretation, process, outcome, and transferability separate.
- Promote only materially distinct findings; corroboration does not create a new gap by itself.
- Treat search scores as triage aids, never as evidence strength.
- Keep the dangerous-child branch bounded: a null within processed sources is not a claim of historical absence.
- Do not diagnose historical actors from conduct descriptions.
- Do not convert historical punishment, banishment, institutionalization, or state custody directly into modern recommendations.

