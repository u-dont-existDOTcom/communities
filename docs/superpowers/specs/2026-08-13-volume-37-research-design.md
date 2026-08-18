# Volume 37 Research Checkpoint Design

## Purpose

Extend the durable *Communal Societies* audit from volumes 1-36 through volume 37 while keeping the project in P0 research/source-audit mode. This checkpoint improves the source inventory, evidence ledger, article-gap bank, and research handoff without editing Joel's article prose.

The approved design is the established per-volume checkpoint used for volumes 33-36. The instruction to continue to the next unit authorizes reuse of that architecture; no new research mode or editorial authority is introduced.

## Exact boundary

- Base branch: `agent/volume-36-research`; published base commit `580367da174772824ac73eddbd1760d76136fea3` and local base tree `e52765a16760f35cce1c9fb5dbaaab9a497bdea7`.
- Working branch: `agent/volume-37-research`.
- Inventory records: `M-0910` through `M-0935`.
- Corpus size: 26 PDFs - 16 in issue 1 and 10 in issue 2.
- Source kinds: 10 articles, 10 book reviews, 2 front-matter files, 1 contents file, 1 table of contents, and 2 editorials.
- Substantive reading boundary: all 20 articles and reviews.
- First possible new finding ID: `F-126`.
- Next handoff after completion: volume 38, 20 PDFs - 11 in issue 1 and 9 in issue 2; 181 journal PDFs remain in volumes 38-45.

## Research architecture

### 1. Corpus recovery and identity

Retrieve each volume-37 PDF from the journal's primary ScholarWorks issue pages. Browser filenames are untrusted; route downloads by SHA-256 to the pre-existing inventory paths. Require all 26 hashes, page counts, and nonempty page-preserving text extractions to match before analysis.

The shared `vol35-40.zip` archive is historical provenance, not a required input. If the container is absent, preserve its existing size, hash, path, status, and integrity-test note unchanged and state that it was not reverified. Do not infer container verification from independently verified members.

### 2. Discovery

Reuse the exact locked volume-36 term and process families. Discovery ranks reading order only; scores never become evidence weights. Produce one row per inventory record, a complete keyword-context file, and a separate child-danger proximity file. Preserve form-feed page boundaries and deterministic ordering.

### 3. Close reading and evidence judgment

Metadata-triage the two front-matter files, contents file, table of contents, and two editorials. Close-read all 20 substantive sources for admission, predation, violence, coercion, discipline, expulsion, ostracism, schism, grievance, protected dissent, leader or asset capture, exit, reintegration, outside intervention, child conduct, child protection, and outcomes.

Every substantive source receives one explicit disposition. Promote a finding only when it adds a materially distinct mechanism, process, outcome, challenge, or bounded negative result. Corroboration belongs in source dispositions and gap reconciliation rather than duplicate findings.

For each proposed finding, separate direct source fact, participant or author allegation, source interpretation, alternative interpretation, response process, outcome, transferability, confidence, source access, and verification needs. Historical clinical labels and legal conclusions cannot be converted into present diagnoses or current legal advice.

### 4. Dangerous-child branch

Resolve every proximity candidate by role: actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. A responsive case requires a persistently dangerous child as actor plus an allegation, assessment, intervention, review, and later outcome. If the complete sequence is absent, record only a bounded volume-37 null; never convert search absence into a historical claim of absence.

### 5. Reconciliation and cumulative state

Append sequential findings from `F-126` only where warranted. Reconcile them into the existing 18-item gap bank; create no new gap merely for corroboration. Update the inventory, evidence ledger, gap bank, README, research state, and a volume-37 report through one idempotent updater. A fresh verifier must prove the complete boundary and the exact volume-38 handoff.

The existing deterministic evidence and gap ledgers remain the least-burdensome justified argument architecture for this P0 audit. A separate claim-dependency graph is unnecessary because no article premise or prose is being changed; any later authorized article revision must reassess that scope.

## Public artifact boundary

Git includes the design, implementation plan, scripts, tests, discovery ranking, report, and updated cumulative ledgers. Git excludes copyrighted PDFs, ZIPs, extracted full text, context dumps, rendered pages or contact sheets, partial downloads, caches, credentials, and non-redacted Drive object IDs.

## Failure handling

- Unknown or duplicate downloaded PDFs stop routing rather than being guessed from filenames.
- Missing members, hash mismatches, page-count mismatches, or empty texts block discovery and close reading.
- Publisher throttling or WAF challenges are retried conservatively in the authorized browser session; failures remain explicit and resumable.
- A verifier failure blocks commit and publication.
- Any new fact that weakens a material interpretation is recorded before reconciliation; the finding is narrowed or withheld rather than patched with rhetorical certainty.

## Verification and publication

Require Python compilation, the full volume-37 test suite, the fresh checkpoint verifier, idempotence of the updater, `git diff --check`, exact public-scope inspection, and a secret/private-locator scan. Publish `agent/volume-37-research`, compare local and remote tree SHAs and changed-file lists, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub.
