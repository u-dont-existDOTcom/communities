# r05 organization / publication QA — 2026-08-17

## Baselines

- Owner-supplied raw Substack editor HTML SHA-256: `d4e46ce84636ab038b1e3b80f1a6f6246242b8e482d43ed648b51595d441eab5`
- r05 article SHA-256: `ccdbca020251e9fab8d60c5ce343d8e42347581e9f13a63e568a0154eb6098bc`
- r05 Ghost report SHA-256: `d90b7904ad1c4460b7ad426ab116f71db3b83d5b3c97f5e9fc9537ce692bf6d2`
- r05 report Markdown SHA-256: `9edaf117487cf5ae00364ef3cd4b9666839db10f231ff9cd5fc0d85184456760`
- r05 clipboard helper SHA-256: `690a3aeacd8c7bc0826b6fc1dbdf068d8603695f28498c607b8bd74152a70856`

## Article architecture / fidelity

- Two cold architecture audits completed.
- `How Much Attention Do You Actually Have for Other People?` is consolidated into the later absorption-math section.
- Values/sexuality compatibility is now in one values branch.
- Zapatista evidence and Joel's experiment/federation proposal are separated by `From One Community to a Movement`.
- Closing action sequence is `Practice Comes Before Property` → `If You Can’t Move` → `What to Do This Month` → Bruderhof/transmission reflection.
- Appendix is a top-level branch with H2 subsections.
- The two owner-fixed Instagram posts remain plain canonical links exactly once each.
- No `node-instagram` object is present.
- `html_islands.py inventory` found 26 source/native objects in the owner baseline and 26 in r05.
- Ordered `(object type, exact source SHA-256)` sequences are identical between baseline and r05.
- No native object was reconstructed or reserialized to accomplish the prose moves.

## Research-report architecture

- 13 top-level H2 sections.
- Old competing public spines `What the earlier books changed` and `Twelve design conclusions from the historical corpus` are removed.
- Evidence is now grouped by dependency: power/truth/correction; care/children/intimate life; resources/exit/capacity; success/continuity/federation; institutional routing.
- Shared inner purpose has one explanatory home; later mentions are descriptive or concluding payoff.
- Couple-problem explanation has one home; second-generation evidence sits under continuity.
- Money-free economics and practice-before-property form one formation path.
- Last literal duplicate paragraph from the formation consolidation was removed.
- Static HTML: no duplicate IDs; all 13 TOC targets resolve; no external script or stylesheet dependency.

## Ghost browser QA

Headless Chromium via `set_content`:

- desktop: root visible; sidebar visible; mobile TOC hidden; 13 H2s; 6 tables; all tested TOC targets exist;
- mobile: root visible; sidebar hidden; mobile TOC visible; 13 H2s; 6 tables;
- first table-column widths: ~216.3 px for all six tables at desktop width, 210 px for all six at mobile width;
- page errors: 0;
- console errors: 0.

This proves local fragment behavior, not a real Ghost-host destination result.

## Substack helper QA

Transfer conversion:

- one visible `Copy Article` control;
- exact `div[dir=auto].body.markup` payload wrapper;
- editor root excluded;
- 20 image object locks removed;
- one non-video digest object remains rich HTML;
- two YouTube object locks removed;
- Share and Subscribe locks removed;
- two Substack video-post digest embeds are converted to canonical post URLs in place;
- no `<video>` markup remains in clipboard payload;
- owner-fixed Instagram links remain ordinary links;
- remaining `contenteditable=false` instances are nontransfer-lock source markup such as horizontal rules.

Headless Chromium:

- primary stubbed `ClipboardItem` / `navigator.clipboard.write` path: PASS;
- forced silent off-screen `execCommand('copy')` fallback: PASS;
- page errors: 0;
- console errors: 0.

This does **not** prove the real Opera → Substack destination reconstruction.
