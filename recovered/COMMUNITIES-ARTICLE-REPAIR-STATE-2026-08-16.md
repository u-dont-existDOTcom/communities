# Communities article repair state — 2026-08-17

Mode: article harmonization authorized; **proposal review in progress**; humanization not started.

## Authority boundary

The uploaded raw Substack editor HTML remains the article baseline. The research-repair candidate described below is **not owner-approved article authority**. It exists only for commentable original-vs-proposed review.

## Completed

- Dedicated branch: `agent/article-repair-20260816`, based on research head `f344d979f7b8f1c2991408b969240d3ed482d4a3`.
- Canonical research change specification reconciled through G-001–G-028.
- Twenty repair operations cover the selected G-001–G-028 applications plus directly relevant C001/C003/C025/C026 integrations.
- The owner's selective-membership/ejection thesis and autonomous-governance correction remain explicit; the candidate does not impose universal inclusion or state-monopoly correction.
- Current FEC publication claims and the March 2026 Sénégal Article 319 correction were source-hardened before proposal review.
- The public research-report link was corrected to an immutable commit URL because `main` does not currently contain `docs/PUBLIC-RESEARCH-REPORT.md`.
- Fail-closed raw-HTML patch architecture and tests remain durable in this branch.

## Current raw baseline

Current-conversation upload: `Pasted text(1).txt`.

SHA-256:

`0062af91b00b637482217755276db3c2b7379f1fb52952e8a1bc39ed90062e86`

This raw editor HTML is the sole authority for links, hierarchy, captions, source order, and native-object identity/placement.

## Current unapproved review candidate

Candidate SHA-256:

`73fba9d8fc486b9a6a6a66994ac339b0d1718d594ea6a160896a05d0dca92fbf`

Commentable changed-passages review SHA-256:

`82f55af92e6d8a2c971b4c720e7ebaba35ec48c81217d41d28e10ceb64da8176`

Review properties:

- 35 changed rows;
- 42 commentable old/new cells;
- `joel-commentable-diff-review-v4` metadata;
- baseline = exact uploaded raw editor source;
- proposal = research-repair candidate;
- Keep / Remove / Brainstorm;
- whole-passage and exact selected-text comments with offsets;
- Humor / Technical detail / Length / Bluntness controls;
- search, changed-only filtering, JSON/Markdown export and copy.

## Cold audits performed before owner review

Two cold audits repaired identified weaknesses before showing the candidate:

1. moved `Experiment Before You Divorce` out of the Founderism four-question sequence and removed its orphaned `parallel` reference;
2. preserved the old dissolution paragraph's unresolved-claims function instead of silently dropping it;
3. corrected autonomous-review wording so it does not imply automatic nation-state supremacy;
4. compressed the federation material from gap-bank/checklist prose into a movement-level argument;
5. rewrote the Escuelita limitation in article language and restored the pre-2013 diffusion attribution control;
6. replaced the weak prison analogy with the actual costly-exit/retention distinction;
7. removed an unnecessary wolves-and-sheep flourish from the non-waivable-rights paragraph;
8. moved premove simulations after the general conduct-evidence rule so the original/new paragraph alignment and thought sequence remain intelligible;
9. fixed the research-report destination to an immutable existing public file.

These cold-audit changes are part of the **review candidate**, not owner-approved prose. The earlier durable operations file remains the pre-review operation set until owner comments are reconciled; do not treat it as the final accepted patch specification.

## Native-object validation

`html_islands.py inventory` on baseline and candidate found 26 semantic/native objects in each. Ordered `(object type, exact source SHA-256)` sequences are identical.

Current inventory by type:

- 19 images;
- 3 digest-post embeds;
- 2 iframe/video embeds;
- 1 Instagram embed;
- 1 Share object.

This establishes source-level object identity/order only. It does not prove final clipboard/Substack destination reconstruction.

## Commentable-review verification

Static review validation: PASS.

Headless Chromium interaction test via the environment-permitted `set_content` path: PASS for decisions, selected-text quote/offset capture, comments, sliders, search, drawer, JSON export, Markdown export, and zero console/page errors.

The environment blocks both `file://` and localhost navigation, so localStorage persistence across reopening the downloaded local HTML cannot be re-proven here. That remains a real Opera/local-file review-interface check, separate from source fidelity and static interaction behavior.

## Exact next action

Deliver the **commentable changed-passages diff first**. Joel reviews it and exports JSON or Markdown comments/decisions. Do not promote the candidate to article authority and do not build the final Substack transfer helper yet.

After Joel returns the review export:

1. reconcile every comment/Keep/Remove/Brainstorm decision;
2. re-run semantic/coherence cold audits;
3. update the durable operations file to the accepted repair set;
4. generate the complete authoritative archival HTML;
5. verify native-object source fidelity again;
6. build/retest the Substack transfer helper from that exact accepted archival HTML;
7. only afterward begin humanization/detector work.
