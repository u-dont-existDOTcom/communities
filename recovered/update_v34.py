#!/usr/bin/env python3
"""Apply the completed volume 34 checkpoint to the durable research artifacts."""

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
        finding_id="F-116",
        track="Track A non-waivable child necessities and external override",
        source_record_id="M-0839",
        source_file="006-mummyjum-the-shaker-pilgrim-encounter-of-1817-1818.pdf",
        journal_volume_issue_year="Vol. 34, no. 1 (2014)",
        article_title="Mummy Jum: The Shaker-Pilgrim Encounter of 1817-1818",
        author="Christian Goodwillie",
        community_group="Isaac Bullard's Pilgrims; Union Village Shakers",
        page_locator="PDF pp. 20, 23; printed pp. 73, 76",
        printed_page_number="73, 76",
        source_access="full text",
        evidence_type="historical synthesis using newspapers, Shaker journals and correspondence, and published travel narratives",
        exact_factual_observation="Goodwillie reports from Timothy Flint that the New Madrid County sheriff brought provisions to the Pilgrims' island and stood guard while starving children ate against Isaac Bullard's orders. Goodwillie later reports that Thomas Nuttall was told two other children had been taken from the remnant group because of their condition. Some former Pilgrims separately left, received assistance, and later joined the Shakers.",
        what_source_establishes="The source reports outside actors bypassing a leader's control of food to meet children's immediate needs, followed by a separate report of child removal. It shows why basic necessities and child protection need a route that does not depend on the implicated authority chain's consent.",
        what_source_does_not_establish="It does not identify the sheriff's legal authority, an assessment standard, who ordered or carried out the child removal, whether it was temporary or permanent, the children's identities, or their later outcomes. It does not independently verify Flint's or Nuttall's information and does not concern a dangerous child actor.",
        author_interpretation="Goodwillie presents the Pilgrim story as a tragic encounter in which the Shakers gained converts and may have saved some lives, while treating several contemporary accounts critically.",
        alternative_interpretation="Hostile newspapers and observers may have sensationalized the group; the sheriff episode may have been one-time relief rather than a child-protection system, and adult departures also reflected individual agency rather than external rescue alone.",
        response_process="Severe deprivation and illness; outside observation and concern; sheriff arrival with provisions; guarded access to food despite the leader's order; later reported removal of two children; voluntary exits and reception of some survivors by another community.",
        outcome="The reported intervention allowed starving children to eat immediately. A later informant said two other children had been removed, but no placement or long-term outcome is given. Ten former Pilgrims were reportedly living with the Shakers by April 1820.",
        transferability="High for non-waivable food and urgent health access, confidential child reporting, an independent child advocate, and a lawful external trigger with documented follow-up; zero for copying armed coercion or historical child removal without modern legal process.",
        article_gap_status="C",
        likely_article_destination="Children / non-waivable rights / selecting external couplings",
        confidence="low-medium",
        external_verification_needed="yes",
        notes="Verify Flint, Nuttall, any New Madrid County record, and family outcomes before using this as a legal precedent. The finding concerns protection from an adult leader, not the dangerous-child branch. DOI: https://doi.org/10.9707/0739-1250.1252",
    ),
    finding(
        finding_id="F-117",
        track="Track A leader capture, isolation, and disabled peer checks",
        source_record_id="M-0861",
        source_file="010-review-of-renegade-amish-beard-cutting-hate-crimes-and-the-trial-of-the-bergholz-barbers.pdf",
        journal_volume_issue_year="Vol. 34, no. 2 (2014)",
        article_title="Review of Renegade Amish: Beard Cutting, Hate Crimes, and the Trial of the Bergholz Barbers",
        author="Lynn S. Neal",
        community_group="Bergholz Amish community",
        page_locator="PDF pp. 2-4; printed pp. 225-227",
        printed_page_number="225-227",
        source_access="full review; underlying book not inspected in this checkpoint",
        evidence_type="scholarly book review of a reconstruction based on legal documents, Amish newsletters, interviews, and the book author's prosecution-expert role",
        exact_factual_observation="The review says Bishop Sam Mullet increasingly separated Bergholz from other Amish communities, excommunicated challengers, rejected other Amish leaders' authority, owned most of the land, and led followers who were largely immediate or extended family. The review attributes failure of the usual checks on a bishop to this isolation and centralization. Internal confinement, paddling, and hair-cutting practices preceded five attacks on disapproving relatives and perceived critics; sixteen defendants were convicted as of the review's publication.",
        what_source_establishes="The reviewed case links the disabling of reciprocal peer checks with a bundle of familial, patriarchal, ecclesiastical, disciplinary, and property authority. It also supplies a sequence in which internal punitive practices were redirected toward outside critics before external criminal prosecution occurred.",
        what_source_does_not_establish="A four-page review cannot isolate causation, establish every participant's voluntariness or individual responsibility, evaluate victim recovery, generalize to Amish life, or provide the case's later appellate and sentencing history. It does not show that kinship, heterodoxy, separation, or charismatic leadership is itself a danger signal.",
        author_interpretation="The reviewer reports Kraybill's analysis that divergence, isolation, and centralized authority prevented ordinary checks from operating, while criticizing the book's limited comparison and its failure to examine the author's prosecution role.",
        alternative_interpretation="Theological difference and kinship/property structure may be context rather than causes; responsibility for the attacks remains individual, and the broader dispute and criminal-law issues require the underlying record.",
        response_process="Challenges followed by excommunication and rejection of outside religious authority; emergence of internal punitive rituals; an idea to apply hair cutting to outsiders; five attacks over two months; arrest, FBI prosecution, joint trial, and convictions reported at the publication date.",
        outcome="The review reports that all sixteen defendants, including Mullet, were convicted at the 2012 trial. It gives no victim follow-up, internal reform, appellate result, resentencing, or later community outcome.",
        transferability="High for auditing whether one person can combine title, family leverage, discipline, religious office, and complaint control while severing reciprocal peer review; high for protecting critics and leavers; low for treating isolation, kinship, or doctrinal difference as safety proxies.",
        article_gap_status="B",
        likely_article_destination="Founderism / capture audit / external accountability",
        confidence="medium",
        external_verification_needed="yes",
        notes="Inspect Kraybill's book, the federal docket and appeals, victims' accounts, and post-2014 outcomes before stating final legal results. Do not adopt or diagnose from the review's cult discussion. DOI: https://doi.org/10.9707/0739-1250.1274",
    ),
    finding(
        finding_id="F-118",
        track="Track A child negative result",
        source_file="Volume 34 discovery corpus",
        journal_volume_issue_year="Volume 34 (2014)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volume 34",
        page_locator="29 PDFs; 21 relevant or contextual close reads; 5 child-danger proximity candidates",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 29 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 21 relevant or contextual close reads found children or adolescents as alleged victims of adult discipline and deprivation, dependents, family and schooling subjects, and people near adult conflict. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from volume 34 under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 35-45, standalone or book-length sources, different terminology, unpublished or protected records, juvenile, educational, medical, disability, or family systems, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, aggregate reporting, source destruction, and routing into professional, family, juvenile, educational, disability, or medical systems may hide relevant cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volume 34.",
        transferability="High for this completed unit; none for the full literature until the remaining journal and standalone sources are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="The cumulative bounded null now covers volumes 1-34. Children harmed, governed, moved, or represented by adults were excluded from the child-as-dangerous-actor result.",
    ),
]


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames == list(NEW_FINDINGS[0]), "ledger schema changed"
    expected_tail = ["F-116", "F-117", "F-118"]
    if len(rows) == 118 and [row["finding_id"] for row in rows[-3:]] == expected_tail:
        rows = rows[:115]
    assert len(rows) == 115 and rows[-1]["finding_id"] == "F-115", "unexpected ledger checkpoint"
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows + NEW_FINDINGS)


CLOSE_IDS = {
    *(f"M-{number:04d}" for number in range(837, 851)),
    *(f"M-{number:04d}" for number in range(855, 862)),
}
PROMOTED_IDS = {"M-0839", "M-0861"}
METADATA_KINDS = {"front_matter", "table_of_contents", "contents", "editorial", "back_matter"}

ARCHIVE_STATUS = "container not locally materialized; 29 publisher member PDFs hash-verified and triaged"
ARCHIVE_NOTE = (
    "Drive inventory row; archive container not locally materialized in this checkpoint; "
    "all 29 member PDFs independently recovered from the primary publisher and matched "
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
        if row["drive_file_id"]:
            row["drive_file_id"] = "REDACTED"
        if row["record_id"] == "D-016":
            row["research_status"] = ARCHIVE_STATUS
            row["local_path"] = ""
            row["notes"] = ARCHIVE_NOTE
        if row["record_type"] != "archive_pdf" or row["volume"] != "34":
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
        row["local_path"] = f"recovered/corpus-v34/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v34/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1
    assert len(seen) == 29, f"expected 29 volume 34 records, got {len(seen)}"
    assert dispositions == Counter({"contextual": 19, "metadata": 8, "promoted": 2}), dispositions
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-004": (
        "Audit whether a leader can sever reciprocal peer oversight or expel challengers while combining family, property, disciplinary, and spiritual authority; nominal affiliation is not a check when its jurisdiction can be rejected unilaterally.",
        ["F-117"],
    ),
    "G-005": (
        "Food and urgent care for children require a non-waivable route around any leader or authority chain that blocks necessities.",
        ["F-116"],
    ),
    "G-007": (
        "Obedience, humility, and harmony are not safety evidence when challengers can be expelled, peer authority rejected, and internal punishment redirected toward critics.",
        ["F-117"],
    ),
    "G-009": (
        "Independent child advocacy must include operative authority to secure basic necessities and trigger lawful protective review when the internal authority chain refuses.",
        ["F-116"],
    ),
    "G-013": (
        "The emergency map must identify who can supply children's basic necessities over internal objection, the lawful trigger for intervention, and who records placement and later outcomes; episodic relief is not a complete protection process.",
        ["F-116"],
    ),
    "G-018": (
        "Volume 34 again found neither evidence validating inner work or long exposure as a dangerous-person filter nor a complete dangerous-child actor response sequence.",
        ["F-118"],
    ),
}


NEW_VERIFICATION_BULLETS = """- **F status:** inspect Flint, Nuttall, any New Madrid County record, and family outcomes before treating the Pilgrim sheriff episode or reported child removal as a legal or safeguarding precedent.
- **F status:** inspect Kraybill's book, the Bergholz federal docket and appeals, victims' accounts, and post-2014 outcomes before presenting the review's convictions or causal sequence as final.
"""


NEW_NONPROMOTIONS = """- The Strang coronation article documents secret government concepts, disputed revelation, insider prestige, loyalty oaths, and ritual founder legitimation; it corroborates founder-capture evidence but supplies no allegation-to-review-to-outcome process.
- The four-community food study documents consensus-oriented governance, nonviolent-communication training, a conflict committee, restorative circles, and nested subcommunities, but tests no dangerous-actor response or independent outcome.
- The Icarian letter's claim that one faction denied medicine to another is relayed by a former member at a distance and lacks a case record, response, or outcome.
- The Shaker print-history article is a provenance warning about partisan allegations, rebuttals, affidavits, suppression, and later recollection; it does not adjudicate the abuse claims or the expulsion-suicide footnote it reports.
- The Las Gaviotas article is explicitly a charismatic founder's public account of consensus, accounting, work, education, and sustainability, without independent member evidence or adversarial governance testing.
- The Ananda reflection is written by a community member and interprets leadership, litigation, departures, and success largely through founder, leader, counsel, and community sources; existing G-006 and G-007 already carry the success-metric warning, while the court and governance claims remain a verification lead.
- The remaining volume 34 reviews supply movement history, institutional context, broad design claims, or retrieval leads without a materially distinct allegation, assessment, intervention, review, and outcome sequence.
"""


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = text.replace(
        "Checkpoint: *Communal Societies* volumes 1-33",
        "Checkpoint: *Communal Societies* volumes 1-34",
    )
    text = text.replace(
        "After reconciling the volume 33 findings rather than inflating the list",
        "After reconciling the volume 34 findings rather than inflating the list",
    )
    text = text.replace(
        "No processed journal evidence through volume 33",
        "No processed journal evidence through volume 34",
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
        lines[index] = "|".join(parts)
        seen.add(gap_id)
    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(lines) + "\n"
    if "inspect Flint, Nuttall" not in text:
        text = text.replace("\n## Explicit non-promotions\n", "\n" + NEW_VERIFICATION_BULLETS + "\n## Explicit non-promotions\n")
    if "The Strang coronation article documents secret government concepts" not in text:
        marker = "- The volume 1-33 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115) are bounded negative results, not evidence that intentional communities never faced or managed such children."
        assert marker in text
        text = text.replace(marker, NEW_NONPROMOTIONS + marker)
    text = text.replace(
        "The volume 1-33 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115)",
        "The volume 1-34 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118)",
    )
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = {
        "*Communal Societies* volumes **1-33** are complete": "*Communal Societies* volumes **1-34** are complete",
        "**701 journal PDFs** were triaged: 233 close-read as relevant or contextual, 207 title/keyword-triaged, and 261 metadata-triaged.": "**730 journal PDFs** were triaged: 254 close-read as relevant or contextual, 207 title/keyword-triaged, and 269 metadata-triaged.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **115 findings** (`F-001` through `F-115`). Volume 33 added four findings: one B, two C, and one F-status bounded negative.": "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **118 findings** (`F-001` through `F-118`). Volume 34 added three findings: one B, one C, and one F-status bounded negative.",
        "`COMMUNITIES-V33-RESEARCH-REPORT.md` records the completed 36-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.": "`COMMUNITIES-V34-RESEARCH-REPORT.md` records the completed 29-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
        "Every one of the 36 volume 33 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, and has nonempty extracted text. The `vol33.zip` archive container itself was not locally materialized, so its saved container hash and ZIP integrity were not reverified in this checkpoint.": "Every one of the 29 volume 34 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The `vol34.zip` archive container itself was not locally materialized, so its saved container hash and ZIP integrity were not reverified in this checkpoint.",
        "Volumes **34-45** have not been processed: **283 journal PDFs**.": "Volumes **35-45** have not been processed: **254 journal PDFs**.",
        "The next bounded journal unit is volume **34: 29 PDFs**—18 in issue 1 and 11 in issue 2.": "The next bounded journal unit is volume **35: 26 PDFs**—12 in issue 1 and 14 in issue 2.",
        "Volume 33 adds: a pre-exit Harmony case in which material dependence, limited outside skills, sole financial custody, and apparent family-vulnerability mapping left an organized dissident bloc reliant on Count Leon's external sponsorship; a Shaker publication channel that protected continuing factional debate while editorial control and participation remained asymmetric; a Bruderhof leaver network that provided contact, limited aid, educational and health support, confidential participation, and a counter-archive but did not secure unrestricted family contact or reform the parent institution; and another bounded dangerous-child null.": "Volume 34 adds: a reported outside override that supplied food to starving Pilgrim children despite the leader's order; a Bergholz case in which bundled family, property, disciplinary, and religious authority operated after reciprocal Amish peer checks were rejected; and another bounded dangerous-child null.",
        "Do not repeat volumes 1-33.": "Do not repeat volumes 1-34.",
        "Retrieve and verify the volume 34 source container; its 29 journal PDFs are the next exact bounded unit.": "Retrieve and verify the 26 volume 35 publisher PDFs; they are the next exact bounded journal unit.",
        "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 29 extracted texts.": "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 26 extracted texts.",
    }
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
        else:
            assert new in text, old
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = {
        "Volumes **1-33** complete": "Volumes **1-34** complete",
        "**701** journal PDFs triaged": "**730** journal PDFs triaged",
        "**233** relevant or contextual close reads": "**254** relevant or contextual close reads",
        "**115** evidence findings (`F-001` through `F-115`)": "**118** evidence findings (`F-001` through `F-118`)",
        "Next unit: **volume 34, 29 PDFs** (18 in issue 1; 11 in issue 2)": "Next unit: **volume 35, 26 PDFs** (12 in issue 1; 14 in issue 2)",
        "[`recovered/COMMUNITIES-V33-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V33-RESEARCH-REPORT.md)": "[`recovered/COMMUNITIES-V34-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V34-RESEARCH-REPORT.md)",
        "beneath `recovered/corpus-v33/`": "beneath `recovered/corpus-v34/`",
        "python recovered/test_v33_workflow.py\npython recovered/verify_v33.py": "python recovered/test_v34_workflow.py\npython recovered/verify_v34.py",
        "all 36 PDF hashes": "all 29 PDF hashes, page counts,",
        "the volume-34 boundary": "the volume-35 boundary",
    }
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
        else:
            assert new in text, old
    README.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    update_ledger()
    update_inventory()
    update_gap_bank()
    update_state()
    update_readme()
    print("updated ledger, inventory, gap bank, state, and README for volume 34")
