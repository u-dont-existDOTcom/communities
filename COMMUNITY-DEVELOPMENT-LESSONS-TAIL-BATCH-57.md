# Community Development Lessons — Creative Tail Batch 57

Updated: 2026-08-15  
Status: append-only foundational privacy/research supplement; no originality claim

---

# Main lesson — In very small communes, expressive survey responses should be treated as identifiable

**Status:** FOUNDATIONAL RESEARCH-CONTROL / KNOWN

Removing names does not create anonymity in a small connected community. Other members may identify a respondent from handwriting, phrasing, grammar, characteristic stories, voice, timing, role details, household facts, or combinations of seemingly harmless context.

Research ethics calls one version of this **deductive disclosure / internal confidentiality**. Stylometry makes the `way of speaking/writing` concern technically explicit: nominally anonymous text can sometimes be attributed to its author from style.

Therefore sensitive small-commune research should assume local re-identification is possible unless the data architecture prevents local actors from ever seeing person-level expressive responses.

---

## B57-L01 — Stop promising anonymity by default

Use precise terms such as:
- confidential;
- independently custodied;
- non-custodial (C024);
- aggregate-only;
- locally unlinkable by design, only when technically justified.

If complete anonymity cannot reasonably be guaranteed, say so in consent materials.

## B57-L02 — Treat expressive channels as identifiers

Potential identifying signals include:
- handwriting;
- free-text prose;
- characteristic wording/spelling;
- voice/audio;
- unique stories;
- rare events;
- exact chronology;
- demographic combinations;
- timestamp/device/account metadata.

## B57-L03 — Prefer fixed-choice formats for routine sensitive measurement

Where the research question allows, use:
- categorical choices;
- bounded scales;
- standardized vignettes;
- indirect/randomized response methods;
- secure aggregation/non-custodial federation pooling.

This reduces stylistic fingerprinting compared with free-text responses.

## B57-L04 — Avoid handwriting in sensitive routine surveys

If paper is needed for accessibility:
- use fixed-choice marks rather than written narrative;
- physically mix forms;
- transfer completed forms directly to independent custody;
- prevent local leaders from inspecting them.

## B57-L05 — Open text needs a separate confidentiality regime

When narrative detail is necessary:
- collect through independent researchers;
- keep raw text/audio inaccessible to local community leadership;
- treat raw narrative as identifiable confidential microdata;
- publish coded/synthesized layers where possible;
- obtain separate consent for verbatim quotation.

## B57-L06 — Presume verbatim quotes are locally attributable

In a small commune, insiders may recognize:
- phrase choice;
- specific events;
- personal philosophy;
- role-specific knowledge.

Prefer semantic summary/pooling for sensitive material unless the participant knowingly accepts attribution risk.

## B57-L07 — Paraphrasing reduces but does not eliminate re-identification

A rewritten quote can still reveal a unique event or relationship.

Review transformed text against insider knowledge and C023 cumulative disclosure history.

## B57-L08 — Separate participation privacy from answer privacy

Even perfectly protected answers can be compromised if people know who participated.

Possible controls:
- universal/private access windows;
- off-site/mobile completion;
- no local attendance list for sensitive modules;
- independent participant contact;
- batch transmission that obscures exact timing.

## B57-L09 — Suppress exact completion metadata

Exact timestamps can reveal who responded if other members saw someone using the device/room at that time.

Do not expose such metadata to local analysts when unnecessary.

## B57-L10 — Avoid unnecessary demographic cross-tabs

A combination such as `parent + treasurer + age band` can uniquely identify someone in a tiny group.

Collect only demographics needed for the research and publish at broader pooled scopes.

## B57-L11 — C024 is strongest for closed-ended sensitive data

Non-custodial secure aggregation can protect fixed-choice inputs from local/central plaintext custody.

It cannot make expressive narrative anonymous if someone later sees the text and recognizes the writer.

## B57-L12 — Some qualitative research should promise confidentiality, not fake anonymity

For questions requiring narrative context, the right design may be:
- explicit confidentiality limits;
- independent custody;
- restricted raw-data access;
- strong publication redaction/synthesis;
- informed consent about residual identification risk.

## B57-L13 — Use independent coding layers

External researchers can transform sensitive narratives into:
- standardized categories;
- themes;
- incident descriptors;
- aggregate counts.

Local/federation users can receive the coded layer without the raw expressive text when adequate.

## B57-L14 — Do not promise anonymity because an LLM paraphrased the text

Automated authorship obfuscation is imperfect, and unique semantic details can still identify respondents. Rewriting can also distort meaning.

## B57-L15 — Measure respondent belief about stylometric/contextual identifiability

Add diagnostics such as:
- `Could another member recognize your phrasing/story?`
- `Could someone infer you from the event described?`
- `Did anyone see when/how you completed this?`
- `Do you believe local leadership can see raw responses?`

## B57-L16 — Let local re-identification risk determine response format

For very small N / high sensitivity:
- no local open-text publication;
- closed-ended secure aggregation;
- qualitative material only under independent confidentiality;
- federation-pooled outputs.

For larger/lower-risk settings, open text may be possible after explicit deductive-disclosure review.

---

# Revised communal research privacy stack

1. **Participation privacy** — can locals tell who participated?
2. **Input confidentiality** — who can inspect raw answers? (C024)
3. **Response-fingerprint privacy** — can the answer itself reveal the author? (Batch 57)
4. **Output/composition privacy** — can released aggregates reconstruct the answer? (C023)

A survey can solve any three and still fail on the fourth.

---

## Consolidation note

Append-only because `agent/final-research-synthesis` contains the active Escuelita-expanded research state. Consolidate only after resolving the latest branch head.
