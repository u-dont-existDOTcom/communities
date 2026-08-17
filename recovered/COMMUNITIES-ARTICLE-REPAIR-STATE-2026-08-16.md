# Communities article repair state — 2026-08-17

Mode: article harmonization authorized; **r02 owner-accepted**; Substack transfer helper built; humanization not started.

## Authority / accepted revision

Joel reviewed r01, supplied six substantive corrections, reviewed the r02 response, then replied `good give me the clipboard helper`. Treat that as owner acceptance of the r02 research-repair revision for the current article-transfer task.

Accepted r02 archival/editor source SHA-256:

`207f9e1d1ff5473e6684c0916f3c1d4557d98307b3bec417f99087d281998da8`

Original uploaded raw Substack editor baseline SHA-256:

`0062af91b00b637482217755276db3c2b7379f1fb52952e8a1bc39ed90062e86`

The accepted r02 preserves the raw Substack editor structure/native-object source order and incorporates the research repair through G-001–G-028 plus Joel's r01 corrections, including the money-free-society architecture and `https://commune-research.u-dont-exist.com/` links.

Durable r01→r02 owner-comment reconciliation:

`recovered/COMMUNITIES-ARTICLE-REPAIR-R02-COMMENT-RESPONSE-2026-08-17.md`

## Native-object source validation

`html_islands.py inventory` found 26 semantic/native objects in r01 and r02; ordered `(object type, exact source SHA-256)` sequence remained identical before owner acceptance.

This proves source-level identity/order, not destination reconstruction.

## Substack clipboard helper

Durable transfer record:

`recovered/COMMUNITIES-ARTICLE-R02-SUBSTACK-TRANSFER-2026-08-17.md`

Helper file delivered to Joel:

`community-research-repair-r02-clipboard-helper.html`

Helper SHA-256:

`a96da9420af92071b877f4de2704f966396a33fb6381ad964da435f1b5af9de9`

Transfer payload SHA-256:

`66e5cd6b7938a65487369673adc15b5b3e51b96a219a2e87ac8cee7e8b2cd26a`

### Current video rule applied

The accepted r02 contains no standalone native Substack-uploaded video object. Its two literal `<video>` elements are inside Substack **video-post digest embeds**. Per Joel's current correction, these do not split the helper; the transfer payload leaves each canonical post URL at its source position so Substack can reconstruct it. The non-video digest preview remains rich HTML.

After conversion there are no `<video>` elements in the payload, so no manual native-video reinsertion step is required for this article.

### Static helper regression

PASS:

- one visible `Copy Article` control;
- exact `<div dir="auto" class="body markup">` wrapper;
- raw editor root excluded;
- immediate `ClipboardItem` / `navigator.clipboard.write()` path;
- silent off-screen `contenteditable` + `execCommand("copy")` fallback;
- both video-post canonical URLs present once in position;
- non-video digest, YouTube, Instagram, images, Share and Subscribe retained on their assigned paths;
- native editor locks removed from transferable object start tags only;
- no paywall/comment-card marker detected.

Instagram and Subscribe remain destination-sensitive and must be checked in the actual Substack draft.

## Exact next action

Joel opens the downloaded helper directly in Opera, clicks `Copy Article`, pastes into a disposable/target Substack draft, and checks object types independently: images/captions, non-video digest preview, both reconstructed video-post URLs, YouTube, Share, Subscribe, Instagram, links, and source order.

Do not treat a successful clipboard operation alone as destination success.

After destination verification, preserve that result durably. Humanization/detector work, if requested, starts from this accepted r02 and must preserve the accepted research repair and native-object placement.
