# Volume 39 Research Checkpoint Design

## Purpose

Extend the durable *Communal Societies* audit from volumes 1-38 through volume 39 while keeping the project in P0 research/source-audit mode. This checkpoint improves the source inventory, evidence ledger, article-gap bank, and research handoff without editing Joel's article prose or silently changing any article argument.

The instruction to continue authorizes reuse of the established per-volume architecture used for volumes 33-38. An issue-only checkpoint would split one journal volume, while processing volumes 39-40 together would enlarge the authenticated corpus and close-reading boundary without improving provenance. One complete volume remains the smallest independently verifiable unit.

## Exact boundary

- Base branch: `agent/volume-38-research`; published base commit `462f0467e35b36910b6497f4223cad8d8e2d8f8f`, local base commit `939427c5d42c9dbe36cd9cbea941e34af37f5475`, and shared base tree `d3bd8f6b1878b2e0a9b56965833bfa056f57c72e`.
- Working branch: `agent/volume-39-research`.
- Inventory records: `M-0956` through `M-0978`.
- Corpus size: 23 PDFs - 11 in issue 1 and 12 in issue 2.
- Substantive reading boundary: 15 sources - 8 issue-1 articles or reviews and 7 issue-2 articles or reviews.
- Metadata boundary: 8 sources - two front-matter files, two contents files, two editorials, and two back-matter files: `M-0956`, `M-0957`, `M-0958`, `M-0966`, `M-0967`, `M-0968`, `M-0969`, and `M-0978`.
- First possible new finding ID: `F-139`.
- Next handoff after completion: volume 40, 9 PDFs in issue 1; 138 journal PDFs remain in volumes 40-45.

## Research architecture

### 1. Corpus recovery and identity

Retrieve each volume-39 PDF from the journal's primary ScholarWorks issue pages. Browser filenames are untrusted; route downloads by SHA-256 to the pre-existing inventory paths. Require all 23 hashes, page counts, and nonempty page-preserving text extractions to match before analysis.

Volume 39 belongs to the shared `vol35-40.zip` container. The container is historical provenance rather than an input requirement. If it remains absent, preserve D-017's existing size, hash, path, status, and prior integrity-test note unchanged. Independently verified publisher members do not imply that the absent archive container was reverified.

### 2. Discovery

Reuse the exact locked volume-38 danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome families. Discovery ranks reading order only; scores never become evidence weights. Produce one ranking row per inventory record, complete keyword contexts, and separate child-danger proximity contexts. Preserve form-feed page boundaries and deterministic sorting.

### 3. Close reading and evidence judgment

Metadata-triage `M-0956`, `M-0957`, `M-0958`, `M-0966`, `M-0967`, `M-0968`, `M-0969`, and `M-0978`. Close-read all other 15 sources for admission, governance, founder control, financial custody, coercion, discipline, expulsion, ostracism, schism, grievance, protected dissent, usable exit, reintegration, outside intervention, child conduct, child protection, and later outcomes.

Every substantive source receives one explicit disposition. Promote a finding only when it adds a materially distinct mechanism, response process, outcome, challenge, or bounded negative result. Corroboration belongs in source dispositions and gap reconciliation rather than duplicate findings.

For each proposed finding, separate direct source fact, participant allegation, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, source access, and verification needs. Historical clinical labels and legal conclusions cannot become present diagnoses or current legal advice. Praise and criticism remain independently recordable.

### 4. Dangerous-child branch

Resolve every proximity candidate by role: actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. A responsive case requires a persistently dangerous child as actor plus allegation, assessment, intervention, review, and later outcome. If the complete sequence is absent, record only a bounded volume-39 null; never convert search absence into a historical claim of absence.

### 5. Reconciliation and cumulative state

Append sequential findings from `F-139` only where warranted. Reconcile them into the existing 18-item gap bank; create no new gap merely for corroboration. Update the inventory, evidence ledger, gap bank, README, research state, and a volume-39 report through one idempotent updater. A fresh verifier must prove the complete boundary and exact volume-40 handoff.

The deterministic evidence ledger and 18-row gap bank remain the least-burdensome justified argument architecture for this P0 audit. A separate claim-dependency graph is unnecessary because no article premise or prose is being changed; any later authorized article revision must reassess that scope.

## Public artifact boundary

Git includes this design, the implementation plan, scripts, tests, discovery ranking, report, and updated cumulative ledgers. Git excludes copyrighted PDFs, ZIPs, extracted full text, context dumps, rendered pages or contact sheets, partial downloads, caches, credentials, and non-redacted Drive object IDs.

## Failure handling

- Unknown or duplicate downloaded PDFs stop routing rather than being guessed from filenames.
- Missing members, hash mismatches, page-count mismatches, or empty texts block discovery and close reading.
- Publisher throttling or WAF challenges are retried conservatively in the authorized browser session; failures remain explicit and resumable.
- A verifier failure blocks commit and publication.
- Any new fact that weakens a material interpretation is recorded before reconciliation; the finding is narrowed or withheld rather than patched with rhetorical certainty.
- Children described as victims, dependents, students, custody subjects, or objects of adult conflict cannot be counted as dangerous-child actors.

## Verification and publication

Require Python compilation, the full volume-39 test suite, the fresh checkpoint verifier, updater idempotence, `git diff --check`, exact public-scope inspection, and a private-locator scan. Publish `agent/volume-39-research`, compare local and remote tree SHAs and complete file lists, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub.
