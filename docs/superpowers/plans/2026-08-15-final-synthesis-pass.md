# Final cross-corpus synthesis pass

Date: 2026-08-15 (Africa/Dakar)  
Mode: P0 research synthesis; no article-prose revision

## Decision

The article-gap bank is not the final research report. It is an article-directed reconciliation layer: each row begins with what the article already says and asks what evidence would require an addition, qualification, or challenge. That makes it the correct change specification for a later editorial phase, but it also makes the article's present architecture the organizing frame.

The final synthesis uses the opposite direction of travel. It begins with all 186 findings and asks which mechanisms recur across cases, which findings contradict or bound one another, which apparent successes are only process or institutional endpoints, which components have positive support, and which questions remain unanswered. The article is considered only after the corpus-directed conclusions are stable.

## Immutable inputs

- `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`: 186 findings, F-001 through F-186.
- `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`: 18 article implications, retained unchanged.
- Primary corpus: 984 *Communal Societies* PDFs across volumes 1-45 and eight standalone substantive sources.
- Adjacent corpus: 20 bounded records across child response, assessment and review, durable treatment and transition, official correction, and fair separation/pooled risk/planned fission.
- Existing bounded reports and source inventories.

The synthesis adds no finding, source, quotation, article gap, diagnosis, or article prose. Evidence that still requires external verification retains that status.

## Unit of analysis

The unit is a load-bearing cross-corpus proposition, not a source count. A finding can support more than one proposition, and many findings come from the same article, community, historical tradition, or bounded search. Counts therefore demonstrate coverage and recurrence in the coded corpus; they are not prevalence estimates, effect sizes, or votes.

Every proposition must preserve four distinctions:

1. source observation versus source or model interpretation;
2. process existence versus implementation and later outcome;
3. intentional-community evidence versus traditional-society, clinical, legal, or instrument evidence;
4. a transferable component versus a complete validated system.

## Horizontal questions

Each finding is recoded against the same questions:

1. What function is being exercised: admission, discipline, care, medicine, custody, property, accounting, work, evidence, appeal, external representation, or succession?
2. Who holds practical control, including appointment, information, agenda, veto, emergency, and sanction power?
3. Can the affected person report, refuse, reply, appeal, obtain records, contact outsiders, remain housed, or leave without losing necessities or family?
4. Is the response conduct-specific, time-limited, proportionate, reviewable, and independent of the challenged actor?
5. What outcome was actually measured: inside-program behavior, later conduct, victim safety, child wellbeing, family burden, material viability, institutional survival, or only completion of a legal or administrative step?
6. What alternative interpretation remains live?
7. What can transfer to a voluntary community, and what requires licensed, statutory, judicial, or other external authority?

## Theme architecture

Every finding receives one primary theme in the crosswalk:

- T-01 authority, role fusion, and capture
- T-02 participation, dissent, reporting, and evidence
- T-03 membership, classification, and safety prediction
- T-04 conflict, bounded separation, and remedy
- T-05 care, medicine, therapy, and governance firewalls
- T-06 children, family, education, and direct rights
- T-07 assets, exit, records, and material security
- T-08 capacity, infrastructure, labor, and external dependence
- T-09 external correction, law, and professional boundaries
- T-10 success, outcomes, source quality, and measurement
- T-11 succession, fission, and movement continuity
- T-12 dangerous-child bounded null and adjacent response evidence

Primary themes are a coverage partition, not an assertion that findings have only one relevance. Multiple relationships are preserved through synthesis-claim IDs and article-gap references.

## Claim-status rubric

- **Recurring qualitative convergence:** the mechanism appears across materially different cases or source lanes, with source limits retained.
- **Protective component:** one or more records support a bounded practice, but not a complete governance system.
- **Counterevidence or tradeoff:** a finding limits a simple prescription or shows that a protection can create another risk.
- **Adjacent boundary evidence:** professional, legal, traditional-society, or instrument evidence informs functions or limits but does not become intentional-community outcome evidence.
- **Bounded null:** the specified evidence pattern was not found under the recorded search; this is not proof of historical or universal absence.
- **Model-assisted synthesis:** a combined architecture is inferred by relating supported components. It is explicitly not represented as source-validated or empirically tested as a package.

## Completeness controls

The pass is complete only if:

- the ledger and gap-bank hashes are unchanged;
- F-001 through F-186 appear exactly once in the crosswalk;
- every finding has a primary theme, at least one non-model-assisted synthesis claim, an evidence role, confidence, verification status, and its complete set of article-gap references;
- the three findings absent from the gap bank altogether—F-027, F-030, and F-032—are still synthesized;
- all twelve themes and S-01 through S-15 appear in the report;
- the report separately states convergence, counterevidence, positive components, children and danger, external boundaries, remaining unknowns, and the relationship to Joel's thesis and article;
- no clinical, custody, judicial, police, restraint, or licensing authority is transferred to a private community;
- no article prose is drafted or silently revised.

## Outputs

- `recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`
- `recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`
- `recovered/update_final_synthesis.py`
- `recovered/verify_final_synthesis.py`
- `recovered/test_final_synthesis_workflow.py`

The report is the comprehension layer. The crosswalk proves finding-level coverage. The gap bank remains the later editorial change specification. The evidence ledger remains the source-grounded authority.
