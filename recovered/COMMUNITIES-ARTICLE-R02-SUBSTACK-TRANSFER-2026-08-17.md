# Building Healing Community — accepted r02 Substack transfer

Date: 2026-08-17
Status: owner accepted r02 by replying `good give me the clipboard helper`; helper built, destination paste not yet tested.

## Accepted archival/editor source

- Revision: `r02`
- SHA-256: `207f9e1d1ff5473e6684c0916f3c1d4557d98307b3bec417f99087d281998da8`
- Provenance: r02 candidate produced from the exact uploaded raw Substack editor HTML after Joel's six r01 comments were reconciled.
- Native-object source check before acceptance: 26 objects; ordered type/hash sequence unchanged from r01.

## Clipboard helper

- Helper file: `community-research-repair-r02-clipboard-helper.html`
- Helper SHA-256: `a96da9420af92071b877f4de2704f966396a33fb6381ad964da435f1b5af9de9`
- Transfer payload SHA-256: `66e5cd6b7938a65487369673adc15b5b3e51b96a219a2e87ac8cee7e8b2cd26a`
- One visible control: `Copy Article`
- Wrapper: `<div dir="auto" class="body markup">…</div>`
- Raw ProseMirror/editor root excluded.
- `ClipboardItem` / `navigator.clipboard.write()` is invoked directly from the click handler with no pre-clipboard asynchronous work.
- Silent off-screen `contenteditable` + `document.execCommand("copy")` fallback retained.

## Video distinction

This r02 source contains two literal `<video>` elements, but both are inside Substack **video-post digest embeds**, not standalone native uploaded-video objects.

Per Joel's current transfer rule, those two video-post embeds do **not** split the helper. They are replaced in the transfer payload by their canonical URLs at the same source positions:

- `https://ibogaqueen.substack.com/p/wheres-utopia-click-read-more-my`
- `https://ibogaqueen.substack.com/p/professor-baby-sheep-taught-me-inner`

After those conversions, no `<video>` element remains in the payload. Therefore there is no manual native-video reinsertion step for this article.

The third, non-video digest-post embed remains rich HTML.

## Other transfer objects

- Images/captions: rich HTML, editor locks removed in transfer payload only.
- Non-video digest preview: rich HTML.
- YouTube: rich HTML.
- Share + Subscribe: rich HTML with `%%share_url%%` / `%%checkout_url%%` preserved.
- Instagram: exact rich HTML retained, but destination reconstruction remains unverified.
- Paywall: none detected.
- Substack comment card: none detected.

## Static regression result

PASS:

- exactly one Copy Article control;
- exactly one payload template;
- exact `div[dir=auto].body.markup` wrapper;
- editor root absent;
- no remaining `<video>`;
- both video-post canonical URLs present once in source position;
- one non-video digest retained;
- two YouTube embeds retained;
- one Instagram embed retained;
- Share and Subscribe placeholders retained;
- direct ClipboardItem path present;
- silent fallback present;
- native editor locks removed from transferable object start tags.

## Validation boundary

This proves the helper was built from the accepted r02 and passes static transfer-conversion regression. It does **not** prove Opera → Substack reconstruction. Paste into a disposable Substack draft and verify images, the non-video digest preview, the two URL-reconstructed video posts, YouTube, Share, Subscribe, Instagram, captions, links, and source order independently.
