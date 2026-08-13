#!/usr/bin/env python3
"""Apply the completed volume 40 checkpoint to cumulative research artifacts."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"
REPORT = ROOT / "COMMUNITIES-V40-RESEARCH-REPORT.md"

PROMOTED_IDS = {"M-0983", "M-0985", "M-0986"}
FUNCTIONAL_METADATA_IDS = {"M-0979", "M-0980", "M-0981", "M-0987"}
ARCHIVE_RECORD_ID = "D-017"
ARCHIVE_EXPECTED = {
    "drive_size_bytes": "78015463",
    "sha256": "95f87d2210fc829ca76b7b495e24d9057db5d4acefe4c055c4f8d41bc32afb39",
    "research_status": "not processed",
    "local_path": "raw/vol35-40.zip",
    "notes": "Drive inventory row; archive downloaded and integrity-tested; members follow",
}


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    """Replace an old checkpoint anchor or confirm the new one is already present."""
    if new in text:
        return text
    if old in text:
        return text.replace(old, new, 1)
    raise AssertionError(f"missing update anchor: {label}")


def extend_once_or_confirm(text: str, anchor: str, addition: str, label: str) -> str:
    """Append to a unique prose anchor once while remaining idempotent."""
    new = anchor + addition
    if new in text:
        return text
    assert anchor in text, f"missing extension anchor: {label}"
    return text.replace(anchor, new, 1)


def validate_reconciled_evidence() -> None:
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    expected_ids = [f"F-{number:03d}" for number in range(1, 147)]
    assert [row["finding_id"] for row in rows] == expected_ids
    new_rows = rows[-4:]
    assert [row["source_record_id"] for row in new_rows] == [
        "M-0983", "M-0985", "M-0986", ""
    ]
    assert Counter(row["article_gap_status"] for row in new_rows) == Counter({
        "C": 3,
        "F": 1,
    })
    assert REPORT.is_file()
    report = REPORT.read_text(encoding="utf-8")
    assert "**4 new findings, F-143 through F-146**" in report


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
        if row["record_type"] != "archive_pdf" or row["volume"] != "40":
            continue
        record_id = row["record_id"]
        seen.add(record_id)
        if record_id in PROMOTED_IDS:
            status = "close read; finding promoted"
            disposition = "promoted"
        elif record_id in FUNCTIONAL_METADATA_IDS:
            status = "metadata triaged"
            disposition = "metadata"
        else:
            status = "contextual close read; no distinct finding"
            disposition = "contextual"
        row["text_extraction_status"] = "extracted"
        row["research_status"] = status
        row["local_path"] = f"recovered/corpus-v40/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v40/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1

    assert seen == {f"M-{number:04d}" for number in range(979, 988)}
    assert dispositions == Counter({"metadata": 4, "promoted": 3, "contextual": 2})
    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed during update: {field}"

    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    replacements = [
        (
            "Checkpoint: *Communal Societies* volumes 1-39",
            "Checkpoint: *Communal Societies* volumes 1-40",
            "gap completed boundary",
        ),
        (
            "After reconciling the volume 39 findings rather than inflating the list",
            "After reconciling the volume 40 findings rather than inflating the list",
            "gap checkpoint description",
        ),
        (
            "No processed journal evidence through volume 39 validates six months of inner work as a reliable con-artist filter.",
            "No processed journal evidence through volume 40 validates six months of inner work as a reliable con-artist filter.",
            "G-018 cumulative boundary",
        ),
        (
            "F-128, F-130 |",
            "F-128, F-130, F-145 |",
            "G-001 evidence",
        ),
        (
            "F-136, F-137 |",
            "F-136, F-137, F-145 |",
            "G-003 evidence",
        ),
        (
            "F-136, F-137, F-139 |",
            "F-136, F-137, F-139, F-143, F-144 |",
            "G-004 evidence",
        ),
        (
            "F-130, F-141 |",
            "F-130, F-141, F-145 |",
            "G-005 evidence",
        ),
        (
            "F-134, F-136, F-140, F-141 |",
            "F-134, F-136, F-140, F-141, F-143 |",
            "G-006 evidence",
        ),
        (
            "F-127, F-132 |",
            "F-127, F-132, F-143 |",
            "G-011 evidence",
        ),
        (
            "F-120, F-135, F-139 |",
            "F-120, F-135, F-139, F-143, F-144 |",
            "G-012 evidence",
        ),
        (
            "F-135, F-137 |",
            "F-135, F-137, F-144, F-145 |",
            "G-013 evidence",
        ),
        (
            "Volume 39 again found neither validation of the filter nor a complete dangerous-child actor response sequence; a one-sided success score and a consent doctrine that overrode a requested safeguard were not safety evidence.",
            "Volume 39 again found neither validation of the filter nor a complete dangerous-child actor response sequence; a one-sided success score and a consent doctrine that overrode a requested safeguard were not safety evidence. Volume 40 again found neither validation of the filter nor a complete dangerous-child actor response sequence; lifetime commitment, symbolic co-trusteeship, and a civil 'lunacy' petition against a reformer were not safety evidence.",
            "G-018 volume 40 result",
        ),
        (
            "F-140, F-141, F-142 |",
            "F-140, F-141, F-142, F-143, F-144, F-145, F-146 |",
            "G-018 evidence",
        ),
        (
            "The volume 1-39 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142) are bounded negative results",
            "The volume 1-40 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146) are bounded negative results",
            "bounded dangerous-child sequence",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)

    # Long table rows are extended at unique terminal sentences so their structure stays intact.
    prose_extensions = [
        (
            "Seniority, popularity, or a spiritual allegation cannot authorize displacement or destruction of a member's property.",
            " A civil or competency petition initiated by implicated leaders also requires conduct-specific evidence and independent review.",
            "G-001 process boundary",
        ),
        (
            "Public assent and a promise never to revise testimony cannot replace an independently preserved dissent record.",
            " A civil or clinical route requested by leaders who oppose the dissent is not independent unless intake, evidence, assessment, and review are protected from that conflict.",
            "G-003 protected dissent",
        ),
        (
            "Founder rejection must also reach enforceable occupancy and acquisition rights: authorize a durable entity, execute acceptable lease or purchase terms, and complete the control transition rather than relying on founder goodwill.",
            " Map authority separately across household, intimate relationship, employment, ownership, and executive domains; a nominal co-trustee or professional drafter is not independent when interests or beneficiary status conflict.",
            "G-004 cross-domain authority",
        ),
        (
            "A consent or equality doctrine cannot override a requested physical safeguard or make a captive adult or minor meaningfully free to accept relationship rules.",
            " Protected dissent also includes freedom from competency or clinical retaliation initiated by the authority being challenged.",
            "G-005 non-waivable dissent",
        ),
        (
            "Report positive practices separately from adverse outcomes, non-waivable harms, missing data, and comparators; an additive score must not let benefit in one domain erase failure in another.",
            " Report business solvency, ownership protection, participation, role conflicts, layoffs, and communal trust separately; an orderly liquidation is not a complete community outcome.",
            "G-006 business outcomes",
        ),
        (
            "Cross-organization work also needs a named operational owner and conflict-safe escalation: shared identity and collegial meetings do not decide who has authority, budget, duties, review responsibility, or power to transfer or close a failing program.",
            " A home/work split also fails when the same people are lovers, supervisors, and executives; preassign decision rights, recusal, affected-member voice, records, and appeal across both domains.",
            "G-011 domain conflict",
        ),
        (
            "When a departing founder holds the land, institutional continuity requires enforceable occupancy, authorized entity signatures, acceptable acquisition terms, and a completed title transition.",
            " A second trustee or professional drafter needs conflict and beneficiary review, separate advice, transparent authority and title, and a remedy that ideology cannot switch off.",
            "G-012 fiduciary conflict",
        ),
        (
            "Map operational ownership and escalation across partner organizations; legal capacity and dependence on water, transport, utilities, schooling, and markets; the legal completion of fund-release and trust conditions; and conflicts in media, medical, political, and investigative channels.",
            " External intake must also be independent of an insider petitioner: preserve the respondent's notice, representation, qualified assessment, proportionality, review, and a route for doctrinal disagreement. Community principle cannot disable lawful recourse against an adverse fiduciary.",
            "G-013 intake and remedy conflicts",
        ),
    ]
    for anchor, addition, label in prose_extensions:
        text = extend_once_or_confirm(text, anchor, addition, label)

    final_old = "- The remaining volume 39 records are functional metadata and supply no further distinct response mechanism or outcome."
    final_new = final_old + "\n" + "\n".join([
        "- Kerista's nonportable stock and retirement position corroborates F-054; the promoted F-143 is limited to cross-domain authority, conflict, consultation, and crisis governance.",
        "- The Bruderhof/BLU 'rule of silence' is a reporting-suppression lead, but the source gives no case-level application, grievance, appeal, or later outcome; it is not promoted.",
        "- The Shaker secret adult transfer, pressure to remain, exit probation, transition aid, and readmission contrasts corroborate existing dissent, family-contact, and usable-exit findings rather than creating duplicates.",
        "- The term-history article changes corpus-definition discipline but supplies no allegation-to-response-to-outcome case.",
        "- The three volume 40 child-danger candidates concern victims, students, activists, dependents, relationship-rule dissenters, and fictional or pedagogical examples—not a persistently dangerous child actor with assessment, intervention, review, and later outcome.",
        "- The remaining volume 40 records are functional metadata and supply no further distinct response mechanism or outcome.",
    ])
    text = replace_once_or_confirm(text, final_old, final_new, "volume 40 non-promotions")

    gap_lines = [line for line in text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
        "B": 8,
        "C": 7,
        "D": 3,
    })
    references = set(re.findall(r"\bF-\d{3}\b", text))
    assert references <= {f"F-{number:03d}" for number in range(1, 147)}
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = [
        ("volumes **1-39**", "volumes **1-40**", "state completed boundary"),
        (
            "**846 journal PDFs** were triaged: 341 close-read as relevant or contextual, 207 title/keyword-triaged, and 298 metadata-triaged.",
            "**855 journal PDFs** were triaged: 346 close-read as relevant or contextual, 207 title/keyword-triaged, and 302 metadata-triaged.",
            "state counts",
        ),
        (
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **142 findings** (`F-001` through `F-142`). Volume 39 added four findings: two B, one C, and one F-status bounded negative.",
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **146 findings** (`F-001` through `F-146`). Volume 40 added four findings: three C and one F-status bounded negative.",
            "state findings",
        ),
        (
            "`COMMUNITIES-V39-RESEARCH-REPORT.md` records the completed 23-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "`COMMUNITIES-V40-RESEARCH-REPORT.md` records the completed 9-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "state report",
        ),
        (
            "Every one of the 23 volume 39 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text.",
            "Every one of the 9 volume 40 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text.",
            "state corpus verification",
        ),
        (
            "Volumes **40-45** have not been processed: **138 journal PDFs**.",
            "Volumes **41-45** have not been processed: **129 journal PDFs**.",
            "state remaining boundary",
        ),
        (
            "The next bounded journal unit is volume **40: 9 PDFs**, all in issue 1.",
            "The next bounded journal unit is volume **41: 20 PDFs**, all in issue 1.",
            "state next unit",
        ),
        (
            "Volume 39 adds: a completed transition from founder-owned land to enforceable institutional occupancy and purchase rights; an explicit warning that additive success scores cannot subtract harm or missing data; a case in which communal doctrine overrode a requested physical safeguard and independent child-consent protections; and another bounded dangerous-child null.",
            "Volume 40 adds: cross-domain authority and conflict rules where communal partners are also business supervisors and executives; conflict-qualified fiduciary and deed review rather than symbolic co-trusteeship; protection against civil or clinical processes initiated to silence dissent; and another bounded dangerous-child null.",
            "state evidence summary",
        ),
        ("Do not repeat volumes 1-39.", "Do not repeat volumes 1-40.", "state resume boundary"),
        (
            "Retrieve and verify the 9 volume 40 publisher PDFs; they are all in issue 1 and form the next exact bounded journal unit.",
            "Retrieve and verify the 20 volume 41 publisher PDFs; they are all in issue 1 and form the next exact bounded journal unit.",
            "state resume next unit",
        ),
        (
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 9 extracted texts.",
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
        ("Volumes **1-39** complete", "Volumes **1-40** complete", "README boundary"),
        ("**846** journal PDFs triaged", "**855** journal PDFs triaged", "README PDF count"),
        ("**341** relevant or contextual close reads", "**346** relevant or contextual close reads", "README close reads"),
        ("**142** evidence findings (`F-001` through `F-142`)", "**146** evidence findings (`F-001` through `F-146`)", "README findings"),
        (
            "Next unit: **volume 40, 9 PDFs** (all in issue 1)",
            "Next unit: **volume 41, 20 PDFs** (all in issue 1)",
            "README next unit",
        ),
        (
            "[`recovered/COMMUNITIES-V39-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V39-RESEARCH-REPORT.md)",
            "[`recovered/COMMUNITIES-V40-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V40-RESEARCH-REPORT.md)",
            "README report link",
        ),
        ("`recovered/corpus-v39/`", "`recovered/corpus-v40/`", "README corpus path"),
        ("python recovered/test_v39_workflow.py", "python recovered/test_v40_workflow.py", "README tests"),
        ("python recovered/verify_v39.py", "python recovered/verify_v40.py", "README verifier"),
        ("all 23 PDF hashes", "all 9 PDF hashes", "README verified PDFs"),
        ("the volume-40 boundary", "the volume-41 boundary", "README next-boundary check"),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    README.write_text(text, encoding="utf-8")


def main() -> None:
    validate_reconciled_evidence()
    update_inventory()
    update_gap_bank()
    update_state()
    update_readme()
    print("updated volume40 findings=4 promoted_sources=3 contextual=2 metadata=4")


if __name__ == "__main__":
    main()
