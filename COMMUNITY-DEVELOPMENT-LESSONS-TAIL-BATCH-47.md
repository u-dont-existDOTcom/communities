# Community Development Lessons — Creative Tail Batch 47

Updated: 2026-08-15  
Status: append-only practical supplement; C023 provisional cross-domain transfer

---

# Main lesson — Small-community anonymity must be protected across the whole history of releases

**Status:** TAIL-PROVISIONAL + PRIVACY/RESEARCH CONTROL  
**Creative Tail:** C023 — Cumulative disclosure-budget / differencing guard

A commune-level result can contain no names and still expose a member once it is combined with earlier/later tables or facts everyone in the community already knows.

Example:
- publish the average for eight members;
- one person leaves;
- publish the new average for seven;
- subtraction can reveal the leaver's response.

Therefore privacy review must evaluate **all overlapping releases jointly**, not certify each table independently.

---

## B47-L01 — Maintain a cumulative release ledger

For every public/member-visible release log:
- variables;
- community/subgroup;
- time window;
- denominator;
- suppression/noise/transformation;
- prior overlapping releases;
- obvious differencing/reconstruction routes.

## B47-L02 — Run differencing attacks before publication

Test at least:
- before/after one entrant/leaver;
- total versus subgroup complement;
- overlapping role/age/parent groups;
- community versus federation totals;
- monthly versus quarterly values;
- combinations with known visible life events.

## B47-L03 — Minimum cell size is necessary but not sufficient

`N >= 5` or `N >= 8` does not protect privacy if several safe-looking cells intersect to isolate one person.

There is no universal safe N.

## B47-L04 — Assume local auxiliary knowledge

Community members already know:
- who left;
- who has children;
- who held a role;
- who had a visible conflict;
- who experienced an event.

Privacy review should model a knowledgeable insider, not an ignorant outsider.

## B47-L05 — Publish sensitive tiny-N outcomes at broader levels

Where necessary use:
- federation pooled results;
- measurement-compatible clusters;
- wider time windows;
- ranges/qualitative thresholds.

Keep detailed community-level results under controlled access when useful for local improvement/research.

## B47-L06 — Separate access tiers

Possible layers:
- individual private report;
- safe community-internal aggregate;
- federation research access;
- public output.

Useful data do not all need to be public.

## B47-L07 — Delay updates after single-person membership changes when needed

Do not publish a fresh aggregate if it effectively reveals the entrant/leaver's contribution.

Pool, delay, widen the window, suppress, or use a formal privacy mechanism.

## B47-L08 — Qualitative details consume privacy too

A quote or narrative can identify the only person in a subgroup and turn a previously safe table into a disclosure.

Review qualitative and quantitative releases together.

## B47-L09 — Protect longitudinal linkage

Panel research may require persistent pseudonymous IDs, but local leadership/public outputs should not receive linkage keys.

Avoid trajectory combinations that trivially identify participants.

## B47-L10 — Differential privacy is optional; composition awareness is not

Formal DP can protect repeated statistical releases, but tiny-N noise can destroy usefulness and implementation is complex.

Use simpler pooling/suppression/access controls when adequate.

If DP is used, define:
- privacy unit;
- neighboring-data model;
- total privacy budget;
- composition over repeated releases;
- entrant/leaver handling;
- refresh policy.

## B47-L11 — Preserve severe-event evidence privately even when public detail is unsafe

Privacy must not erase rare severe events from the research/safeguarding record.

Keep exact confidential data where legitimately needed while publishing only privacy-safe pooled information.

## B47-L12 — Transparency can focus on method/process

A small community can publish:
- instrument;
- participation rate;
- method;
- privacy rules;
- independent-review status;
- whether thresholds were met;

without publishing every sensitive result.

## B47-L13 — Privacy failure creates later reporting bias

Connect to Batches 43–44.

If members see someone reidentified from supposedly anonymous aggregates, future participants will rationally trust confidentiality less and may face-save more.

Privacy protection therefore affects both ethics **and** measurement validity.

---

## Target-domain note

Cloughjordan Ecovillage's research guidance already warns that details in a small community can easily identify members, and EVIST excludes very small ecovillages from its survey. C023 extends this to **composition across repeated releases**, which one-release anonymity rules do not solve.

---

## Consolidation note

Append-only because `agent/final-research-synthesis` contains the active Escuelita-expanded research state. Consolidate only after resolving the current branch head.
