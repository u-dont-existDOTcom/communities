#!/usr/bin/env python3
"""Commit the completed Communal Societies volumes 26-28 research checkpoint."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
GAPS = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
REPORT = ROOT / "COMMUNITIES-V26-V28-RESEARCH-REPORT.md"


def finding(**kwargs: str) -> dict[str, str]:
    return kwargs


NEW_FINDINGS = [
    finding(
        finding_id="F-077",
        track="Track A response process",
        source_record_id="M-0604",
        source_file="011-the-society-of-separatists-of-zoar-vs-zoar-and-the-courts.pdf",
        journal_volume_issue_year="Vol. 26, no. 1 (2006)",
        article_title="The Society of Separatists of Zoar vs....: Zoar and the Courts",
        author="Kathleen M. Fernandez",
        community_group="Society of Separatists of Zoar",
        page_locator="PDF pp. 2-9; printed pp. 105-112",
        printed_page_number="105-112",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="historical legal synthesis using articles of agreement, notices, testimony, and reported court decisions",
        exact_factual_observation="Zoar's articles assigned disputes to a five-member Standing Committee and stripped a dissatisfied member of further membership rights. After reports of tavern drunkenness, fighting, secret money, and hoarded goods, Johannes Goesele refused the committee hearing and remained in the tavern. Counsel then issued a conduct-specific eviction notice inviting excuse, extenuation, and cause against expulsion. Goesele sued instead. Courts upheld the communal contract under which separation or expulsion ended property claims; his wife could receive support only by returning to live and work at Zoar. The Society later gave the impoverished former members supplies.",
        what_source_establishes="Conduct-specific notice and an offered hearing can coexist with a severe, structurally coercive consequence. Judicial enforcement of a property contract does not establish that the internal fact-finding, forfeiture rule, or practical exit was fair.",
        what_source_does_not_establish="It does not prove every allegation against Goesele, show that the committee was independent, establish what evidence it weighed, show whether he received the notice before suing, or make the nineteenth-century forfeiture holdings current law.",
        author_interpretation="The author presents the litigation as both a dismissal problem and a landmark validation of communal property arrangements.",
        alternative_interpretation="Goesele's refusal to attend may have defeated a usable internal remedy, and forfeiture may have been central to preserving the common estate; later material aid also complicates a simple abandonment account.",
        response_process="Standing Committee jurisdiction; allegations and testimony; offered hearing; conduct-specific notice and opportunity to show cause; expulsion and eviction; external litigation; conditional support and later supplies. No neutral internal appeal is described.",
        outcome="The dismissal produced nearly twenty years of litigation. The former members recovered no equity and experienced poverty; the Society survived and provided some supplies.",
        transferability="High for separating notice and fact-finding from exit equity, ensuring independent appeal, and preserving unconditional transition support for spouses and dependents.",
        article_gap_status="C",
        likely_article_destination="Fair separation / money and land / outside response",
        confidence="high",
        external_verification_needed="yes",
        notes="Do not treat the reported court holdings as current legal advice. DOI: https://doi.org/10.9707/0739-1250.1491",
    ),
    finding(
        finding_id="F-078",
        track="Track A separation and escalation",
        source_record_id="M-0600",
        source_file="007-easter-1832-a-brief-interlude-of-peace-for-georg-rapp-s-harmony-society.pdf",
        journal_volume_issue_year="Vol. 26, no. 1 (2006)",
        article_title="Easter, 1832: A Brief Interlude of Peace for Georg Rapp's Harmony Society",
        author="Eileen Aiken English",
        community_group="Harmony Society and New Philadelphia seceders",
        page_locator="PDF pp. 4-7; printed pp. 39-42",
        printed_page_number="39-42",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="historical reconstruction from conflicting community accounts, depositions, correspondence, and press material",
        exact_factual_observation="The Harmony Society and 1832 seceders agreed to a $105,000 separation payment in three installments with deductions and release conditions. The first payment was reduced and later adjusted; the final payment was delayed while the payer demanded release of claims. With the splinter settlement in debt and short of food and medicine, a delegation of 79 men arrived to present an appeal and seek asset records. Accounts disagree about weapons and who initiated violence. The militia intervened and a trial was scheduled, but the splinter society dissolved and the trial never occurred.",
        what_source_establishes="A written exit settlement can fail when one side controls deductions, records, release conditions, and disbursement. Without a neutral accounting and escalation channel, urgent material need and mixed-purpose collective action can turn an equity dispute into a safety crisis.",
        what_source_does_not_establish="It does not resolve the competing accounts of payment, weapons, assault, or intent; establish the exact legal entitlement of either side; or show that neutral escrow alone would have prevented the conflict.",
        author_interpretation="The author concludes that neither side won and that bitterness and institutional damage outlasted the immediate dispute.",
        alternative_interpretation="The seceders' own spending, leadership, and debt contributed materially to their desperation, while the Harmony Society may have had legitimate unresolved-claim concerns.",
        response_process="Negotiated installment agreement; deductions and appeal; delayed final payment; written collective appeal; attempted access to records; disputed violence; militia and court referral; no completed adjudication.",
        outcome="The splinter society dissolved before trial, members scattered, bitterness persisted, and the Harmony Society entered a long economic decline.",
        transferability="High for neutral valuation, common records, escrow, payer-independent disbursement, rapid hardship relief, and a safe channel for contested mass exit.",
        article_gap_status="C",
        likely_article_destination="Fair separation / money and land / conflict architecture",
        confidence="medium",
        external_verification_needed="yes",
        notes="The source explicitly reconstructs incompatible accounts; do not choose a culprit where it does not. DOI: https://doi.org/10.9707/0739-1250.1487",
    ),
    finding(
        finding_id="F-079",
        track="Track A governance safeguard",
        source_record_id="M-0606",
        source_file="013-changing-pilots-in-mid-stream-how-german-american-communitarian-societies-successfully-handled-the-deaths-of-t.pdf",
        journal_volume_issue_year="Vol. 26, no. 1 (2006)",
        article_title="Changing Pilots in Mid-Stream: How German-American Communitarian Societies Successfully Handled the Deaths of Their Founders",
        author="Michael Taylor",
        community_group="Harmony Society",
        page_locator="PDF p. 5; printed p. 138",
        printed_page_number="138",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="comparative historical synthesis",
        exact_factual_observation="George Rapp made no succession provision. A democratically elected Council of Elders, created during an earlier legal crisis with limited temporal authority, became the Society's religious and secular governing body after his death. When designated religious leader Jacob Henrici tried to establish absolute authority, the council and co-trustee R. L. Baker rebuked him. Henrici accepted the rebuke and remained minister; the community survived the transition for decades.",
        what_source_establishes="A representative body created before a succession crisis can become a practical override: it constrained a would-be autocrat without requiring either submission or total removal, and separated ministry from final governance.",
        what_source_does_not_establish="It does not show how inclusive the election was, whether the council could handle abuse allegations, how often it checked leaders, or that the later society was otherwise democratic or safe.",
        author_interpretation="The author credits shared goals and the expanded Council of Elders with allowing the Society to survive its initial leadership transition.",
        alternative_interpretation="Henrici's willingness to accept correction and the community's continuity of purpose may have mattered as much as the council's formal design.",
        response_process="Preexisting elected council; post-founder expansion of authority; collective rebuke of successor; successor accepts limited role and remains in office.",
        outcome="The attempted concentration of power was checked and the Society continued for decades.",
        transferability="High for installing an elected, independently legitimate body before succession and giving it power to narrow a leader's role without making every correction existential.",
        article_gap_status="B",
        likely_article_destination="Founderism / succession / tested override",
        confidence="high",
        external_verification_needed="yes",
        notes="A positive mechanism, not proof that the council was adequate in all domains. DOI: https://doi.org/10.9707/0739-1250.1493",
    ),
    finding(
        finding_id="F-080",
        track="Track A governance safeguard",
        source_record_id="M-0606",
        source_file="013-changing-pilots-in-mid-stream-how-german-american-communitarian-societies-successfully-handled-the-deaths-of-t.pdf",
        journal_volume_issue_year="Vol. 26, no. 1 (2006)",
        article_title="Changing Pilots in Mid-Stream: How German-American Communitarian Societies Successfully Handled the Deaths of Their Founders",
        author="Michael Taylor",
        community_group="Community of True Inspiration / Amana",
        page_locator="PDF pp. 8-10; printed pp. 141-143",
        printed_page_number="141-143",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="comparative historical synthesis",
        exact_factual_observation="An 1854 inspired testimony attributed to Christian Metz condemned any dissolution of communal ties and threatened deprivation and disgrace for those responsible. In 1919, older members who remembered the testimony rejected a constitutional revision permitting reorganization or dissolution. In 1932, the Great Change separated the religious and business sides, allowing economic reorganization while preserving the church's stated spiritual purpose.",
        what_source_establishes="A dead founder's recorded words can retain a practical veto long after personal succession succeeds. Institutional separation can make revision possible by protecting the valued purpose while changing the legal-economic form.",
        what_source_does_not_establish="It does not prove the testimony alone caused the 1919 rejection, quantify the cost of delay, establish unanimity in 1932, or show that structural separation solves other capture risks.",
        author_interpretation="The author treats shared goals, rather than transfer of charisma, as the main continuity mechanism and the Great Change as a smooth adaptation.",
        alternative_interpretation="Economic pressures and generational change may have driven both the delayed resistance and eventual reorganization more than institutional design did.",
        response_process="Archived prophetic prohibition; failed constitutional revision; later separation of religious and business institutions.",
        outcome="Reorganization was delayed in 1919 and achieved in 1932 without dissolving the religious body.",
        transferability="High for testing whether amendment rules bind founding texts and for considering separable legal entities when mission and operating form must change at different speeds.",
        article_gap_status="B",
        likely_article_destination="Founderism / rule revision / plan the funeral",
        confidence="high",
        external_verification_needed="yes",
        notes="The source discusses inherited veto power, not a dangerous-person case. DOI: https://doi.org/10.9707/0739-1250.1493",
    ),
    finding(
        finding_id="F-081",
        track="Track A source-method warning",
        source_record_id="M-0617",
        source_file="010-validation-in-the-shaker-era-of-manifestations-a-process-analysis.pdf",
        journal_volume_issue_year="Vol. 26, no. 2 (2006)",
        article_title="Validation in the Shaker Era of Manifestations: A Process Analysis",
        author="Glendyne Wergland",
        community_group="Shakers",
        page_locator="PDF pp. 5-6 and 11-16; printed pp. 124-125 and 130-135",
        printed_page_number="124-125, 130-135",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="historical process analysis using Shaker journals and visitor accounts",
        exact_factual_observation="Leaders treated separately reported matching visions as corroboration, then sent Isaac Newton Youngs to place obstacles in the girls' path and test them. Youngs was already a committed believer; after validating the visions he demonstrated their actions to leaders and peers, potentially supplying a script. A skeptical journal keeper was replaced. When a girl admitted augmenting a gift, the deception was said to have been exposed and reproved by a true gift. Doubt was veiled, questioning was discouraged to preserve union, contradictory gifts emerged, and leaders later restricted manifestations and closed public worship.",
        what_source_establishes="Multiple reports and an apparently empirical test are not independent when investigators, witnesses, vocabulary, incentives, and final authority share the same prior commitment. Punishing criticism and using the disputed channel to validate itself weakens falsification.",
        what_source_does_not_establish="It does not prove that all visions were feigned, that leaders knowingly manufactured evidence, that the girls were dangerous, or that the described restraint and regulation were clinically appropriate.",
        author_interpretation="The author models the episode as a multi-stage social validation process in which official acceptance enabled spread and later required regulation.",
        alternative_interpretation="Shared belief does not itself make an experience false; leaders did test claims, expose at least some pretense, and eventually narrow disruptive public behavior.",
        response_process="Separate reports; insider testing; demonstration; leadership validation; criticism suppression; insider policing of fraud; later restrictions and closure to outsiders.",
        outcome="The manifestations spread, generated contradictions and control problems, and were eventually constrained; public worship later became more moderate.",
        transferability="High for evidence-channel independence, blinded or outside assessment, preservation of dissent, and avoiding circular validation in allegations or safety reviews.",
        article_gap_status="C",
        likely_article_destination="Evidence protocol / dissent / safety proxies",
        confidence="high",
        external_verification_needed="yes",
        notes="The girl's admitted embellishment is not a dangerous-child case. DOI: https://doi.org/10.9707/0739-1250.1504",
    ),
    finding(
        finding_id="F-082",
        track="Track A capture attempt",
        source_record_id="M-0619",
        source_file="012-the-outlaws-of-kalalau-the-aloha-spirit-and-threats-to-the-commune.pdf",
        journal_volume_issue_year="Vol. 26, no. 2 (2006)",
        article_title="The Outlaws of Kalalau, the Aloha Spirit, and Threats to the Commune",
        author="Jeffrey S. Rasley",
        community_group="Outlaws of Kalalau",
        page_locator="PDF pp. 5-6 and 8-11; printed pp. 170-171 and 173-176",
        printed_page_number="170-171, 173-176",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="small first-person observational account with follow-up conversations and email",
        exact_factual_observation="The group recognized Chaz only as a mediator and had no means to exclude anyone from the valley, though it could socially exclude a person. Member Akamai announced that thirty young Hawaiians willing to resist state authority would come to clear sacred sites. He later wrote that only Hawaiians could live in the community he intended to establish and the current Outlaws would be visitors. Chaz relied on an informal understanding and then dismissed the plan as impractical. A court jailed Akamai for camping violations and failure to appear; the proposed replacement community had not materialized by the author's next visit.",
        what_source_establishes="An open-access ethos and purely mediating leadership supplied no internal forum or authority for testing an explicit proposal to displace existing members. The leader relied on personal assurance and feasibility rather than a decision, boundary, or contingency.",
        what_source_does_not_establish="It does not show that the announced group existed, that violence or displacement was imminent, that Akamai had practical control, that other members were intimidated, or that the park prosecution addressed the internal capture proposal.",
        author_interpretation="The author treats both state pressure and Akamai's sovereignty project as threats, while reporting that residents ultimately regarded the latter as foolish and unlikely.",
        alternative_interpretation="The proposal may have been aspirational rhetoric and nonintervention may have been proportionate; the group's lack of land title also limited any formal exclusion power.",
        response_process="Informal disclosure; private assurance to mediator; no recorded group deliberation or conditions; leader feasibility judgment; unrelated external law enforcement.",
        outcome="The proposal was unrealized at the observed checkpoint, Akamai served a short sentence on park charges, and the existing group continued.",
        transferability="Moderate for requiring a defined body to assess capture proposals, membership displacement, threatened force, and conflicts between open access and residents' safety.",
        article_gap_status="C",
        likely_article_destination="Founderism / capture test / open-door limits",
        confidence="medium",
        external_verification_needed="yes",
        notes="Tiny, informal group and a first-person account; the state action was not an internal safety remedy. DOI: https://doi.org/10.9707/0739-1250.1506",
    ),
    finding(
        finding_id="F-083",
        track="Track A classification failure",
        source_record_id="M-0648",
        source_file="004-utopian-communal-experiments-in-tasmania-a-litany-of-failure.pdf",
        journal_volume_issue_year="Vol. 28, no. 1 (2008)",
        article_title="Utopian Communal Experiments in Tasmania: A Litany of Failure?",
        author="William Metcalf",
        community_group="Southport Village Settlement",
        page_locator="PDF pp. 13-17; printed pp. 12-16",
        printed_page_number="12-16",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="historical synthesis using prospectus, press reports, official inspection, and site research",
        exact_factual_observation="An outside Ladies Committee controlled finances, selected members, appointed the manager, and imposed forty-one rules. Residents then faced poor soil, inadequate food, exposed housing, an allegedly incompetent manager, intrusive rules, and interpersonal conflict. After six months, fourteen families had left or been expelled as 'unsuitable or unworthy' and were replaced by other desperate unemployed people. The ten remaining men voted to end communal work and divide the land into individual allotments.",
        what_source_establishes="Opaque suitability labels and rapid replacement can turn a site, management, capacity, and voice failure into an alleged member-character failure. Screening more people does not correct a structurally unworkable environment.",
        what_source_does_not_establish="It does not identify which families left and which were expelled, specify the conduct behind any expulsion, prove the replacements were unsuitable, or isolate the effect of communal versus individual tenure.",
        author_interpretation="The author emphasizes repeated Tasmanian communal failure and describes Southport as paternalistic, poorly planned, and materially harsh.",
        alternative_interpretation="Some departures or expulsions may have been justified, and individual allotments may have improved incentives independently of governance or site quality.",
        response_process="Outside selection and rules; informal conflict smoothing; departures and unspecified expulsions; immediate replacement; member ballot to abandon communal work.",
        outcome="Communalism ended after six months; families worked separate plots, outside support later ceased, and only six families remained by 1898.",
        transferability="High for auditing admission and expulsion labels against site capacity, manager competence, resident voice, and comparable outcomes after replacement.",
        article_gap_status="D",
        likely_article_destination="Membership pipeline / math of absorption / labor and voice",
        confidence="high",
        external_verification_needed="yes",
        notes="Preserve the source's combined phrase 'left or been expelled'; it does not support treating every departure as removal. DOI: https://doi.org/10.9707/0739-1250.1437",
    ),
    finding(
        finding_id="F-084",
        track="Track A system response and child protection",
        source_record_id="M-0649",
        source_file="005-evolution-of-the-family-international-children-of-god-in-the-direction-of-a-responsive-communitarian-religion.pdf",
        journal_volume_issue_year="Vol. 28, no. 1 (2008)",
        article_title="Evolution of The Family International/Children of God in the Direction of a Responsive Communitarian Religion",
        author="Gordon Shepherd and Gary Shepherd",
        community_group="The Family International / Children of God",
        page_locator="PDF pp. 9-15; printed pp. 34-40",
        printed_page_number="34-40",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="historical and organizational synthesis informed by leadership interviews, visits to 23 homes in 16 countries, 21 headquarters interviews, observation, and movement publications",
        exact_factual_observation="The 1975 appointed hierarchy was described as susceptible to abuses of power; Berg responded by firing the entire leadership, appointing replacements, allowing homes to elect shepherds, and eventually disbanding the old organization. The authors report some adult-minor sexual contact following Berg's teachings in the late 1970s and early 1980s. Later rules abolished such contact under excommunication and banishment. The 1995 Charter specified child education, physical and mental health, age-based sexual rules, and home governance after legal consultation, grassroots workshops, revision, and a leadership vote; it was later updated under external and internal pressure.",
        what_source_establishes="The movement used organization-wide removal, elected local leadership, categorical safeguarding rules, legal input, member consultation, and a revisable charter in response to systemic abuse and child-related pressure. System reform and case-level accountability are separate functions.",
        what_source_does_not_establish="It does not provide individual allegation-to-assessment cases, show who was responsible, establish repair for harmed children, test whether the purge or bans were enforced fairly, quantify abuse, or independently validate claims that later police investigations found no evidence.",
        author_interpretation="The authors interpret the changes as substantial movement toward a more responsive communitarian religion.",
        alternative_interpretation="Their sustained access to current leaders and homes may favor the institution's reform narrative; a whole-tier purge sacrifices individual adjudication, and later reforms may also have served legitimacy and liability goals.",
        response_process="Wholesale leadership removal and reorganization; elected local shepherds; categorical prohibition with expulsion sanction; Charter drafting with legal and grassroots input; periodic revision and specialist boards.",
        outcome="The organization survived, formalized child-related rules, and broadened participation, but the source does not establish victim repair or case-level outcomes.",
        transferability="High for pairing system-wide safeguarding reform with a separate, independent case process, records, remedies, implementation audit, and child advocacy.",
        article_gap_status="C",
        likely_article_destination="Children / fair separation / non-waivable rights / governance",
        confidence="medium",
        external_verification_needed="yes",
        notes="The source is unusually access-dependent and sympathetic. Its characterization of critics and exonerating raid claims are not adopted as independent findings. DOI: https://doi.org/10.9707/0739-1250.1438",
    ),
    finding(
        finding_id="F-085",
        track="Track A shadow governance",
        source_record_id="M-0649",
        source_file="005-evolution-of-the-family-international-children-of-god-in-the-direction-of-a-responsive-communitarian-religion.pdf",
        journal_volume_issue_year="Vol. 28, no. 1 (2008)",
        article_title="Evolution of The Family International/Children of God in the Direction of a Responsive Communitarian Religion",
        author="Gordon Shepherd and Gary Shepherd",
        community_group="The Family International",
        page_locator="PDF pp. 16-20 and 23-25; printed pp. 41-45 and 48-50",
        printed_page_number="41-45, 48-50",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="organizational ethnography and leadership-access synthesis",
        exact_factual_observation="Many channels, editors, boards, and local councils participated in policy and prophecy, but Maria selected topics, commissioned channels, approved published prophecies, and always retained final approval. At home level, conflicts submitted to prophecy were typically muted and outward consensus achieved. Later restructuring purged 'lackadaisical and dissident' members and made whole homes subject to status downgrade for missing annual benchmarks. The authors conclude that when prophecy and democracy conflict, theos overrides demos.",
        what_source_establishes="Distributed participation, multiple reviewers, elected officers, and consensus rituals do not constitute an override when one person controls the final evidence-policy channel and whole-unit sanctions reward conformity. Formal participation and practical veto must be tested separately.",
        what_source_does_not_establish="It does not show that every prophecy session was coerced, that every dissenter was unsafe or harmless, how benchmark appeals worked, or that the leadership used its final authority maliciously.",
        author_interpretation="The authors describe a durable theo-democracy that is more participatory yet remains on the authoritarian side of the spectrum.",
        alternative_interpretation="Extensive consultation may have constrained final authority in practice even without a formal veto, and common standards may have served legitimate coordination and safeguarding functions.",
        response_process="Multi-stage consultation and editing; final leader approval; local prophecy-based consensus; centralized compliance monitoring; whole-home downgrade and membership purge.",
        outcome="Participation expanded while centralized control became more complex and effective; significant defection continued and final doctrinal authority remained concentrated.",
        transferability="High for mapping who commissions evidence, edits it, sets the question, controls final approval, hears appeals, and bears sanctions—not merely counting participants or votes.",
        article_gap_status="D",
        likely_article_destination="Founderism / evidence channels / cohesion and dissent",
        confidence="high",
        external_verification_needed="yes",
        notes="Use the source's own mixed conclusion; do not treat participatory procedure as either wholly fake or independently decisive. DOI: https://doi.org/10.9707/0739-1250.1438",
    ),
    finding(
        finding_id="F-086",
        track="Track A external complaint and settlement",
        source_record_id="M-0663",
        source_file="004-waco-and-oneida-the-impact-of-public-opinion-on-the-survival-of-unconventional-religious-communal-groups-in-am.pdf",
        journal_volume_issue_year="Vol. 28, no. 2 (2008)",
        article_title="Waco and Oneida: The Impact of Public Opinion on the Survival of Unconventional Religious-Communal Groups in America",
        author="Lawrence Foster",
        community_group="Oneida Community",
        page_locator="PDF pp. 10-14; printed pp. 9-13",
        printed_page_number="9-13",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="interpretive historical synthesis using a published compilation of primary Oneida sources",
        exact_factual_observation="After Henry Seymour severely whipped his mentally disturbed wife Tryphena, her father obtained an assault-and-battery indictment and nine members were required to testify. A settlement ended the charge: the community paid asylum expenses and promised an annual stipend after discharge. When the family later threatened additional indictments, Oneida hosted neighbors and paid the complainant for a discharge and, conditionally, for using his influence to stop the indictments. The community resumed complex marriage. The article describes no internal discipline or assessment of Seymour.",
        what_source_establishes="An external complaint produced treatment support and material provision that the internal system had not supplied. Conciliation can reduce escalation while also redirecting attention from offender accountability to institutional survival and suppression of further legal scrutiny.",
        what_source_does_not_establish="It does not show that the settlement was unfair to Tryphena, that the later indictments had merit, that Seymour faced no unreported consequences, or that litigation rather than conciliation would have produced a better outcome.",
        author_interpretation="The author praises Oneida's compromise, public relations, admission of mistakes, and nonviolent handling of hostile outsiders as a survival strategy.",
        alternative_interpretation="Avoiding a public trial may have protected Tryphena and secured care; the payment could be ordinary settlement rather than improper suppression. The absent internal accountability record remains material either way.",
        response_process="Family complaint and criminal indictment; witness testimony; out-of-court treatment and stipend agreement; later public outreach; payment conditioned on discharge and efforts to stop further indictments; no internal offender review described.",
        outcome="Charges were defused, the community resumed its practices and survived for decades, while the source records support for Tryphena but no stated consequence for the person who whipped her.",
        transferability="High for distinguishing victim support, mediation, legal settlement, public relations, evidence preservation, and offender accountability as separate requirements.",
        article_gap_status="C",
        likely_article_destination="Outside mediator / fair separation / legal coupling / evidence protocol",
        confidence="medium",
        external_verification_needed="yes",
        notes="The article is strongly polemical about Waco; only the documented Oneida sequence is promoted. DOI: https://doi.org/10.9707/0739-1250.1452",
    ),
    finding(
        finding_id="F-087",
        track="Track A source-method correction",
        source_record_id="M-0667",
        source_file="008-dark-error-s-night-will-soon-be-gone-dynamics-of-participation-in-new-harmony-1824-1827.pdf",
        journal_volume_issue_year="Vol. 28, no. 2 (2008)",
        article_title="Dark Error's Night Will Soon Be Gone!: Dynamics of Participation in New Harmony, 1824-1827",
        author="Peter Hohn",
        community_group="New Harmony",
        page_locator="PDF pp. 3 and 10-13; printed pp. 68 and 75-78",
        printed_page_number="68, 75-78",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="quantitative historical analysis of community ledgers compared with narrative accounts",
        exact_factual_observation="A received explanation blamed New Harmony's failure on open admission and lazy, inefficient, parasitic members. The contribution-and-consumption ledgers showed no significant deterioration over time; low-skilled members did not live comparatively free from the common store; local settlers contributed materially at high levels; and members elected to draft the constitution contributed about half the average while consuming near the average. The author notes that informal economies and intellectual contributions are incompletely captured.",
        what_source_establishes="Contemporaneous administrative records can test and reverse stigmatizing narratives about low-status members. Productivity, class, official-account participation, and elite status are not self-validating evidence of character or safety.",
        what_source_does_not_establish="It does not prove that no one exploited the community, capture informal exchange or intellectual work completely, assess dangerous conduct, or show that ledger contribution should determine moral worth.",
        author_interpretation="The author argues that inherited identities and incompatible visions, not simple malingering, better explain the experiment's end.",
        alternative_interpretation="The ledgers may miss precisely the informal work, concealment, quality differences, or interpersonal conduct that informed participants' judgments.",
        response_process="Retrospective audit of debits and credits against a longstanding blame narrative; no historical bad-actor adjudication is described.",
        outcome="The parasite explanation was not supported by the tested ledger patterns, and elite contributors were not materially superior by the same measure.",
        transferability="High for auditing admission, contribution, and expulsion labels with predeclared measures, comparable groups, complete records, and explicit measurement limits.",
        article_gap_status="D",
        likely_article_destination="Safety proxies / membership pipeline / math of absorption",
        confidence="high",
        external_verification_needed="yes",
        notes="An audit of a safety proxy, not a dangerous-person case. DOI: https://doi.org/10.9707/0739-1250.1456",
    ),
    finding(
        finding_id="F-088",
        track="Track A founder exception",
        source_record_id="M-0666",
        source_file="007-mary-baker-eddy-s-households-community-experiments-in-early-christian-science-history.pdf",
        journal_volume_issue_year="Vol. 28, no. 2 (2008)",
        article_title="Mary Baker Eddy's Households: Community Experiments in Early Christian Science History",
        author="Michael W. Hamilton",
        community_group="Mary Baker Eddy's Pleasant View household / Christian Science",
        page_locator="PDF pp. 6-7; printed pp. 63-64",
        printed_page_number="63-64",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="historical synthesis quoting the Church Manual",
        exact_factual_observation="Christian Science combined democratically governed branch churches with a self-perpetuating central board. A Church Manual bylaw required a three-year member, upon Eddy's written request, to report to her within ten days and serve for three consecutive years. Refusal, or departure without directors' consent, led to excommunication upon Eddy's complaint. Service paid $1,000 per year plus board; married helpers could be separated from spouses and children, though some couples served and some workers were released early.",
        what_source_establishes="A federal or democratic organizational form can coexist with a personalized founder exception that compels service through religious sanction and converts refusal or early exit into an offense.",
        what_source_does_not_establish="It does not state how often the bylaw was invoked or enforced, show legal compulsion beyond church sanction, establish that all service was involuntary, or prove abuse within the household.",
        author_interpretation="The author places the bylaw within Eddy's effort to train followers for continuity and notes both public criticism and the movement's democratic branch structure.",
        alternative_interpretation="Members may have regarded the paid service as a valued religious duty, and board consent plus early releases may have provided meaningful flexibility.",
        response_process="Founder request; ten-day reporting deadline; three-year duty; board consent for early release; excommunication initiated by founder complaint for refusal or unauthorized departure.",
        outcome="The household was staffed and used for leadership formation; the article does not enumerate refusals, sanctions, or individual later outcomes.",
        transferability="High for auditing founder-specific bylaws, compelled labor, family separation, refusal rights, term limits, and who can initiate sanctions.",
        article_gap_status="D",
        likely_article_destination="Founderism / non-waivable rights / labor and exit",
        confidence="high",
        external_verification_needed="yes",
        notes="Religious excommunication is not equated here with legal confinement. DOI: https://doi.org/10.9707/0739-1250.1455",
    ),
    finding(
        finding_id="F-089",
        track="Track A failed override and hidden authority",
        source_record_id="M-0669",
        source_file="010-review-of-the-order-of-the-solar-temple-the-temple-of-death.pdf",
        journal_volume_issue_year="Vol. 28, no. 2 (2008)",
        article_title="Review of The Order of the Solar Temple: The Temple of Death",
        author="Holly Folk",
        community_group="Order of the Solar Temple",
        page_locator="PDF pp. 2-4; printed pp. 96-98",
        printed_page_number="96-98",
        supporting_excerpt="",
        source_access="full text",
        evidence_type="book review summarizing a multi-author scholarly collection",
        exact_factual_observation="The Solar Temple operated through multiple names and shell organizations, with important information hidden from all but an inner circle. Luc Jouret was the visible Grand Master while Joseph Di Mambro held greater but less conspicuous authority. Jouret lost the title around 1990-1991, but the review says it is unclear whether Di Mambro accepted the ouster; Jouret retained close ties and formed a shadow organization. In 1994 the inner circle murdered some labeled traitors, drugged and shot others, and killed themselves; additional deaths followed in 1995 and 1997.",
        what_source_establishes="Formal removal from a visible title is not a tested override if hidden authority, personal networks, parallel organizations, information, and operational access remain intact.",
        what_source_does_not_establish="It does not establish that the failed removal caused the killings, resolve who acted willingly, identify a single trigger, describe an internal appeal, or correct discrepancies in the underlying edited volume.",
        author_interpretation="The reviewer emphasizes secrecy, layered authority, membership decline, external pressure, and unresolved social dynamics, while criticizing the underlying collection's gaps.",
        alternative_interpretation="The later violence may have arisen from changes after the title dispute that no formal override available in 1990 could reasonably have predicted or prevented.",
        response_process="Formal title removal; uncertain acceptance by hidden superior authority; continuing network ties and shadow organization; no transparent containment or evidence review described.",
        outcome="The network remained operative and later produced three episodes of murder-suicide totaling seventy-four deaths.",
        transferability="High in principle, but only moderate evidentially: removal must cut practical authority, assets, security access, communications, and parallel entities and must be independently verified.",
        article_gap_status="C",
        likely_article_destination="Founderism / tested override / evidence preservation",
        confidence="medium",
        external_verification_needed="yes",
        notes="Review-level evidence only. The teenage daughter and other children were victims, resisters, or escapees—not dangerous-child actors. DOI: https://doi.org/10.9707/0739-1250.1458",
    ),
    finding(
        finding_id="F-090",
        track="Track A child negative result",
        source_record_id="",
        source_file="Volumes 26-28 discovery corpus",
        journal_volume_issue_year="Volumes 26-28 (2006-2008)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volumes 26-28",
        page_locator="82 PDFs; 41 relevant or contextual close reads",
        printed_page_number="",
        supporting_excerpt="",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 82 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 41 relevant or contextual close reads found child victims and dependents, youth rebellion in aggregate, ordinary misconduct, a girl who admitted embellishing a religious performance, and fictional child cruelty or violence. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from this completed chunk under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 29-45, standalone sources, different terminology, unpublished records, book-length sources, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, fiction, aggregate reporting, and routing into education, medicine, juvenile law, family records, or memoir may hide cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volumes 26-28.",
        transferability="High for this chunk; none for the full literature until the remaining sources and standalone books are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="Adult actors near child terms, child victims, ordinary conduct, aggregate claims, and invented characters were excluded. The cumulative bounded null now covers volumes 1-28.",
    ),
]


CLOSE_READS = {
    "M-0598": "Context: founder censure, schism, and later repudiation of exit payments; F-078 carries the stronger separation sequence",
    "M-0599": "Context: a worker was sent away after secret sale of common goods and alcohol use, then readmitted; one opaque episode does not establish persistent danger or a review standard",
    "M-0600": "Promoted as F-078",
    "M-0601": "Source-method context: a disputed translation generated an extreme allegation, but no community danger-response process is documented",
    "M-0603": "Historiography and public-memory context; no internal danger-response case",
    "M-0604": "Promoted as F-077",
    "M-0605": "Founder-death primary-source context; F-079 and F-080 carry the distinct governance mechanisms",
    "M-0606": "Promoted as F-079 and F-080",
    "M-0611": "Property, withdrawal, and nonprofit-structure context; no distinct dangerous-actor sequence",
    "M-0612": "Bruderhof labor, migration, and leadership-crisis context; stronger existing findings already cover exit and contact control",
    "M-0613": "Gentle admonition and non-shunning context; no severe-conduct case or later outcome",
    "M-0615": "Open admission, founder conflict, poor capacity, and collapse corroboration; no distinct response process",
    "M-0616": "Admission-screening and contradictory need/credit criteria; no internal bad-actor response",
    "M-0617": "Promoted as source-method finding F-081; the child performer was not a dangerous actor",
    "M-0618": "Authority and individualism context; no materially distinct case",
    "M-0619": "Promoted with small-sample caution as F-082",
    "M-0620": "Applied-behavior-analysis social-validity principles are design context, not historical response evidence",
    "M-0622": "Failed-prediction and leader-health review context; already represented by stronger evidence",
    "M-0623": "Review-level Shaker overwork and possible suicide lead; insufficient process detail",
    "M-0627": "Verification lead: a compressed HIV-transmission and leadership-failure account lacks actor knowledge, process, and outcome detail",
    "M-0633": "Outsider and legal rhetoric about Amana; no direct internal response case",
    "M-0634": "Hopedale admission and elected-council context; no conduct-specific case or outcome",
    "M-0636": "Primary-observer context on Oneida criticism and refunds; stronger findings already carry the mechanisms",
    "M-0637": "Movement-authored Family tract; useful for source role and continuity claims, not independent evidence of reform",
    "M-0639": "Review-level Sufi succession and gift-economy context; no danger-response process",
    "M-0641": "Drop City memoir context; no materially distinct response process",
    "M-0648": "Promoted as F-083",
    "M-0649": "Promoted with access-dependence caution as F-084 and F-085",
    "M-0650": "Verification lead: Sandford medicine, flogging, death, arrest, and prison are compressed into a short secondary summary",
    "M-0654": "Child memoir context: outside visits and parent contact enabled comparison and exit; already represented by stronger child evidence",
    "M-0655": "Exit context: a leaver was materially unprepared and help-seeking was suppressed; corroborates existing findings",
    "M-0656": "Review-level allegation of ministerial power abuse; underlying memoir required before promotion",
    "M-0663": "Oneida sequence promoted as F-086; the article's Waco claims were not promoted",
    "M-0664": "Movement theology asserts supreme priestly authority but supplies no allegation-response process",
    "M-0665": "Explicit non-promotion: apparent dangerous-child and attack sequences are fictionalized; historical abuse leads require separate verification",
    "M-0666": "Promoted as F-088",
    "M-0667": "Promoted as F-087",
    "M-0668": "Review-level Mormon succession and schism context; no distinct override outcome",
    "M-0669": "Promoted at review-level confidence as F-089",
    "M-0672": "Catholic Worker post-founder review context; no specific danger-response process",
    "M-0674": "Strongly interpretive review of violence in Mormon history; insufficient case process for promotion",
}


GAP_REFS = {
    "G-001": ["F-077", "F-078", "F-082", "F-084", "F-086"],
    "G-003": ["F-081", "F-085", "F-089"],
    "G-004": ["F-079", "F-080", "F-082", "F-085", "F-088", "F-089"],
    "G-005": ["F-084", "F-088"],
    "G-007": ["F-081", "F-085", "F-089"],
    "G-008": ["F-077"],
    "G-009": ["F-084"],
    "G-010": ["F-083", "F-087"],
    "G-011": ["F-078", "F-086"],
    "G-012": ["F-077", "F-078"],
    "G-013": ["F-078", "F-082", "F-086", "F-089"],
    "G-014": ["F-083", "F-088"],
    "G-015": ["F-083"],
    "G-016": ["F-078", "F-079", "F-080"],
    "G-017": ["F-084"],
    "G-018": ["F-081", "F-082", "F-083", "F-084", "F-085", "F-087", "F-088", "F-089"],
}


GAP_ADDITIONS = {
    "G-001": " Neutral control of records, valuation, escrow, and disbursement is part of due process; a whole-tier purge or payment conditioned on stopping charges cannot replace case-level adjudication.",
    "G-003": " Multiple reports are not independent when generated, tested, edited, and approved inside one belief-and-authority chain, and a formal ouster is hollow if a shadow organization survives.",
    "G-004": " The practical override must also bind dead-founder texts, hidden networks, parallel entities, founder-only complaint powers, and final control of the evidence-policy channel.",
    "G-005": " Add freedom from founder-compelled service and family separation, with an unpunished right to refuse or end a role.",
    "G-007": " Outward consensus and broad consultation can coexist with a final personal veto, whole-unit penalties, and sanctions for dissent.",
    "G-008": " Support for a spouse or dependent must not be conditioned on returning to live and work under the institution that expelled the household member.",
    "G-009": " System-wide child rules and specialist boards are useful, but they do not replace case-level independent child advocacy, remedy, and outcome review.",
    "G-010": " Audit labels such as unsuitable, unworthy, lazy, or parasitic against site conditions and contemporaneous records, including whether high-status decision makers meet the same contribution standard.",
    "G-011": " Conciliation and settlement must not buy evidence suppression or substitute for victim support, offender accountability, and preserved outside reporting.",
    "G-012": " Exit accounting needs neutral escrow, common access to records, payer-independent disbursement, and rapid hardship relief while claims are disputed.",
    "G-013": " Outside punishment may address an unrelated offense, while a private settlement can end scrutiny without resolving internal accountability; map purpose as well as jurisdiction.",
    "G-014": " Opaque 'unsuitable or unworthy' classifications can shift structural failure onto low-voice residents, while paid religious service can still be compulsory through institutional sanction.",
    "G-015": " Diagnose soil, food, housing, manager competence, finance, and resident voice before attributing failure to member character or replacing residents.",
    "G-016": " A preexisting council can check a successor, but continuity also needs a way to amend dead-founder vetoes and a neutral process for financing a mass separation.",
    "G-017": " Written child education and health standards require independent implementation evidence and a route for children to report failures outside the authority chain.",
    "G-018": " Administrative records can reverse parasite narratives; whole-home compliance and externally assigned suitability are no more reliable as safety evidence than charisma or productivity.",
}


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames
    assert fields is not None
    assert rows and rows[75]["finding_id"] == "F-076", "Unexpected ledger base boundary"
    tail_ids = {r["finding_id"] for r in rows[76:]}
    expected_ids = {r["finding_id"] for r in NEW_FINDINGS}
    if tail_ids and tail_ids != expected_ids:
        raise RuntimeError(f"Unexpected findings after F-076: {sorted(tail_ids)}")
    rows = rows[:76] + NEW_FINDINGS
    for row in rows:
        missing = set(fields) - set(row)
        extra = set(row) - set(fields)
        if missing or extra:
            raise RuntimeError(f"Ledger schema mismatch for {row.get('finding_id')}: missing={missing}, extra={extra}")
    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def kind_of(row: dict[str, str]) -> str:
    m = re.search(r"(?:^|;)kind=([^;]+)", row["notes"])
    return m.group(1) if m else ""


def update_inventory() -> tuple[list[dict[str, str]], Counter[str]]:
    with INVENTORY.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames
    assert fields is not None and len(rows) == 1005
    metadata_kinds = {"front_matter", "contents", "table_of_contents", "editorial", "back_matter"}
    counts: Counter[str] = Counter()
    promoted = {r["source_record_id"] for r in NEW_FINDINGS if r["source_record_id"]}
    for row in rows:
        if row["volume"] not in {"26", "27", "28"}:
            continue
        kind = kind_of(row)
        if kind in metadata_kinds:
            status = "metadata triaged"
        elif row["record_id"] in promoted:
            status = "close read; finding promoted"
        elif row["record_id"] in CLOSE_READS:
            status = "contextual close read; no distinct finding"
        else:
            status = "title and keyword triaged"
        row["research_status"] = status
        row["text_extraction_status"] = "extracted"
        row["local_path"] = f"recovered/corpus-v26-v28/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v26-v28/{Path(row['internal_filename']).with_suffix('.txt').as_posix()}"
        counts[status] += 1
    if counts != Counter({
        "close read; finding promoted": 11,
        "contextual close read; no distinct finding": 30,
        "title and keyword triaged": 21,
        "metadata triaged": 20,
    }):
        raise RuntimeError(f"Unexpected volume 26-28 disposition counts: {counts}")
    with INVENTORY.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return rows, counts


def update_gap_bank() -> None:
    text = GAPS.read_text(encoding="utf-8")
    text = re.sub(r"Checkpoint: \*Communal Societies\* volumes 1-\d+", "Checkpoint: *Communal Societies* volumes 1-28", text, count=1)
    text = re.sub(
        r"After reconciling the volume \d+-\d+ findings rather than inflating the list,",
        "After reconciling the volume 26-28 findings rather than inflating the list,",
        text,
        count=1,
    )
    out = []
    for line in text.splitlines():
        m = re.match(r"\| (G-\d{3}) \|", line)
        if not m:
            out.append(line)
            continue
        gid = m.group(1)
        parts = line.split("|")
        if gid in GAP_ADDITIONS and GAP_ADDITIONS[gid].strip() not in parts[4]:
            parts[4] = parts[4].rstrip() + GAP_ADDITIONS[gid]
        parts[4] = parts[4].rstrip() + " "
        if gid in GAP_REFS:
            existing = [x.strip() for x in parts[7].split(",") if x.strip()]
            for ref in GAP_REFS[gid]:
                if ref not in existing:
                    existing.append(ref)
            parts[7] = " " + ", ".join(existing) + " "
        out.append("|".join(parts))
    text = "\n".join(out) + "\n"
    text = text.replace(
        "No volume 1-20 evidence validates six months of inner work as a reliable con-artist filter.",
        "No processed journal evidence through volume 28 validates six months of inner work as a reliable con-artist filter.",
    )

    verification = """
- **F status:** verify The Family International's child-abuse chronology, rule enforcement, police-raid outcomes, later official inquiries, and survivor accounts independently; the available article depends heavily on leadership access.
- **F status:** verify the Harmony and Oneida settlement sequences in underlying agreements, court files, and victim-centered records before presenting them as legal or safeguarding precedent.
- **F status:** verify the Kalalau identities, announced displacement plan, and park-court chronology; the article is a small first-person account and the prosecution concerned park offenses, not the internal proposal.
- **F status:** verify the Solar Temple authority network, formal ouster, shell organizations, and homicide chronology in primary investigations and later scholarship; the available source is a short review.
- **F status:** retrieve the underlying sources for the compressed Sandford child-medical-death and Anabaptist HIV-transmission accounts before using either as a case.
""".strip()
    marker = "- **F status:** verify The Family International's child-abuse chronology"
    if marker not in text:
        anchor = "\n## Explicit non-promotions\n"
        text = text.replace(anchor, "\n" + verification + "\n" + anchor, 1)

    old_child_null = "- The volume 1-25 dangerous-child searches (F-031, F-048, F-064, F-076) are bounded **F (needs more corpus coverage)** negative results, not evidence that intentional communities never faced or managed such children."
    new_child_null = "- The volume 1-28 dangerous-child searches (F-031, F-048, F-064, F-076, F-090) are bounded negative results, not evidence that intentional communities never faced or managed such children."
    text = text.replace(old_child_null, new_child_null)
    nonpromotions = """
- *The Family's Own Story* is a movement-authored hagiographic tract and is not independent evidence that the later governance system worked as claimed.
- The apparent child animal-torture, bullying, dagger attack, and arson sequence in the Harris article is explicitly fictionalized and cannot count as a dangerous-child case.
- The Hutterite ministerial-abuse review, the Anabaptist HIV case, and the Sandford medical and flogging summary lack the process detail required for promotion; they remain retrieval leads.
""".strip()
    marker = "- *The Family's Own Story* is a movement-authored"
    if marker not in text:
        text = text.rstrip() + "\n" + nonpromotions + "\n"
    else:
        text = text.rstrip() + "\n"
    while text.count(new_child_null) > 1:
        first = text.find(new_child_null)
        second = text.find(new_child_null, first + len(new_child_null))
        text = text[:second] + text[second + len(new_child_null) + 1 :]
    GAPS.write_text(text, encoding="utf-8")


def write_state() -> None:
    STATE.write_text(
        """# Communities Research State

Updated: 2026-08-12 (Africa/Dakar)

## Authority and mode

- Primary mode: **P0 research/source audit only**. No article prose has been edited.
- Research question: what intentional communities and small-scale/traditional societies actually did with dangerous, exploitative, persistently antisocial, or capture-seeking people, with a distinct branch for dangerous children.
- Article comparator: the two available final/published PDFs are byte-identical and their extracted text is identical. Raw Substack editor HTML is absent, so links, native objects, heading hierarchy, captions, and media placement are not authoritatively available.
- The difficult-child branch remains an empirical gap. Repeated bounded negative results are not evidence that intentional communities never faced or managed such children.

## Durable completed checkpoint

- *Communal Societies* volumes **1-28** are complete for title and keyword triage.
- **543 journal PDFs** were triaged: 140 close-read as relevant or contextual, 182 title/keyword-triaged, and 221 metadata-triaged.
- `COMMUNITIES-EVIDENCE-LEDGER.csv` contains **90 findings** (`F-001` through `F-090`). Volumes 26-28 added 14 findings: two B, seven C, four D, and one F-status bounded negative.
- `COMMUNITIES-ARTICLE-GAP-BANK.md` retains 18 reconciled article-gap items: 8 partially present, 7 apparently missing, and 3 challenges to the article.
- `COMMUNITIES-V26-V28-RESEARCH-REPORT.md` records the completed 82-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.
- The source inventory contains 1,005 records total: 984 journal PDFs, 3 archive manifests, and 18 Drive-level source/container records.
- All 984 journal PDFs have extracted text. Every one of the 82 volume 26-28 PDFs matched its inventoried SHA-256 hash, and all 82 new text extractions are nonempty.
- M-0398's pre-extracted text ended at printed page 107; printed pages 108-113 were inspected directly from the source PDF and the affected ledger row records that access path.

## Exact pending boundary

- Volumes **29-45** have not been processed: **441 journal PDFs**.
- The next bounded journal unit is volumes **29-30: 64 PDFs** in `vol29-30.zip`.
- Eight standalone Drive sources are inventoried but not yet represented by durable local text or close-read findings:
  1. *The Riddle of Amish Culture* (EPUB)
  2. *Alienation and Charisma*
  3. *Commitment and Community*
  4. *The Mountain People*
  5. *The !Kung San*
  6. Richard Wrangham, “Targeted conspiratorial killing, human self-domestication and the evolution of groupishness”
  7. `Zarpentinedissertation.pdf`
  8. *Evil Genes*
- The downloaded ZIPs are source containers, not additional substantive documents.

## Current evidence picture

- Adult/community-level evidence now includes ostracism, removal, punitive and unilateral expulsion, confinement to reduce self/other risk, leader and asset capture, crisis-driven expert dependency, dissent and apostate suppression, admission failure under cash pressure, evidence-channel monopoly, sanctions drifting into conformity enforcement, peer practice substituting for medicine, failed-prediction absorption, portable pension protection, civil recovery, arbitration, founder removal after factional violence, protected caucuses, reversible conflict trials, and shadow governance beneath formal democracy.
- Volumes 26-28 add: conduct-specific notice paired with confiscatory exit; a mass-separation settlement that failed without neutral accounting; a preexisting elected council that checked a successor; a dead founder's text acting as a later veto; insider evidence tests that lacked independence; an unadjudicated capture/displacement proposal in an open-access group; structural failure relabeled as member unworthiness; system-wide child-protection reform without case-level accountability; participatory procedure under a final prophetic veto; victim support and legal conciliation without stated offender accountability; ledger evidence reversing parasite labels; founder-compelled service inside a democratic form; and a formal ouster that left a shadow authority network intact.
- Existing evidence does **not** validate contribution, productivity, therapeutic fluency, long residence, cohesion, outward consensus, institutional survival, centralization, criminal history, poverty, distress, nonconformity, whole-home compliance, or an administrator's suitability label as safety proxies.
- Existing child-related evidence concerns exit capacity, peer-group power, education, medical neglect, unequal schooling, dissent rights, custody and contact conflict, broad adult punishment authority, collective childrearing, age-ordered adult sexual authority, non-inherited adult membership, punishment-centered compliance, and system-level safeguarding rules. It still does not answer how a community handled a child who remained gravely dangerous despite ordinary care and accountability.
- The strongest process contrast remains internal versus independent correction. Consultation, mediation, or settlement can be useful, but they do not substitute for independent evidence review, victim support, offender accountability, appeal, and outcome follow-up.
- Historical mental-health and legal sources are useful for locating mechanisms and gaps, but the DSM-IV-era framework and 1992 legal analysis require current authoritative verification before practical recommendations.
- Traditional-society evidence and intentional-community evidence must remain separate until a transfer argument is made. Execution, banishment, abandonment, policing, institutionalization, or state custody cannot be converted directly into a modern recommendation.

## Resume procedure

1. Do not repeat volumes 1-28.
2. Retrieve and verify `vol29-30.zip`; its 64 journal PDFs are the next exact bounded unit.
3. Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 64 extracted texts.
4. Close-read every source that may bear on admission, predation, violence, discipline, expulsion, ostracism, schism, grievance, child conduct, child protection, leader capture, dissent, reintegration, outside intervention, or outcome.
5. Append only materially distinct findings and preserve source access, what the source does not establish, alternative interpretation, process, outcome, transferability, and verification needs.
6. Reconcile findings into the existing 18-item gap bank; do not create a new gap merely for corroboration.
7. Process standalone sources as a separate evidence stream and mark source access exactly.
8. After each bounded unit, update this state file before further work.

## Stop conditions

- Do not draft or revise article prose without separate authorization.
- Do not diagnose historical actors as having ASPD or psychopathy unless a source establishes an appropriate clinical basis; describe conduct and mechanisms.
- Do not treat absence in search vocabulary as proof of absence.
- Do not import tribal killing, abandonment, banishment, policing, institutionalization, or state custody into a modern recommendation without legal, ethical, developmental, and practical transfer analysis.
""",
        encoding="utf-8",
    )


def md_escape(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")


def write_report(inventory_rows: list[dict[str, str]]) -> None:
    by_id = {r["record_id"]: r for r in inventory_rows}
    table = []
    for rid, disposition in CLOSE_READS.items():
        title = md_escape(by_id[rid]["article_title"])
        table.append(f"| {rid} | “{title}” | {disposition} |")
    close_table = "\n".join(table)
    REPORT.write_text(
        f"""# *Communal Societies* Volumes 26-28 Research Report

Checkpoint date: 2026-08-12 (Africa/Dakar)
Mode: P0 source audit only; no article prose edited

## Completion boundary

All **82 PDFs** in volumes 26-28 were processed:

- **41** relevant or contextual close reads
- **21** additional articles or reviews title- and keyword-triaged
- **20** front matter, contents, editorials, and back matter metadata-triaged

The cumulative journal boundary is now volumes 1-28: **543 PDFs**, comprising 140 close reads, 182 additional title/keyword triages, and 221 metadata triages. The evidence ledger contains **14 new findings, F-077 through F-090**: two B, seven C, four D, and one F-status bounded negative. Reconciliation did not create a new gap category; the article-gap bank still contains 18 material items, classified as 8 B, 7 C, and 3 D.

## Main result

This tranche shows why a community needs separate systems for evidence, immediate protection, accountability, fair separation, and governance override. A vote, settlement, purge, or formal title change can perform one of those functions while failing the others.

1. **Notice is not enough when exit confiscates everything.** Zoar used a standing committee and a conduct-specific notice inviting excuse, extenuation, and cause against expulsion. Yet rejecting the committee's judgment ended all membership rights, courts upheld zero exit equity, and a spouse's support depended on returning to live and work at Zoar. The process had recognizable form but a materially coercive consequence. (F-077)
2. **Exit payments need neutral control before desperation becomes a safety event.** Harmony's installment settlement with mass seceders broke down over deductions, releases, payment, and access to records. A large delegation with mixed motives arrived, violence was alleged on both sides, the militia intervened, and the trial never occurred. Neutral valuation, shared records, escrow, and hardship relief are part of conflict prevention. (F-078)
3. **A preexisting elected body can check a successor without destroying the office.** After George Rapp died without a succession plan, an elected Council of Elders expanded its authority and rebuked Jacob Henrici when he tried to rule absolutely. He accepted the rebuke and remained minister. That is a rare positive example of a practical override. (F-079)
4. **The founder can keep vetoing after death.** An 1854 inspired testimony against dissolution helped block Amana constitutional revision in 1919. The 1932 Great Change finally separated the business and religious sides, preserving the spiritual institution while making economic reorganization possible. Amendment tests must include founding texts, not only living officeholders. (F-080)
5. **Multiple witnesses are not independent when they share the same signal and judge.** Shaker leaders compared separate visions, used a committed believer to test them, circulated his demonstration, discouraged doubt, and interpreted an admitted embellishment through the same disputed spiritual channel. Later contradiction and disruption required restriction. The lesson is about evidence independence, not whether every reported vision was false. (F-081)
6. **An open gate can leave the group without an answer to a capture proposal.** A Kalalau member announced that thirty allies would come and later said only Hawaiians could live in his intended community, relegating current residents to visitors. The informal leader relied on personal assurance and impracticality because the group had no exclusion authority or decision forum. External law acted on park violations, not the internal proposal. (F-082)
7. **Structural failure can be mislabeled as bad members.** At Southport, outsiders controlled money, selection, management, and forty-one intrusive rules while residents faced poor soil, food shortage, bad housing, and weak management. Fourteen families left or were expelled as “unsuitable or unworthy” and were replaced; communalism then ended. The source cannot say which exits were justified, but it shows why suitability labels must be audited against system conditions. (F-083)
8. **System reform is necessary and still not case accountability.** The Family responded to abuse in an appointed hierarchy by firing the entire tier and later electing local shepherds. It prohibited adult-minor sexual contact under banishment and adopted a legally reviewed, member-consulted Charter with child-health, education, and age rules. The source supplies no allegation-to-assessment cases, victim repair, or independent enforcement audit. (F-084)
9. **Participation can be real while the veto remains personal.** The Family used boards, editors, councils, votes, and many prophecy channels, but Maria set topics and retained final approval; conflict was typically muted into outward consensus, dissenters were purged, and whole homes could be downgraded. Even this sympathetic source concludes that divine authority overrode democracy. (F-085)
10. **Conciliation can support a victim and still evade offender accountability.** After a Oneida member severely whipped his mentally ill wife, her father's indictment produced asylum payment and a continuing stipend. Later, the community paid the complainant for a discharge and help stopping more indictments, then resumed its practices. No internal consequence for the person who used the violence is described. (F-086)
11. **Records can overturn the parasite story.** New Harmony ledgers did not support the familiar claim that low-skilled or local members consumed without contributing; locally rooted participants contributed heavily, and constitutional-committee elites contributed about half the average while consuming near it. The records have limits, but they demonstrate how to test stigmatizing labels rather than treating productivity or class as safety evidence. (F-087)
12. **Democratic branches do not cure a founder-only exception.** Mary Baker Eddy's church combined democratically governed branches with a bylaw requiring selected members to report within ten days and serve her for three years; refusal or early departure without consent triggered excommunication on her complaint. Formal structure and personalized compulsion coexisted. (F-088)
13. **Removing the visible title is not an override if the shadow network survives.** A review of the Solar Temple literature reports that Luc Jouret lost the Grand Master title while retaining ties and forming a parallel organization under a less visible superior authority. The later murder-suicides cannot be causally reduced to that failed ouster, but the case demonstrates why practical authority, information, security access, and shell entities must be disabled and checked. (F-089)

## Dangerous-child result

The separate child-as-dangerous-actor search covered every extracted text in the 82-PDF unit. Discovery counted six substantive term families—danger, sanction, governance, child, exit, and clinical—and five process families—allegation, assessment, intervention, review, and outcome. It then inspected child-danger terms in proximity and close-read all plausible sources. The score (`danger × 3 + sanction × 2 + governance + child + exit + clinical × 3`) prioritized reading; it was not treated as evidence weight.

The apparent child hits resolved into other categories:

- Family International material concerned children as victims, dependents, members governed by later rules, or an aggregate “youth rebellion,” not a case-level dangerous child.
- Solar Temple children and teenagers were killed, assigned a spiritual role, resisted, or escaped; they were not the dangerous actors.
- Waco and Oneida passages concerned adult actors and child victims or bystanders.
- A Shaker girl admitted embellishing a religious performance and another young person was physically restrained during worship; neither source documented persistent dangerous conduct or the required sequence.
- In the Harris article, a child who tortured animals and bullied and the later dagger and fire plot were explicitly fictionalized. Historical child-separation and punishment claims remain verification leads.
- Other hits concerned ordinary school discipline, child labor, babies and dependents, adult conflict near child terms, metaphor, bibliography, or OCR proximity.

No source documented the requested sequence: **a persistently dangerous child as actor → allegation → assessment → intervention → review → later outcome**. F-090 records a bounded null for volumes 26-28. Together with F-031, F-048, F-064, and F-076, it extends the completed journal null through volume 28 without converting it into a historical claim of absence.

## Close-read disposition

| Record | Source | Disposition |
|---|---|---|
{close_table}

## Extraction, discovery, and source cautions

- The `vol26-28.zip` SHA-256 matched the inventory value `5ccad3867f4b8c8fc628074099f70745f85fbc555c65052b1aa85ca2d1159e29`; the ZIP integrity test passed. All 82 PDF hashes matched, all 82 `pdftotext -layout` outputs are nonempty, and there are no missing source PDFs.
- Discovery ranking covered all 82 files. The vocabulary is broader than the previous tranche's child-only pairing, so raw hit and score counts should not be compared across reports as if they were a stable measurement scale.
- M-0649 is unusually dependent on access to current Family leaders, homes, headquarters staff, and movement publications. Its mixed account is useful, but its characterization of critics and its claim that raids found no evidence require independent legal, official, and survivor-centered verification.
- M-0663 is strongly polemical in its Waco analysis. Only the more document-specific Oneida sequence was promoted, and even that needs underlying primary and victim-centered review.
- M-0619 is a small first-person account of an informal group. Its capture-proposal finding is medium-confidence and does not establish imminent violence.
- M-0669 is a four-page book review that itself identifies unresolved discrepancies in the underlying edited collection. It supports a shadow-authority mechanism at medium confidence, not a complete causal history of the killings.
- M-0648 groups people who left with people who were expelled. The ledger preserves that ambiguity and does not infer misconduct from the label “unsuitable or unworthy.”
- Historical conduct is described without retrospective psychiatric diagnosis. Terms such as mentally ill, dissident, unsuitable, unworthy, traitor, or parasite are attributed to sources or analyzed as labels, not adopted as neutral safety categories.

## Next exact boundary

The next journal unit is **volumes 29-30: 64 PDFs** in `vol29-30.zip`. Volumes 29-45 contain **441 pending PDFs** in total. Eight standalone Drive sources remain a separate pending evidence stream.
""",
        encoding="utf-8",
    )


def main() -> None:
    update_ledger()
    inventory_rows, _ = update_inventory()
    update_gap_bank()
    write_state()
    write_report(inventory_rows)
    print("updated ledger, inventory, gap bank, state, and volumes 26-28 report")


if __name__ == "__main__":
    main()
