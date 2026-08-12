#!/usr/bin/env python3
"""Apply the completed volume 35 checkpoint to the durable research artifacts."""

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
        finding_id="F-119",
        track="Track A external legal scope and claim-specific remedy",
        source_record_id="M-0877",
        source_file="003-the-seventh-elect-church-in-israel-seattles-long-haired-preachers.pdf",
        journal_volume_issue_year="Vol. 35, no. 2 (2015)",
        article_title="The Seventh Elect Church in Israel: Seattle's ‘Long-Haired Preachers’",
        author="Barbara Hainley",
        community_group="Seventh Elect Church in Israel",
        page_locator="PDF pp. 18-22; printed pp. 147-151",
        printed_page_number="147-151",
        source_access="full text; cited court opinions and records not independently retrieved in this checkpoint",
        evidence_type="historical synthesis using Washington court records, church materials, census records, and contemporary press",
        exact_factual_observation="Hainley reports that in 1925 a judge ordered Daniel Salwt to return property given by a former member who expected him to cure her illness, finding that she was legally defrauded even though Salwt sincerely believed he could heal. After Salwt's death, a 1931 court awarded property to the church as trust property rather than Salwt's personal property. In 1932 the Washington Supreme Court held that former members had surrendered property under a signed free-will contract and forfeited rights on leaving, and treated Salwt's teachings as religious opinion or prophecy. In 1934 forty-nine former members sought property return and church dissolution; the judge excluded sexual testimony as unrelated to church doctrine and dismissed the suit on religious-freedom grounds.",
        what_source_establishes="External adjudication is claim- and remedy-specific. Transaction rescission, trust title, contract forfeiture, dissolution, alleged leader conduct, and religious freedom can receive different legal treatment without any one proceeding independently auditing the institution's whole safety, equity, or governance system.",
        what_source_does_not_establish="It does not establish that every judgment was legally or factually correct, that the former members' allegations were true, that every property transfer had the same inducement or contract, that the forums were practically accessible, or that current Washington or other law would produce the same results. It does not itself adjudicate threats, deprivation, sexual conduct, or member recovery.",
        author_interpretation="Hainley presents the court cases as revealing the colony's inner life and emphasizes that, apart from the 1925 property-return order and a small artist's claim, the courts found for the church and against disaffected former members.",
        alternative_interpretation="The differing results may reflect different parties, pleadings, evidence, transactions, and legal questions rather than inconsistency. The later judgments can be understood as protecting voluntary gift terms, trust ownership, and religious liberty while leaving other alleged harms outside the remedy requested or proved.",
        response_process="Individual property-return action and restitution order in 1925; post-death title litigation and 1931 trust ruling; former-member appeal and 1932 state supreme-court decision; 1934 property-and-dissolution action joined by the state; disputed testimony; exclusion of evidence; dismissal on religious-freedom grounds.",
        outcome="One former member obtained return of property tied to a healing expectation. The church retained title in the later litigation; former members were held to have forfeited surrendered property on exit; the dissolution action was dismissed. The article reports no holistic safety review, internal reform, or later outcome for the former members.",
        transferability="High for mapping each external actor's jurisdiction, question, evidence requirements, standing, remedy, stopping rule, and follow-up; high for independent advice before signing asset-surrender terms. Low for treating any historical judgment as current legal advice or a complete assessment of institutional safety.",
        article_gap_status="C",
        likely_article_destination="Fair separation / money and land / selecting legal couplings",
        confidence="medium",
        external_verification_needed="yes",
        notes="Inspect the 1925 decree, 1931 superior-court record, 1932 Washington Supreme Court opinion, 1934 pleadings and judgment, party evidence, and current law before using a legal proposition. Keep former-member allegations separately attributed. DOI: https://doi.org/10.9707/0739-1250.1235",
    ),
    finding(
        finding_id="F-120",
        track="Track A delegated professional asset capture and delayed recovery",
        source_record_id="M-0877",
        source_file="003-the-seventh-elect-church-in-israel-seattles-long-haired-preachers.pdf",
        journal_volume_issue_year="Vol. 35, no. 2 (2015)",
        article_title="The Seventh Elect Church in Israel: Seattle's ‘Long-Haired Preachers’",
        author="Barbara Hainley",
        community_group="Seventh Elect Church in Israel",
        page_locator="PDF pp. 23-24; printed pp. 152-153",
        printed_page_number="152-153",
        source_access="full text; underlying accounting, appellate, delegation, and recovery records not independently retrieved in this checkpoint",
        evidence_type="historical synthesis using a court opinion and contemporary press",
        exact_factual_observation="In 1978 the four remaining, elderly members sued Gerald L. Rogers, their business manager of ten years, for an accounting and fired him. Hainley reports that a court found Rogers had gained their trust and control of church assets by falsely representing shared interest in their beliefs and an intention to act in the church's financial interest, then diverted assets to his own account and entangled the church in investment litigation. He was ordered to make nearly $2 million in restitution; the judgment was reportedly upheld, but shielding of assets meant that it took nearly ten years for the church to acquire some property. Rogers was later convicted in separate fraud cases.",
        what_source_establishes="An actor outside the resident group is not independent merely by profession or distance. Delegated financial custody can itself become a capture point, and even a successful accounting action and restitution judgment may not produce prompt or complete recovery.",
        what_source_does_not_establish="It does not reconstruct the original engagement, signatory authority, statements, audit access, first warning, exact amount diverted or ultimately recovered, every church officer's diligence, or which modern control would have prevented the loss. The later criminal convictions concerned separate schemes and do not prove each fact in the church dispute.",
        author_interpretation="Hainley describes a protracted legal battle in which a trusted manager diverted the shrinking church's assets and resisted recovery after judgment.",
        alternative_interpretation="The case may reflect a particular fraud against a very small elderly leadership group rather than an inherent defect in using outside professionals. The outside court process did eventually establish liability and enable recovery of some assets.",
        response_process="Ten-year management relationship and practical asset control; suspected diversion; firing and accounting suit in 1978; restitution judgment; reported appellate affirmance; asset shielding; multi-year property recovery; separate later federal prosecutions.",
        outcome="The court reportedly ordered nearly $2 million in restitution. The church acquired some property only after almost ten years; the article does not state the final recovery total, loss allocation, or resulting control reforms.",
        transferability="High for bounded delegation, dual authorization, direct statements to the governed body, conflict disclosure, independent review, periodic control testing, rapid revocation and account freeze, fidelity coverage where appropriate, and a preselected reporting and recovery route. Low for treating professional status itself as evidence of either trustworthiness or danger.",
        article_gap_status="C",
        likely_article_destination="Money and land / founderism capture audit / selecting legal couplings",
        confidence="medium",
        external_verification_needed="yes",
        notes="Inspect the accounting action, appellate record, engagement and account documents, asset-recovery record, and church statements before using the figures or outcome as precedent. DOI: https://doi.org/10.9707/0739-1250.1235",
    ),
    finding(
        finding_id="F-121",
        track="Track A child negative result",
        source_file="Volume 35 discovery corpus",
        journal_volume_issue_year="Volume 35 (2015)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volume 35",
        page_locator="26 PDFs; 22 relevant or contextual close reads; 10 child-danger proximity candidates",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 26 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 22 relevant or contextual close reads found children or adolescents as alleged victims, dependents, students, relocated household members, demographic or biographical subjects, political and religious figures, or participants in ordinary exploratory youth behavior. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from volume 35 under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 36-45, standalone or book-length sources, different terminology, unpublished or protected records, juvenile, educational, medical, disability, or family systems, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, aggregate reporting, source destruction, and routing into professional, family, juvenile, educational, disability, or medical systems may hide relevant cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volume 35.",
        transferability="High for this completed unit; none for the full literature until the remaining journal and standalone sources are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="The cumulative bounded null now covers volumes 1-35. Children harmed, governed, moved, educated, or represented by adults were excluded from the child-as-dangerous-actor result.",
    ),
]


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames == list(NEW_FINDINGS[0]), "ledger schema changed"
    expected_tail = ["F-119", "F-120", "F-121"]
    if len(rows) == 121 and [row["finding_id"] for row in rows[-3:]] == expected_tail:
        rows = rows[:118]
    assert len(rows) == 118 and rows[-1]["finding_id"] == "F-118", "unexpected ledger checkpoint"
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows + NEW_FINDINGS)


CLOSE_IDS = {
    *(f"M-{number:04d}" for number in range(865, 875)),
    *(f"M-{number:04d}" for number in range(877, 889)),
}
PROMOTED_IDS = {"M-0877"}
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
        if row["record_type"] != "archive_pdf" or row["volume"] != "35":
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
        row["local_path"] = f"recovered/corpus-v35/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v35/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1
    assert len(seen) == 26, f"expected 26 volume 35 records, got {len(seen)}"
    assert dispositions == Counter({"contextual": 21, "metadata": 4, "promoted": 1}), dispositions
    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed during update: {field}"
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-001": (
        "A court ruling on one transfer, title, contract, or dissolution claim does not supply a holistic review of threats, necessities, leader conduct, equity, or safety; each concern needs its own evidence, forum, remedy, and follow-up.",
        ["F-119"],
    ),
    "G-004": (
        "The capture audit must cover delegated outsiders as well as insiders: a trusted business manager can gain practical control through representations of shared interest and loyalty.",
        ["F-120"],
    ),
    "G-012": (
        "An outside professional needs bounded authority, dual authorization, direct statements to the governed body, conflict disclosure, independent review, rapid revocation, and a recovery plan; a judgment may arrive long before assets do. A surrender contract also needs independent pre-signing advice and non-waivable protections because later religious-freedom or trust litigation may not restore member equity.",
        ["F-119", "F-120"],
    ),
    "G-013": (
        "Courts answer the claims and remedies before them; transaction rescission, trust title, forfeiture, dissolution, and religious-freedom review can set different boundaries without supplying a holistic safety audit. The external map must also include a route to report and freeze suspected diversion by the community's own outside professional.",
        ["F-119", "F-120"],
    ),
    "G-018": (
        "Volume 35 again found neither evidence validating inner work or long exposure as a dangerous-person filter nor a complete dangerous-child actor response sequence.",
        ["F-121"],
    ),
}


NEW_VERIFICATION_BULLETS = """- **F status:** inspect the Seventh Elect 1925 decree, 1931 superior-court record, 1932 Washington Supreme Court opinion, 1934 pleadings and judgment, party evidence, and current law before using its contrasting outcomes as legal precedent.
- **F status:** inspect the Rogers accounting and appellate records, engagement and account documents, asset-recovery record, and church statements before treating the reported diversion, restitution figure, or recovery as a financial-control precedent.
"""


NEW_NONPROMOTIONS = """- The Harmonist dormitory article directly documents household displacement, account consolidation, and later restoration, but the route by which members expressed discontent and its causal role in the move to Economy are inferred; F-072 already carries the reversible-trial principle.
- The kibbutz higher-education article strongly corroborates F-016 and F-018 through educational restriction, leaver stigma, youth criticism, departures, and eventual opening, but does not add a distinct mechanism.
- The Millerite-Shaker article documents targeted post-disappointment recruitment, rapid assimilation, family conflict, and quick exit while emphasizing that the reasons for departure remain unknown.
- The new Oneida synthesis materially corroborates F-009, F-022, F-049, F-056, and F-057 on leader authority, captured criticism, mental-health spiritualization, relationship hierarchy, and dissolution; it is not promoted as duplicate evidence.
- The Communal Studies Association retrospective, Louise Michel/Icaria history, and Shaker stewardship article provide institutional, political, and ecological context without a complete target response process.
- The remaining volume 35 reviews supply compressed leader, site, source, exit, conflict, youth, material-culture, or movement context without a materially distinct allegation, assessment, intervention, review, and outcome sequence.
"""


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = text.replace(
        "Checkpoint: *Communal Societies* volumes 1-34",
        "Checkpoint: *Communal Societies* volumes 1-35",
    )
    text = text.replace(
        "After reconciling the volume 34 findings rather than inflating the list",
        "After reconciling the volume 35 findings rather than inflating the list",
    )
    text = text.replace(
        "No processed journal evidence through volume 34",
        "No processed journal evidence through volume 35",
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
    if "inspect the Seventh Elect 1925 decree" not in text:
        text = text.replace("\n## Explicit non-promotions\n", "\n" + NEW_VERIFICATION_BULLETS + "\n## Explicit non-promotions\n")
    if "The Harmonist dormitory article directly documents" not in text:
        marker = "- The volume 1-34 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118) are bounded negative results, not evidence that intentional communities never faced or managed such children."
        assert marker in text
        text = text.replace(marker, NEW_NONPROMOTIONS + marker)
    text = text.replace(
        "The volume 1-34 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118)",
        "The volume 1-35 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121)",
    )
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = {
        "*Communal Societies* volumes **1-34** are complete": "*Communal Societies* volumes **1-35** are complete",
        "**730 journal PDFs** were triaged: 254 close-read as relevant or contextual, 207 title/keyword-triaged, and 269 metadata-triaged.": "**756 journal PDFs** were triaged: 276 close-read as relevant or contextual, 207 title/keyword-triaged, and 273 metadata-triaged.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **118 findings** (`F-001` through `F-118`). Volume 34 added three findings: one B, one C, and one F-status bounded negative.": "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **121 findings** (`F-001` through `F-121`). Volume 35 added three findings: two C and one F-status bounded negative.",
        "`COMMUNITIES-V34-RESEARCH-REPORT.md` records the completed 29-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.": "`COMMUNITIES-V35-RESEARCH-REPORT.md` records the completed 26-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
        "Every one of the 29 volume 34 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The `vol34.zip` archive container itself was not locally materialized, so its saved container hash and ZIP integrity were not reverified in this checkpoint.": "Every one of the 26 volume 35 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `vol35-40.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
        "Volumes **35-45** have not been processed: **254 journal PDFs**.": "Volumes **36-45** have not been processed: **228 journal PDFs**.",
        "The next bounded journal unit is volume **35: 26 PDFs**—12 in issue 1 and 14 in issue 2.": "The next bounded journal unit is volume **36: 21 PDFs**—10 in issue 1 and 11 in issue 2.",
        "Volume 34 adds: a reported outside override that supplied food to starving Pilgrim children despite the leader's order; a Bergholz case in which bundled family, property, disciplinary, and religious authority operated after reciprocal Amish peer checks were rejected; and another bounded dangerous-child null.": "Volume 35 adds: contrasting Seventh Elect court outcomes showing that external remedies are claim-specific rather than holistic; a later case in which a trusted outside manager captured assets and a restitution judgment preceded recovery by years; and another bounded dangerous-child null.",
        "Do not repeat volumes 1-34.": "Do not repeat volumes 1-35.",
        "Retrieve and verify the 26 volume 35 publisher PDFs; they are the next exact bounded journal unit.": "Retrieve and verify the 21 volume 36 publisher PDFs; they are the next exact bounded journal unit.",
        "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 26 extracted texts.": "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 21 extracted texts.",
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
        "Volumes **1-34** complete": "Volumes **1-35** complete",
        "**730** journal PDFs triaged": "**756** journal PDFs triaged",
        "**254** relevant or contextual close reads": "**276** relevant or contextual close reads",
        "**118** evidence findings (`F-001` through `F-118`)": "**121** evidence findings (`F-001` through `F-121`)",
        "Next unit: **volume 35, 26 PDFs** (12 in issue 1; 14 in issue 2)": "Next unit: **volume 36, 21 PDFs** (10 in issue 1; 11 in issue 2)",
        "[`recovered/COMMUNITIES-V34-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V34-RESEARCH-REPORT.md)": "[`recovered/COMMUNITIES-V35-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V35-RESEARCH-REPORT.md)",
        "beneath `recovered/corpus-v34/`": "beneath `recovered/corpus-v35/`",
        "python recovered/test_v34_workflow.py\npython recovered/verify_v34.py": "python recovered/test_v35_workflow.py\npython recovered/verify_v35.py",
        "all 29 PDF hashes, page counts,": "all 26 PDF hashes, page counts,",
        "the volume-35 boundary": "the volume-36 boundary",
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
    print("updated ledger, inventory, gap bank, state, and README for volume 35")
