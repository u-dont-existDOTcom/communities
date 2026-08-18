# Volume 40 Research Checkpoint Design

## Purpose

Extend the durable *Communal Societies* audit from volumes 1-39 through volume 40 while keeping the project in P0 research/source-audit mode. This checkpoint updates the source inventory, evidence ledger, article-gap bank, and research handoff without editing Joel's article prose or silently changing an article claim.

Joel's instruction to continue authorizes the established one-volume architecture used for volumes 33-39. Volume 40 contains only one nine-member issue, so the complete volume is also the smallest independently verifiable publisher boundary.

## Exact boundary

- Base branch: `agent/volume-39-research`; published base commit `34404cad4b4c739b8af1d488df08f3ed18b9dbcc`, local base commit `bdb1199c25682bc7f64ffa51135aedc2eec8e678`, and shared base tree `4472e52a3928c3abb0411e0db7ad7ab684054771`.
- Working branch: `agent/volume-40-research`.
- Inventory records: `M-0979` through `M-0987`.
- Corpus size: 9 PDFs, all in issue 1.
- Substantive reading boundary: 5 articles, `M-0982` through `M-0986`.
- Metadata boundary: 4 records: front matter `M-0979`, table of contents `M-0980`, editorial `M-0981`, and back matter `M-0987`.
- First possible new finding ID: `F-143`.
- Next handoff after completion: volume 41, 20 PDFs in issue 1; 129 journal PDFs remain in volumes 41-45.

## Research architecture

### 1. Corpus recovery and identity

Retrieve every volume-40 PDF from the primary ScholarWorks issue page. Browser filenames are untrusted; route downloads solely by SHA-256 to the pre-existing inventory destinations. Require all 9 hashes, inventoried page counts, nonempty page-preserving text extractions, and visible first-page identities to match before discovery.

Volume 40 is the last volume represented in the shared `vol35-40.zip` container. That container remains historical provenance rather than an input requirement. If it remains absent, preserve D-017's saved size, hash, path, status, and prior integrity-test note unchanged. Independently verifying all nine publisher members must not be reported as reverifying the absent container.

### 2. Discovery

Reuse the exact locked volume-39 danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome families. Discovery ranks reading order only; scores never become evidence weights. Produce one deterministic ranking row per record, complete keyword contexts, and separate child-danger proximity contexts while preserving form-feed page boundaries.

### 3. Close reading and evidence judgment

Metadata-triage `M-0979`, `M-0980`, `M-0981`, and `M-0987`. Close-read all five articles for admission, governance, founder control, business and asset power, discipline, coercion, dissent, expulsion, ostracism, schism, grievance, usable exit, marriage or celibacy enforcement, child conduct and protection, outside intervention, reintegration, and later outcomes.

Every substantive source receives one explicit disposition. Promote a finding only when it adds a materially distinct mechanism, response process, outcome, challenge, or bounded negative result. Corroboration belongs in source dispositions and gap reconciliation rather than duplicate findings.

For each proposed finding, separate direct source fact, participant allegation, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, exact source access, and verification needs. Historical clinical labels and legal conclusions cannot become present diagnoses or current legal advice. Positive and adverse outcomes remain independently recordable.

### 4. Dangerous-child branch

Resolve every child-danger proximity candidate by role: actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. A responsive case requires a persistently dangerous child as actor plus allegation, assessment, intervention, review, and later outcome. If the complete sequence is absent, record only a bounded volume-40 null; never convert search absence into a historical absence claim.

### 5. Reconciliation and cumulative state

Append sequential findings from `F-143` only where warranted. Reconcile them into the existing 18-item gap bank; create no new gap merely for corroboration. Update the inventory, evidence ledger, gap bank, README, research state, and volume-40 report through one idempotent updater. A fresh verifier must prove the complete boundary and exact volume-41 handoff.

The deterministic evidence ledger and 18-row gap bank remain the least-burdensome justified argument architecture for this P0 audit. No article dependency graph is added because no article premise or prose is changing.

## Public artifact boundary

Git includes this design, the implementation plan, scripts, tests, discovery ranking, report, and updated cumulative ledgers. Git excludes copyrighted PDFs, ZIPs, extracted full text, keyword and child-context dumps, rendered pages or contact sheets, partial downloads, caches, credentials, and non-redacted Drive object IDs.

## Failure handling

- Unknown or duplicate downloads stop routing rather than being guessed from filenames.
- Missing members, hash mismatches, page-count mismatches, empty texts, or visible identity failures block discovery and close reading.
- Publisher throttling or WAF challenges receive only conservative bounded retries in the authorized browser session; failures remain explicit and resumable.
- A verifier failure blocks commit and publication.
- Evidence that weakens a proposed interpretation is recorded before reconciliation; the finding is narrowed or withheld rather than rhetorically patched.
- Children described as victims, dependents, students, custody subjects, or objects of adult conflict cannot be counted as dangerous-child actors.

## Verification and publication

Require Python compilation, the complete volume-40 test suite, the fresh checkpoint verifier, updater idempotence, `git diff --check`, exact public-scope inspection, and a private-locator scan. Publish `agent/volume-40-research`, compare local and remote trees and complete file lists, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub.
