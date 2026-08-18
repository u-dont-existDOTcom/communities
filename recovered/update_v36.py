#!/usr/bin/env python3
"""Apply the completed volume 36 checkpoint to the durable research artifacts."""

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
        finding_id="F-122",
        track="Track A communication-access mechanism for vulnerable residents",
        source_record_id="M-0892",
        source_file="004-camphill-at-seventy-five-developmental-communalism-in-process.pdf",
        journal_volume_issue_year="Vol. 36, no. 1 (2016)",
        article_title="Camphill at Seventy-Five: Developmental Communalism in Process",
        author="Daniel McKanan",
        community_group="Camphill Soltane; Camphill movement",
        page_locator="PDF p. 16; printed p. 39",
        printed_page_number="39",
        source_access="full text; author interview and participant-observation synthesis; method materials and participant outcome records not independently inspected",
        evidence_type="sympathetic outsider case synthesis based on long participant observation, site visits, and interviews",
        exact_factual_observation="McKanan reports that leaders at Camphill Soltane worked with the Council on Quality and Leadership to train coworkers and employees in ‘reliable interviewing.’ He says the practice was intended to help people, including those with limited communication skills, articulate what they value and need to build meaningful lives, and that it empowered the community to work together toward each person's goals.",
        what_source_establishes="A resident-voice system is not accessible merely because everyone is formally invited to speak. Communication support designed for people with limited speech or other communication differences can be an operational bridge between individual preference, grievance access, and community planning.",
        what_source_does_not_establish="It does not validate the method's accuracy, consent process, confidentiality, interviewer neutrality, false-positive or false-negative rate, use in disputes, protection from retaliation, or long-term effect on safety and autonomy. It does not report disabled participants' independent assessments of the practice.",
        author_interpretation="McKanan presents reliable interviewing and self-advocacy as innovations emerging in a Camphill that accepts employed staff and learns from the wider disability-rights and social-care fields.",
        alternative_interpretation="The reported empowerment may reflect broader staffing, advocacy, or organizational changes rather than the interview method itself. Interview-supported communication can also become interviewer-shaped or coercive unless the person chooses the support and it is separated from sanctions and membership decisions.",
        response_process="Partnership with an outside quality-and-leadership organization; training of coworkers and employees; supported interviews with people who may have limited communication; articulation of individual values and needs; community planning around stated goals.",
        outcome="The author reports greater self-advocacy and community coordination around individual goals. No independent participant feedback, complaint case, adverse result, durability measure, or later safeguarding outcome is supplied.",
        transferability="High for offering voluntary communication accommodations, participant-selected supporters, confidential channels, independent interpretation checks, and a firewall from discipline, membership, employment, and benefits decisions. Low for adopting a named method as validated without current disability-rights and empirical review.",
        article_gap_status="C",
        likely_article_destination="Dissent and grievance access / non-waivable voice / external partnerships",
        confidence="medium",
        external_verification_needed="yes",
        notes="Inspect the reliable-interviewing method, training, consent and confidentiality rules, participant accounts, error controls, and later Camphill outcomes before treating it as a validated safeguarding instrument. DOI: https://doi.org/10.9707/0739-1250.1214",
    ),
    finding(
        finding_id="F-123",
        track="Track A external-intervention false-positive challenge",
        source_record_id="M-0896",
        source_file="008-review-of-storming-zion-government-raids-on-religious-communities.pdf",
        journal_volume_issue_year="Vol. 36, no. 1 (2016)",
        article_title="Review of Storming Zion: Government Raids on Religious Communities",
        author="Timothy Miller",
        community_group="Religious intentional communities subjected to government raids",
        page_locator="PDF pp. 2-4; printed pp. 90-92",
        printed_page_number="90-92",
        source_access="full review; underlying book and individual raid records not inspected in this checkpoint",
        evidence_type="scholarly book review of a comparative study of government raids",
        exact_factual_observation="Miller says Wright and Palmer document dozens of raids on religious communities in several countries and argue that many were based on false premises. He reports their analysis of a pathway involving anticult organizations, angry former members who receive disproportionate attention, self-described cult experts, media uptake, and law-enforcement action. He notes that the federal operation against the Branch Davidians near Waco ended in a fire that killed more than eighty people.",
        what_source_establishes="External intervention has its own capture and false-positive risks. Government status, media repetition, former-member status, or a claimed expert label does not substitute for conduct-specific evidence, qualification, conflict disclosure, proportionality, and independent review of a coercive action.",
        what_source_does_not_establish="A four-page favorable review does not show that every raid was unjustified, adjudicate any particular allegation, establish a cross-case false-positive rate, or evaluate every warrant, child-protection concern, official decision, injury, remedy, or later reform. It does not justify discounting former members or urgent safety reports as a class.",
        author_interpretation="Miller endorses the book as meticulously documented and sees the raids as a deeply troubling pattern of bigotry and persecution strongly influenced by the anticult movement.",
        alternative_interpretation="Authorities may have had credible evidence or non-waivable protection duties in some cases, and a harmful outcome does not by itself prove that initiating an investigation was wrong. The relevant distinction is between evidence-based, proportionate action and category-driven escalation, not between intervention and nonintervention.",
        response_process="Allegations and anticult framing; self-described expertise and media amplification; agency investigation or raid; case-specific criminal, custody, or other proceedings summarized by the reviewed book; no common pre-raid evidence standard or post-raid audit is described by the review.",
        outcome="The review says the premise for many raids proved groundless and identifies catastrophic loss of life at Waco. It does not quantify outcomes across the cases or supply victim follow-up, official after-action findings, remedies, or a validated alternative protocol.",
        transferability="High for conduct-specific corroboration, expertise and conflict checks, least-restrictive intervention, child-specific lawful authority, operational proportionality, a stated stopping rule, evidence preservation, and independent after-action review. Zero for categorical distrust of government, former members, religious minorities, or child-protection reports.",
        article_gap_status="D",
        likely_article_destination="Selecting legal couplings / safety proxies / external-accountability design",
        confidence="medium-low",
        external_verification_needed="yes",
        notes="Inspect Wright and Palmer's book and each underlying raid record before naming a predicate or result as settled fact. Preserve serious allegations and child-safety concerns as evidence to assess, not facts to accept or dismiss by category. DOI: https://doi.org/10.9707/0739-1250.1218",
    ),
    finding(
        finding_id="F-124",
        track="Track A evidence preservation across organizational succession",
        source_record_id="M-0906",
        source_file="008-review-of-oneida-from-free-love-utopia-to-well-set-table.pdf",
        journal_volume_issue_year="Vol. 36, no. 2 (2016)",
        article_title="Review of Oneida: From Free Love Utopia to Well-Set Table",
        author="Thomas A. Guiler",
        community_group="Oneida Community; Oneida Limited; descendant community",
        page_locator="PDF pp. 2, 4-5; printed pp. 177, 179-180",
        printed_page_number="177, 179-180",
        source_access="full review; underlying descendant-authored book, cited study, corporate records, and repositories not independently inspected",
        evidence_type="scholarly review of a descendant-authored history",
        exact_factual_observation="Guiler reports that in 1947 a group of Oneida Limited employees, possibly including author Ellen Wayland-Smith's grandfather, loaded the contents of G. W. Noyes's Oneida Community archive onto a truck, took it to a dump, and burned it. He describes the reported archive as a large collection, says participants and motives remain uncertain, and notes that the destroyed contents cannot now be known.",
        what_source_establishes="A community's evidence system can fail after the communal phase ends. A successor corporation, descendant group, or later leadership cohort may control and destroy records needed for accountability and historical review, so preservation duties must survive changes in legal form and personnel.",
        what_source_does_not_establish="The review does not inventory the destroyed records, identify every participant, prove a motive, show whether copies survived elsewhere, establish a legal preservation duty, or independently verify the event. The proposed motives—commercial reputation, outsider exclusion, apology, or erasure—remain speculation.",
        author_interpretation="Guiler treats the burning as a revealing contradiction between Oneida's meticulous record culture and descendants' possible wish to shield family, corporate reputation, or communal memory.",
        alternative_interpretation="The destruction may have involved ordinary disposal, privacy concerns, misunderstood custody, or a narrower record set than later descriptions imply. Even so, uncertain scope and motive reinforce the need for documented retention and destruction decisions rather than proving deliberate concealment.",
        response_process="Successor-entity custody of a former community archive; reported transport and burning; later descendant research, review, and speculative reconstruction; no contemporaneous preservation review, independent repository transfer, inventory, duplication, or recovery process is reported.",
        outcome="The reported record set was irreversibly destroyed, leaving later researchers unable to determine its contents or confidently reconstruct why it was burned. The review identifies no institutional remedy or preservation reform.",
        transferability="High for independent archival custody, redundant copies, retention schedules, legal holds, privacy-sensitive access, logged destruction approvals, and succession terms binding later entities. Low for inferring misconduct from the absence of a record or treating every record as suitable for unrestricted public access.",
        article_gap_status="C",
        likely_article_destination="Protected evidence channel / founderism capture audit / plan the funeral",
        confidence="low-medium",
        external_verification_needed="yes",
        notes="Inspect Wayland-Smith's book, the sociological study mentioned by Guiler, corporate and family records, and surviving Oneida repositories before stating the event's scope, participants, or motive. DOI: https://doi.org/10.9707/0739-1250.1207",
    ),
    finding(
        finding_id="F-125",
        track="Track A child negative result",
        source_file="Volume 36 discovery corpus",
        journal_volume_issue_year="Volume 36 (2016)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volume 36",
        page_locator="21 PDFs; 17 relevant or contextual close reads; 6 child-danger proximity candidates",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 21 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 17 relevant or contextual close reads found children or young people as laborers, students, dependents, residents, alleged or actual victims, biographical or theological figures, descendants, and music audiences. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from volume 36 under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 37-45, standalone or book-length sources, different terminology, unpublished or protected records, juvenile, educational, medical, disability, or family systems, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, aggregate reporting, source destruction, and routing into professional, family, juvenile, educational, disability, or medical systems may hide relevant cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volume 36.",
        transferability="High for this completed unit; none for the full literature until the remaining journal and standalone sources are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="The cumulative bounded null now covers volumes 1-36. Children harmed, governed, educated, employed, interviewed, or represented by adults were excluded from the child-as-dangerous-actor result.",
    ),
]


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames == list(NEW_FINDINGS[0]), "ledger schema changed"
    expected_tail = ["F-122", "F-123", "F-124", "F-125"]
    if len(rows) == 125 and [row["finding_id"] for row in rows[-4:]] == expected_tail:
        rows = rows[:121]
    assert len(rows) == 121 and rows[-1]["finding_id"] == "F-121", "unexpected ledger checkpoint"
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows + NEW_FINDINGS)


CLOSE_IDS = {
    *(f"M-{number:04d}" for number in range(891, 899)),
    *(f"M-{number:04d}" for number in range(901, 910)),
}
PROMOTED_IDS = {"M-0892", "M-0896", "M-0906"}
METADATA_KINDS = {"contents", "editorial"}

ARCHIVE_RECORD_ID = "D-017"
ARCHIVE_EXPECTED = {
    "drive_size_bytes": "78015463",
    "sha256": "95f87d2210fc829ca76b7b495e24d9057db5d4acefe4c055c4f8d41bc32afb39",
    "research_status": "not processed",
    "local_path": "raw/vol35-40.zip",
    "notes": "Drive inventory row; archive downloaded and integrity-tested; members follow",
}


def update_inventory() -> None:
    with INVENTORY.open(newline="", encoding="utf-8") as handle:
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
        if row["record_type"] != "archive_pdf" or row["volume"] != "36":
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
        row["local_path"] = f"recovered/corpus-v36/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v36/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1
    assert len(seen) == 21, f"expected 21 volume 36 records, got {len(seen)}"
    assert dispositions == Counter({"contextual": 14, "metadata": 4, "promoted": 3}), dispositions
    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed during update: {field}"
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-003": (
        "A reporting channel must be communication-accessible to people with limited speech or other communication differences, and evidence preservation must survive succession through independent custody, duplication, retention rules, and logged destruction authority.",
        ["F-122", "F-124"],
    ),
    "G-004": (
        "The capture audit must follow accountability records into successor corporations and descendant bodies; control of archives can outlive formal communal authority.",
        ["F-124"],
    ),
    "G-005": (
        "The right to reply, report, and shape one's own care needs communication accommodations chosen by the person and firewalled from discipline, membership, work, and benefits decisions.",
        ["F-122"],
    ),
    "G-013": (
        "External actors need false-positive controls too: conduct-specific corroboration, qualified and conflict-disclosed expertise, least-restrictive action, proportionality, a stopping rule, evidence preservation, and independent after-action review.",
        ["F-123"],
    ),
    "G-018": (
        "A categorical cult label, media repetition, former-member status, claimed expertise, or government action is an evidence input rather than a validated danger proxy. Volume 36 again found neither evidence validating inner work or long exposure as a dangerous-person filter nor a complete dangerous-child actor response sequence.",
        ["F-123", "F-125"],
    ),
}


NEW_VERIFICATION_BULLETS = """- **F status:** inspect Camphill's reliable-interviewing method, training, consent, confidentiality, participant accounts, error controls, and later outcomes before treating it as a validated safeguarding instrument.
- **F status:** inspect *Storming Zion* and each raid's predicate, warrant, child-safety record, legal findings, injuries, remedies, and after-action review before naming any allegation or false-positive conclusion as settled fact.
- **F status:** inspect Wayland-Smith's Oneida history, the study cited by Guiler, corporate and family records, and surviving repositories before stating the 1947 archive destruction's scope, participants, or motive.
"""


NEW_NONPROMOTIONS = """- Dancing Rabbit's council, board, recall, delegated power levels, review windows, consensus redesign, and proposed background checks corroborate existing admission and governance findings; the background-check debate has no adoption or outcome record.
- The 1810 Union Village confrontation strongly corroborates F-062: civil officials, rights claims, direct inspection, and individual voluntariness interviews displaced categorical hostility and immediately defused violence, but the Shaker-centered source base does not reconstruct the original allegations or independent follow-up.
- Camphill's scheduled and surprise inspections, individualized care plans, shared-home investigation constraints, nonprofit-board authority, and Action for Botton mediation are useful external-coupling and governance context without a second independently tested safeguarding outcome.
- The ecovillage equity warning, Pinery exit-forfeiture covenant, and *Naked in the Woods* review materially corroborate F-005, F-042, F-077, F-092, F-119, and G-012 rather than adding a distinct usable-exit mechanism.
- The New Lanark review complicates benevolent paternalism through child labor, schooling, housing oversight, and workforce control but supplies no case-level grievance, review, or member outcome.
- The remaining volume 36 sources supply music, movement, succession, identity, language, founder, or historical context without a materially distinct allegation, assessment, intervention, review, and outcome sequence.
"""


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = text.replace(
        "Checkpoint: *Communal Societies* volumes 1-35",
        "Checkpoint: *Communal Societies* volumes 1-36",
    )
    text = text.replace(
        "After reconciling the volume 35 findings rather than inflating the list",
        "After reconciling the volume 36 findings rather than inflating the list",
    )
    text = text.replace(
        "No processed journal evidence through volume 35",
        "No processed journal evidence through volume 36",
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
        parts[7] = " " + evidence + " "
        lines[index] = "|".join(parts)
        seen.add(gap_id)
    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(lines) + "\n"
    if "inspect Camphill's reliable-interviewing method" not in text:
        text = text.replace("\n## Explicit non-promotions\n", "\n" + NEW_VERIFICATION_BULLETS + "\n## Explicit non-promotions\n")
    if "Dancing Rabbit's council, board, recall" not in text:
        marker = "- The volume 1-35 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121) are bounded negative results, not evidence that intentional communities never faced or managed such children."
        assert marker in text
        text = text.replace(marker, NEW_NONPROMOTIONS + marker)
    text = text.replace(
        "The volume 1-35 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121)",
        "The volume 1-36 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125)",
    )
    GAP_BANK.write_text(text, encoding="utf-8")


def replace_idempotently(text: str, replacements: dict[str, str]) -> str:
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
        else:
            assert new in text, old
    return text


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = {
        "Updated: 2026-08-12 (Africa/Dakar)": "Updated: 2026-08-13 (Africa/Dakar)",
        "*Communal Societies* volumes **1-35** are complete": "*Communal Societies* volumes **1-36** are complete",
        "**756 journal PDFs** were triaged: 276 close-read as relevant or contextual, 207 title/keyword-triaged, and 273 metadata-triaged.": "**777 journal PDFs** were triaged: 293 close-read as relevant or contextual, 207 title/keyword-triaged, and 277 metadata-triaged.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **121 findings** (`F-001` through `F-121`). Volume 35 added three findings: two C and one F-status bounded negative.": "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **125 findings** (`F-001` through `F-125`). Volume 36 added four findings: two C, one D, and one F-status bounded negative.",
        "`COMMUNITIES-V35-RESEARCH-REPORT.md` records the completed 26-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.": "`COMMUNITIES-V36-RESEARCH-REPORT.md` records the completed 21-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
        "Every one of the 26 volume 35 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `vol35-40.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.": "Every one of the 21 volume 36 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `vol35-40.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
        "Volumes **36-45** have not been processed: **228 journal PDFs**.": "Volumes **37-45** have not been processed: **207 journal PDFs**.",
        "The next bounded journal unit is volume **36: 21 PDFs**—10 in issue 1 and 11 in issue 2.": "The next bounded journal unit is volume **37: 26 PDFs**—16 in issue 1 and 10 in issue 2.",
        "Volume 35 adds: contrasting Seventh Elect court outcomes showing that external remedies are claim-specific rather than holistic; a later case in which a trusted outside manager captured assets and a restitution judgment preceded recovery by years; and another bounded dangerous-child null.": "Volume 36 adds: communication-access interviewing for residents with limited speech; a warning that categorical expertise and agency action can produce coercive false positives; reported destruction of Oneida records by a successor corporation's employees; and another bounded dangerous-child null.",
        "Do not repeat volumes 1-35.": "Do not repeat volumes 1-36.",
        "Retrieve and verify the 21 volume 36 publisher PDFs; they are the next exact bounded journal unit.": "Retrieve and verify the 26 volume 37 publisher PDFs; they are the next exact bounded journal unit.",
        "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 21 extracted texts.": "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 26 extracted texts.",
    }
    STATE.write_text(replace_idempotently(text, replacements), encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = {
        "Volumes **1-35** complete": "Volumes **1-36** complete",
        "**756** journal PDFs triaged": "**777** journal PDFs triaged",
        "**276** relevant or contextual close reads": "**293** relevant or contextual close reads",
        "**121** evidence findings (`F-001` through `F-121`)": "**125** evidence findings (`F-001` through `F-125`)",
        "Next unit: **volume 36, 21 PDFs** (10 in issue 1; 11 in issue 2)": "Next unit: **volume 37, 26 PDFs** (16 in issue 1; 10 in issue 2)",
        "[`recovered/COMMUNITIES-V35-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V35-RESEARCH-REPORT.md)": "[`recovered/COMMUNITIES-V36-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V36-RESEARCH-REPORT.md)",
        "beneath `recovered/corpus-v35/`": "beneath `recovered/corpus-v36/`",
        "python recovered/test_v35_workflow.py\npython recovered/verify_v35.py": "python recovered/test_v36_workflow.py\npython recovered/verify_v36.py",
        "all 26 PDF hashes, page counts,": "all 21 PDF hashes, page counts,",
        "the volume-36 boundary": "the volume-37 boundary",
    }
    README.write_text(replace_idempotently(text, replacements), encoding="utf-8")


if __name__ == "__main__":
    update_ledger()
    update_inventory()
    update_gap_bank()
    update_state()
    update_readme()
    print("updated ledger, inventory, gap bank, state, and README for volume 36")
