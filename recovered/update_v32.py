#!/usr/bin/env python3
"""Apply the completed volume 32 checkpoint to the durable research artifacts."""

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
        finding_id="F-106",
        track="Track A membership-screening evidence quality",
        source_record_id="M-0775",
        source_file="005-social-innovations-for-communal-and-ecological-living-lessons-from-sustainability-research-and-observations-in.pdf",
        journal_volume_issue_year="Vol. 32, no. 1 (2012)",
        article_title="Social Innovations for Communal and Ecological Living: Lessons from Sustainability Research and Observations in Intentional Communities",
        author="Iris Kunze",
        community_group="Seven intentional communities in India, the United Kingdom, and Germany",
        page_locator="PDF pp. 10-13; printed pp. 47-50",
        printed_page_number="47-50",
        source_access="full text",
        evidence_type="purposive qualitative study using prior research, a 113-community survey, observation, interviews, and documents",
        exact_factual_observation="The study selected communities that already matched a normative list including self-organization, shared ownership, consensus or decentralized decisions, transparency, more than twenty members, and at least five years of existence. It then reported that all seven observed communities had developed applicant testing and acceptance procedures, often lasting half a year or more, and described probation as insurance for the community.",
        what_source_establishes="Long-established communities in this purposive sample used extended mutual-acquaintance and probation procedures; those procedures are therefore plausible practices to test, not evidence that duration itself detects bad faith or danger.",
        what_source_does_not_establish="The design does not estimate false positives or false negatives, compare accepted and rejected applicants, track harmful conduct, isolate probation from other features, or show that probation caused survival. Selecting on preferred organization and prior persistence prevents a causal effectiveness claim.",
        author_interpretation="The author presents the observed procedures as successful community-management tools and argues that established communities became more selective as applicant demand and infrastructure needs changed.",
        alternative_interpretation="Stable communities may have had the capacity to sustain longer admissions processes, while selection and survivorship explain part of the apparent association; probation may also filter difference or need rather than dangerous conduct.",
        response_process="Theory-derived selection criteria; purposive community selection; restudies and short participant-observation visits; interviews; description of applicant probation.",
        outcome="The sampled communities had survived at least five years and used the reported procedures, but the study supplies no applicant-level safety or later-conduct outcome.",
        transferability="High as a research-design warning and moderate as a candidate admission practice; any modern protocol needs conduct-specific validation, comparable records, and outcome review.",
        article_gap_status="D",
        likely_article_destination="From visitor to member / safety proxies / research-method note",
        confidence="high",
        external_verification_needed="no",
        notes="Do not cite this study as validation that six months of exposure identifies con artists. DOI: https://doi.org/10.9707/0739-1250.1316",
    ),
    finding(
        finding_id="F-107",
        track="Track A concentrated financial custody and non-pursuit",
        source_record_id="M-0776",
        source_file="006-a-visit-to-the-shaker-village-of-white-water-in-1881.pdf",
        journal_volume_issue_year="Vol. 32, no. 1 (2012)",
        article_title="A Visit to the Shaker Village of White Water in 1881",
        author="Thomas Sakmyster",
        community_group="White Water Shaker community",
        page_locator="PDF pp. 8-9 and 20; printed pp. 63-64 and 75",
        printed_page_number="63-64, 75",
        source_access="full text",
        evidence_type="scholarly framing of an 1881 visitor account, compared with an 1829 elder's letter",
        exact_factual_observation="Judge A. G. W. Carter recalled that a charismatic preacher who also controlled village funds allegedly stole a large amount and fled with a Shaker woman around 1829. White Water residents remembered the episode in 1881 but supplied a likely incorrect name; a sister elder said the community did not pursue him because of its principle of nonresistance. An 1829 elder's letter independently called the likely preacher corrupt and dishonest but did not record theft.",
        what_source_establishes="The source preserves a report in which preaching authority and financial custody were concentrated and a non-pursuit norm left alleged wrongdoing without documented recovery or public accountability. Nonviolence and nonretaliation still require evidence preservation, reporting, restitution, and role separation.",
        what_source_does_not_establish="It does not prove the theft or sexual allegation, establish the offender's identity, state the amount, reconstruct the accounts, show whether leaders took any unrecorded protective action, or demonstrate what pursuit would have recovered.",
        author_interpretation="Sakmyster identifies Nathan Burlingame as the likely preacher and says Carter's account implies possible embezzlement and licentious conduct, while noting the contemporary letter does not state the specific allegations.",
        alternative_interpretation="Fifty-year memory, folklore, politeness, and a mistaken name may have altered the account; non-pursuit may have reflected limited jurisdiction or recovery prospects as well as doctrine.",
        response_process="Suspicions outside the community; departure; retrospective community acknowledgment; reported decision not to pursue.",
        outcome="The visitor said the preacher was not heard from again; the article identifies no investigation, accounting, restitution, or later remedy.",
        transferability="High in principle for dual authorization, timely accounts, preserved records, protected external reporting, and restitution without vengeance; low for treating the historical allegation as adjudicated fact.",
        article_gap_status="C",
        likely_article_destination="Money and land / nonviolent accountability / selecting legal couplings",
        confidence="low",
        external_verification_needed="yes",
        notes="Verify the identity, funds, departure, and any Shaker response before naming the alleged theft. DOI: https://doi.org/10.9707/0739-1250.1317",
    ),
    finding(
        finding_id="F-108",
        track="Track B asset lock, mission drift, and false-positive longevity",
        source_record_id="M-0787",
        source_file="004-charitable-trusts-and-longevity-in-new-zealand-s-intentional-communities.pdf",
        journal_volume_issue_year="Vol. 32, no. 2 (2012)",
        article_title="Charitable Trusts and Longevity in New Zealand's Intentional Communities",
        author="Olive Jones",
        community_group="Renaissance, Riverside, Tui, and Wilderland communities",
        page_locator="PDF pp. 20-24; printed pp. 116-120",
        printed_page_number="116-120",
        source_access="full text",
        evidence_type="comparative doctoral research using current and former resident interviews, documents, and thirty-five years of participant experience",
        exact_factual_observation="Charitable trusts kept four community properties collectively owned in perpetuity and prevented private gain from sale. At Renaissance, most founders and the productive core left, collective enterprise largely faded, buildings and land deteriorated, and around forty residents remained; the trust structure nevertheless made sale, subdivision, privatization, or closure exceptionally difficult. The study also reports that some long-term residents across the communities lacked the capital or outside earning capacity needed to relocate.",
        what_source_establishes="A protective asset lock can preserve land while decoupling legal survival from mission performance, community health, and usable exit. Perpetuity therefore needs scheduled purpose review, renewal or recharter rules, independent assessment, and a humane dissolution or succession path.",
        what_source_does_not_establish="It does not show that trust ownership alone caused every social or maintenance problem, that every resident wanted to leave, that dissolution was preferable, or that perpetual ownership cannot enable a later revival.",
        author_interpretation="Jones treats the trust as a central cause of unusual longevity and a double-edged structure that can protect collective land while immobilizing a dysfunctional or purpose-depleted community.",
        alternative_interpretation="The same lock prevented factional privatization, retained affordable housing, and preserved land for a future resident group; continuing occupancy may reflect preference and social value as well as constraint.",
        response_process="Founder departures; continued trust ownership and occupancy; limited maintenance funding; no sale, subdivision, or closure.",
        outcome="The land remained collective and occupied, but Renaissance's legal continuity coexisted with weak collective life, neglected assets, and mission drift.",
        transferability="High for treating survival and success separately and for pairing asset protection with mission metrics, periodic independent review, exit liquidity, and a defined sunset, recharter, or successor process.",
        article_gap_status="B",
        likely_article_destination="Why communities fail / plan the funeral / money and land",
        confidence="high",
        external_verification_needed="yes",
        notes="Verify current deed terms, board practice, resident views, and property conditions before making present-tense claims. DOI: https://doi.org/10.9707/0739-1250.1328",
    ),
    finding(
        finding_id="F-109",
        track="Track A nominal override without duty, trigger, or recusal",
        source_record_id="M-0787",
        source_file="004-charitable-trusts-and-longevity-in-new-zealand-s-intentional-communities.pdf",
        journal_volume_issue_year="Vol. 32, no. 2 (2012)",
        article_title="Charitable Trusts and Longevity in New Zealand's Intentional Communities",
        author="Olive Jones",
        community_group="Renaissance Community Trust",
        page_locator="PDF p. 10; printed p. 106",
        printed_page_number="106",
        source_access="full text",
        evidence_type="comparative doctoral research plus founder and former-trustee participant knowledge",
        exact_factual_observation="Jones reports that former residents repeatedly asked the Renaissance trustees to intervene, particularly in matters involving violence and illegal activities, but the trustees were unable or unwilling to act. She attributes the paralysis to an ambiguous deed that omitted operational duties, inability to reach a united decision, resident trustees' conflicts of interest, and an original ideology that limited trustees to holding land rather than directing community affairs. The trustees formally retained ultimate power to sell and close, but agreement and charitable-destination rules made that step unlikely.",
        what_source_establishes="An override body is not a safety mechanism merely because it holds ultimate legal power. It needs an affirmative duty, conduct-based trigger, decision rule, recusal standard, interim protection authority, evidence channel, and route to independent or public response.",
        what_source_does_not_establish="The article does not specify the alleged incidents, identify actors, adjudicate whether violence or illegality occurred, document each appeal, show what intervention was legally available, or report later safety outcomes.",
        author_interpretation="Jones argues that deed ambiguity, nonintervention ideology, internal conflict, and trustee-beneficiary conflicts made the trust incapable of responding when the resident group departed from the trust's purposes.",
        alternative_interpretation="Trustee restraint may have protected resident self-government and avoided overreach; criminal or civil authorities, rather than land trustees, may have held responsibility for some alleged conduct, but the article does not document those routes.",
        response_process="Former-resident appeals to trustees; trustee indecision and nonintervention; continued community operation.",
        outcome="No trust intervention or independent review is documented, and the community continued under the same basic ownership arrangement.",
        transferability="High for writing operational duties and escalation routes into the governing instrument before crisis, including mandatory external reporting where law or immediate safety requires it.",
        article_gap_status="C",
        likely_article_destination="Fair separation / tested override / selecting legal couplings",
        confidence="medium",
        external_verification_needed="yes",
        notes="Treat violence and illegal-activity references as unadjudicated reports until board records, incident records, and other perspectives are retrieved. DOI: https://doi.org/10.9707/0739-1250.1328",
    ),
    finding(
        finding_id="F-110",
        track="Track B title transfer without appointment-power transfer",
        source_record_id="M-0787",
        source_file="004-charitable-trusts-and-longevity-in-new-zealand-s-intentional-communities.pdf",
        journal_volume_issue_year="Vol. 32, no. 2 (2012)",
        article_title="Charitable Trusts and Longevity in New Zealand's Intentional Communities",
        author="Olive Jones",
        community_group="Wilderland Community Trust",
        page_locator="PDF pp. 19-20; printed pp. 115-116",
        printed_page_number="115-116",
        source_access="full text",
        evidence_type="comparative doctoral research using interviews, founder writings, records, and long-term observation",
        exact_factual_observation="Dan and Edith Hansen transferred Wilderland's land to a charitable trust but the deed made them trustees for life and gave them power to elect or re-elect the other resident trustees, whose terms lasted three years. Jones reports unequal authority, insecurity, cliques, and high turnover. After the founders' deaths, their daughter's High Court effort to dismantle the community and return control to the family failed; a new board then began a management and building-compliance plan.",
        what_source_establishes="Transferring title out of a founder's name does not transfer practical control when the founder retains lifetime appointment and reappointment power. An anti-capture design must map trustee selection, term limits, removal, succession, resident voice, and control after death as well as the deed holder.",
        what_source_does_not_establish="It does not prove that every appointment was manipulated, that founder control alone caused turnover or weak buildings, that a different election system would have prevented conflict, or that the post-founder plan succeeded.",
        author_interpretation="Jones treats the retained appointment power as continuing founder control that intensified insecurity, while also crediting the trust's ownership with preserving Wilderland after the founders died.",
        alternative_interpretation="Lifetime founder trusteeship may have been intended to preserve purpose and continuity; the failed family challenge suggests that the asset lock ultimately resisted hereditary reclamation.",
        response_process="Trust transfer with reserved appointment powers; trustee and non-trustee conflict; founder deaths; family court challenge; new-board planning and code negotiations.",
        outcome="The family did not regain the property, founder appointment control ended after death, and a successor board began formal management and compliance work.",
        transferability="High for testing whether formal title separation also changes appointment, removal, succession, information, and operational authority.",
        article_gap_status="B",
        likely_article_destination="Founderism / tested override / money and land",
        confidence="high",
        external_verification_needed="yes",
        notes="Inspect the trust deed, High Court record, board minutes, and later outcomes before presenting this as a current governance model. DOI: https://doi.org/10.9707/0739-1250.1328",
    ),
    finding(
        finding_id="F-111",
        track="Track A child negative result",
        source_file="Volume 32 discovery corpus",
        journal_volume_issue_year="Volume 32 (2012)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volume 32",
        page_locator="27 PDFs; 19 relevant or contextual close reads; 9 child-danger proximity candidates",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 27 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 19 relevant or contextual close reads found children as students, dependents, residents, custody or raid subjects, disability-service recipients, victims of adult sexual abuse or alleged castration, and childhood biographical subjects. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from volume 32 under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 33-45, standalone sources, different terminology, unpublished records, book-length sources, juvenile, educational, medical, or family records, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, aggregate reporting, source destruction, and routing into professional, family, juvenile, or disability systems may hide relevant cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volume 32.",
        transferability="High for this completed unit; none for the full literature until the remaining journal and standalone sources are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="The cumulative bounded null now covers volumes 1-32. Children harmed or governed by adults and youth-service recipients were excluded from the child-as-dangerous-actor result.",
    ),
]


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames == list(NEW_FINDINGS[0]), "ledger schema changed"
    expected_tail = [f"F-{number:03d}" for number in range(106, 112)]
    if len(rows) == 111 and [row["finding_id"] for row in rows[-6:]] == expected_tail:
        rows = rows[:105]
    assert len(rows) == 105 and rows[-1]["finding_id"] == "F-105", "unexpected ledger checkpoint"
    all_rows = rows + NEW_FINDINGS
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)


CLOSE_IDS = {
    "M-0774", "M-0775", "M-0776", "M-0777", "M-0778", "M-0779",
    "M-0780", "M-0781", "M-0782", "M-0787", "M-0788", "M-0789",
    "M-0790", "M-0791", "M-0792", "M-0793", "M-0794", "M-0795",
    "M-0796",
}

PROMOTED_IDS = {"M-0775", "M-0776", "M-0787"}
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
        if row["record_id"] == "D-013":
            row["research_status"] = "container processed; 13 member PDFs triaged"
            row["local_path"] = "recovered/vol32-iss1.zip"
            row["notes"] = "Drive inventory row; archive downloaded, integrity-tested, and processed; 13 members follow"
        if row["record_id"] == "D-014":
            row["research_status"] = "container processed; 14 member PDFs triaged"
            row["local_path"] = "recovered/vol32-iss2.zip"
            row["notes"] = "Drive inventory row; archive downloaded, integrity-tested, and processed; 14 members follow"
        if row["record_type"] != "archive_pdf" or row["volume"] != "32":
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
        row["local_path"] = f"recovered/corpus-v32/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v32/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1
    assert len(seen) == 27, f"expected 27 volume 32 records, got {len(seen)}"
    assert dispositions == Counter({"contextual": 16, "metadata": 8, "promoted": 3}), dispositions
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-001": (
        "A nonresistance or nonintervention norm cannot waive evidence preservation, restitution, independent review, or a lawful safety response; a land-holding body needs an operational duty and trigger rather than only ultimate closure power.",
        ["F-107", "F-109"],
    ),
    "G-003": (
        "A trustee or board route must specify affirmative duties, decision rules, conflicts, and an independent escalation path; otherwise repeated appeals can terminate in institutional indecision.",
        ["F-109"],
    ),
    "G-004": (
        "Transferring title is not transferring control when a founder retains lifetime trustee status and appointment or reappointment power; test the deed's nomination, removal, term, succession, and resident-voice rules.",
        ["F-109", "F-110"],
    ),
    "G-006": (
        "Measure mission performance and usable exit separately from legal survival: a perpetual asset lock can preserve collective land while collective life, maintenance, and purpose decay. Add periodic purpose review and a recharter, successor, or humane sunset path.",
        ["F-108"],
    ),
    "G-007": (
        "Perpetual ownership and continued occupancy are no more reliable as safety or flourishing evidence than cohesion or retention when the legal form makes closure and relocation difficult.",
        ["F-108"],
    ),
    "G-010": (
        "A purposive study of already stable, normatively selected communities shows that long probation exists, but cannot establish predictive validity, false-positive rates, or a causal effect on safety or survival.",
        ["F-106"],
    ),
    "G-012": (
        "A permanent trust needs scheduled mission review, conflict recusal, defined intervention duties, exit liquidity, and a recharter or sunset route; title separation must also separate appointment power. A non-pursuit ethic does not replace dual authorization, preserved accounts, or restitution.",
        ["F-107", "F-108", "F-109", "F-110"],
    ),
    "G-013": (
        "Specify who reports alleged violence, illegality, or asset diversion when internal doctrine favors nonresistance or trustees define themselves as mere land-holders; outside jurisdiction must not depend on unanimous internal reinterpretation.",
        ["F-107", "F-109"],
    ),
    "G-016": (
        "A perpetual asset entity should be able to pass land to a legitimate successor group without preserving a defunct resident culture, while protecting current residents through independent review and usable transition support.",
        ["F-108", "F-110"],
    ),
    "G-018": (
        "Volume 32 again found no evidence validating inner work or long exposure as a dangerous-person filter; its most favorable probation study selected already stable communities and reported no applicant-level safety outcomes.",
        ["F-106", "F-111"],
    ),
}


NEW_VERIFICATION_BULLETS = """- **F status:** verify the White Water preacher-treasurer's identity, alleged diversion of funds, departure, and the community's response in contemporary records; the 1881 account contains a mistaken name and the 1829 letter does not state the theft.
- **F status:** inspect the Renaissance and Wilderland trust deeds, trustee and incident records, the Wilderland High Court file, later board reforms, present property conditions, and current/former resident perspectives before naming either trust as a current governance precedent.
"""


NEW_NONPROMOTIONS = """- Oneida's stock conversion, member shares, housing rights, education and elder benefits, and planned company town materially corroborate F-022 and the adaptive-dissolution gaps but do not add a distinct danger-response mechanism.
- The seven-community sustainability study documents long probation as a practice, not a validated bad-faith or dangerous-person filter; its purposive survivor sample is recorded in F-106 as a source-limit finding.
- The new-kibbutz study provides a useful small-group advocate, subordinate veto, committee transparency, and federation model, but reports no adversarial capture test or independent later outcome beyond the continuity evidence already in F-023 and G-016.
- Euree Street's mortgage pressure forced rapid replacement with people described as non-compatible, strongly corroborating F-033 and G-015; it does not establish danger or a mechanism materially different from startup finance overriding admission criteria.
- The Hutterite review reports flexible everyday discipline but also divisive leader conflict and colony use of state policing power for religious decisions; without a specified case, evidence record, or outcome it remains a verification lead rather than a new finding.
- The Camphill review's internal research-training program and disabled-member voice work are useful models for an internal school-research function, but the review also identifies unsupported claims and scope ambiguity and supplies no independent safeguarding outcome.
- The Jonestown review corroborates leader coercion, political insulation from defectors' complaints, investigative reporting, and catastrophic late intervention already represented by F-011 and F-097; its reviewer warns that the narrative includes speculative internal thoughts.
- The Children of God review primarily presents leader interviews and movement self-description; its references to adult child molesters and later openness do not supply case-level accountability beyond F-084 and F-085.
"""


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = text.replace(
        "Checkpoint: *Communal Societies* volumes 1-31",
        "Checkpoint: *Communal Societies* volumes 1-32",
    )
    text = text.replace(
        "After reconciling the volume 31 findings rather than inflating the list",
        "After reconciling the volume 32 findings rather than inflating the list",
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
            parts[4] = parts[4].replace("through volume 31", "through volume 32")
        lines[index] = "|".join(parts)
        seen.add(gap_id)
    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(lines) + "\n"
    if "verify the White Water preacher-treasurer's identity" not in text:
        text = text.replace("\n## Explicit non-promotions\n", "\n" + NEW_VERIFICATION_BULLETS + "\n## Explicit non-promotions\n")
    if "Oneida's stock conversion" not in text:
        marker = "- The volume 1-31 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105) are bounded negative results, not evidence that intentional communities never faced or managed such children."
        assert marker in text
        text = text.replace(marker, NEW_NONPROMOTIONS + marker)
    text = text.replace(
        "The volume 1-31 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105)",
        "The volume 1-32 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111)",
    )
    GAP_BANK.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    update_ledger()
    update_inventory()
    update_gap_bank()
    print("updated ledger, inventory, and gap bank for volume 32")
