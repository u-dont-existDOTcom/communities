# Community Development Lessons — Creative Tail Batch 31

Updated: 2026-08-15  
Status: append-only practical supplement; C020 provisional cross-domain survivor

## Main lesson — Make the political effect of community fission/merger explicit
**Status:** TAIL-PROVISIONAL + PRACTICAL  
**Creative Tail:** C020

A federation that wants communities to reproduce can accidentally reward or punish reproduction through its representation rule.

The important distinction is:

- **community reproduction/fission is legitimate institutional development**;
- weighted-voting theory nevertheless shows that changing one voter/player into two, or merging two into one, can change coalition power even when total population/nominal weight is preserved.

Do not treat daughters as fake identities or Sybil attacks. Use split/merge voting theory only to expose the representation consequence.

---

## B31-L01 — Audit federation power before and after a planned fission
**Status:** TAIL-PROVISIONAL + PRACTICAL

Before a parent community divides into daughters that will become federation members, calculate both the old and proposed voting games.

Record:

- nominal weights/seats;
- quota(s);
- Penrose-Banzhaf or another appropriate pivotal-power index;
- veto/dummy status;
- minimum winning coalitions;
- aggregate power of the daughter lineage if daughters vote identically;
- possible power when daughters vote independently;
- power changes imposed on third-party communities.

A population-preserving split can change actual power even under population-linear weights.

---

## B31-L02 — Run an aligned-preference split/merge counterfactual
**Status:** TAIL-PROVISIONAL + PRACTICAL

Use this diagnostic question:

> If the same people were divided into two organizational members but the daughters voted identically to the old parent, how much would aggregate federation influence change solely because the organizational boundary changed?

Call the answer the **split/merge representation effect**.

It is not automatically a flaw. It isolates what the institutional boundary itself contributes.

---

## B31-L03 — Decide whether autonomous-community voice deserves a premium independent of population
**Status:** PRACTICAL / CONSTITUTIONAL CHOICE

A federation may reasonably believe that two genuinely autonomous communities deserve more collective political voice than one community containing the same number of people because they have:

- different land/sites;
- separate budgets and risk;
- independent memberships;
- distinct governance;
- potentially divergent local interests.

If so, say so explicitly and quantify the effect.

Do not describe the result as individual population equality if the rule intentionally adds an autonomy/community-unit premium.

---

## B31-L04 — Distinguish genuine fission from administrative fragmentation
**Status:** PRACTICAL / KNOWN

Separate representation should not follow automatically from creating another legal shell, project name, residential cluster, or accounting entity.

Before granting a new federation voice, define what constitutes an autonomous member community:

- independent membership authority;
- independent operating budget/assets;
- real local decision authority;
- separate obligations/liabilities;
- durable site/community identity;
- ability to disagree with the parent;
- other federation-specific criteria.

The criteria should make it possible to reproduce legitimately without creating an easy vote-multiplication loophole.

---

## B31-L05 — Analyze representation effects on everyone, not only the splitting community
**Status:** PRACTICAL / KNOWN

Fission changes the coalition game for every member.

A parent can lose aggregate power while another community becomes much more pivotal; a previously weak community can become a necessary partner; a veto can appear or disappear.

Therefore planned fission review should publish the power change for all communities.

---

## B31-L06 — Do not assume one-community/one-vote is politically neutral toward reproduction
**Status:** PRACTICAL / KNOWN

If every independent community receives one vote, a successful split can increase the lineage's combined organizational vote count.

Illustration: three equal organizational voters each have one-third of the Banzhaf power under simple majority. If one becomes two independent daughters and all four organizations receive equal votes, each has one-quarter; the two daughters together have one-half if aligned.

This may be exactly the autonomy premium the federation wants. It is not neutral.

---

## B31-L07 — Do not assume population-linear weights are fission-neutral in actual power
**Status:** TAIL-PROVISIONAL + PRACTICAL

Population-linear weights preserve **total nominal weight** when a parent population is divided among daughters.

They do **not** preserve pivotal power because the set of players and winning coalitions changes.

Conditional Batch 31 toy example:

- before: weights `[100,64,9]`, 60% quota → Banzhaf `[0.60,0.20,0.20]`;
- after splitting 100 into 50+50: `[50,50,64,9]`, same 60%-of-population quota → Banzhaf `[0.25,0.25,0.4167,0.0833]`.

The daughters' aligned aggregate power is `0.50`, below the unsplit parent's `0.60`, even though total population weight is unchanged.

The numbers are illustrative, not a recommendation for any particular federation.

---

## B31-L08 — Square-root representation needs the same fission audit
**Status:** PRACTICAL / KNOWN

Because square root is concave:

`sqrt(n1) + sqrt(n2) > sqrt(n1+n2)`

for positive daughter sizes, so splitting mechanically increases the **sum of nominal square-root weights**.

But actual voting power can still fall or behave non-monotonically after the quota and coalition structure are recomputed.

Therefore do not infer the political fission incentive from the weight formula alone.

---

## B31-L09 — Put representation effects into the planned-fission protocol
**Status:** TAIL-PROVISIONAL + PRACTICAL

The communities research already treats planned fission as more than asset division. Add federation representation to the checklist:

1. people/household choice;
2. asset/debt division;
3. viable sites and runway;
4. records and family contact;
5. successor governance;
6. federation membership transition;
7. **before/after voting-power audit**;
8. explicit decision on any autonomy premium or fission penalty/subsidy;
9. later review after daughters become behaviorally independent.

This keeps political representation from becoming an invisible side payment attached to reproduction.

---

## B31-L10 — Audit merger effects too
**Status:** PRACTICAL / KNOWN

The same logic runs in reverse when communities merge.

Before a merger, calculate whether two members becoming one will:

- lower aggregate voice;
- increase aggregate pivotal power;
- change other communities' veto/pivotal positions;
- unintentionally encourage fragmentation to preserve representation.

Do not make two communities remain organizationally separate solely because the federation's voting rule imposes a political merger tax unless that tradeoff is explicit and accepted.

---

# Batch 31 disposition

C020 survives provisionally only as the target-domain operational connection:

> **A movement that treats daughter-community formation as success should measure whether its federation constitution politically subsidizes or penalizes that success.**

Weighted-voting split/merge effects themselves are old. Dynamic child-community representation is also already a formal research topic. The proposed status-quo improvement is to make the reproduction–representation interaction an explicit part of intentional-community federation and planned-fission design.
