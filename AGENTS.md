# Intentional Communities research agent map

## Authority

1. Current owner and task scope
2. `docs/INDEX.md` for current research authority and read order
3. The active volume handoff/report, evidence ledger, source inventory, and gap bank named there
4. Current verification scripts, artifacts, and Git history
5. Relevant current patterns from `u-dont-existDOTcom/universal-dev-architecture`

This repository is P0 research unless the owner explicitly authorizes article editing.

## Validation

For an active checkpoint branch:

- Regression suite: `python recovered/test_adjacent_durable_transition_workflow.py` (or the current bounded-unit successor)
- Full source verification: `python recovered/verify_adjacent_durable_transition.py`; run source-dependent predecessor checks only when their exact local corpora are restored
- Syntax: `python -m compileall recovered`
- Patch hygiene: `git diff --check`

CI runs only repository-contained checks. Missing copyrighted/private source material must be reported as unavailable, never fabricated or treated as verified.

## Workflow

Use one volume-scoped task branch/worktree and a pull request. Keep source triage, close reading, findings, article-gap implications, and verification status distinct. Maintain a durable handoff and next boundary. Do not merge a checkpoint until its repository-contained tests pass and source-dependent receipts are explicitly recorded.

## Branch roles

- `main`: accepted canonical research checkpoints and governance
- `agent/volume-*-research`: volume-scoped research work and evidence updates
- task branches: governance or tooling changes

## Safety

Do not commit copyrighted PDFs, extracted full text, private Drive identifiers, credentials, browser/session state, or unrestricted context dumps. Hashes, derived metadata, bounded quotations, and reproducible findings remain subject to the project evidence rules.

## Code review rules

- Keep source fact, author interpretation, reviewer report, alternative interpretation, process, outcome, and transferability separate.
- A search score is a triage aid, not evidence strength; a bounded null is not a historical absence claim.
- Do not diagnose historical actors or convert historical punishment, banishment, institutionalization, or custody directly into modern recommendations.

Treat chat as disposable working memory. A fresh worker must recover the exact checkpoint and next boundary from Git.

