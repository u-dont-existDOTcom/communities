# Community Development Lessons — Creative Tail Batch 58

Updated: 2026-08-15  
Status: append-only foundational privacy/research supplement; no originality claim

---

# Main lesson — Survey privacy starts before submission

**Status:** FOUNDATIONAL RESEARCH-CONTROL / KNOWN

In communal housing, a response can be exposed before any secure storage or anonymity system matters: someone can walk in, look over a shoulder, see a paper form left on a table, use the shared device afterward, or infer answers from what remains on screen.

Therefore the research privacy model needs a separate **collection-scene privacy** layer.

---

## B58-L01 — Audit the physical/digital completion scene

Check:
- room privacy;
- shared devices;
- foot traffic;
- unattended paper/screens;
- browser history/cache/autofill;
- screen visibility/reflections;
- printed/scanned copies;
- paper disposal;
- exact completion timing.

## B58-L02 — Do not require sensitive surveys in common spaces

Provide a genuinely private completion option rather than dining halls, common offices, group meetings, or supervised sessions.

## B58-L03 — Support safe pause-and-resume

Digital sensitive modules should, where practical:
- blank/hide answers when paused;
- require re-entry/reauthentication to resume;
- avoid leaving an answer summary visible;
- minimize plaintext drafts on shared devices.

## B58-L04 — Seal paper responses immediately

If paper is necessary:
- prefer fixed-choice marks over handwriting;
- use opaque envelopes;
- never leave completed forms unattended;
- avoid local-leader inspection;
- transfer sealed batches to independent custody;
- destroy working copies securely when policy allows.

## B58-L05 — Treat shared devices as a separate threat model

Protect against:
- browser back/history;
- autofill;
- local storage/cache;
- downloads;
- screenshots;
- recent-items lists;
- saved credentials.

## B58-L06 — Make a quick glance reveal as little as possible

Avoid large persistent highlighted answers or summary screens on sensitive modules. Consider privacy filters on shared devices where useful, while preserving accessibility.

## B58-L07 — Protect participation timing

If everyone knows who disappeared to complete the `confidential survey`, participation privacy has already weakened.

Use broad windows, remote/off-site options, and no local attendance list for sensitive modules.

## B58-L08 — Do not create local sensitive artifacts unnecessarily

Avoid asking members to store raw sensitive notes in:
- community notebooks;
- shared drives;
- local email accounts;
- printed forms that remain on site.

Route data directly into independent/non-custodial systems where feasible.

## B58-L09 — Ask whether collection privacy was actually achieved

Possible post-module diagnostics:
- `Were you alone while answering?`
- `Could anyone see your screen/paper?`
- `Were you interrupted?`
- `Did you leave the response unattended?`
- `Did anyone ask what you answered?`

Use this to qualify evidence quality, not blame respondents.

## B58-L10 — Allow recovery after observed exposure

If someone believes their response was seen, provide a route to flag/replace/invalidate the submission where technically possible, with clear version handling.

## B58-L11 — Make privacy-enhanced participation normal

Do not create a special `secret room` that itself signals dissatisfaction. Privacy should be routine and available to everyone.

## B58-L12 — One privacy incident can alter later reporting

A visible breach can reduce future candor across the entire community.

Track privacy incidents and changes in respondent trust/reporting mode.

## B58-L13 — Collection-scene privacy and response-fingerprint privacy are independent

A respondent can be alone during completion but later identified from prose/handwriting (Batch 57). A fixed-choice response can be non-identifying in itself yet exposed by shoulder-surfing during completion.

Both must pass.

## B58-L14 — Private space cannot be assumed in communal housing

Ask whether members actually have access to a private place/device for sensitive participation. Co-residential life can make this the binding privacy constraint.

---

# Revised research privacy stack

1. **Participation privacy** — can locals tell who participated?
2. **Collection-scene privacy** — can someone observe the response while being created or left unattended?
3. **Input confidentiality** — who can inspect submitted raw answers? (C024)
4. **Response-fingerprint privacy** — can style/context identify the author? (Batch 57)
5. **Output/composition privacy** — can aggregate releases reconstruct the answer? (C023)

A system can solve four and still fail through the fifth.

---

## Consolidation note

Append-only because `agent/final-research-synthesis` contains the active Escuelita-expanded research state. Consolidate only after resolving the current branch head.
