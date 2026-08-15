# Intentional Communities Evidence Audit

This repository preserves the reusable workflow and derived checkpoints for a source audit of *Communal Societies*. The active mode is **P0 research only**: the published article is not edited here.

## Current checkpoint

- Volumes **1-45** complete
- **984** journal PDFs triaged
- **443** relevant or contextual close reads
- **192** evidence findings (`F-001` through `F-192`)
- **19** reconciled article gaps: 8 partially present, 7 apparently missing, and 4 challenges
- Primary assigned corpus: **complete, 984 journal PDFs plus 8 standalone sources**
- Corrected cross-corpus synthesis: **complete; all 192 findings mapped across 13 themes**

The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The corrected corpus-wide conclusion is [`recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`](recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md), with finding-level coverage in [`recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`](recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv). The load-bearing state-monopoly correction is [`recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`](recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md).

## Repository layout

- `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv` — finding-level evidence, source limits, alternative interpretations, outcomes, and verification needs
- `recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md` — corpus-directed conclusions, tensions, boundaries, and remaining unknowns
- `recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md` — Zapatista, Cheran, CRAC-PC, and UNDRIP correction to the prior state-centric interface rule
- `recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-EVIDENCE-LEDGER.csv` — six bounded correction findings, F-187 through F-192
- `recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv` — one-row-per-finding map from all 186 findings to synthesis themes, claims, evidence roles, and article gaps
- `recovered/COMMUNITIES-SOURCE-INVENTORY.csv` — journal metadata, member hashes, extraction state, and dispositions; private Drive object IDs are redacted
- `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md` — reconciled implications for the article without changing its prose
- `recovered/COMMUNITIES-V*-RESEARCH-REPORT.md` — bounded checkpoint reports
- `recovered/V*-DISCOVERY-RANKING.csv` — reproducible reading-priority outputs; scores are not evidence weights
- `recovered/discover_*.py`, `update_*.py`, and `verify_*.py` — discovery, idempotent update, and regression workflow
- `docs/superpowers/plans/` — execution plans and scope constraints

## Verification

With the exact local source corpora restored beneath `recovered/corpus-v45/` and `recovered/corpus-standalone/`, run:

```bash
python recovered/test_autonomy_legal_pluralism_workflow.py
python recovered/verify_autonomy_legal_pluralism.py
```

The current verifier retains all Unit E checks, locks the evidence ledger and article-gap bank against synthesis-time mutation, requires one crosswalk row for every finding, verifies the twelve-theme and fifteen-claim architecture, confirms the three gap-unreferenced findings are nevertheless synthesized, and checks the final report's epistemic and transfer boundaries. Source PDFs, ZIP containers, extracted full text, keyword contexts, and child-proximity contexts are intentionally excluded from Git.

## Evidence rules

- Keep source fact, author interpretation, alternative interpretation, process, outcome, and transferability separate.
- Promote only materially distinct findings; corroboration does not create a new gap by itself.
- Treat search scores as triage aids, never as evidence strength.
- Keep the dangerous-child branch bounded: a null within processed sources is not a claim of historical absence.
- Do not diagnose historical actors from conduct descriptions.
- Do not convert historical punishment, banishment, institutionalization, or state custody directly into modern recommendations.

