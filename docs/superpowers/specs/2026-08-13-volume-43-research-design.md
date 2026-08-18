# Volume 43 Research Checkpoint Design

## Purpose

Extend the durable *Communal Societies* audit from volumes 1-42 through volume 43 while keeping the project in P0 research/source-audit mode. This checkpoint updates the source inventory, evidence ledger, article-gap bank, and research handoff without editing Joel's article prose or silently changing an article claim.

Joel's instruction to continue authorizes the established one-volume architecture used for volumes 33-42. Volume 43 contains 20 members in issue 1 and 17 in issue 2, so the complete 37-member volume is the next independently verifiable publisher boundary. Processing one issue would leave a partial-volume checkpoint; combining volumes 43-45 would turn the bounded unit into an 85-PDF sweep without improving source identity or argument safety.

## Exact boundary

- Base branch: `agent/volume-42-research`; published base commit `97d1d39d700690bc5796232e35893ea24576ee42`, local base commit `e7cf1a1a71744a49fd533e51a39f248cb51a7c5c`, and shared base tree `3673e58347f894ab2f5fec32fb0d42cb50b398af`.
- Working branch: `agent/volume-43-research`.
- Inventory records: `M-0046` through `M-0082`.
- Corpus size: 37 PDFs: 20 in issue 1 and 17 in issue 2.
- Nonmetadata reading boundary: 29 sources--8 research articles, 18 book reviews, and 3 book notes. The inventory's broad `kind=article` label includes the three publication-designated book notes.
- Metadata boundary: 8 records: `M-0046`, `M-0047`, `M-0048`, `M-0065`, `M-0066`, `M-0067`, `M-0081`, and `M-0082`.
- First possible new finding ID: `F-152`.
- Next handoff after completion: volume 44, 33 PDFs--20 in issue 1 and 13 in issue 2; 48 journal PDFs remain in volumes 44-45.

## Research architecture

### 1. Corpus recovery and identity

Retrieve every volume-43 PDF from the two primary ScholarWorks issue pages. Browser filenames are untrusted; route downloads solely by SHA-256 to the pre-existing inventory destinations. Require all 37 hashes, inventoried page counts, nonempty page-preserving text extractions, and visible first-page identities to match before discovery.

Volume 43 shares `COMMUNAL-SOCIETIES-v41-v45.zip`, inventory record `D-003`, with volumes 41-42. The container is historical provenance rather than an input requirement. If it remains absent, preserve D-003's saved size, hash, path, status, and prior integrity-test note byte-for-byte. Independently verifying publisher members must not be reported as reverifying the absent archive container.

### 2. Discovery

Reuse the exact locked volume-42 danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome families. Discovery ranks reading order only; scores never become evidence weights. Produce one deterministic ranking row per record, complete keyword contexts, and separate child-danger proximity contexts while preserving form-feed page boundaries.

### 3. Close reading and evidence judgment

Metadata-triage `M-0046`, `M-0047`, `M-0048`, `M-0065`, `M-0066`, `M-0067`, `M-0081`, and `M-0082`. Close-read all 29 nonmetadata sources, including every research article, book review, and book note, for admission, governance, founder control, business and asset power, discipline, coercion, dissent, expulsion, ostracism, schism, grievance, usable exit, marriage or celibacy enforcement, disability and care, child conduct and protection, outside intervention, reintegration, and later outcomes.

Every nonmetadata source receives one explicit disposition. Promote a finding only when it adds a materially distinct mechanism, response process, outcome, challenge, or bounded negative result. Corroboration belongs in source dispositions and gap reconciliation rather than duplicate findings.

For each proposed finding, separate direct source fact, participant allegation, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, exact source access, and verification needs. Historical clinical labels and legal conclusions cannot become present diagnoses or current legal advice. Positive and adverse outcomes remain independently recordable. A book review or book note may establish only what its writer directly reports or evaluates; claims about the discussed book require access to the book itself before being treated as book-level findings.

### 4. Dangerous-child branch

Resolve every child-danger proximity candidate by role: actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. A responsive case requires a persistently dangerous child as actor plus allegation, assessment, intervention, review, and later outcome. If the complete sequence is absent, record only a bounded volume-43 null; never convert search absence into a historical absence claim.

### 5. Reconciliation and cumulative state

Append sequential findings from `F-152` only where warranted. Reconcile them into the existing 18-item gap bank; create no new gap merely for corroboration. Update the inventory, evidence ledger, gap bank, README, research state, and volume-43 report through one idempotent updater. A fresh verifier must prove the complete boundary and exact volume-44 handoff.

The deterministic evidence ledger and 18-row gap bank remain the least-burdensome justified argument architecture for this P0 audit. No article dependency graph is added because no article premise or prose is changing. If a source challenges a load-bearing article premise, record that challenge and its evidence boundaries for later author review; do not repair the article inside this checkpoint.

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

Require Python compilation, the complete volume-43 test suite, the fresh checkpoint verifier, updater idempotence, `git diff --check`, exact public-scope inspection, and a private-locator scan. Publish `agent/volume-43-research`, compare local and remote trees and complete file lists, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub.
