# Community Development Lessons — Creative Tail Batch 45

Updated: 2026-08-15  
Status: append-only practical supplement; no originality claim

---

# Main lesson — Treat linked households as joint placement objects in federated matching

**Status:** PRACTICAL / KNOWN + C013 EXTENSION

Matching-with-couples theory shows that once pairs/households have joint preferences over pairs of placements, stable matching can fail to exist. A federation therefore should not treat couples, coparents, households or linked-care dyads as independent applicants and try to repair the assignment afterward.

---

## B45-L01 — Represent linked placement constraints explicitly

Possible acceptable configurations:
- same community;
- specified nearby-community pair;
- both accepted or neither;
- temporary split for a bounded period;
- no split acceptable.

## B45-L02 — Distinguish hard constraints from preferences

Do not infer from rankings alone.

Examples:
- `must live together` — potentially hard;
- `prefer same work area` — soft;
- `coparents need communities within 20 km` — potentially hard;
- `temporary separation acceptable for 4 weeks` — bounded soft constraint.

## B45-L03 — Do not promise a stable clearing outcome always exists

With couples/households, a stable matching may not exist.

If the federation coordinates matches, state whether the output is:
- stable when found;
- best feasible / minimum-conflict;
- advisory recommendations only.

Preserve opt-out and local admission authority.

## B45-L04 — Keep bounded placement slack where feasible

Small capacity flexibility can sometimes make an otherwise infeasible linked matching feasible.

Possible communal slack:
- flexible guest/trial room;
- federation transition housing;
- temporary satellite housing;
- one delayed-finalization opening;
- acceptable paired nearby-community placement.

Do not overfill beyond safety/housing limits merely to satisfy the algorithm.

## B45-L05 — Thin applicant/opening markets reduce the value of complex clearing

Linked constraints consume feasible combinations quickly.

Do not delay applicants for a theoretical centralized matching round if the federation is too thin for the benefit to exceed vacancy/waiting costs.

## B45-L06 — Household placement interacts with C009 cohort composition

A household changes several variables together:
- housing;
- children/care;
- work skills;
- age structure;
- relationship topology;
- future care/birth needs.

During founding/expansion, evaluate the household as part of the candidate set rather than merely individual scores.

## B45-L07 — Disclose hard linked constraints before final clearing

Privacy-relevant relationship detail can remain private, but placement constraints that can invalidate the match need to be known before commitments are proposed.

## B45-L08 — When exact stability fails, show the blocking configurations

Instead of returning a black-box failure, report:
- which household/community combinations conflict;
- which capacity constraint causes the conflict;
- what small change would make the assignment feasible.

This enables human negotiation.

## B45-L09 — Nearby split placements create governance interface questions

If members of one household reside in different communities, clarify:
- childcare/care obligations;
- transport;
- labor expectations;
- benefits;
- membership/voting;
- privacy/records;
- conflict jurisdiction.

A matching solution can otherwise create a later governance dispute.

## B45-L10 — Evaluate household outcomes after placement

Track:
- retention;
- household stability;
- satisfaction;
- childcare burden;
- transfer/exit;
- effects on receiving community.

Placement completion is not itself success.

---

## Consolidation note

Append-only because `agent/final-research-synthesis` contains the active Escuelita-expanded research state. Consolidate only after resolving the current branch head.
