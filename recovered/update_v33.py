#!/usr/bin/env python3
"""Apply the completed volume 33 checkpoint to the durable research artifacts."""

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
        finding_id="F-112",
        track="Track A exit dependency and dissent leverage",
        source_record_id="M-0803",
        source_file="006-the-life-and-legacy-of-count-leon-the-man-who-cleft-the-harmonie.pdf",
        journal_volume_issue_year="Vol. 33, no. 1 (2013)",
        article_title="The Life and Legacy of Count Leon: The Man Who Cleft the Harmonie",
        author="Eileen Aiken English",
        community_group="Harmony Society and New Philadelphia seceders",
        page_locator="PDF pp. 27, 32-33; printed pp. 70, 75-76",
        printed_page_number="70, 75-76",
        source_access="full text",
        evidence_type="archival historical reconstruction using society records, petitions, correspondence, depositions, and press material",
        exact_factual_observation="The article says a large dissident bloc depended on Georg and Friedrich Rapp, lacked skills needed to survive outside, had surrendered earnings and inheritances into accounts controlled by Friedrich, and was unlikely to leave individually. A Rapp document listed petition signers by family beside notes on vulnerabilities such as poverty, parents remaining, or a spouse obligated to the Society; the author says it appears to have been used to pressure reconsideration. After a failed leadership challenge, Count Leon's party financed legal representation and offered a new communal project; 176 adults with 75 children seceded together.",
        what_source_establishes="Material and family dependency can inhibit individual exit, while an opposition with no protected internal channel may become reliant on an outside charismatic sponsor whose interests, promises, and competence have not been independently tested.",
        what_source_does_not_establish="It does not prove that the vulnerability list was actually used coercively, that every dissident lacked agency or outside capacity, that Leon caused the underlying conflict, or that reliance on any outside sponsor is necessarily exploitative.",
        author_interpretation="English presents Leon as a catalyst who converted longstanding Harmonist discontent into a schism through material assistance, charismatic authority, and promises of a different communal life.",
        alternative_interpretation="The dissidents had substantial grievances and could regard Leon's resources as enabling collective bargaining and a usable exit rather than as manipulation; family-linked notes may have been informational rather than retaliatory.",
        response_process="Private discontent; prohibited contacts; dissident council and petition; failed attempt to replace leadership; counter-agreement and vulnerability file; outside-funded legal negotiation; collective secession and installment settlement.",
        outcome="A group of 176 adults and 75 children seceded. Their New Philadelphia Society later faced debt, food and medical shortages, disputed payments, and conflict before dissolving in 1833.",
        transferability="High for independent pre-exit advice, protected organizing, an exit reserve, portable skills, protected family contact, anti-retaliation rules, and neutral separation support; low for assigning motive to the historical actors without the underlying records.",
        article_gap_status="C",
        likely_article_destination="Fair separation / outward door / membership and exit",
        confidence="medium",
        external_verification_needed="yes",
        notes="Distinct from F-078, which covers settlement mechanics and escalation after secession. Verify the vulnerability document's use and the dependency claims in the underlying records. DOI: https://doi.org/10.9707/0739-1250.1281",
    ),
    finding(
        finding_id="F-113",
        track="Track A protected internal dissent and editorial asymmetry",
        source_record_id="M-0802",
        source_file="005-let-down-your-buckets-declension-and-the-debate-on-shaker-marginality.pdf",
        journal_volume_issue_year="Vol. 33, no. 1 (2013)",
        article_title='"Let Down Your Buckets": Declension and the Debate on Shaker Marginality',
        author="Wendy Wood Davis",
        community_group="United Society of Believers (Shakers)",
        page_locator="PDF pp. 22-27; printed pp. 39-44",
        printed_page_number="39-44",
        source_access="full text",
        evidence_type="historical analysis using Central Ministry journals and circulars, letters, speeches, and the official Shaker periodical",
        exact_factual_observation="During the long conservative-progressive conflict, the official Shaker monthly became a shared forum. The Central Ministry defended individual freedom to express different views and said diversity helped clarify error; it pre-screened submissions and rejected some material as too controversial but refused to silence Frederick Evans. The progressive faction nevertheless dominated early issues and Evans served as editor from 1873 to 1875, while many conservatives were reluctant to engage publicly. The dispute nearly ended the publication and continued in its pages until publication ceased in 1899.",
        what_source_establishes="A protected common forum can keep a major institutional dispute visible and inside a shared organization, but permission to speak is not equal voice when content approval, editorial appointments, submission volume, and willingness to publish are uneven.",
        what_source_does_not_establish="It does not show that the periodical prevented a schism, caused institutional survival, distributed attention fairly, improved member safety, or applied content review neutrally between factions.",
        author_interpretation="Davis concludes that neither faction won, but the debate helped participating Shakers find more modern and socially relevant voices while inherited bonds remained intact.",
        alternative_interpretation="Ministry tolerance may itself have been the decisive safeguard, while progressive dominance may have reflected greater participation and editorial skill rather than formal exclusion; shared doctrine may have sustained unity more than the publication did.",
        response_process="Official journal; open factional submissions; ministerial pre-publication review; editorial changes; complaints; a ministry circular defending diversity; continued publication and debate.",
        outcome="The factions continued to argue without a formal split described in the article; the journal continued until 1899, while membership declined and neither program achieved its full aims.",
        transferability="High for a protected internal dissent forum with transparent editorial allocation, viewpoint-neutral rules, minority access, appeal, and records; moderate for assuming that one common publication can carry every grievance.",
        article_gap_status="C",
        likely_article_destination="Founderism / protected dissent / internal research and publication",
        confidence="high",
        external_verification_needed="no",
        notes="The source documents both pluralism and asymmetry; do not flatten it into a simple success story. DOI: https://doi.org/10.9707/0739-1250.1280",
    ),
    finding(
        finding_id="F-114",
        track="Track B post-exit mutual aid and counter-accountability",
        source_record_id="M-0818",
        source_file="007-a-community-of-bruderhof-leavers-reflections-on-the-kit-hummer-process.pdf",
        journal_volume_issue_year="Vol. 33, no. 2 (2013)",
        article_title="A Community of Bruderhof Leavers: Reflections on the KIT/Hummer Process",
        author="J. Timothy Johnson and Ruth Lambach",
        community_group="Bruderhof leavers and the KIT/Hummer network",
        page_locator="PDF pp. 5-19; printed pp. 164-178",
        printed_page_number="164-178",
        source_access="full text",
        evidence_type="participant-observer qualitative case study using a purposive, self-selected focus group, publications, archives, and the authors' long involvement",
        exact_factual_observation="Leavers created the KIT newsletter in 1989; within a few years it reached about five hundred addresses and was joined by gatherings, an email network, memoir publishing, archives, and a fund that gave limited help to some leavers. Later support included college-admission letters, explanations of financial constraints, health and emergency networking, and informal aid to newer leavers. KIT kept public and private subscriber lists because some participants feared identification could jeopardize remaining family contact. The authors report strong success in contact and heritage work, mixed healing, and marginal-to-failed success in changing the Bruderhof or securing unrestricted family access.",
        what_source_establishes="An independently controlled alumni or leaver network can convert a scattered exit population into practical transition support, confidential peer contact, an archive of counter-narratives, and an external feedback constituency. Such a network can support leavers without functioning as an effective appeal or reform mechanism inside the parent institution.",
        what_source_does_not_establish="The self-selected, nonrepresentative study does not estimate outcomes for all leavers, compare participants with nonparticipants, independently verify the article's allegations about the Bruderhof, or prove that the network caused healing, educational entry, or later wellbeing.",
        author_interpretation="The authors describe KIT as a generally effective multifunctional virtual community for many participants while emphasizing its limited influence on Bruderhof conduct and family-access rules.",
        alternative_interpretation="People with unresolved or negative experiences may be more likely to participate, the network can consolidate an adversarial collective narrative, and younger leavers may prefer different channels; some nonparticipants may have moved on successfully without it.",
        response_process="Informal contact; newsletter; gatherings; email network; small fund; memoir publication and archiving; private identities; targeted educational, financial, health, and relational support.",
        outcome="The network persisted for more than two decades and supported some leavers; at the study date the Hummer had about forty-five participants and the newsletter more than two hundred addresses. The formal fund dissolved, and unrestricted family contact or institutional reform was not achieved.",
        transferability="High for an optional, independent alumni channel with confidential lists, emergency grants, education and document support, archives, gatherings, and periodic feedback; low for treating participant allegations as adjudicated facts.",
        article_gap_status="B",
        likely_article_destination="Fair separation / outward door / alumni feedback / movement continuity",
        confidence="medium",
        external_verification_needed="yes",
        notes="Do not duplicate F-051's source-limited family-contact finding. Verify the wiretap, litigation, and retaliation claims separately before naming them; the durable finding here is the leaver-network mechanism and its reported limits. DOI: https://doi.org/10.9707/0739-1250.1296",
    ),
    finding(
        finding_id="F-115",
        track="Track A child negative result",
        source_file="Volume 33 discovery corpus",
        journal_volume_issue_year="Volume 33 (2013)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volume 33",
        page_locator="36 PDFs; 28 relevant or contextual close reads; 9 child-danger proximity candidates",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 36 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 28 relevant or contextual close reads found children as dependents in mass exit, leavers or victims of adult conflict, family and schooling subjects, theological figures, fictional characters, and people near adult political or religious violence. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from volume 33 under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 34-45, standalone or book-length sources, different terminology, unpublished or protected records, juvenile, educational, medical, disability, or family systems, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, aggregate reporting, source destruction, and routing into professional, family, juvenile, educational, disability, or medical systems may hide relevant cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volume 33.",
        transferability="High for this completed unit; none for the full literature until the remaining journal and standalone sources are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="The cumulative bounded null now covers volumes 1-33. Children harmed, governed, moved, or represented by adults and children in fiction were excluded from the child-as-dangerous-actor result.",
    ),
]


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames == list(NEW_FINDINGS[0]), "ledger schema changed"
    expected_tail = [f"F-{number:03d}" for number in range(112, 116)]
    if len(rows) == 115 and [row["finding_id"] for row in rows[-4:]] == expected_tail:
        rows = rows[:111]
    assert len(rows) == 111 and rows[-1]["finding_id"] == "F-111", "unexpected ledger checkpoint"
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows + NEW_FINDINGS)


CLOSE_IDS = {
    *(f"M-{number:04d}" for number in range(801, 811)),
    *(f"M-{number:04d}" for number in range(815, 833)),
}
PROMOTED_IDS = {"M-0802", "M-0803", "M-0818"}
METADATA_KINDS = {"front_matter", "contents", "editorial", "back_matter"}

ARCHIVE_STATUS = "container not locally materialized; 36 publisher member PDFs hash-verified and triaged"
ARCHIVE_NOTE = (
    "Drive inventory row; archive container not locally materialized in this checkpoint; "
    "all 36 member PDFs independently recovered from the primary publisher and matched "
    "saved inventory SHA-256 values"
)


def update_inventory() -> None:
    with INVENTORY.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    dispositions: Counter[str] = Counter()
    seen: set[str] = set()
    for row in rows:
        # This repository is public. Preserve source metadata and hashes while
        # keeping private Drive object locators out of Git.
        if row["drive_file_id"]:
            row["drive_file_id"] = "REDACTED"
        if row["record_id"] == "D-015":
            row["research_status"] = ARCHIVE_STATUS
            row["local_path"] = ""
            row["notes"] = ARCHIVE_NOTE
        if row["record_type"] != "archive_pdf" or row["volume"] != "33":
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
        row["local_path"] = f"recovered/corpus-v33/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v33/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1
    assert len(seen) == 36, f"expected 36 volume 33 records, got {len(seen)}"
    assert dispositions == Counter({"contextual": 25, "metadata": 8, "promoted": 3}), dispositions
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-001": (
        "Exit safeguards begin before valuation: when members lack independent advice, outside skills, liquid resources, and protection from family-based leverage, organized dissent can become dependent on an untested outside sponsor.",
        ["F-112"],
    ),
    "G-003": (
        "A common publication channel needs transparent editorial allocation, viewpoint-neutral content rules, appeal, and minority access; permission to speak is not equal voice when one faction dominates submissions or editorial seats. An independent alumni channel also needs confidentiality where public participation could cost family contact.",
        ["F-113", "F-114"],
    ),
    "G-005": (
        "Protected family contact must not depend on silence about the institution or avoidance of an independent leaver association.",
        ["F-114"],
    ),
    "G-008": (
        "A leaver network can supply transition money, educational letters, emergency contacts, records, and a substitute social field; privacy protections may be essential where public participation threatens remaining family ties.",
        ["F-112", "F-114"],
    ),
    "G-012": (
        "Exit reserves and independent advice must exist before a factional rupture; otherwise common funds and sole custody can turn an ordinary departure choice into all-or-nothing collective action.",
        ["F-112"],
    ),
    "G-016": (
        "Treat an alumni network as exit and continuity infrastructure with independent communications, small grants, records, gatherings, and intergenerational succession; distinguish support and counter-accountability from actual reform of the parent institution.",
        ["F-114"],
    ),
    "G-018": (
        "Volume 33 again found neither evidence validating inner work or long exposure as a dangerous-person filter nor a complete dangerous-child actor response sequence.",
        ["F-115"],
    ),
}


NEW_VERIFICATION_BULLETS = """- **F status:** inspect the Rapp vulnerability list, petitions, accounts, secession agreement, and correspondence before treating the apparent pressure tactic, members' outside incapacity, or the fairness of the settlement as established fact.
- **F status:** verify KIT's wiretap, litigation, retaliation, and family-contact claims in court, organizational, and other participant records; study nonparticipants and younger leavers before treating the participant-observer cohort as representative.
"""


NEW_NONPROMOTIONS = """- The Count Leon article substantially corroborates F-078's settlement and escalation sequence; F-112 is limited to the distinct pre-exit dependency, vulnerability-mapping, and outside-sponsor mechanism.
- The Oneida liberation-theology reflection presents educational, material, architectural, gender, and sexual practices through a largely affirmative descendant-trustee lens; F-009, F-022, F-049, and F-056 already carry the relevant governance limits.
- The Sholem tourism reinterpretation documents foreclosure, faction, and later arrests, but later alleged conduct does not establish applicant danger or an internal screening-and-response process; its infrastructure failure remains contextual.
- The Shaker gift-drawing article and the transcribed Golden Wheel illuminate collaborative sacred authorship, racial critique, and revelation timing, but add no independent authority-validation or response mechanism beyond F-039 and F-081.
- The *Arcadia* review concerns fiction and is excluded from factual dangerous-actor evidence. The Mormon, Klan, and anti-Mormon reviews concern outside violence, public categories, or compressed biography rather than a complete internal response process.
- Reviews describing Lothlorien autonomy, Hutterite departure and rule change, Christian-community handbooks, utopian theory, communal definitions, or stability offer design ideas or broad claims without a case-level allegation, assessment, intervention, review, and outcome.
- The KIT article's wiretap, lawsuit, abuse, and family-contact allegations are not separately promoted as adjudicated facts; F-114 records the independently organized leaver network, practical supports, confidentiality choice, and self-reported limits.
"""


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = text.replace(
        "Checkpoint: *Communal Societies* volumes 1-32",
        "Checkpoint: *Communal Societies* volumes 1-33",
    )
    text = text.replace(
        "After reconciling the volume 32 findings rather than inflating the list",
        "After reconciling the volume 33 findings rather than inflating the list",
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
            parts[4] = parts[4].replace("through volume 32", "through volume 33")
        lines[index] = "|".join(parts)
        seen.add(gap_id)
    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(lines) + "\n"
    if "inspect the Rapp vulnerability list" not in text:
        text = text.replace("\n## Explicit non-promotions\n", "\n" + NEW_VERIFICATION_BULLETS + "\n## Explicit non-promotions\n")
    if "The Count Leon article substantially corroborates F-078" not in text:
        marker = "- The volume 1-32 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111) are bounded negative results, not evidence that intentional communities never faced or managed such children."
        assert marker in text
        text = text.replace(marker, NEW_NONPROMOTIONS + marker)
    text = text.replace(
        "The volume 1-32 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111)",
        "The volume 1-33 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115)",
    )
    GAP_BANK.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    update_ledger()
    update_inventory()
    update_gap_bank()
    print("updated ledger, inventory, and gap bank for volume 33")
