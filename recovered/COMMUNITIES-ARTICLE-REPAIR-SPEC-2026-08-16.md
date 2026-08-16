# Communities article repair specification — 2026-08-16

Status: **AUTHORIZED ARTICLE HARMONIZATION**  
Mode: research repair only; detector/humanization comes later  
Working branch: `agent/article-repair-20260816`  
Research base: canonical `recovered/COMMUNITIES-ARTICLE-GAP-BANK-CURRENT.md` (G-001–G-028)

## Authoritative article source

Use the raw Substack editor HTML in the user's File Library named `Pasted text.txt`, created/modified 2026-08-15T10:58:17Z. It begins with the editable Tiptap/ProseMirror root (`data-testid="editor"`) and preserves Substack-native image, video, Instagram, digest-post, button, link, and caption objects.

Do **not** substitute the published page, a PDF export, rendered HTML, or extracted prose. Those lose editor-native structure.

The exact repair operations are machine-readable in:

- `recovered/COMMUNITIES-ARTICLE-REPAIR-OPS-2026-08-16.json`

Application is fail-closed via:

- `scripts/apply_community_article_repair.py`

Tests:

- `tests/test_apply_community_article_repair.py`

## Thesis-integrity rule

The repair does not replace the author's thesis with the research synthesis. It does four narrower things:

1. correct publication-facing factual/currentness problems;
2. add mechanisms the evidence showed were materially missing;
3. mark where evidence does **not** establish a stronger claim the article might otherwise imply;
4. make the author's preferred architecture more operational without converting it into a duty of universal inclusion, state dependence, professional rule, or federation centralization.

Where research challenged a claim, the repair changes the claim explicitly rather than silently softening it. In particular:

- long visits / inner-work performance are **not** treated as validated dangerous-person or manipulator screens;
- community/peer care is **not** treated as automatic clinical, disciplinary, custody, evidentiary, or membership authority;
- independent correction is **not** equated with nation-state correction;
- cohesion, survival, occupancy, and retention are **not** treated as sufficient success metrics;
- the Zapatista Escuelita is **not** claimed to have already produced a demonstrated lineage of durable descendant communes with human-outcome panels;
- serious/generalized danger can still justify ejection; restorative work is not an obligation to rehabilitate a dangerous person inside the commune.

## Gap-to-operation crosswalk

| Gap | Repair disposition |
|---|---|
| G-001 fair separation | `AR-13` adds conduct threshold, immediate protection, evidence/recusal/reply/review, protected transition, outside trigger. |
| G-002 peer-care firewall | `AR-02` separates care from membership, work, housing, child, medical, and evidentiary authority. |
| G-003 protected dissent/reporting | `AR-03`, `AR-04`, `AR-13` add non-waivable reporting, founder-independent review, and separation review. |
| G-004 follow-the-power founder audit | `AR-04` follows deed, accounts, appointments, records, admissions, reviewers, access, complaints. |
| G-005 non-waivable rights floor | `AR-03` adds bodily safety, food/sleep, independent care, private thought, outside contact, protected reporting, usable exit. |
| G-006 outcome dashboard | `AR-05`, `AR-14` distinguish human/function outcomes from institutional survival and add dissolution continuity. |
| G-007 cohesion is not safety | `AR-03`, `AR-05` explicitly reject retention/consensus/survival as sufficient proof. |
| G-008 materially usable exit | `AR-06`, `AR-12` add pre-opt-in adulthood transition resources and liquid exit capacity. |
| G-009 bounded child authority | `AR-07A/B`, `AR-03` add a reporting/advocate route outside community leadership and non-waivable rights. |
| G-010 premove simulations | `AR-09`, `AR-10` add real decision/work/conflict simulations and staged high-consequence access. |
| G-011 preselected independent mediator/ombud | `AR-13` selects the route before crisis and distinguishes mediation from evidence/adjudication. |
| G-012 financial controls | `AR-12`, `AR-14` add account visibility, dual control, conflicts, valuation, liquidity, and dissolution continuity. |
| G-013 jurisdiction / nonoptional duties | `AR-02`, `AR-13` keep peer care inside competence and map escalation to competent non-self-reviewing layers. |
| G-014 role rights for nonmembers | `AR-10` gives visitors/workers/renters/interns role-specific standing without general governance rights. |
| G-015 site/capability budget | `AR-11` adds water/housing/food/health/debt/runway/labor/transport/school/market/critical-skill constraints. |
| G-016 movement continuity/fission | `AR-14`, `AR-15`, `AR-16` add living-will continuity, experiment-before-fission, and translocal infrastructure. |
| G-017 present-tense child audit | `AR-05`, `AR-06`, `AR-07A/B` add later child outcomes, adult option, and independent child routes. |
| G-018 dangerous-person filter challenge | `AR-08`, `AR-09` remove the implied visit-duration lie detector and require conduct-specific evidence. |
| G-019 autonomy/legal-pluralism correction | `AR-13` explicitly corrects state-monopoly framing while preserving law/rights floors. |
| G-020 Escuelita lineage ladder | `AR-05`, `AR-17` make replication an outcome to measure and explicitly state what the audit did not establish. |
| G-021 experiment before fission | `AR-15` creates microexperiment → semi-autonomous → nearby seed → fission gradient with asset-gating caveat. |
| G-022 boundary egalitarianism | `AR-10` adds role-specific standing for exposed nonmembers. |
| G-023 federation anti-starvation | `AR-16` budgets boring translocal capacity and degraded/restart work. |
| G-024 modular federation services | `AR-16` separates bilateral/local, function-specific, and general layers and isolates financial-risk authority. |
| G-025 federation membership lifecycle | `AR-16` uses current FEC full/in-dialogue/friend distinctions to preserve non-convergent alliance. |
| G-026 mobility interface | `AR-16` defines thin-adapter responsibility rather than internal-system harmonization. |
| G-027 purpose-specific accounting | `AR-16` distinguishes grants, pooled protection, loans, guarantees, commitments, exchange, nontransactional transfer. |
| G-028 constitutional casebook | `AR-16` preserves hard-case facts/reasoning/dissent/consequences/rule version and reruns after rule changes. |

Additional strict-survivor integrations selected because they directly close article dependencies:

- C001 → `AR-16` constitutional casebook application;
- C003 → `AR-15` cheap pilots do not fairly test every asset/scale-gated institutional package;
- C025 → `AR-14` permanent communal living-will bundle;
- C026 → `AR-06` adulthood option grant before adult regime opt-in.

## Source-hardening selected for publication

Only claims actually changed/added are source-hardened here rather than reopening the whole 198-finding corpus.

### Federation of Egalitarian Communities

Primary current pages checked 2026-08-16:

- https://www.egalitariancommunities.org/ — states this is the new official FEC website, the old `thefec.org` site is out of date/no longer maintained, and the organization is in an active rebuilding phase.
- https://www.egalitariancommunities.org/initiatives — describes current monthly calls, annual assembly, independently governed PEACH, exchange trips, mini-grants, and reduced outreach during rebuilding.
- https://www.egalitariancommunities.org/communities — distinguishes Full Members, Communities in Dialogue, and stable Friends that either do not meet criteria or choose not to pursue membership.
- https://www.egalitariancommunities.org/policies — lists the current Constitution, Mini-Grant Policy, Exchange Program Policy, full-member criteria, and official statuses.

Publication repair therefore changes the article's obsolete `thefec.org` link to the current official domain and uses only current FEC claims visible on those primary pages. The more detailed historical LEX/LETS/parity and kibbutz-finance evidence remains in the public research report rather than being re-litigated in article prose.

### Sénégal Article 319

Primary/current legal verification checked 2026-08-16:

- Senegal Ministry of Justice, project/adoption material for law n°05/2026 modifying Article 319: https://justice.sec.gouv.sn/assemblee-nationale-adoption-du-projet-de-loi-n05-2026-modifiant-larticle-319-du-code-penal/
- Human Dignity Trust's text/status page for enacted Law No. 2026-08 of 27 March 2026: https://www.humandignitytrust.org/resources/law-no-2026-08-of-march-27-2026-amending-article-319-of-law-no-65-60-of-july-21-1965/

The repair keeps the author's argument and makes the factual wording more precise: 5–10 years for same-sex sexual acts under the amended provision, plus new offences concerning public apology/promotion and specified financing/support.

## Native-object preservation / application contract

The patcher is intentionally not an HTML reserializer. It performs exact string replacements/inserts so all untouched source bytes remain untouched. It refuses to emit output if:

- any operation anchor occurs zero or more than once;
- the input lacks the raw Substack editor marker;
- the ordered marker sequence for images, digest embeds, YouTube embeds, Instagram embeds, and Substack share/checkout buttons changes.

It emits an audit JSON containing before/after SHA-256, byte counts, every applied operation ID, and the native-object marker inventory.

## Application command

Once the authoritative raw editor file is locally available:

```bash
python scripts/apply_community_article_repair.py \
  /path/to/Pasted\ text.txt \
  --ops recovered/COMMUNITIES-ARTICLE-REPAIR-OPS-2026-08-16.json \
  --output repaired/community-article-research-harmonized.html \
  --audit repaired/community-article-research-harmonized.audit.json
```

Run `--check` first if desired; it validates all anchors and native-object invariants without writing repaired HTML.

## After this repair

Do not begin detector-driven humanization until the patched raw HTML has been applied and audited. The next phase is then prose/humanization work against this research-harmonized version, with lossless-claim preservation and native Substack objects still frozen.
