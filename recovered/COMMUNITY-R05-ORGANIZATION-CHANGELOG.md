# r05 organization and deduplication change log

## Baselines

- Owner-supplied Substack editor HTML: `d4e46ce84636ab038b1e3b80f1a6f6246242b8e482d43ed648b51595d441eab5`
- Research report r04 Ghost: `db6ad5777595124a2cbdded2a467c6c43b403019a70ec752c7006fdede647ee1`

## r05 outputs

- Article: `ccdbca020251e9fab8d60c5ce343d8e42347581e9f13a63e568a0154eb6098bc`
- Report Ghost card: `d90b7904ad1c4460b7ad426ab116f71db3b83d5b3c97f5e9fc9537ce692bf6d2`
- Article architecture map: `1e618140f18c8e4b9a719a0bd14742543265e35dab143993d53073d1eb869bb0`
- Report architecture map: `5f7fe92ffb28f30bb92dd0071d7b9afa1c3aba0866131ac611730931e43eb654`

## Article consolidations

1. `How Much Attention Do You Actually Have for Other People?` → consolidated into `The Math of Absorption, and Who This Isn’t For`; its first four setup paragraphs were moved intact, while the obsolete “later I’ll give the arithmetic” promise was removed.
2. `Please Choose the Values Before Falling in Love With the View` → moved from the children branch to the forming-group branch before resources/land.
3. `Experiment Before You Divorce` + `Federation Without Building Another State` → grouped under new H1 `From One Community to a Movement`.
4. `Practice Comes Before Property`, `If You Can’t Move`, and `What to Do This Month` → moved out of the Sénégal branch and reordered as the final practical sequence.
5. Appendix heading levels repaired.
6. Two repeated escuelita explanations removed because the opening already defines the mission and the Zapatista section later supplies the evidence.
7. Federation's repeated “purpose gives meaning” paragraph compressed to the concrete movement-level function.
8. The sexuality/gender compatibility paragraph moved into the values section, restoring the antecedent of “that list.”
9. The Bruderhof/transmission reflection moved after `What to Do This Month`, so the article now has one true ending.

No owner-supplied Instagram links were altered.

## Report consolidations

1. Removed `What the earlier books changed` as a competing organizing spine. Its unique mechanisms were moved to the dependency they explain.
2. Replaced the flat `Twelve design conclusions` spine with four dependency groups: power/truth/correction; care/children/intimate life; resources/exit/capacity; success/continuity/federation.
3. Shared inner purpose now has one explanatory home. The later formation section no longer redefines it.
4. The couple problem has one explanatory home; second-generation evidence moved to continuity.
5. Federation's meaning function is stated once; later federation material is operational.
6. The money-free model and practice-before-property sequence are merged into one formation path.
7. The child-safety unresolved case is placed with child/care design rather than as an isolated top-level detour.
8. The local/federated/professional/direct-right table is kept as a synthesis after the grouped design implications.
9. A second cold audit removed the last literal duplicate “beautiful land…” paragraph left after the formation-path consolidation.

## Derivatives and validation

- Reader-facing report Markdown: `9edaf117487cf5ae00364ef3cd4b9666839db10f231ff9cd5fc0d85184456760`
- Substack clipboard helper: `690a3aeacd8c7bc0826b6fc1dbdf068d8603695f28498c607b8bd74152a70856`
- Current owner raw Substack baseline: `d4e46ce84636ab038b1e3b80f1a6f6246242b8e482d43ed648b51595d441eab5`
- Owner-fixed Instagram URLs are plain links in both baseline and r05 article; no `node-instagram` native object is reintroduced.
- Native-object inventory: 26 source objects; ordered `(type, exact source hash)` sequence is unchanged between owner baseline and r05 article.
- Ghost static/browser QA: 13 H2 TOC targets, six tables, all anchors resolve; first-column widths ~216.3 px desktop and 210 px mobile; zero page/console errors in headless Chromium `set_content` QA.
- Clipboard-helper primary `ClipboardItem` path and forced silent `execCommand` fallback both passed headless Chromium tests. This does not prove Opera→Substack destination reconstruction.

## GitHub storage representation

The exact r05 article and Ghost report are committed on the article-repair branch as lossless bzip2-compressed base64 text artifacts because the connected GitHub text-contents path is not a safe place to stream/re-serialize the 199 KB raw Substack editor HTML. Reconstruction is deterministic and must reproduce the source hashes above before use. The Mermaid maps, QA, change log, and state remain ordinary readable Markdown.
