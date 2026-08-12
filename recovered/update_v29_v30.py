#!/usr/bin/env python3
"""Apply the completed volumes 29-30 checkpoint to the durable CSV artifacts."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"


def finding(**values: str) -> dict[str, str]:
    fields = [
        "finding_id",
        "track",
        "source_record_id",
        "source_file",
        "journal_volume_issue_year",
        "article_title",
        "author",
        "community_group",
        "page_locator",
        "printed_page_number",
        "supporting_excerpt",
        "source_access",
        "evidence_type",
        "exact_factual_observation",
        "what_source_establishes",
        "what_source_does_not_establish",
        "author_interpretation",
        "alternative_interpretation",
        "response_process",
        "outcome",
        "transferability",
        "article_gap_status",
        "likely_article_destination",
        "confidence",
        "external_verification_needed",
        "notes",
    ]
    row = {field: "" for field in fields}
    row.update(values)
    return row


NEW_FINDINGS = [
    finding(
        finding_id="F-091",
        track="Track A capture-seeking label and adjudication",
        source_record_id="M-0683",
        source_file="008-the-communal-wanderings-of-august-jacobi.pdf",
        journal_volume_issue_year="Vol. 29, no. 1 (2009)",
        article_title="The Communal Wanderings of August Jacobi",
        author="Peter Hoehnle",
        community_group="Community of True Inspiration at Ebenezer",
        page_locator="PDF p. 4; printed p. 43",
        printed_page_number="43",
        source_access="full text",
        evidence_type="historical reconstruction using journals, a private memorandum, and a membership record",
        exact_factual_observation="August Jacobi arrived in July 1851, was accepted on probation, and was appointed in November to teach English to young male members. Six months later the elders expelled him after what the membership record called a 'Godly disclosure.' Leaders described a false and proud heart, disobedience, deception, slyness, and a ravenous wolf, but the author states that the 'trouble' prompting expulsion is not recorded in Ebenezer or Amana sources. The author's suggestion that Jacobi may have sought influence or power is expressly speculative.",
        what_source_establishes="Probation, useful service, and confident insider labels can coexist with a record that never identifies the alleged conduct. A capture-seeking or deception label is not itself a conduct-specific allegation, evidentiary finding, or reviewable reason.",
        what_source_does_not_establish="It does not prove Jacobi was innocent, identify what he did, show what evidence the elders possessed, document notice or reply, or establish that he attempted to capture the community.",
        author_interpretation="The author emphasizes the archival silence about the trouble and cautiously proposes an attempted search for influence or power as one possibility.",
        alternative_interpretation="Serious conduct may have been known to contemporaries but omitted for privacy, theological convention, or archival loss; the expulsion may therefore have been justified even though the surviving record cannot show it.",
        response_process="Probation; teaching appointment; elder assessment framed as spiritual disclosure; expulsion. No conduct-specific notice, member reply, recusal, or appeal is described.",
        outcome="Jacobi left Ebenezer after expulsion and continued his communal travels; the source records no internal review or later correction of the labels.",
        transferability="High for requiring conduct-specific allegations, preserved evidence, reply, and appeal before treating deception, infiltration, or capture language as an adjudicated fact.",
        article_gap_status="C",
        likely_article_destination="Membership pipeline / fair separation / capture-seeking test",
        confidence="high",
        external_verification_needed="yes",
        notes="High confidence in the documented opacity, not in any underlying allegation. DOI: https://doi.org/10.9707/0739-1250.1408",
    ),
    finding(
        finding_id="F-092",
        track="Track A materially usable exit",
        source_record_id="M-0681",
        source_file="006-community-sustainability-the-challenge-of-intergenerational-change.pdf",
        journal_volume_issue_year="Vol. 29, no. 1 (2009)",
        article_title="Community Sustainability: The Challenge of Intergenerational Change",
        author="Peter H. Cock",
        community_group="Moora Moora Cooperative Community",
        page_locator="PDF pp. 7-8; printed pp. 28-29",
        printed_page_number="28-29",
        source_access="full text",
        evidence_type="first-person organizational reflection by an original participant",
        exact_factual_observation="Moora Moora created a loan scheme for share and house purchases and guaranteed that the community would buy out a departing member after a two-year wait. The author says credit-union funding was available but expensive, the community had placed the interests of entrants ahead of leavers, and the amount returned on leaving was not commensurate with the cost of moving elsewhere.",
        what_source_establishes="A formal buyout promise and nominal permission to leave do not make exit materially usable when the delay, valuation, and liquidity leave a member unable to rehouse elsewhere.",
        what_source_does_not_establish="It supplies no contract text, amounts, valuation method, completed payout example, hardship case, default rate, or later reform outcome.",
        author_interpretation="The author treats the loan and guarantee as progress that deliberately makes entry and exit easier but not too easy, while acknowledging unresolved equity.",
        alternative_interpretation="A waiting period and discounted payout may be necessary to prevent a common estate from being destabilized by turnover; the unresolved question is whether that collective need is paired with a viable transition for the leaver.",
        response_process="Entry financing; guaranteed community buyout; two-year wait; costly external credit; no neutral valuation, escrow, hardship bridge, or accelerated safety exit is described.",
        outcome="The mechanism existed, but the author reported that joining was cheap relative to common assets and leaving remained expensive relative to relocation.",
        transferability="High for testing exit deadlines, valuation sufficiency, liquidity, hardship relief, household needs, and funding independence rather than counting a buyout clause alone.",
        article_gap_status="C",
        likely_article_destination="Children's outward door / money and land / fair separation",
        confidence="high",
        external_verification_needed="yes",
        notes="The source describes policy from an insider perspective rather than auditing completed payouts. DOI: https://doi.org/10.9707/0739-1250.1406",
    ),
    finding(
        finding_id="F-093",
        track="Track A conflict timing and mediation",
        source_record_id="M-0681",
        source_file="006-community-sustainability-the-challenge-of-intergenerational-change.pdf",
        journal_volume_issue_year="Vol. 29, no. 1 (2009)",
        article_title="Community Sustainability: The Challenge of Intergenerational Change",
        author="Peter H. Cock",
        community_group="Moora Moora Cooperative Community",
        page_locator="PDF pp. 10-11; printed pp. 31-32",
        printed_page_number="31-32",
        source_access="full text",
        evidence_type="first-person organizational reflection by an original participant",
        exact_factual_observation="Moora Moora employed an outside facilitator whose approach was a circle or 'go around' to learn how members and groups saw current conflicts. The author reports that mediation was difficult once conflict had exploded and supporters reinforced opposing camps. When significant conflict remained unresolved, members eventually left; rebuilding consumed finite time, energy, and friendships.",
        what_source_establishes="The existence of an outside mediator is not enough if the route activates only after factional identities and informal reinforcement have hardened. Timing and pre-crisis legitimacy are part of the mechanism.",
        what_source_does_not_establish="It does not describe one complete dispute, facilitator selection, confidentiality, recommendations, compliance, comparative outcomes, or whether earlier mediation would have prevented departures.",
        author_interpretation="The author sees unresolved conflict as both a sustainability threat and a recurring drain on a community that can rebuild only so many times.",
        alternative_interpretation="Some conflicts may have reflected irreconcilable priorities for which departure was an appropriate outcome; the circle process may have surfaced differences even if it did not reconcile them.",
        response_process="Outside facilitator; cooperative-wide circle; late-stage mediation after escalation; no specified early trigger, binding follow-up, or route around a conflicted leader is described.",
        outcome="Some unresolved conflicts ended in member exits and costly rebuilding; the source does not quantify or compare cases.",
        transferability="High in principle for selecting and normalizing an outside route at formation, defining early triggers, and following outcomes; moderate as case evidence because the account is aggregate.",
        article_gap_status="C",
        likely_article_destination="Conflict architecture / outside mediation",
        confidence="medium",
        external_verification_needed="no",
        notes="This is an experienced participant's aggregate process account, not a controlled comparison. DOI: https://doi.org/10.9707/0739-1250.1406",
    ),
    finding(
        finding_id="F-094",
        track="Track A protected reporting and scoped outside response",
        source_record_id="M-0699",
        source_file="006-marie-ogden-and-the-home-of-truth-a-millennial-prophet-and-the-life-and-decline-of-her-community.pdf",
        journal_volume_issue_year="Vol. 29, no. 2 (2009)",
        article_title="Marie Ogden and the Home Of Truth: A Millennial Prophet and the Life and Decline of her Community",
        author="Bradley C. Whitsel",
        community_group="Home of Truth",
        page_locator="PDF pp. 17-20; printed pp. 40-43",
        printed_page_number="40-43",
        source_access="full text",
        evidence_type="historical synthesis using regional press and movement records",
        exact_factual_observation="Edith Peshak died of cancer in February 1935 after she and her husband joined in hope that Marie Ogden could cure her. For four months Ogden denied death to residents and used washings, forced feedings, and laying on of hands on the corpse while seeking resurrection. Information of unknown origin reached the sheriff as many members departed. Officials inspected the mummified remains and reported no obvious health risk requiring burial. Ogden then restricted outsider contact. In 1937 authorities and Peshak's adult son demanded a death certificate; a recent defector alleged that Ogden had secretly ordered cremation in 1935 so colonists would not know. Ogden did not answer that allegation but signed the certificate to avoid possible prosecution. Authorities did not require disclosure of the remains or further response. Roughly fifteen loyal members remained and the failed resurrection was reframed spiritually.",
        what_source_establishes="An outside truth boundary may depend on a protected insider route, and each agency intervention has a limited purpose. Inspection and correction of a legal record can leave evidence preservation, body disposition, internal disclosure, and community accountability unresolved.",
        what_source_does_not_establish="It does not show that medical treatment was denied before death, identify the person who first reported, prove the alleged cremation, establish a prosecutable offense, or show what fuller intervention was legally authorized at the time.",
        author_interpretation="The author links the affair to mass departure, loss of confidence, prophetic disconfirmation, and the community's decline, while noting uncertainty about the precise reasons members left.",
        alternative_interpretation="Officials may reasonably have stopped when no immediate health risk or burial requirement applied; remaining members may have sincerely accepted Ogden's theology rather than simply being coerced.",
        response_process="Internal concealment and ritual treatment of the corpse; possible insider report; sheriff investigation and inspection; leader-imposed isolation; later defector allegation; renewed official and family demand; prosecution pressure; death-certificate compliance; no reported inquiry into the allegation or body location.",
        outcome="Death was formally recorded, but the location and disposition of the remains remained unresolved in the account. Most members left; a small loyal group continued under a revised spiritual explanation.",
        transferability="High for predefining confidential reporting, records preservation, agency handoffs, purpose and stopping rules, and follow-up when one outside actor resolves only one part of a safety event.",
        article_gap_status="C",
        likely_article_destination="Outside reporting / evidence preservation / legal and medical couplings",
        confidence="high",
        external_verification_needed="yes",
        notes="The cremation and source of the initial leak remain allegations or inferences. No pre-death medical-neglect finding is made. DOI: https://doi.org/10.9707/0739-1250.1424",
    ),
    finding(
        finding_id="F-095",
        track="Track A tested constitutional override",
        source_record_id="M-0700",
        source_file="007-the-ongoing-shaker-covenant.pdf",
        journal_volume_issue_year="Vol. 29, no. 2 (2009)",
        article_title="The Ongoing Shaker Covenant",
        author="Stephen J. Paterwic",
        community_group="United Society of Believers / Shakers",
        page_locator="PDF pp. 3-7; printed pp. 64-68",
        printed_page_number="64-68",
        source_access="full text",
        evidence_type="corrective historical argument using covenants, ministry minutes, correspondence, and legal records",
        exact_factual_observation="Shaker covenants were read to members and revisions required their signatures or approval. A general revision proposed by ministry member Giles Avery in 1877 was never adopted. The 1957 amendments allowed the Ministry to close a society and dispose of its property, assets, and personnel only with approval of the affected membership; Eldress Emma King obtained written approvals. In 1963 King withheld central approval for Sabbathday Lake admissions but wrote that the local community could proceed on its own responsibility. The author argues that the Ministry lacked power to close the Covenant and that the local admission route remained open.",
        what_source_establishes="A practical constitutional override can include an accessible and periodically reread governing document, affected-member assent, a documented failed leader-proposed amendment, and a subordinate body's ability to proceed despite central disapproval.",
        what_source_does_not_establish="It does not show that every signature was independent or informed, test the covenant in a safety allegation, establish equal voice, or prove that the author's contested correction of the closure narrative is the only interpretation.",
        author_interpretation="The author seeks to correct the repeated claim that King closed Shaker membership and argues from the covenant and governance record that she lacked unilateral authority.",
        alternative_interpretation="The article says King expected unquestioning obedience, so formal written assent may not equal independent consent; practical deference and legal authority may also have diverged.",
        response_process="Annual or periodic reading; member signatures; failed 1877 proposal; affected-member approval for 1957 closure and asset powers; local option to reject central advice on admissions.",
        outcome="The 1877 revision failed, the 1957 amendments passed with written approvals, and Sabbathday Lake continued admitting members despite the Ministry's refusal to endorse the plan.",
        transferability="High for testing amendment and override clauses against actual leaders, requiring affected-member approval, preserving local refusal, and keeping governing texts inspectable.",
        article_gap_status="B",
        likely_article_destination="Founderism / tested override / amendment and branch rights",
        confidence="high",
        external_verification_needed="yes",
        notes="Positive mechanism with a consent caveat; the article is an advocacy-style correction grounded in cited primary records. DOI: https://doi.org/10.9707/0739-1250.1425",
    ),
    finding(
        finding_id="F-096",
        track="Track A capture-seeking entity design",
        source_record_id="M-0702",
        source_file="009-our-land-rodger-mcafee-and-his-life-long-quest-for-community-in-america.pdf",
        journal_volume_issue_year="Vol. 29, no. 2 (2009)",
        article_title="Our Land: Rodger McAfee and His Life-Long Quest for Community in America",
        author="Morgan E. Bowen",
        community_group="Our Land",
        page_locator="PDF pp. 29-31 and 35; printed pp. 108-110 and author's note",
        printed_page_number="108-110",
        source_access="full text",
        evidence_type="sympathetic reflection based primarily on founder interviews, with selected press and record corroboration",
        exact_factual_observation="After earlier cooperative efforts failed and during a long foreclosure conflict, Rodger McAfee described an evolving three-part design: a perpetual farmland trust whose assets could not be indebted or sold, an Our Land cooperative community, and a Unifam religious organization. He explicitly presented religious organization as a means of membership control and exclusion, saying it would let him remove people he perceived as secret agents. The article does not show that this church structure was created or used. An author's note reports that after McAfee's death the federal government foreclosed on the farm and corporate assets, while Our Land Corporation retained eighty acres elsewhere under his son's presidency.",
        what_source_establishes="Entity form, a land lock, and spiritual language can be proposed partly to increase a founder's power to classify and exclude perceived infiltrators. The reason a protective legal structure is chosen is itself an anti-capture audit question.",
        what_source_does_not_establish="It does not validate McAfee's legal claims about churches, show that perceived agents existed, establish incorporation or implementation of Unifam, show an expulsion case, or prove that the proposed structure caused foreclosure or would have prevented it.",
        author_interpretation="The author treats McAfee as a compelling visionary and friend but explicitly leaves the veracity of much of his story to the reader and says the account remains primarily McAfee's own perspective.",
        alternative_interpretation="McAfee had experienced real political and foreclosure conflict and may have sought a sincere spiritual community plus legitimate defenses against disruption; a properly governed trust can protect common land without concentrating adjudicatory power.",
        response_process="Proposed perpetual trust; proposed cooperative; proposed religious membership gate and expulsion power based on founder perception. No independent board, conduct threshold, evidence test, notice, or appeal is described.",
        outcome="The contemplated exclusion system is not shown in operation. The main farm and assets were later foreclosed; a separate eighty-acre parcel remained with the corporation for another farming group.",
        transferability="High as a capture-seeking design test: audit the purpose, operator, evidence standard, legal review, independent board, and whether trust or entity powers bind the founder and security actors.",
        article_gap_status="D",
        likely_article_destination="Money and land / founderism / capture test",
        confidence="medium",
        external_verification_needed="yes",
        notes="The finding is limited to self-described intent and proposed design. It does not adopt McAfee's statutory claims or allegations of infiltration. DOI: https://doi.org/10.9707/0739-1250.1427",
    ),
    finding(
        finding_id="F-097",
        track="Track A failed incapacity override and dissent route",
        source_record_id="M-0701",
        source_file="008-seeing-the-faces.pdf",
        journal_volume_issue_year="Vol. 29, no. 2 (2009)",
        article_title="Seeing the Faces",
        author="Laura Kohl Johnston",
        community_group="Peoples Temple / Jonestown",
        page_locator="PDF pp. 7-9; printed pp. 78-80",
        printed_page_number="78-80",
        source_access="full text",
        evidence_type="retrospective first-person survivor account",
        exact_factual_observation="Johnston reports that discussion of Jim Jones's deteriorating physical and mental health was taboo. When members tried to establish a triumvirate to succeed him in governing Jonestown, Jones flatly refused. Rumors of unhappiness or unwillingness to stay triggered public confrontation. About twenty defectors left with Congressman Leo Ryan on November 18, 1978; Johnston says Jones had concealed personal information and then coerced residents toward mass death. She survived because she had been assigned to Georgetown and later reconstructed the last day through survivor conversations and researchers she trusted.",
        what_source_establishes="A succession or incapacity safeguard that the leader can refuse is not an override. Health concerns, dissent, and contemplated exit require a confidential route outside the leader's information and sanction system.",
        what_source_does_not_establish="It does not show the proposed triumvirate's membership, authority, independence, or likely effectiveness, and it cannot establish that accepting it would have prevented the murders and deaths. It is retrospective and partly reconstructs events the author did not witness.",
        author_interpretation="The survivor presents leader isolation, paranoia, concealed facts, coercion, and hostility to defection as part of the final collapse while emphasizing the humanity and constructive work of many members.",
        alternative_interpretation="The rejected triumvirate may itself have been insufficient, and the catastrophe involved multiple operational, political, and psychological conditions beyond the failed succession proposal.",
        response_process="Member-proposed triumvirate; unilateral leader refusal; taboo on incapacity discussion; public confrontation of rumored dissent; physical exit by a group of defectors; no independent review or non-retaliation route described.",
        outcome="The override did not activate. The defectors' departure coincided with the final crisis and mass deaths; surviving members later built mutual support, memorial, and public-education work.",
        transferability="High for making incapacity and replacement mechanisms non-waivable, independently triggered, confidential, and operational before a leader controls information and exit.",
        article_gap_status="C",
        likely_article_destination="Founderism / incapacity override / protected dissent and exit",
        confidence="medium",
        external_verification_needed="yes",
        notes="Do not reduce the Jonestown catastrophe causally to the refused triumvirate. DOI: https://doi.org/10.9707/0739-1250.1426",
    ),
    finding(
        finding_id="F-098",
        track="Track A succession practice and adaptive override",
        source_record_id="M-0726",
        source_file="004-dissolution-as-an-act-of-creation-the-koreshan-unity.pdf",
        journal_volume_issue_year="Vol. 30, no. 2 (2010)",
        article_title="Dissolution as an Act of Creation: The Koreshan Unity",
        author="Lynn Rainard",
        community_group="Koreshan Unity",
        page_locator="PDF pp. 14-23; printed pp. 13-22",
        printed_page_number="13-22",
        source_access="full text",
        evidence_type="historical synthesis using community archives, publications, correspondence, and newspapers",
        exact_factual_observation="Cyrus Teed's rules required his and Victoria Gratia's consent for changes, but he routinely disregarded the formal structure and kept Gratia traveling with him, limiting her chance to develop independent leadership. After his death no single voice controlled the response, members guarded his body, factions hardened, and members left. Gratia's earlier failure during a coal, illness, and cash crisis and her later inability to resolve food and creditor problems undermined confidence. After she left and married, directors removed her, redirected payments to Estero, and elected James Bubbett board president with George Hunt's support. The majority reinterpreted central founder doctrine, while dissidents and exiles continued other versions. The reorganized settlement then experienced a comparatively stable period despite long-run decline.",
        what_source_establishes="A named successor is not resilience when the founder prevents delegated practice. A workable transition may require independent control of contributions, board election, authority to remove a successor, capacity to amend founder doctrine, and room for dissenting continuities.",
        what_source_does_not_establish="It does not show that Gratia's removal was procedurally fair, free of factional or sex bias, justified as a safety measure, or approved by all members; later stability does not establish autonomy or overall wellbeing.",
        author_interpretation="The author argues that partial dissolution through departure, doctrinal redefinition, and organizational reshaping can be creative and can extend communal life.",
        alternative_interpretation="The directors may have used crisis and Gratia's marriage to rationalize a factional seizure, while doctrinal reinterpretation protected loyalty to Teed more than independent governance.",
        response_process="Unpracticed designated succession; post-death factional conflict; noncompliance and departure; director removal of successor; redirection of contribution flows; board election; doctrinal amendment; continuing dissident branches.",
        outcome="The immediate succession plan failed, but a board-led reorganization and revised doctrine produced a more stable period. Membership later declined and rival interpretations persisted.",
        transferability="High for requiring real delegated practice before succession, independent board and financial powers, a tested removal route, amendment authority, and a non-punitive way for dissenters to fork.",
        article_gap_status="B",
        likely_article_destination="Founderism / succession / continuity and adaptive dissolution",
        confidence="high",
        external_verification_needed="yes",
        notes="A positive adaptability mechanism with serious procedural and bias caveats; it is not a dangerous-actor adjudication. DOI: https://doi.org/10.9707/0739-1250.1387",
    ),
    finding(
        finding_id="F-099",
        track="Track A supported household exit",
        source_record_id="M-0732",
        source_file="010-review-of-nightwatch-an-inquiry-into-solitude-alone-on-the-prairie-with-the-hutterites.pdf",
        journal_volume_issue_year="Vol. 30, no. 2 (2010)",
        article_title="Review of Nightwatch: An Inquiry into Solitude: Alone on the Prairie with the Hutterites",
        author="Peter Hoehnle",
        community_group="Starland Hutterite colony",
        page_locator="PDF p. 3; printed p. 122",
        printed_page_number="122",
        source_access="full text",
        evidence_type="book review summarizing a former member's memoir",
        exact_factual_observation="The review says Robert Rhodes, his wife, and their three children left Starland because of internal spiritual turmoil and concern for their daughters under traditional constraints. The colony gave the family a vehicle and money to begin outside, and the senior minister gave Rhodes what the reviewer calls a unique and likely unprecedented blessing as a Hutterite brother-at-large.",
        what_source_establishes="A constructive exit can combine material runway for the whole household with permission to retain a durable, non-governing affiliation rather than requiring relational erasure.",
        what_source_does_not_establish="It gives no amounts, terms, timing, eligibility rule, independent verification, experience of the daughters, or later material and relational outcomes, and it does not show that other leavers received the same support.",
        author_interpretation="The reviewer treats the memoir as unusually balanced and the supported departure as evidence that it is not a harsh critique of colony life.",
        alternative_interpretation="The support may have been discretionary and exceptional rather than a right, and the blessing may not have preserved practical contact or belonging.",
        response_process="Family decision to leave; colony-provided vehicle and money; senior minister's continuing-affiliation blessing. No adjudication, appeal, or standardized exit protocol is described.",
        outcome="The family began life outside with material help and symbolic continuing affiliation; the review supplies no later follow-up.",
        transferability="Moderate but promising for household-scale transition support, explicit alumni status, protected contact, and exit assistance that is not conditioned on return.",
        article_gap_status="B",
        likely_article_destination="Children's outward door / fair separation / relational continuity",
        confidence="medium",
        external_verification_needed="yes",
        notes="Review-level evidence and apparently exceptional practice; retrieve the memoir before treating it as a replicable policy. DOI: https://doi.org/10.9707/0739-1250.1393",
    ),
    finding(
        finding_id="F-100",
        track="Track A child negative result",
        source_file="Volumes 29-30 discovery corpus",
        journal_volume_issue_year="Volumes 29-30 (2009-2010)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volumes 29-30",
        page_locator="64 PDFs; 30 relevant or contextual close reads",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 64 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 30 relevant or contextual close reads found children as victims, dependents, students, objects of ordinary adult discipline, pressured spiritual figures, or relatives near adult conflict. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from this completed chunk under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 31-45, standalone sources, different terminology, unpublished records, book-length sources, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, aggregate reporting, and routing into education, medicine, juvenile law, family records, or memoir may hide cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volumes 29-30.",
        transferability="High for this chunk; none for the full literature until the remaining journal and standalone sources are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="Child victims, dependents, ordinary discipline, childhood biography, adult conflict near child terms, and review-level speculation were excluded. The cumulative bounded null now covers volumes 1-30.",
    ),
]


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames == list(NEW_FINDINGS[0]), "ledger schema changed"
    expected_tail = [f"F-{number:03d}" for number in range(91, 101)]
    if len(rows) == 100 and [row["finding_id"] for row in rows[-10:]] == expected_tail:
        rows = rows[:90]
    assert len(rows) == 90 and rows[-1]["finding_id"] == "F-090", "unexpected ledger checkpoint"
    all_rows = rows + NEW_FINDINGS
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)


CLOSE_IDS = {
    "M-0681", "M-0682", "M-0683", "M-0684", "M-0686", "M-0687",
    "M-0689", "M-0691", "M-0697", "M-0698", "M-0699", "M-0700",
    "M-0701", "M-0702", "M-0706", "M-0712", "M-0714", "M-0715",
    "M-0716", "M-0717", "M-0726", "M-0727", "M-0728", "M-0729",
    "M-0730", "M-0732", "M-0733", "M-0734", "M-0735", "M-0738",
}

PROMOTED_IDS = {
    "M-0681", "M-0683", "M-0699", "M-0700",
    "M-0701", "M-0702", "M-0726", "M-0732",
}

METADATA_KINDS = {"front_matter", "contents", "editorial", "back_matter"}


def update_inventory() -> None:
    with INVENTORY.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    dispositions: Counter[str] = Counter()
    seen: set[str] = set()
    for row in rows:
        if row["record_type"] != "archive_pdf" or row["volume"] not in {"29", "30"}:
            continue
        record_id = row["record_id"]
        seen.add(record_id)
        kind = row["notes"].removeprefix("kind=")
        if record_id in PROMOTED_IDS:
            status = "close read; finding promoted"
            disposition = "promoted"
        elif record_id in CLOSE_IDS:
            status = "contextual close read; no distinct finding"
            disposition = "contextual"
        elif kind in METADATA_KINDS:
            status = "metadata triaged"
            disposition = "metadata"
        else:
            status = "title and keyword triaged"
            disposition = "title"
        row["text_extraction_status"] = "extracted"
        row["research_status"] = status
        row["local_path"] = f"recovered/corpus-v29-v30/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v29-v30/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1
    assert len(seen) == 64, f"expected 64 volume 29-30 records, got {len(seen)}"
    assert dispositions == Counter({"metadata": 16, "contextual": 22, "title": 18, "promoted": 8}), dispositions
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-001": (
        "A spiritually ratified 'deceiver' or 'infiltrator' label is not a conduct record, and entity-form powers cannot replace notice and review.",
        ["F-091", "F-096"],
    ),
    "G-003": (
        "The route must also accept incapacity and concealed-evidence reports and specify what happens when an outside agency corrects only one legal fact.",
        ["F-091", "F-094", "F-097"],
    ),
    "G-004": (
        "Test constitutional amendment against the leader, actual delegated practice before succession, subordinate veto points, control of contribution flows, and whether the leader can refuse the replacement process.",
        ["F-095", "F-096", "F-097", "F-098"],
    ),
    "G-006": (
        "Adaptive dissolution may preserve a community by changing doctrine, leadership, and membership rather than preserving every original form.",
        ["F-098"],
    ),
    "G-007": (
        "A taboo on leader incapacity and public confrontation of rumored leavers can coexist with member devotion and high collective competence.",
        ["F-097"],
    ),
    "G-008": (
        "A usable exit needs enough timely value to relocate, optional continued affiliation, and practical support for the whole departing household.",
        ["F-092", "F-099"],
    ),
    "G-010": (
        "Probation and useful service do not validate a later capture label when the alleged conduct is never recorded.",
        ["F-091"],
    ),
    "G-011": (
        "Outside facilitation should be familiar and trigger before camps harden; merely adding a mediator after escalation may not prevent exit.",
        ["F-093"],
    ),
    "G-012": (
        "A guaranteed buyout still fails when the wait and amount make relocation impracticable; a permanent trust also needs an independent anti-capture review.",
        ["F-092", "F-096", "F-098"],
    ),
    "G-013": (
        "Define the external actor's purpose and stopping rule: a health inspection, death certificate, foreclosure, or criminal case may leave different safety and evidence questions untouched.",
        ["F-094", "F-096", "F-097"],
    ),
    "G-016": (
        "Continuity can combine board election, redirected contributions, doctrinal amendment, supported departure, and a non-governing alumni identity.",
        ["F-098", "F-099"],
    ),
    "G-018": (
        "An unparticularized 'secret agent,' 'false heart,' or deception label remains a hypothesis even after probation or long service.",
        ["F-091", "F-096"],
    ),
}


NEW_VERIFICATION_BULLETS = """- **F status:** inspect the Ebenezer and Amana originals and translation choices before attributing substantive misconduct to August Jacobi; the durable finding is that the surviving account never specifies the trouble.
- **F status:** retrieve Moora Moora's buyout instrument, valuations, payout histories, and later reforms before treating the two-year guarantee as a current or standardized policy.
- **F status:** verify the Home of Truth sheriff, health, death-certificate, and body-disposition record and the defector's cremation allegation; do not infer that Edith Peshak was denied medical care before death.
- **F status:** inspect the Shaker covenants, ministry minutes, written approvals, and 1963 correspondence before treating member assent and local refusal as independently effective.
- **F status:** verify which Our Land entities and trusts were actually formed, the federal foreclosure record, and the reported militia episode; do not adopt McAfee's statutory claims or allegations of infiltration.
- **F status:** corroborate the Peoples Temple triumvirate proposal and refusal in additional survivor and documentary sources; do not claim that accepting it would have prevented the final catastrophe.
- **F status:** inspect Koreshan board, contribution, and removal records and the gendered factional context before presenting Victoria Gratia's removal as a fair model.
- **F status:** retrieve *Nightwatch* before treating Starland's vehicle, money, and brother-at-large blessing as a standardized or sufficient exit policy.
"""


NEW_NONPROMOTIONS = """- Moora Moora's late circle mediation is promoted only as an aggregate timing lesson, not proof that earlier facilitation would have resolved a particular conflict.
- *A Third Way* describes decentralized elders, community discipline of children, monitoring, and excommunication, but supplies no complete allegation-to-outcome case; its broad adult discipline is already represented by stronger evidence.
- The Emissary of Divine Light succession reflection shows an egalitarian reform effort defeated by hierarchy and followed by exits, but it lacks a defined decision body, evidentiary record, and later outcome sufficient for a distinct finding.
- Reviews of *Escape*, *When Men Become Gods*, *Stolen Innocence*, *Not Without My Sister*, and *Days of Fire and Glory* remain verification leads where they compress serious allegations, rely on unidentified or disputed sources, or omit process and outcome detail.
- The child guru and suicidal-child passages in *Wet Hot and Wild*, and the children in FLDS, Children of God, Peoples Temple, and related reviews, concern children as pressured actors, victims, or dependents—not persistently dangerous children.
- *Soul To Keep* records fasting, observation, and council admission around a child's suicidal crisis, but not an independent safeguarding process or later outcome.
- The translated 1881 George Rapp account and the Amana hired-labor study add opacity and low-voice labor context but no materially distinct danger-response sequence.
"""


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = text.replace(
        "Checkpoint: *Communal Societies* volumes 1-28",
        "Checkpoint: *Communal Societies* volumes 1-30",
    )
    text = text.replace(
        "After reconciling the volume 26-28 findings rather than inflating the list",
        "After reconciling the volume 29-30 findings rather than inflating the list",
    )
    lines = text.splitlines()
    seen: set[str] = set()
    for index, line in enumerate(lines):
        if not line.startswith("| G-"):
            continue
        parts = line.split("|")
        gap_id = parts[1].strip()
        if gap_id not in GAP_ADDITIONS:
            continue
        sentence, references = GAP_ADDITIONS[gap_id]
        if sentence not in parts[4]:
            parts[4] = parts[4].rstrip() + " " + sentence + " "
        evidence = parts[7].strip()
        for reference in references:
            if reference not in {item.strip() for item in evidence.split(",")}:
                evidence += ", " + reference
        parts[7] = " " + evidence + " "
        if gap_id == "G-018":
            parts[4] = parts[4].replace("through volume 28", "through volume 30")
        lines[index] = "|".join(parts)
        seen.add(gap_id)
    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(lines) + "\n"
    if "inspect the Ebenezer and Amana originals" not in text:
        text = text.replace("\n## Explicit non-promotions\n", "\n" + NEW_VERIFICATION_BULLETS + "\n## Explicit non-promotions\n")
    if "Moora Moora's late circle mediation" not in text:
        marker = "- The volume 1-28 dangerous-child searches (F-031, F-048, F-064, F-076, F-090) are bounded negative results, not evidence that intentional communities never faced or managed such children."
        assert marker in text
        text = text.replace(marker, NEW_NONPROMOTIONS + marker)
    text = text.replace(
        "The volume 1-28 dangerous-child searches (F-031, F-048, F-064, F-076, F-090)",
        "The volume 1-30 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100)",
    )
    GAP_BANK.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    update_ledger()
    update_inventory()
    update_gap_bank()
    print("updated ledger, inventory, and gap bank for volumes 29-30")
