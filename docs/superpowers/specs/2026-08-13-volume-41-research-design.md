# Volume 41 Research Checkpoint Design

## Purpose

Extend the durable *Communal Societies* audit from volumes 1-40 through volume 41 while keeping the project in P0 research/source-audit mode. This checkpoint updates the source inventory, evidence ledger, article-gap bank, and research handoff without editing Joel's article prose or silently changing an article claim.

Joel's instruction to continue authorizes the established one-volume architecture used for volumes 33-40. Volume 41 contains one 20-member issue, so the complete volume is also the smallest independently verifiable publisher boundary.

## Exact boundary

- Base branch: `agent/volume-40-research`; published base commit `a3a7552a15daa06b222cca01d907d6c0a483f3ab`, local base commit `fb12e9b072e81b9a4444be3df02449d54821e2db`, and shared base tree `253f4c97aaebd06d5939ffb844048726226cd7e4`.
- Working branch: `agent/volume-41-research`.
- Inventory records: `M-0002` through `M-0021`.
- Corpus size: 20 PDFs, all in issue 1.
- Nonmetadata reading boundary: 16 sources—8 articles and 8 book reviews.
- Metadata boundary: 4 records: back matter `M-0004`, editorial `M-0019`, table of contents `M-0020`, and front matter `M-0021`.
- First possible new finding ID: `F-147`.
- Next handoff after completion: volume 42, 24 PDFs across issues 1 and 2; 109 journal PDFs remain in volumes 42-45.

## Research architecture

### 1. Corpus recovery and identity

Retrieve every volume-41 PDF from the primary ScholarWorks issue page. Browser filenames are untrusted; route downloads solely by SHA-256 to the pre-existing inventory destinations. Require all 20 hashes, inventoried page counts, nonempty page-preserving text extractions, and visible first-page identities to match before discovery.

Volume 41 is the first volume represented in `COMMUNAL-SOCIETIES-v41-v45.zip`, inventory record `D-003`. The container is historical provenance rather than an input requirement. If it remains absent, preserve D-003's saved size, hash, path, status, and prior integrity-test note unchanged. Independently verifying publisher members must not be reported as reverifying the absent archive container.

### 2. Discovery

Reuse the exact locked volume-40 danger, sanction, governance, child, exit, clinical, allegation, assessment, intervention, review, and outcome families. Discovery ranks reading order only; scores never become evidence weights. Produce one deterministic ranking row per record, complete keyword contexts, and separate child-danger proximity contexts while preserving form-feed page boundaries.

### 3. Close reading and evidence judgment

Metadata-triage `M-0004`, `M-0019`, `M-0020`, and `M-0021`. Close-read all 16 nonmetadata sources, including every article and book review, for admission, governance, founder control, business and asset power, discipline, coercion, dissent, expulsion, ostracism, schism, grievance, usable exit, marriage or celibacy enforcement, disability and care, child conduct and protection, outside intervention, reintegration, and later outcomes.

Every nonmetadata source receives one explicit disposition. Promote a finding only when it adds a materially distinct mechanism, response process, outcome, challenge, or bounded negative result. Corroboration belongs in source dispositions and gap reconciliation rather than duplicate findings.

For each proposed finding, separate direct source fact, participant allegation, author interpretation, alternative interpretation, response process, outcome, transferability, confidence, exact source access, and verification needs. Historical clinical labels and legal conclusions cannot become present diagnoses or current legal advice. Positive and adverse outcomes remain independently recordable. A book review may establish only what the reviewer directly reports or evaluates; claims about the reviewed book require access to the book itself before being treated as book-level findings.

### 4. Dangerous-child branch

Resolve every child-danger proximity candidate by role: actor, victim, dependent, student, biographical, theological, fictional, or unrelated mention. A responsive case requires a persistently dangerous child as actor plus allegation, assessment, intervention, review, and later outcome. If the complete sequence is absent, record only a bounded volume-41 null; never convert search absence into a historical absence claim.

### 5. Reconciliation and cumulative state

Append sequential findings from `F-147` only where warranted. Reconcile them into the existing 18-item gap bank; create no new gap merely for corroboration. Update the inventory, evidence ledger, gap bank, README, research state, and volume-41 report through one idempotent updater. A fresh verifier must prove the complete boundary and exact volume-42 handoff.

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

Require Python compilation, the complete volume-41 test suite, the fresh checkpoint verifier, updater idempotence, `git diff --check`, exact public-scope inspection, and a private-locator scan. Publish `agent/volume-41-research`, compare local and remote trees and complete file lists, and read back `COMMUNITIES-RESEARCH-STATE.md` from GitHub.
