# Community Development Lessons — Creative Tail Batch 30

Updated: 2026-08-15  
Status: append-only practical supplement; C019 provisional cross-domain survivor

## Main lesson — Design federation voting **power**, not merely voting weights
**Status:** TAIL-PROVISIONAL + PRACTICAL  
**Creative Tail:** C019

Weighted federation rules often specify numbers of votes, delegate counts, population weights, and supermajority thresholds. Those are inputs to the governance game; they are **not the resulting distribution of influence**.

A federation that cares about egalitarian representation should first decide what it wants to equalize, then compute what its actual rule produces.

Possible objectives are different:

- equal sovereignty of member communities;
- equal indirect influence of individual adult members;
- a hybrid giving small communities a floor while responding to population;
- preventing one very large community from dominating;
- protecting meaningful minority blocking power while retaining enough ability to act.

No formula is neutral until the objective is explicit.

---

## B30-L01 — Model both tiers of a federation
**Status:** TAIL-PROVISIONAL + PRACTICAL

For each community, record how its position is actually formed:

- consensus;
- member majority;
- delegate discretion;
- instructed delegate;
- multiple delegates;
- appeal/overrule route;
- abstention/absence.

Then record the federation tier:

- each community's weight;
- decision quota;
- quorum;
- proxy rules;
- whether delegates from one community vote as one bloc;
- decision-specific thresholds.

Individual influence is a property of the **combined two-tier procedure**, not the top-tier weight table alone.

---

## B30-L02 — Compute pivotal power instead of reading influence off the weight column
**Status:** TAIL-PROVISIONAL + PRACTICAL

For a small weighted federation, calculate exact coalition power under the real quota. Useful measures include Penrose-Banzhaf and Shapley-Shubik indices, supplemented where possible by simulations based on actual voting/correlation patterns.

A 37% nominal weight can have the same pivotal power as a 5% weight if the coalition structure makes the two communities interchangeable as the same larger community's necessary partner. Conversely, a large weight can become an outright dictator or veto player at some quotas.

The accompanying Creative Tail repo now contains:

`analysis/weighted_voting_power.py`

for exact small-game Banzhaf and Shapley-Shubik calculation.

---

## B30-L03 — Do not paste in the Penrose square-root rule
**Status:** PRACTICAL / KNOWN

The classic Penrose result is useful because it shows why simple population proportionality need not equalize indirect individual influence in a two-tier system.

But its familiar square-root result depends on strong assumptions, including a model of how individuals vote within constituencies. Correlated preferences and small numbers of communities can change the result materially.

Even more importantly, the mathematical target is a **power distribution**; simply assigning square-root weights does not generally guarantee square-root voting power.

Use the Penrose model as one sensitivity case, not a sacred constitution-writing formula.

---

## B30-L04 — Analyze weights and decision quota together
**Status:** PRACTICAL / KNOWN

A voting rule is not `weights` alone.

The same weights under a 50%, 60%, or 2/3 threshold can produce completely different:

- winning coalitions;
- veto players;
- dummy players;
- ability to act;
- individual/community power.

Therefore any fairness review that changes weights without recalculating the quota-game is incomplete.

---

## B30-L05 — Stress-test actual correlation and bloc behavior
**Status:** PRACTICAL / KNOWN

Communities are not independent random electorates. Members share housing, work, ideology, friendship and institutional history; delegates may deliberate together; communities may have recurring alliances.

Run at least several models:

1. independent binary preferences;
2. correlated preferences within communities;
3. correlated preferences across communities;
4. delegates voting as rigid local blocs;
5. delegate discretion after federation deliberation;
6. empirical historical coalition frequencies where enough data exist.

If the supposed fairness of a voting rule disappears under plausible correlation, say so.

---

## B30-L06 — Recompute representation after membership/population changes
**Status:** PRACTICAL / KNOWN

A new community joining, one leaving, or a large population shift can change coalition power discontinuously even when all existing weights remain the same.

Re-audit after:

- a community joins/leaves;
- a major population shift;
- a quota change;
- an internal decision-rule change;
- a change in number/authority of delegates.

Do not wait until a contentious vote reveals the new power structure accidentally.

---

## B30-L07 — Decide whose population counts
**Status:** PRACTICAL / KNOWN

Population-based representation needs a constitutional definition:

- full adult members only?;
- provisional members?;
- children/dependents?;
- residents who are not members?;
- people on long leave?;
- supported nonresidents?;

The correct answer depends on what representation is meant to represent. Do not let a convenient directory count silently become voting law.

---

## B30-L08 — Audit supermajority rules for unexpected veto and dummy power
**Status:** PRACTICAL / KNOWN

A supermajority can protect minorities but also produce unintuitive coalition power. A small community may become a critical partner; another much larger community may add no pivotal power in some configurations.

Before adopting 3/5, 2/3, 3/4, etc., calculate who can:

- initiate a winning coalition;
- block every coalition;
- never change an outcome;
- become indispensable only with certain partners.

Choose the threshold for substantive reasons, then inspect the resulting power—not the other way around.

---

## B30-L09 — Solve the inverse power problem when fairness matters
**Status:** TAIL-PROVISIONAL + PRACTICAL

If a federation can state the power distribution it wants, search over candidate weights **and quotas** for a rule that approximates that target under the chosen behavioral model.

Do not hand-set weights equal to desired power shares.

For a very small federation, exact enumeration is cheap enough that there is little excuse not to inspect alternatives directly.

---

## B30-L10 — Publish assumptions so mathematics does not become false legitimacy
**Status:** PRACTICAL / KNOWN

A power calculation can look objective while hiding political/model choices.

Publish:

- representation objective;
- population definition;
- local-vote model;
- top-tier rule;
- power index used;
- correlation assumptions;
- sensitivity cases;
- known uncertainty.

Mathematics should expose the consequences of choices, not disguise those choices as mathematical necessity.

---

# Conditional FEC illustration — not a claim about the live 2026 rule

The current official FEC website says the former `thefec.org` site is outdated and the network is rebuilding. Current public pages list three full-member communities at roughly:

- Twin Oaks: about 100 adults and children;
- East Wind: about 60 adults and 4 children;
- Alpha Farm: 9 residents.

Older FEC material describes a population-based fallback vote, but this supplement does **not** assume that exact historical mechanism remains the live current policy.

If, purely for illustration, the three populations `[100, 64, 9]` were used as linear weights with a 60% winning quota:

- nominal weight shares ≈ 57.8%, 37.0%, 5.2%;
- exact normalized Banzhaf top-tier powers = **60%, 20%, 20%**.

East Wind and Alpha would have equal pivotal power in this simple coalition game despite radically different nominal weights.

Replacing those weights with square roots `[10, 8, 3]` while keeping a 60% quota produces the same winning-coalition structure and still gives **60/20/20** Banzhaf power. At a 50% quota, every pair wins and the Banzhaf powers become equal thirds.

The point is not that one of these rules is correct. It is:

> **The quota and coalition geometry determine power jointly with weights. An egalitarian federation should inspect the result rather than trusting an intuitive formula.**

---

# Batch 30 disposition

C019 survives provisionally as a cross-domain operational transfer. Voting-power theory itself is old and extensively developed. The target contribution is applying its full `objective → two-tier model → power calculation → inverse design → sensitivity audit` loop to intentional-community federations.

Demote C019 if a close intentional-community/cooperative-federation implementation is found that already routinely performs this type of power-index/inverse-rule analysis.
