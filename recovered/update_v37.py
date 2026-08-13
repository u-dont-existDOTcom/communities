#!/usr/bin/env python3
"""Apply the completed volume 37 checkpoint to the durable research artifacts."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"


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
        finding_id="F-126",
        track="Track A institutional gatekeeper capture in child acquisition",
        source_record_id="M-0922",
        source_file="013-review-of-the-family.pdf",
        journal_volume_issue_year="Vol. 37, no. 1 (2017)",
        article_title="Review of The Family",
        author="Bill Metcalf",
        community_group="The Family (Anne Hamilton-Byrne group), Australia",
        page_locator="PDF pp. 3-4; printed pp. 114-115",
        printed_page_number="114-115",
        source_access="full book review; underlying book, hospital and social-service records, placement records, participant accounts, and official inquiries not independently inspected",
        evidence_type="book-review synthesis of an investigative history",
        exact_factual_observation="Metcalf reports that Anne Hamilton-Byrne's influential inner circle included a physicist, psychiatrist, and lawyer, while many other members were nurses and social workers. He says the group adopted or stole children and that most had been born to unmarried women who were convinced, cajoled, or forced to let their children be taken by Family members working in hospital and social-service roles.",
        what_source_establishes="Professional credentials and service-system access can become capture surfaces when the same actor or loyalty network influences referral, consent, custody, approval, placement, and records. Independence requires role-specific conflict checks and an auditable route around an implicated gatekeeper.",
        what_source_does_not_establish="The review does not identify every worker, mother, child, transfer, legal instrument, agency decision, or official who knew; establish that every acquisition followed the same path; adjudicate individual responsibility; or make professional status itself evidence of misconduct.",
        author_interpretation="The reviewer presents influential and professionally placed adherents as part of the mechanism by which The Family acquired and isolated children.",
        alternative_interpretation="The failures may have differed across cases and may also reflect weak law, fragmented records, agency blind spots, or misconduct by particular people rather than a whole profession or service system.",
        response_process="Recruitment of influential professionals and service workers; contact with unmarried mothers through hospital or social-service roles; reported pressure or coercion to surrender children; transfer to the isolated Uptop property; years of rumor without investigation; later escape, report, and police raid.",
        outcome="Police and social workers released almost twenty children in 1987. The review supplies no acquisition-by-acquisition audit, institutional reform record, placement follow-up, or later child outcome.",
        transferability="High for independent verification of custody and consent, conflict disclosure, separation of referral from approval and placement, dual authorization, traceable records, and protected external reporting. None for treating a credential or profession as a danger proxy.",
        article_gap_status="C",
        likely_article_destination="Children / external couplings / founder and gatekeeper capture audit",
        confidence="medium",
        external_verification_needed="yes",
        notes="Inspect Johnston and Jones's book, survivor and family accounts, hospital and social-service records, adoption and placement files, police evidence, court records, and later official inquiries. Preserve allegations with attribution and do not infer misconduct from professional status alone. DOI: https://doi.org/10.9707/0739-1250.1196",
    ),
    finding(
        finding_id="F-127",
        track="Track A trauma support and evidence preservation after child rescue",
        source_record_id="M-0922",
        source_file="013-review-of-the-family.pdf",
        journal_volume_issue_year="Vol. 37, no. 1 (2017)",
        article_title="Review of The Family",
        author="Bill Metcalf",
        community_group="The Family (Anne Hamilton-Byrne group), Australia",
        page_locator="PDF pp. 4-5; printed pp. 115-116",
        printed_page_number="115-116",
        source_access="full book review; underlying book, interview records, police files, charging analysis, court rulings, care records, and child follow-up not independently inspected",
        evidence_type="book-review synthesis of rescue and later legal process",
        exact_factual_observation="Metcalf reports that one girl escaped and told police about abuse, police released the children in a 1987 raid, and social workers kept the newly liberated children together to reduce trauma. He says this meant a court could regard their evidence as contaminated. Hamilton-Byrne later pleaded guilty only to making a false declaration and received a $5,000 fine; the review says several caregivers were jailed for welfare fraud but not for the reported beatings and starvation.",
        what_source_establishes="Immediate survivor support and evidentiary independence can impose simultaneous, potentially conflicting duties. A response needs coordinated but distinct trauma care, independent account-taking, source attribution, record preservation, and protection against suggestion or joint rehearsal.",
        what_source_does_not_establish="The review supplies no interview protocol, testimony, contamination ruling, evidentiary analysis, charging memorandum, complete case outcome, or causal proof that keeping the children together produced the limited charges. It does not establish current evidence law or justify withholding support or isolating survivors.",
        author_interpretation="The reviewer treats the social workers' trauma-reduction decision as creating a vulnerability in later legal use of the children's accounts.",
        alternative_interpretation="The legal outcome may also reflect delay, jurisdiction, offense definitions, corroboration, charging choices, fugitive status, or other missing evidence. Keeping the children together may have been necessary for welfare even if it complicated fact-finding.",
        response_process="Escape and police report; raid and release of almost twenty children; group support intended to reduce trauma; uncertainty about charges; later extradition; limited plea and separate welfare-fraud cases.",
        outcome="Hamilton-Byrne received a fine after a plea to making a false declaration, and the review reports welfare-fraud imprisonment for several caregivers but no abuse conviction or long-term child follow-up.",
        transferability="High for trauma-informed care coordinated with separately trained, independent interviewers; prompt individual accounts; preserved original words and metadata; disclosure of cross-contact; and ongoing support. None for sacrificing care to create cleaner evidence.",
        article_gap_status="C",
        likely_article_destination="Children / grievance and evidence architecture / external response",
        confidence="medium-low",
        external_verification_needed="yes",
        notes="Inspect the underlying book, survivor accounts, raid and interview records, charging decisions, court files, care plans, and later inquiries before claiming contamination or causation. The reviewer's retrospective diagnosis of Hamilton-Byrne is not adopted. DOI: https://doi.org/10.9707/0739-1250.1196",
    ),
    finding(
        finding_id="F-128",
        track="Track A inspection-to-exit logistics under capture risk",
        source_record_id="M-0933",
        source_file="008-a-new-map-for-understanding-peoples-temple-and-jim-jones.pdf",
        journal_volume_issue_year="Vol. 37, no. 2 (2017)",
        article_title="A New Map for Understanding Peoples Temple and Jim Jones",
        author="Laura Johnston Kohl",
        community_group="Peoples Temple; Jonestown",
        page_locator="PDF pp. 9-10; printed pp. 206-207",
        printed_page_number="206-207",
        source_access="full text; survivor-authored interpretive article discussing two historical books and the author's experience; visit-planning and airstrip records not independently inspected",
        evidence_type="survivor-authored historical synthesis and book analysis",
        exact_factual_observation="Kohl reports that defectors and Concerned Relatives contacted the US government and found an ally in Congressman Leo Ryan. Ryan visited Jonestown with relatives and media; several residents said they planned to leave. Kohl says he had made no provision for leavers and there were not enough airplane seats, causing a delay. The departing group later reached the airstrip, armed Jonestown residents followed, and five people, including Ryan and one former resident, were killed.",
        what_source_establishes="A high-risk inspection can surface confidential demand for immediate exit and thereby create a new operational risk. The inspection plan needs protected staging, sufficient transport, communications, and medical and security contingencies before leavers are exposed.",
        what_source_does_not_establish="The article supplies no passenger manifest, seat count, planning record, full timeline, security assessment, or independent reconstruction of every decision. It cannot establish that the seat shortage caused the attack, that additional seats would have prevented it, or that routine visits should be militarized.",
        author_interpretation="Kohl presents Jones as treating exit and custody as existential challenges to his authority and regards the lack of provision for leavers as a delay that could have proved fatal to more people.",
        alternative_interpretation="The attack may have occurred regardless of the seat shortage. A safe plan might have required postponement, separate transport, a protected site, or a different security posture rather than additional seats alone.",
        response_process="Defectors and relatives report concerns; congressional visit with relatives and media; residents disclose a wish to leave; inadequate transport capacity and delay; movement to the airstrip; armed pursuit and attack.",
        outcome="Five people were killed at the airstrip, followed by the mass deaths in Jonestown and additional deaths in Georgetown. The source supplies no causal counterfactual or post-event logistics reform.",
        transferability="High for pre-visit risk assessment, confidential interviews, protected separation and staging, manifests and sufficient transport, communications, medical support, and a contingency route around the inspected authority. Low for copying the historical intervention without current legal and operational review.",
        article_gap_status="C",
        likely_article_destination="External couplings / usable exit / inspection and emergency map",
        confidence="medium",
        external_verification_needed="yes",
        notes="Inspect congressional planning records, passenger manifests, contemporaneous reporting, investigative files, Reiterman and Guinn's books, and other survivor accounts before stating the logistics, authorization, or causal counterfactual as settled fact. DOI: https://doi.org/10.9707/0739-1250.1181",
    ),
    finding(
        finding_id="F-129",
        track="Track B success metric for external sponsor dependence",
        source_record_id="M-0929",
        source_file="004-the-political-economy-of-communal-life-zionist-settlement-policy-and-kibbutz-collective-practices-19202010.pdf",
        journal_volume_issue_year="Vol. 37, no. 2 (2017)",
        article_title="The Political Economy of Communal Life: Zionist Settlement Policy and Kibbutz Collective Practices, 1920-2010",
        author="Daniel DeMalach",
        community_group="Israeli kibbutz movement; World Zionist Organization; State of Israel",
        page_locator="PDF pp. 19-23; printed pp. 146-150",
        printed_page_number="146-150",
        source_access="full text; macro-historical argument based on published demographic, policy, credit, and movement sources; underlying datasets and agreements not independently reanalyzed",
        evidence_type="political-economy history and long-period organizational synthesis",
        exact_factual_observation="DeMalach reports that public agricultural resources and bank credit expanded sharply during the 1970s as kibbutzim served renewed settlement policy, coinciding with prosperity, population growth, and stable collective practices. He then describes large support cuts, real-interest debt, restricted credit, and a 1995 state-bank-kibbutz debt agreement under which kibbutzim were pressured to abandon equal pay. He argues that diffusion and decline of collective practices closely followed changing settlement policy.",
        what_source_establishes="Institutional persistence and voluntary retention can be materially shaped by an external sponsor's land, capital, credit, recruitment, and political objectives. A success dashboard should measure sponsor purpose, subsidy and credit exposure, and robustness after support changes rather than treating longevity as wholly endogenous performance.",
        what_source_does_not_establish="The article does not prove that public support was the sole cause of kibbutz growth or decollectivization, measure individual safety or autonomy, adjudicate the political project it describes, or assign a causal share among policy, ideology, markets, demographics, technology, and internal governance.",
        author_interpretation="DeMalach presents changing Zionist settlement priorities as a key factor neglected by culturally and internally focused accounts, while explicitly treating the explanation as complementary rather than exclusive.",
        alternative_interpretation="Internal commitment, leadership, demographic change, global markets, technological change, and organizational learning may explain part of the same trajectory. Sponsor withdrawal may expose pre-existing weaknesses rather than create them.",
        response_process="External allocation of land, capital, recruitment support, credit, and political authority; federative enforcement of collective practices; policy and budget shift; debt crisis and restricted credit; tripartite debt restructuring tied to organizational change.",
        outcome="The article reports periods of population growth and stable collective practice under expanding support, followed by insolvency pressure and widespread decollectivization, including adoption of differential pay by more than three quarters of kibbutzim over the following fifteen years.",
        transferability="High for adding sponsor purpose, subsidy and credit dependence, contingent liabilities, and post-support performance to a success dashboard. None for treating the historical settlement objective or public financing model as a general recommendation.",
        article_gap_status="B",
        likely_article_destination="Why communities fail / success dashboard / material viability",
        confidence="medium",
        external_verification_needed="yes",
        notes="Verify the policy chronology, budget and credit figures, debt agreement, organizational classifications, and alternative economic histories before using exact figures or causal shares. The finding is a measurement warning, not an endorsement of the political objectives described. DOI: https://doi.org/10.9707/0739-1250.1177",
    ),
    finding(
        finding_id="F-130",
        track="Track A informal majoritarian sanction and member property",
        source_record_id="M-0930",
        source_file="005-the-gods-of-the-dunes-the-diverse-spiritual-practices-and-beliefs-of-the-dunites.pdf",
        journal_volume_issue_year="Vol. 37, no. 2 (2017)",
        article_title="The Gods of the Dunes: The Diverse Spiritual Practices and Beliefs of the Dunites",
        author="Amy Hart",
        community_group="Dunites; Oceano, California",
        page_locator="PDF p. 16; printed p. 167, footnote 42",
        printed_page_number="167",
        source_access="full text; cautionary footnote summarizing Norm Hammond's secondary history; underlying participant, property, and legal records not independently inspected",
        evidence_type="historical article relying on a secondary anecdote for the promoted sequence",
        exact_factual_observation="Hart recounts that a dispute between Hugo Seelig and Elwood Decker over the nature of the Hindu goddess Kali led Seelig to believe Decker was using black magic against him. Because Seelig had lived in the dunes longer, public support reportedly shifted toward him. Decker moved away, and other Dunites burned his cabin to remove negative energies. The same account says he returned five years later and stayed another ten years.",
        what_source_establishes="A pluralistic, low-formality community can still let seniority and popularity turn a supernatural allegation into displacement and destruction of a member's property. A later return does not itself validate the allegation, decision, or sanction.",
        what_source_does_not_establish="The article does not establish cabin ownership, consent, who decided or participated, whether Decker was forced to leave, what evidence was considered, whether law or restitution followed, why he returned, or whether reconciliation occurred. The promoted sequence rests on a book not inspected here.",
        author_interpretation="Hart calls the episode a disconcerting example of tolerance gone wrong and also suggests it can be read as social pressure maintaining order without formal hierarchy.",
        alternative_interpretation="The cabin may have been abandoned, jointly controlled, or burned with consent; Decker's move and later return may have reflected circumstances not preserved in the summary. Those possibilities cannot be resolved from the article.",
        response_process="Religious-philosophical dispute; black-magic allegation; informal public alignment based partly on seniority; Decker's departure; cabin destruction framed as removal of negative energy; later return.",
        outcome="Decker reportedly returned after five years and remained another decade. No fact-finding record, appeal, restitution, accountability, or explanation of the return is supplied.",
        transferability="High for belief-neutral conduct standards, notice, evidence review, property authority, conflict recusal, and independent appeal before displacement or destruction. Low for drawing broader conclusions from the unverified anecdote.",
        article_gap_status="C",
        likely_article_destination="Fair separation / non-waivable rights / cohesion warning",
        confidence="low-medium",
        external_verification_needed="yes",
        notes="Inspect Hammond's book and any participant, property, community, fire, or legal records before stating ownership, consent, authorization, coercion, or reconciliation. Preserve the supernatural claim as an allegation, not a fact. DOI: https://doi.org/10.9707/0739-1250.1178",
    ),
    finding(
        finding_id="F-131",
        track="Track A child negative result",
        source_record_id="",
        source_file="Volume 37 discovery corpus",
        journal_volume_issue_year="Volume 37 (2017)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volume 37",
        page_locator="26 PDFs; 20 relevant or contextual close reads; 6 child-danger proximity candidates",
        printed_page_number="",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 26 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 20 relevant or contextual close reads found children or young people as students, dependents, residents, service recipients, custody subjects, alleged or actual victims, demographic units, and people near outsider rumors about adults. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from volume 37 under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 38-45, standalone or book-length sources, different terminology, unpublished or protected records, juvenile, educational, medical, disability, or family systems, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, aggregate reporting, source destruction, and routing into professional, family, juvenile, educational, disability, or medical systems may hide relevant cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volume 37.",
        transferability="High for this completed unit; none for the full literature until the remaining journal and standalone sources are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="The cumulative bounded null now covers volumes 1-37. Children harmed, governed, educated, placed, rescued, represented, or involved in adult custody conflict were excluded from the child-as-dangerous-actor result.",
    ),
]


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    assert new in text, f"missing update anchor: {label}"
    return text


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    expected_existing = [f"F-{number:03d}" for number in range(1, 126)]
    ids = [row["finding_id"] for row in rows]
    if ids == expected_existing:
        rows.extend(NEW_FINDINGS)
    else:
        expected_complete = [f"F-{number:03d}" for number in range(1, 132)]
        assert ids == expected_complete, "unexpected evidence-ledger boundary"
        assert rows[-6:] == NEW_FINDINGS, "existing volume 37 findings differ"
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


PROMOTED_IDS = {"M-0922", "M-0929", "M-0930", "M-0933"}
METADATA_KINDS = {"front_matter", "contents", "table_of_contents", "editorial"}
ARCHIVE_RECORD_ID = "D-017"
ARCHIVE_EXPECTED = {
    "drive_size_bytes": "78015463",
    "sha256": "95f87d2210fc829ca76b7b495e24d9057db5d4acefe4c055c4f8d41bc32afb39",
    "research_status": "not processed",
    "local_path": "raw/vol35-40.zip",
    "notes": "Drive inventory row; archive downloaded and integrity-tested; members follow",
}


def update_inventory() -> None:
    with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed before update: {field}"
    dispositions: Counter[str] = Counter()
    seen: set[str] = set()
    for row in rows:
        if row["drive_file_id"]:
            row["drive_file_id"] = "REDACTED"
        if row["record_type"] != "archive_pdf" or row["volume"] != "37":
            continue
        record_id = row["record_id"]
        seen.add(record_id)
        kind = row["notes"].removeprefix("kind=")
        if record_id in PROMOTED_IDS:
            status = "close read; finding promoted"
            disposition = "promoted"
        elif kind in METADATA_KINDS:
            status = "metadata triaged"
            disposition = "metadata"
        else:
            status = "contextual close read; no distinct finding"
            disposition = "contextual"
        row["text_extraction_status"] = "extracted"
        row["research_status"] = status
        row["local_path"] = f"recovered/corpus-v37/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v37/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1
    assert len(seen) == 26, f"expected 26 volume 37 records, got {len(seen)}"
    assert dispositions == Counter({"contextual": 16, "metadata": 6, "promoted": 4}), dispositions
    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed during update: {field}"
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-001": (
        "A high-risk inspection that uncovers leavers needs protected staging, sufficient transport, communications, medical and security contingencies, and a confidential extraction route. Seniority, popularity, or a spiritual allegation cannot authorize displacement or destruction of a member's property.",
        ["F-128", "F-130"],
    ),
    "G-003": (
        "Survivor support and evidence intake need coordinated but distinct roles, and an inspection route must include a confidential extraction plan for people who disclose a wish to leave.",
        ["F-127", "F-128"],
    ),
    "G-004": (
        "Audit professional gatekeepers who control referral, custody, consent, approval, placement, or records; credentials do not remove loyalty conflicts.",
        ["F-126"],
    ),
    "G-005": (
        "Spiritual pluralism does not waive conduct-specific process or property protections; later return cannot retroactively validate a sanction.",
        ["F-130"],
    ),
    "G-006": (
        "Report sponsor purpose, subsidy and credit exposure, and performance after support changes; externally financed persistence is not the same outcome as endogenous resilience.",
        ["F-129"],
    ),
    "G-007": (
        "A pluralistic self-description, informal coexistence, or later return does not validate an unreviewed spiritual accusation or property sanction.",
        ["F-130"],
    ),
    "G-009": (
        "Audit every professional role in child acquisition and placement through independent custody and consent verification, conflict disclosure, dual review, and traceable records.",
        ["F-126"],
    ),
    "G-011": (
        "Trauma-informed survivor care should continue, but should not be merged with group evidence testing or joint rehearsal; preserve independent accounts without isolating people from needed support.",
        ["F-127"],
    ),
    "G-013": (
        "A high-risk inspection needs confidential interview and extraction logistics, while child-placement systems need independent consent, custody, conflict, and record checks.",
        ["F-126", "F-127", "F-128"],
    ),
    "G-018": (
        "Volume 37 again found neither evidence validating inner work or long exposure as a dangerous-person filter nor a complete dangerous-child actor response sequence.",
        ["F-131"],
    ),
}


NEW_VERIFICATION_BULLETS = """- **F status:** inspect Johnston and Jones's *The Family*, survivor and family accounts, hospital and social-service records, placement files, police evidence, court records, care records, and later inquiries before treating the gatekeeper or evidence-contamination sequences as adjudicated; do not adopt the reviewer's retrospective diagnosis.
- **F status:** inspect Peoples Temple congressional planning, passenger manifests, contemporary reporting, investigation files, and survivor accounts before treating the exit logistics, authorization, or causal counterfactual as settled.
- **F status:** verify the kibbutz policy chronology, budget and credit figures, debt agreement, classifications, and alternative economic histories before using exact figures or causal shares; the finding is not an endorsement of the political objective described.
- **F status:** inspect Hammond's Dunites history and any participant, property, community, fire, or legal records before stating cabin ownership, consent, authorization, coercion, or reconciliation.
"""


NEW_NONPROMOTIONS = """- The TM retirement sequence materially corroborates F-054, while negativity suppression, information control, banishment, covert exit networks, and post-founder rigidity corroborate F-058 and F-097 rather than creating duplicate findings.
- The Moravian-Camphill history's co-resident care, no-wage tradition, professional insularity, external opacity, and golden-age warning corroborate F-054, F-122, and existing transparency and success gaps without a case-level safety outcome.
- The Mormon apocalyptic article strongly corroborates F-011 and F-058: external persecution and failed redress can become proof inside a closed prediction system, while accommodation can soften it.
- *Lived Utopianism*, the Pacific Coast Chapter history, and the Twin Oaks reflection provide conflict, scaling, labor, family, and adaptive-governance context without an independently reviewed safety outcome.
- The non-extraction portions of the Peoples Temple article corroborate F-011 and F-097 on custody conflict, dissent suppression, leader incapacity, and public/private narrative; they are not duplicated as new findings.
- The children in *The Family* are alleged victims, and the youth and custody subjects in the Peoples Temple article are recipients, dependents, or objects of adult conflict—not persistently dangerous child actors.
- The remaining volume 37 sources supply property, archive, town-planning, religious-pluralism, lifecycle, craft, formation, movement, or continuity context without a materially distinct response mechanism and later outcome.
"""


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-36",
        "Checkpoint: *Communal Societies* volumes 1-37",
        "gap checkpoint",
    )
    text = replace_once_or_confirm(
        text,
        "After reconciling the volume 36 findings rather than inflating the list",
        "After reconciling the volume 37 findings rather than inflating the list",
        "gap reconciliation version",
    )
    text = replace_once_or_confirm(
        text,
        "No processed journal evidence through volume 36",
        "No processed journal evidence through volume 37",
        "gap journal boundary",
    )
    text = replace_once_or_confirm(
        text,
        "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125) are bounded negative results",
        "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131) are bounded negative results",
        "gap bounded-null list",
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
        existing = {item.strip() for item in evidence.split(",")}
        for reference in references:
            if reference not in existing:
                evidence += ", " + reference
                existing.add(reference)
        parts[7] = " " + evidence + " "
        lines[index] = "|".join(parts)
        seen.add(gap_id)
    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(lines) + "\n"
    if "inspect Johnston and Jones's *The Family*" not in text:
        text = text.replace(
            "\n## Explicit non-promotions\n",
            "\n" + NEW_VERIFICATION_BULLETS + "\n## Explicit non-promotions\n",
            1,
        )
    if "The TM retirement sequence materially corroborates F-054" not in text:
        text = text.rstrip() + "\n" + NEW_NONPROMOTIONS
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = [
        ("volumes **1-36**", "volumes **1-37**", "state completed boundary"),
        (
            "**777 journal PDFs** were triaged: 293 close-read as relevant or contextual, 207 title/keyword-triaged, and 277 metadata-triaged.",
            "**803 journal PDFs** were triaged: 313 close-read as relevant or contextual, 207 title/keyword-triaged, and 283 metadata-triaged.",
            "state counts",
        ),
        (
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **125 findings** (`F-001` through `F-125`). Volume 36 added four findings: two C, one D, and one F-status bounded negative.",
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **131 findings** (`F-001` through `F-131`). Volume 37 added six findings: four C, one B, and one F-status bounded negative.",
            "state findings",
        ),
        (
            "`COMMUNITIES-V36-RESEARCH-REPORT.md` records the completed 21-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "`COMMUNITIES-V37-RESEARCH-REPORT.md` records the completed 26-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "state report",
        ),
        (
            "Every one of the 21 volume 36 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text.",
            "Every one of the 26 volume 37 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text.",
            "state corpus verification",
        ),
        (
            "Volumes **37-45** have not been processed: **207 journal PDFs**.",
            "Volumes **38-45** have not been processed: **181 journal PDFs**.",
            "state remaining boundary",
        ),
        (
            "The next bounded journal unit is volume **37: 26 PDFs**—16 in issue 1 and 10 in issue 2.",
            "The next bounded journal unit is volume **38: 20 PDFs**—11 in issue 1 and 9 in issue 2.",
            "state next unit",
        ),
        (
            "Volume 36 adds: communication-access interviewing for residents with limited speech; a warning that categorical expertise and agency action can produce coercive false positives; reported destruction of Oneida records by a successor corporation's employees; and another bounded dangerous-child null.",
            "Volume 37 adds: capture through professional child-placement gatekeepers; the need to separate trauma support from evidentiary testing; confidential extraction logistics for high-risk inspections; external sponsor dependence as a success metric; informal majoritarian property punishment after a spiritual allegation; and another bounded dangerous-child null.",
            "state evidence summary",
        ),
        ("Do not repeat volumes 1-36.", "Do not repeat volumes 1-37.", "state resume boundary"),
        (
            "Retrieve and verify the 26 volume 37 publisher PDFs; they are the next exact bounded journal unit.",
            "Retrieve and verify the 20 volume 38 publisher PDFs; they are the next exact bounded journal unit.",
            "state resume next unit",
        ),
        (
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 26 extracted texts.",
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 20 extracted texts.",
            "state resume corpus size",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = [
        ("Volumes **1-36** complete", "Volumes **1-37** complete", "README boundary"),
        ("**777** journal PDFs triaged", "**803** journal PDFs triaged", "README PDF count"),
        ("**293** relevant or contextual close reads", "**313** relevant or contextual close reads", "README close reads"),
        ("**125** evidence findings (`F-001` through `F-125`)", "**131** evidence findings (`F-001` through `F-131`)", "README findings"),
        (
            "Next unit: **volume 37, 26 PDFs** (16 in issue 1; 10 in issue 2)",
            "Next unit: **volume 38, 20 PDFs** (11 in issue 1; 9 in issue 2)",
            "README next unit",
        ),
        (
            "[`recovered/COMMUNITIES-V36-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V36-RESEARCH-REPORT.md)",
            "[`recovered/COMMUNITIES-V37-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V37-RESEARCH-REPORT.md)",
            "README report link",
        ),
        ("`recovered/corpus-v36/`", "`recovered/corpus-v37/`", "README corpus path"),
        ("python recovered/test_v36_workflow.py", "python recovered/test_v37_workflow.py", "README tests"),
        ("python recovered/verify_v36.py", "python recovered/verify_v37.py", "README verifier"),
        ("all 21 PDF hashes", "all 26 PDF hashes", "README verified PDFs"),
        ("the volume-37 boundary", "the volume-38 boundary", "README next-boundary check"),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    README.write_text(text, encoding="utf-8")


def main() -> None:
    update_ledger()
    update_inventory()
    update_gap_bank()
    update_state()
    update_readme()
    print("updated volume37 findings=6 promoted_sources=4 contextual=16 metadata=6")


if __name__ == "__main__":
    main()
