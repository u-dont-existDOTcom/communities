# Volume 36 Research Checkpoint Design

## Purpose

Extend the durable *Communal Societies* audit from volumes 1–35 through volume 36 while keeping the project in P0 research/source-audit mode. This checkpoint must improve the source inventory, evidence ledger, article-gap bank, and research handoff without editing Joel's article prose.

The approved design is the established per-volume checkpoint used for volumes 33–35. The instruction to continue to the next unit authorizes reuse of that architecture; no new research mode or editorial authority is introduced.

## Exact boundary

- Base branch: `agent/volume-35-research` at `8ba68f5adec215ab7a63374204a3d1384f98cdf4`.
- Working branch: `agent/volume-36-research`.
- Inventory records: `M-0889` through `M-0909`.
- Corpus size: 21 PDFs—10 in issue 1 and 11 in issue 2.
- Source kinds: 6 articles, 11 book reviews, 2 contents files, and 2 editorials.
- Substantive reading boundary: all 17 articles and reviews.
- First possible new finding ID: `F-122`.
- Next handoff after completion: volume 37, 26 PDFs—16 in issue 1 and 10 in issue 2; 207 journal PDFs remain in volumes 37–45.

## Research architecture

### 1. Corpus recovery and identity

Retrieve each volume-36 PDF from the journal's primary ScholarWorks issue pages. Browser filenames are untrusted; route downloads by SHA-256 to the pre-existing inventory paths. Require all 21 hashes, page counts, and nonempty page-preserving text extractions to match before analysis.

The shared `vol35-40.zip` archive is historical provenance, not a required input. If the container is absent, preserve its existing size, hash, path, status, and integrity-test note unchanged and state that it was not reverified. Do not infer container verification from independently verified members.

### 2. Discovery

Reuse the exact locked volume-35 term and process families. Discovery ranks reading order only; scores never become evidence weights. Produce one row per inventory record, a complete keyword-context file, and a separate child-danger proximity file. Preserve form-feed page boundaries and deterministic ordering.

### 3. Close reading and evidence judgment

Metadata-triage the two contents files and two editorials. Close-read all 17 substantive sources for admission, predation, violence, coercion, discipline, expulsion, ostracism, schism, grievance, protected dissent, leader or asset capture, exit, reintegration, outside intervention, child conduct, child protection, and outcomes.

Every substantive source receives one explicit disposition. Promote a finding only when it adds a materially distinct mechanism, process, outcome, challenge, or bounded negative result. Corroboration belongs in source dispositions and gap reconciliation rather than duplicate findings.

For each proposed finding, separate direct source fact, participant or author allegation, source interpretation, alternative interpretation, response process, outcome, transferability, confidence, source access, and verification needs. Historical clinical labels and legal conclusions cannot be converted into present diagnoses or current legal advice.

### 4. Dangerous-child branch

Resolve every proximity candidate by role: actor, victim, dependent, student, biographical/theological/fictional figure, or unrelated mention. A responsive case requires a persistently dangerous child as actor plus an allegation, assessment, intervention, review, and later outcome. If the complete sequence is absent, record only a bounded volume-36 null; never convert search absence into a historical claim of absence.

### 5. Reconciliation and cumulative state

Append sequential findings from `F-122` only where warranted. Reconcile them into the existing 18-item gap bank; create no new gap merely for corroboration. Update the inventory, evidence ledger, gap bank, README, research state, and a volume-36 report through one idempotent updater. A fresh verifier must prove the complete boundary and the exact volume-37 handoff.

The existing deterministic evidence and gap ledgers are the least-burdensome justified argument architecture for this P0 audit. A separate claim-dependency graph is unnecessary because no article premise or prose is being changed; any later authorized article revision must reassess that scope.

## Public artifact boundary

Git includes the design, implementation plan, scripts, tests, discovery ranking, report, and updated cumulative ledgers. Git excludes copyrighted PDFs, ZIPs, extracted full text, context dumps, rendered pages/contact sheets, partial downloads, caches, credentials, and non-redacted Drive object IDs.

## Failure handling

- Unknown or duplicate downloaded PDFs stop routing rather than being guessed from filenames.
- Missing members, hash mismatches, page-count mismatches, or empty texts block discovery and close reading.
- Publisher throttling or WAF challenges are retried conservatively in the authorized browser session; failures remain explicit and resumable.
- A verifier failure blocks commit and publication.
- Any new fact that weakens a load-bearing interpretation is recorded before reconciliation; the finding is narrowed or withheld rather than patched with rhetorical certainty.

## Verification and publication

Require Python compilation, the full volume-36 test suite, the fresh checkpoint verifier, idempotence of the updater, `git diff --check`, exact public-scope inspection, and a secret/private-locator scan. Publish `agent/volume-36-research`, then compare local and remote tree SHAs and changed-file lists and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub.
