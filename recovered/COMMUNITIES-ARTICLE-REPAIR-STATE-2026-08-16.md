# Communities article repair state — 2026-08-16

Mode: article harmonization authorized; humanization not started.

## Completed

- Created dedicated branch `agent/article-repair-20260816` from research head `f344d979f7b8f1c2991408b969240d3ed482d4a3`.
- Reconciled canonical G-001–G-028 article-gap manifest.
- Selected 20 exact repair operations covering all 28 gaps plus directly relevant C001/C003/C025/C026 integrations.
- Preserved the owner's selective-membership/ejection argument and autonomous-governance correction rather than silently replacing them with universal inclusion or state-monopoly language.
- Source-hardened current FEC publication claims against the new official FEC site and current initiative/community/status pages.
- Source-hardened the March 2026 Senegal Article 319 change against Senegal Ministry of Justice material and the enacted Law No. 2026-08 status/text page.
- Added a fail-closed raw-HTML patcher and tests. The patcher requires every anchor exactly once and refuses output if the ordered Substack native-object marker inventory changes.
- Local TDD verification after implementation: 7 tests passed.

## Durable artifacts

- `recovered/COMMUNITIES-ARTICLE-REPAIR-SPEC-2026-08-16.md`
- `recovered/COMMUNITIES-ARTICLE-REPAIR-OPS-2026-08-16.json`
- `scripts/apply_community_article_repair.py`
- `tests/test_apply_community_article_repair.py`

## Current application blocker

The authoritative raw editor source exists in the user's ChatGPT File Library as `Pasted text.txt` (2026-08-15T10:58:17Z), but File Library references are not mounted into the execution filesystem and the current connector set exposes no raw-byte download action for that File Library object. Google Drive search did not find a copy under that name.

Therefore the repaired HTML has **not** been generated yet. Do not reconstruct the full raw editor HTML from extracted prose or substitute the published page/PDF, because that would risk losing Substack-native embeds/objects.

## Exact next action

Obtain the authoritative `Pasted text.txt` bytes in the active conversation/runtime (simplest route: re-upload that raw file in the current conversation), then run:

```bash
python scripts/apply_community_article_repair.py \
  '/path/to/Pasted text.txt' \
  --ops recovered/COMMUNITIES-ARTICLE-REPAIR-OPS-2026-08-16.json \
  --check

python scripts/apply_community_article_repair.py \
  '/path/to/Pasted text.txt' \
  --ops recovered/COMMUNITIES-ARTICLE-REPAIR-OPS-2026-08-16.json \
  --output repaired/community-article-research-harmonized.html \
  --audit repaired/community-article-research-harmonized.audit.json
```

Then verify all 20 operations applied once, native markers are unchanged, read the repaired prose for semantic coherence, package the repaired HTML + audit as a ZIP for the user, and only afterward begin the detector/humanization phase.
