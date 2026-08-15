# Public Research Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a research-only, public-facing transparency report derived from the completed 198-finding communities audit, prepare an appendix link for later article integration, and make the derivative artifact reproducible and verifiable without editing article prose.

**Architecture:** Keep the evidence ledger and final synthesis authoritative. Add one public Markdown comprehension layer under `docs/`, plus a research-only appendix-link handoff. A small idempotent updater refreshes only a delimited statistics block from the canonical CSVs; a verifier and regression test enforce thesis/evidence separation, exact counts, required provenance links, and the no-article-edit boundary.

**Tech Stack:** Markdown; Python 3 standard library; existing CSV/Markdown repository artifacts; Git/GitHub.

## Global Constraints

- Mode remains **P0 research only**; no published article prose is edited.
- Preserve Joel's thesis exactly: **communal living is a return to our evolved ancestral pattern; large societies breed anomie and capture by psychopaths.**
- State clearly that the completed corpus was not designed to test ancestral evolution, comparative anomie, psychopathy prevalence, or whether large societies are more capturable than small societies.
- Keep empirical findings, owner thesis, model-assisted synthesis, bounded nulls, and future verification needs distinct.
- Do not reopen volumes 1-45, the standalone corpus, completed adjacent units, legal-pluralism correction, or Escuelita descendant audit.
- The article-gap bank remains the future editorial change specification; do not silently apply it.
- Do not commit copyrighted PDFs, EPUBs, extracted full text, private Drive identifiers, credentials, browser state, or source ZIPs.
- Any later article insertion must use a registered authoritative article source/raw editor HTML; the present repository does not authorize article editing.

---

### Task 1: Public report and appendix handoff

**Files:**
- Create: `docs/PUBLIC-RESEARCH-REPORT.md`
- Create: `docs/ARTICLE-APPENDIX-RESEARCH-LINK.md`

**Interfaces:**
- Consumes: `recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`, `recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`, `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`, `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`, legal-pluralism and Escuelita reports.
- Produces: a public comprehension layer and an exact future appendix-link target; neither is article prose.

- [ ] **Step 1: Write the report with explicit thesis/evidence separation and an auto-statistics marker block.**
- [ ] **Step 2: Include the evidence ceiling, counterevidence, dangerous-child bounded null, legal-pluralism correction, Escuelita lineage ceiling, and remaining unknowns.**
- [ ] **Step 3: Link every technical audit layer needed to reproduce the report.**
- [ ] **Step 4: Write a separate appendix-link handoff that states no insertion has occurred and names the post-merge canonical GitHub target.**

### Task 2: Idempotent statistics updater

**Files:**
- Create: `recovered/update_public_research_report.py`

**Interfaces:**
- Consumes: `COMMUNITIES-EVIDENCE-LEDGER.csv`, `COMMUNITIES-SYNTHESIS-CROSSWALK.csv`, `COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv`, `COMMUNITIES-ARTICLE-GAP-BANK.md`, and the auto-statistics markers in `docs/PUBLIC-RESEARCH-REPORT.md`.
- Produces: byte-stable replacement of only the delimited public statistics block.

- [ ] **Step 1: Parse and validate sequential F-001 through F-198 finding IDs.**
- [ ] **Step 2: Derive close-read/corpus counts already encoded in the report authority, confidence counts, external-verification counts, theme counts, adjacent-record count, and B/C/D gap counts.**
- [ ] **Step 3: Replace exactly one marker block and fail on missing/duplicate markers.**
- [ ] **Step 4: Run twice and confirm no second-pass byte changes.**

### Task 3: Public-report verifier and regression test

**Files:**
- Create: `recovered/verify_public_research_report.py`
- Create: `recovered/test_public_research_report_workflow.py`

**Interfaces:**
- Consumes: the report, appendix handoff, updater, and canonical research artifacts.
- Produces: repository-contained PASS/FAIL checks for derivative integrity.

- [ ] **Step 1: Write verifier assertions for exact thesis wording, explicit non-test boundary, P0/no-edit statement, 198-finding coverage, verification disclosure, and required relative links.**
- [ ] **Step 2: Assert the report labels S-15/model-assisted synthesis as unvalidated as a complete package and treats the dangerous-child and Escuelita negative results as bounded evidence ceilings rather than absence claims.**
- [ ] **Step 3: Assert the appendix handoff says insertion has not occurred and does not claim raw Substack authority.**
- [ ] **Step 4: Write a temp-copy regression test: updater -> hash -> updater -> same hash -> verifier PASS.**
- [ ] **Step 5: Run verifier and regression test.**

### Task 4: Navigation and durable state

**Files:**
- Modify: `README.md`
- Modify: `docs/INDEX.md`
- Modify: `recovered/COMMUNITIES-RESEARCH-STATE.md`
- Modify: `docs/FRESH-CONVERSATION-HANDOFF.md`

**Interfaces:**
- Consumes: completed public-report unit.
- Produces: durable discovery and next-boundary routing for future workers.

- [ ] **Step 1: Link the public report from README and repository index.**
- [ ] **Step 2: Record that the public transparency artifact is complete while article editing remains unauthorized.**
- [ ] **Step 3: Record the next recommended phase as article integration plus claim-selective publication verification, not unbounded new research.**
- [ ] **Step 4: Preserve the option for a later new bounded research question if Joel chooses one.**

### Task 5: Verification, packaging, and GitHub durability

**Files:**
- Create locally for delivery: `communities-public-research-report-2026-08-15.zip`

**Interfaces:**
- Consumes: all new/modified repository files and selected non-copyrighted audit artifacts.
- Produces: verified GitHub commit on `agent/final-research-synthesis` and a downloadable ZIP with checksums.

- [ ] **Step 1: Run updater twice, public verifier, public regression test, current Escuelita regression/verifier, and `python -m compileall -q recovered`.**
- [ ] **Step 2: Run `git diff --check` and scan for forbidden binary/source artifacts.**
- [ ] **Step 3: Build a ZIP containing the public report, appendix handoff, final synthesis, crosswalk, evidence ledger, gap bank, legal-pluralism report, Escuelita report, and SHA-256 manifest.**
- [ ] **Step 4: Re-resolve the live GitHub branch head immediately before writing; create a fast-forward commit only if the expected parent is still current.**
- [ ] **Step 5: Fetch committed files and compare Git blob SHAs/content with the verified local artifacts.**
- [ ] **Step 6: Report the checkpoint in at most five bullets, the research-vs-integration decision, GitHub durability, and ZIP link.
