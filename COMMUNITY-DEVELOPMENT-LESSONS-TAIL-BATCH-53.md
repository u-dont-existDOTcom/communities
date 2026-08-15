# Community Development Lessons — Creative Tail Batch 53

Updated: 2026-08-15  
Status: append-only practical supplement; C024 provisional cross-domain transfer

---

# Main lesson — Sensitive federation research need not centralize readable raw answers

**Status:** TAIL-PROVISIONAL + PRIVACY/RESEARCH ARCHITECTURE  
**Creative Tail:** C024 — Non-custodial federation research

For suitable aggregate questions, design the research system so neither local community leadership nor the federation research office needs to possess readable individual responses.

Secure aggregation, secure multiparty computation (MPC), federated analytics, secret sharing and differential privacy are established technologies. The communal transfer is the trust architecture.

---

# Two separate privacy layers

## Layer A — input confidentiality

Goal: no single local/federation administrator sees raw individual answers.

Possible approaches:
- independent custodian baseline;
- split-key/secret-sharing trustees;
- secure aggregation;
- MPC;
- federated analytics.

## Layer B — output disclosure control

Goal: the aggregate result itself does not identify someone.

Use C023:
- cumulative release ledger;
- differencing checks;
- pooling;
- suppression/coarsening;
- access tiers;
- formal DP when justified.

**Input encryption without output control is insufficient.**

---

## B53-L01 — Start with simple aggregate use cases

Good early candidates:
- counts;
- rates;
- means;
- category histograms;
- reporting-pressure diagnostic totals;
- C022 measurement-canary distributions;
- pooled current/leaver outcomes.

Do not use heavy cryptography for its own sake.

## B53-L02 — Separate eligibility verification from answer contents

Members need one-person/eligible participation without linking identity to response.

Possible structure:
1. independent eligibility authority issues one-time token;
2. answer service verifies token;
3. token cannot be mapped back to answer by the analyst/local leaders.

## B53-L03 — Split trust where useful

Possible trustees:
- federation research office;
- independent ombud/research nonprofit;
- elected privacy trustee.

No one trustee can reconstruct individual responses alone.

## B53-L04 — Publish the threat model

State plainly:
- who can collude;
- what metadata remain visible;
- who holds keys/shares;
- dropout behavior;
- query authorization;
- output protection;
- what the system **does not** protect.

## B53-L05 — Govern queries, not just data access

Unlimited aggregate queries can reconstruct private data even if raw inputs are encrypted.

Every query should pass C023 cumulative disclosure review.

## B53-L06 — Explain privacy in understandable language

A member-facing promise should say only what is technically true, e.g.:

> No community leader and no single federation researcher receives your readable individual answer; only approved aggregate results are recoverable after enough participants contribute.

Do not promise anonymity if small-N output can still identify someone.

## B53-L07 — Independently verify privacy software/protocol

Where cryptography is used:
- open specification/code where possible;
- independent security review;
- reproducible deployment/configuration;
- public threat model;
- update/incident process.

## B53-L08 — Secure aggregation does not fix face-saving by itself

It can reduce fear of custody/reprisal, but not:
- genuine conformity;
- identity-protective beliefs;
- coordinated lying;
- bad questions;
- misunderstanding.

Combine with Batches 43–44.

## B53-L09 — Raw data never collected centrally cannot later be captured centrally

This limits harm from:
- future federation leadership change;
- analyst misconduct;
- data breach;
- political capture;
- some legal demands.

The exact legal/security effect depends on implementation/jurisdiction.

## B53-L10 — Some research still needs controlled contextual data

C024 is not appropriate for every:
- qualitative interview;
- safeguarding investigation;
- complex case reconstruction;
- individual follow-up.

Use minimum necessary identifiable data under explicit consent/rights rules.

## B53-L11 — Tiny community outputs can remain unsafe

Eight encrypted answers that produce an exact eight-person aggregate can still expose a person.

The result may need to be:
- federation-pooled;
- noisy/coarsened;
- restricted-access;
- unpublished.

## B53-L12 — Non-custodial federation pooling can make indirect-question methods more feasible

B44 list/randomized-response techniques often need more N than one commune can provide. Federation secure aggregation can pool compatible data without centralizing raw answers.

## B53-L13 — Test whether stronger technical privacy actually changes reporting

Where ethically feasible, compare ordinary independent confidentiality with a stronger non-custodial mode.

Measure:
- privacy confidence;
- participation;
- sensitive-report prevalence.

If responses shift, custody fear is part of the measurement environment.

---

# Deployment ladder

1. independent organizational custody + C023 release controls;
2. separate eligibility tokens from response identity;
3. pilot simple secure aggregation for one useful sensitive statistic;
4. test whether trust/reporting improves;
5. expand to MPC/federated analytics/DP only if demonstrated value exceeds complexity.

---

## Consolidation note

Append-only because `agent/final-research-synthesis` contains the active Escuelita-expanded research state. Consolidate only after resolving the current branch head.
