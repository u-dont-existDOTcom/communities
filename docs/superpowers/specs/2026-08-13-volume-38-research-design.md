# Volume 38 Research Checkpoint Design

## Purpose

Extend the durable *Communal Societies* audit from volumes 1-37 through volume 38 while keeping the project in P0 research/source-audit mode. This checkpoint improves the source inventory, evidence ledger, article-gap bank, and research handoff without editing Joel's article prose.

The instruction to continue to the next unit authorizes reuse of the established per-volume architecture used for volumes 33-37. Three boundaries were considered: one volume, the remainder of the 35-40 archive, or metadata-only processing from saved inventory records. One volume is selected because it supplies a complete, independently verifiable issue boundary without deferring source authentication or creating an oversized close-reading batch.

## Exact boundary

- Base branch: `agent/volume-37-research`; published base commit `8e230ca4ea549e149aac6a587915d0644ef17084` and local base tree `0bbd7b51a09140cee8aa6fd5de7b12fb73a978b1`.
- Working branch: `agent/volume-38-research`.
- Inventory records: `M-0936` through `M-0955`.
- Corpus size: 20 PDFs - 11 in issue 1 and 9 in issue 2.
- Substantive reading boundary: 13 sources - 8 issue-1 articles or reviews and 5 issue-2 articles.
- Metadata boundary: 7 sources - front matter, two editorials, contents, table of contents, contributors, and the Jonestown bibliography. The inventory labels the last two as articles, but their document functions are metadata; the source report will preserve that distinction explicitly.
- First possible new finding ID: `F-132`.
- Next handoff after completion: volume 39, 23 PDFs - 11 in issue 1 and 12 in issue 2; 161 journal PDFs remain in volumes 39-45.

## Research architecture

### 1. Corpus recovery and identity

Retrieve each volume-38 PDF from the journal's primary ScholarWorks issue pages. Browser filenames are untrusted; route downloads by SHA-256 to the pre-existing inventory paths. Require all 20 hashes, page counts, and nonempty page-preserving text extractions to match before analysis.

The shared `vol35-40.zip` archive is historical provenance, not a required input. If the container is absent, preserve its existing size, hash, path, status, and integrity-test note unchanged and state that it was not reverified. Independently verified publisher members do not imply verification of the absent archive container.

### 2. Discovery

Reuse the exact locked volume-37 danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome families. Discovery ranks reading order only; scores never become evidence weights. Produce one row per inventory record, complete keyword contexts, and separate child-danger proximity contexts. Preserve form-feed page boundaries and deterministic ordering.

### 3. Close reading and evidence judgment

Metadata-triage `M-0936`, `M-0937`, `M-0938`, `M-0947`, `M-0948`, `M-0949`, and `M-0955`. Close-read all other 13 sources for admission, predation, violence, coercion, discipline, expulsion, ostracism, schism, grievance, protected dissent, leader or asset capture, exit, reintegration, outside intervention, child conduct, child protection, and outcomes.

Every substantive source receives one explicit disposition. Promote a finding only when it adds a materially distinct mechanism, process, outcome, challenge, or bounded negative result. Corroboration belongs in source dispositions and gap reconciliation rather than duplicate findings.

For each proposed finding, separate direct source fact, participant or author allegation, source interpretation, alternative interpretation, response process, outcome, transferability, confidence, source access, and verification needs. Historical clinical labels and legal conclusions cannot become present diagnoses or current legal advice. Praise and criticism remain independently recordable.

### 4. Dangerous-child branch

Resolve every proximity candidate by role: actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. A responsive case requires a persistently dangerous child as actor plus an allegation, assessment, intervention, review, and later outcome. If the complete sequence is absent, record only a bounded volume-38 null; never convert search absence into a historical claim of absence.

### 5. Reconciliation and cumulative state

Append sequential findings from `F-132` only where warranted. Reconcile them into the existing 18-item gap bank; create no new gap merely for corroboration. Update the inventory, evidence ledger, gap bank, README, research state, and a volume-38 report through one idempotent updater. A fresh verifier must prove the complete boundary and exact volume-39 handoff.

The existing deterministic evidence and gap ledgers remain the least-burdensome justified argument architecture for this P0 audit. A separate claim-dependency graph is unnecessary because no article premise or prose is being changed; any later authorized article revision must reassess that scope.

## Public artifact boundary

Git includes this design, the implementation plan, scripts, tests, discovery ranking, report, and updated cumulative ledgers. Git excludes copyrighted PDFs, ZIPs, extracted full text, context dumps, rendered pages or contact sheets, partial downloads, caches, credentials, and non-redacted Drive object IDs.

## Failure handling

- Unknown or duplicate downloaded PDFs stop routing rather than being guessed from filenames.
- Missing members, hash mismatches, page-count mismatches, or empty texts block discovery and close reading.
- Publisher throttling or WAF challenges are retried conservatively in the authorized browser session; failures remain explicit and resumable.
- The semantic metadata reclassification of contributors and bibliography must remain visible in the report and verifier rather than silently altering their historical inventory kinds.
- A verifier failure blocks commit and publication.
- Any new fact that weakens a material interpretation is recorded before reconciliation; the finding is narrowed or withheld rather than patched with rhetorical certainty.

## Verification and publication

Require Python compilation, the full volume-38 test suite, the fresh checkpoint verifier, updater idempotence, `git diff --check`, exact public-scope inspection, and a private-locator scan. Publish `agent/volume-38-research`, compare local and remote tree SHAs and changed-file lists, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub.
