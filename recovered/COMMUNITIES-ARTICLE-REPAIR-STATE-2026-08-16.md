# Communities article repair state — 2026-08-17

Mode: article harmonization authorized; **r05 architecture/dedup candidate committed for owner review**; detector/humanization not started.

## Current owner baseline

Joel supplied fresh raw Substack editor HTML after manually replacing two broken Instagram native embeds with ordinary Instagram post links because Substack's Instagram embed behavior had failed.

Owner raw source SHA-256:

`d4e46ce84636ab038b1e3b80f1a6f6246242b8e482d43ed648b51595d441eab5`

Those two ordinary links are now source authority for this task:

- `https://instagram.com/p/DVyl1a2lAuZ/`
- `https://instagram.com/p/DaLvZV2qIk2/`

Do not reconstruct native Instagram embeds from them.

## Prior accepted checkpoint

r02 was owner-accepted during the earlier research-repair/comment cycle. Later r03/r04 local passes integrated the Zapatista, money-free-community, Auroville, couple-problem, Liedloff, and directory-scope corrections. r05 starts from Joel's newly supplied raw Substack source, not from an older helper.

## r05 article candidate

Article SHA-256:

`ccdbca020251e9fab8d60c5ce343d8e42347581e9f13a63e568a0154eb6098bc`

Main architecture repairs:

1. consolidated the early `How Much Attention Do You Actually Have for Other People?` setup into `The Math of Absorption, and Who This Isn’t For`;
2. removed repeated escuelita explanations while preserving opening definition and Zapatista evidence/payoff;
3. separated the Zapatista example from Joel's own movement design under new H1 `From One Community to a Movement`;
4. moved `Please Choose the Values Before Falling in Love With the View` into the forming-group branch;
5. moved the sexuality/gender compatibility paragraph into that values section, restoring the antecedent of `that list`;
6. promoted `Resources, Land, and Exit Terms` to H2;
7. moved `Practice Comes Before Property / If You Can’t Move / What to Do This Month` out of the Sénégal branch;
8. moved the Bruderhof/transmission reflection after the one-month action steps so it is the article's true ending;
9. promoted Appendix to H1 with H2 subsections.

Owner-supplied Instagram links were not altered.

## Article native-object fidelity

Baseline and r05 each contain 26 inventoried native/source objects.

Ordered `(object type, exact source SHA-256)` sequences are identical between Joel's owner raw baseline and r05. The final organization pass therefore changes prose/heading topology without mutating or reordering the inventoried native-object sequence.

This proves source-level object identity/order only, not destination reconstruction.

## r05 research companion

Ghost-card SHA-256:

`d90b7904ad1c4460b7ad426ab116f71db3b83d5b3c97f5e9fc9537ce692bf6d2`

Markdown companion SHA-256:

`9edaf117487cf5ae00364ef3cd4b9666839db10f231ff9cd5fc0d85184456760`

The r04 report had three competing organizational spines:

- why the desired intersection disappears;
- what earlier books changed;
- twelve design conclusions.

r05 keeps one reader path:

1. target;
2. method;
3. selective living-case sweep;
4. Zapatistas as closest integrated example;
5. why the full combination is hard;
6. recurring systems failure;
7. evidence-supported conclusions vs Joel's chosen design commitments;
8. design implications grouped by dependency;
9. staged formation toward a money-free community;
10. model risks;
11. unknowns;
12. conclusion;
13. source map.

Shared inner purpose now has one explanatory home. Couple dynamics have one explanatory home. Federation's meaning function is not reintroduced every time federation appears. Money-free economics and practice-before-property are one formation sequence. The final literal duplicate from that consolidation was removed in the second cold audit.

## Mermaid control maps

Article architecture:

`recovered/BUILDING-HEALING-COMMUNITY-R05-ARCHITECTURE.md`

Report architecture:

`recovered/COMMUNITY-RESEARCH-REPORT-R05-ARCHITECTURE.md`

The maps are visual indexes over this r05 candidate, not authority over Joel's supplied source or future owner corrections.

## Report/Ghost QA

- 13 top-level H2 branches;
- desktop and mobile TOCs resolve to the same 13 targets;
- six report tables;
- first table column is ~216.3 px desktop and 210 px mobile across all six tables;
- no duplicate IDs;
- no external script or stylesheet dependencies;
- headless Chromium `set_content` QA: zero page errors and zero console errors.

This does not prove a real Ghost-host destination result.

## r05 Substack clipboard helper

Helper SHA-256:

`690a3aeacd8c7bc0826b6fc1dbdf068d8603695f28498c607b8bd74152a70856`

The helper is rebuilt from the exact r05 archival/editor article.

Transfer treatment:

- one rich-HTML payload; no standalone native uploaded-video object exists;
- two Substack video-post digest embeds become their canonical post URLs in place;
- non-video digest, YouTube, images, Share, and Subscribe remain rich HTML on their established paths;
- the two Instagram items remain Joel's ordinary links;
- editor root excluded;
- only transferable native-object locks are removed.

Headless Chromium primary ClipboardItem path and forced silent `execCommand('copy')` fallback both passed. Real Opera → Substack destination reconstruction remains unverified.

## Durable files in this r05 checkpoint

Exact large HTML artifacts are stored losslessly as bzip2-compressed base64 so GitHub's text-contents connector does not have to reserialize or truncate fragile raw editor markup:

- `recovered/BUILDING-HEALING-COMMUNITY-R05-ARTICLE.bz2.base64`
  - reconstruct: `base64 -d ... | bzip2 -dc > BUILDING-HEALING-COMMUNITY-R05-ARTICLE.html`
  - reconstructed SHA-256: `ccdbca020251e9fab8d60c5ce343d8e42347581e9f13a63e568a0154eb6098bc`
- `recovered/COMMUNITY-RESEARCH-REPORT-R05-GHOST.bz2.base64`
  - reconstruct: `base64 -d ... | bzip2 -dc > COMMUNITY-RESEARCH-REPORT-R05-GHOST.html`
  - reconstructed SHA-256: `d90b7904ad1c4460b7ad426ab116f71db3b83d5b3c97f5e9fc9537ce692bf6d2`
- `recovered/BUILDING-HEALING-COMMUNITY-R05-ARCHITECTURE.md`
- `recovered/COMMUNITY-RESEARCH-REPORT-R05-ARCHITECTURE.md`
- `recovered/COMMUNITY-R05-ORGANIZATION-CHANGELOG.md`
- `recovered/COMMUNITY-R05-QA.md`

The exact Substack helper remains in the delivered local artifact family and can be added with the same compressed representation if another worker needs repository-only reconstruction. The article/report content and topology themselves are durable here.

The existing technical `docs/PUBLIC-RESEARCH-REPORT.md` is deliberately not overwritten in this checkpoint; it remains the evidence-transparency layer. r05 is the reader-facing companion/research narrative.

## Exact next action

Joel reviews r05 article/report organization. If accepted:

1. record r05 owner acceptance;
2. run only requested/surgical prose corrections;
3. perform a real Opera → Substack destination test before claiming helper success;
4. test the Ghost card in the actual Ghost HTML-card destination before claiming hosted success;
5. begin detector/humanization work only if explicitly requested, using the r05 architecture maps as a blocking topology check.
