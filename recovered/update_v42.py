#!/usr/bin/env python3
"""Apply the completed volume 42 checkpoint to cumulative research artifacts."""

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
REPORT = ROOT / "COMMUNITIES-V42-RESEARCH-REPORT.md"

PROMOTED_IDS = {"M-0025", "M-0027"}
FUNCTIONAL_METADATA_IDS = {
    "M-0022",
    "M-0023",
    "M-0024",
    "M-0033",
    "M-0034",
    "M-0035",
    "M-0036",
    "M-0045",
}
ARCHIVE_RECORD_ID = "D-003"
ARCHIVE_EXPECTED = {
    "drive_size_bytes": "55770584",
    "sha256": "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c",
    "research_status": "not processed",
    "local_path": "raw/COMMUNAL-SOCIETIES-v41-v45.zip",
    "notes": "Drive inventory row; archive downloaded and integrity-tested; members follow",
}
ARCHIVE_RAW_ROW = (
    "D-003,drive_archive,REDACTED,COMMUNAL-SOCIETIES-v41-v45.zip,application/zip,"
    "55770584,COMMUNAL-SOCIETIES-v41-v45.zip,,,,,,,,,,"
    "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c,"
    "not_applicable,not processed,raw/COMMUNAL-SOCIETIES-v41-v45.zip,,"
    "Drive inventory row; archive downloaded and integrity-tested; members follow"
)


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
    expected_ids = [f"F-{number:03d}" for number in range(1, 152)]
    assert [row["finding_id"] for row in rows] == expected_ids
    new_rows = rows[-3:]
    assert [row["source_record_id"] for row in new_rows] == ["M-0025", "M-0027", ""]
    assert Counter(row["article_gap_status"] for row in new_rows) == Counter({
        "C": 2,
        "F": 1,
    })
    assert REPORT.is_file()
    report = REPORT.read_text(encoding="utf-8")
    assert "**3 new findings, F-149 through F-151**" in report


def update_inventory() -> None:
    raw_before = INVENTORY.read_text(encoding="utf-8-sig")
    assert raw_before.splitlines().count(ARCHIVE_RAW_ROW) == 1

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
        if row["record_type"] != "archive_pdf" or row["volume"] != "42":
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
        relative = Path(row["internal_filename"]).relative_to("archive")
        row["text_extraction_status"] = "extracted"
        row["research_status"] = status
        row["local_path"] = f"recovered/corpus-v42/{relative.as_posix()}"
        row["text_path"] = f"recovered/corpus-v42/{relative.with_suffix('.txt').as_posix()}"
        dispositions[disposition] += 1

    assert seen == {f"M-{number:04d}" for number in range(22, 46)}
    assert dispositions == Counter({"contextual": 14, "metadata": 8, "promoted": 2})
    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed during update: {field}"

    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    raw_after = INVENTORY.read_text(encoding="utf-8-sig")
    assert raw_after.splitlines().count(ARCHIVE_RAW_ROW) == 1, "D-003 row changed byte-for-byte"


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    replacements = [
        (
            "Checkpoint: *Communal Societies* volumes 1-41",
            "Checkpoint: *Communal Societies* volumes 1-42",
            "gap completed boundary",
        ),
        (
            "After reconciling the volume 41 findings rather than inflating the list",
            "After reconciling the volume 42 findings rather than inflating the list",
            "gap checkpoint description",
        ),
        (
            "No processed journal evidence through volume 41 validates six months of inner work as a reliable con-artist filter.",
            "No processed journal evidence through volume 42 validates six months of inner work as a reliable con-artist filter.",
            "G-018 cumulative boundary",
        ),
        (
            "F-130, F-141, F-145 |",
            "F-130, F-141, F-145, F-149, F-150 |",
            "G-005 evidence",
        ),
        (
            "F-136, F-140, F-141, F-143 |",
            "F-136, F-140, F-141, F-143, F-150 |",
            "G-006 evidence",
        ),
        (
            "F-099, F-104, F-112, F-114 |",
            "F-099, F-104, F-112, F-114, F-150 |",
            "G-008 evidence",
        ),
        (
            "F-104, F-116, F-126, F-141 |",
            "F-104, F-116, F-126, F-141, F-149, F-150 |",
            "G-009 evidence",
        ),
        (
            "F-137, F-144, F-145, F-147 |",
            "F-137, F-144, F-145, F-147, F-149 |",
            "G-013 evidence",
        ),
        (
            "F-029, F-043, F-084 |",
            "F-029, F-043, F-084, F-150 |",
            "G-017 evidence",
        ),
        (
            "Volume 41 again found neither validation of the filter nor a complete dangerous-child actor response sequence; a mandatory complaint forum, outward conformity, and managed answers to an outside psychologist were not safety evidence.",
            "Volume 41 again found neither validation of the filter nor a complete dangerous-child actor response sequence; a mandatory complaint forum, outward conformity, and managed answers to an outside psychologist were not safety evidence. Volume 42 again found neither validation of the filter nor a complete dangerous-child actor response sequence; adult-defined openness, positive memories, and broad social-sustainability correlations were not safety evidence.",
            "G-018 volume 42 result",
        ),
        (
            "F-146, F-147, F-148 |",
            "F-146, F-147, F-148, F-149, F-150, F-151 |",
            "G-018 evidence",
        ),
        (
            "The volume 1-41 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148) are bounded negative results",
            "The volume 1-42 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148, F-151) are bounded negative results",
            "bounded dangerous-child sequence",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)

    prose_extensions = [
        (
            "State non-waivable rights: bodily safety, sleep, food, independent medical access, private thought, outside and family contact, relationship choice, education, child advocacy, reply and appeal, and freedom from violence, deprivation, or secret adjudication.",
            " Private bathing and sleeping space are part of bodily safety, and collective care cannot assign a child substitute-parent duties without age-appropriate limits, a protected refusal right, and named adult accountability.",
            "G-005 child privacy and caregiving",
        ),
        (
            "Report positive practices separately from adverse outcomes, non-waivable harms, missing data, and comparators; an additive score must not let benefit in one domain erase failure in another.",
            " Report child benefits separately from deprivation, role overload, family-bond loss, transition shock, and later outcomes.",
            "G-006 child outcome separation",
        ),
        (
            "For minor children, the outward door begins with verified lawful custody and consent, preserved contact and location records, and an independent route when adults disagree.",
            " When a minor leaves with adults, supply immediate orientation, schooling and health continuity, records, protected family restoration, and age-appropriate reintegration support rather than postponing the outward door until adulthood.",
            "G-008 minor transition",
        ),
        (
            "Independent child advocacy must remain effective when adult leadership invokes communal doctrine to reject requested safety or consent safeguards.",
            " Safeguarding also requires child-controlled bathing and sleeping boundaries, named adult supervision, and a bar on using an older child as a substitute caregiver beyond age and capacity.",
            "G-009 physical and role safeguards",
        ),
        (
            "External researchers and evaluators need direct private access, confidentiality limits, retaliation-safe follow-up, and a way to preserve and correct discrepant accounts.",
            " Child-protection and housing review should audit private bathing and sleeping space and access boundaries rather than assume adult collective consent governs minors.",
            "G-013 child-safe housing review",
        ),
        (
            "Written child education and health standards require independent implementation evidence and a route for children to report failures outside the authority chain.",
            " The implementation audit should include adequate schooling and continuity when a minor leaves, not only written standards.",
            "G-017 education continuity",
        ),
    ]
    for anchor, addition, label in prose_extensions:
        text = extend_once_or_confirm(text, anchor, addition, label)

    verification_anchor = (
        "- **F status:** inspect Kerista's Gestalt-o-Rama rules and records, participant accounts across positions and periods, the psychologist's book and interview materials, confidentiality conditions, and later corrections before assigning conduct, motive, prevalence, or research fault."
    )
    verification_new = verification_anchor + "\n" + "\n".join([
        "- **F status:** inspect the Centrepoint interview record, retrospective child studies, plans and rules, participant accounts, police and court records, and child-protection records before identifying an offender or assigning prevalence, legal findings, or causal shares.",
        "- **F status:** inspect Israel's memoir, diary provenance, interviews, other child and adult accounts, Love Family rules, school and health records, and official records before assigning group-wide prevalence, authority, motive, diagnosis, or causation.",
    ])
    text = replace_once_or_confirm(text, verification_anchor, verification_new, "F-149 and F-150 verification queue")

    final_old = (
        "- The remaining volume 41 articles and reviews supply exit, succession, labor, material-culture, governance, disability, heritage, external-context, or source-method corroboration without a further materially distinct response mechanism and outcome; four records are functional metadata."
    )
    final_new = final_old + "\n" + "\n".join([
        "- F-149 is limited to child-specific physical privacy and safeguarding-by-design. It does not identify the alleged offender, equate every open plan with abuse, or claim that doors alone form a protection system.",
        "- F-150 preserves Altus's source-quality warning and Rachel Israel's positive as well as adverse memories; it does not generalize one memoir to every child or diagnose the cause of later distress.",
        "- East Wind's labor protocol, social enforcement, removable managers, burnout, sanitation resignation, and unresolved advertising conflict deepen existing governance, labor, and success cautions without an independently reviewed safety outcome.",
        "- The six-community social-sustainability study's support, shared vision, egalitarian governance, privacy, volunteer, founder, and rule findings corroborate existing gaps; its small cross-sectional English-accessible sample cannot establish causation or universal effects.",
        "- Laurieston Hall and Lifespan, Fourierist afterlives, gendered labor, marketing, visual-source provenance, early Latter-day Saint communalism, spiritual memoir, food networks, and fiction supply corroboration or source leads rather than materially distinct response mechanisms.",
        "- The seven volume 42 child-danger candidates concern alleged or reported victims, dependents, students, community members, substitute caregivers, family-form examples, and fictional or unrelated lexical proximity—not a persistently dangerous child actor with assessment, intervention, review, and later outcome.",
        "- The remaining volume 42 records are functional metadata and supply no further distinct response mechanism or outcome.",
    ])
    text = replace_once_or_confirm(text, final_old, final_new, "volume 42 non-promotions")

    gap_lines = [line for line in text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
        "B": 8,
        "C": 7,
        "D": 3,
    })
    references = set(re.findall(r"\bF-\d{3}\b", text))
    assert references <= {f"F-{number:03d}" for number in range(1, 152)}
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = [
        ("volumes **1-41**", "volumes **1-42**", "state completed boundary"),
        (
            "**875 journal PDFs** were triaged: 362 close-read as relevant or contextual, 207 title/keyword-triaged, and 306 metadata-triaged.",
            "**899 journal PDFs** were triaged: 378 close-read as relevant or contextual, 207 title/keyword-triaged, and 314 metadata-triaged.",
            "state counts",
        ),
        (
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **148 findings** (`F-001` through `F-148`). Volume 41 added two findings: one C and one F-status bounded negative.",
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **151 findings** (`F-001` through `F-151`). Volume 42 added three findings: two C and one F-status bounded negative.",
            "state findings",
        ),
        (
            "`COMMUNITIES-V41-RESEARCH-REPORT.md` records the completed 20-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "`COMMUNITIES-V42-RESEARCH-REPORT.md` records the completed 24-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "state report",
        ),
        (
            "Every one of the 20 volume 41 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `COMMUNAL-SOCIETIES-v41-v45.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
            "Every one of the 24 volume 42 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `COMMUNAL-SOCIETIES-v41-v45.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
            "state corpus verification",
        ),
        (
            "Volumes **42-45** have not been processed: **109 journal PDFs**.",
            "Volumes **43-45** have not been processed: **85 journal PDFs**.",
            "state remaining boundary",
        ),
        (
            "The next bounded journal unit is volume **42: 24 PDFs**, split evenly across issues 1 and 2.",
            "The next bounded journal unit is volume **43: 37 PDFs**, with 20 in issue 1 and 17 in issue 2.",
            "state next unit",
        ),
        (
            "Volume 41 adds: protection against a required complaint-and-growth forum becoming a founder's discipline channel; independent participant access and correction safeguards for outside evaluation; and another bounded dangerous-child null.",
            "Volume 42 adds: child-controlled privacy and safeguarding-by-design for bathing and sleeping space; named adult accountability, age-appropriate limits, protected family bonds, and transition support in collective childrearing; and another bounded dangerous-child null.",
            "state evidence summary",
        ),
        ("Do not repeat volumes 1-41.", "Do not repeat volumes 1-42.", "state resume boundary"),
        (
            "Retrieve and verify the 24 volume 42 publisher PDFs; 12 are in issue 1 and 12 are in issue 2, together forming the next exact bounded journal unit.",
            "Retrieve and verify the 37 volume 43 publisher PDFs; 20 are in issue 1 and 17 are in issue 2, together forming the next exact bounded journal unit.",
            "state resume next unit",
        ),
        (
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 24 extracted texts.",
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 37 extracted texts.",
            "state resume corpus size",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = [
        ("Volumes **1-41** complete", "Volumes **1-42** complete", "README completed boundary"),
        ("**875** journal PDFs triaged", "**899** journal PDFs triaged", "README total"),
        (
            "**362** relevant or contextual close reads",
            "**378** relevant or contextual close reads",
            "README close reads",
        ),
        (
            "**148** evidence findings (`F-001` through `F-148`)",
            "**151** evidence findings (`F-001` through `F-151`)",
            "README findings",
        ),
        (
            "Next unit: **volume 42, 24 PDFs** (12 in issue 1; 12 in issue 2)",
            "Next unit: **volume 43, 37 PDFs** (20 in issue 1; 17 in issue 2)",
            "README next unit",
        ),
        (
            "[`recovered/COMMUNITIES-V41-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V41-RESEARCH-REPORT.md)",
            "[`recovered/COMMUNITIES-V42-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V42-RESEARCH-REPORT.md)",
            "README latest report",
        ),
        (
            "With the exact local source corpus restored beneath `recovered/corpus-v41/`, run:",
            "With the exact local source corpus restored beneath `recovered/corpus-v42/`, run:",
            "README corpus path",
        ),
        ("python recovered/test_v41_workflow.py", "python recovered/test_v42_workflow.py", "README tests"),
        ("python recovered/verify_v41.py", "python recovered/verify_v42.py", "README verifier"),
        (
            "The verifier checks all 20 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-42 boundary.",
            "The verifier checks all 24 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-43 boundary.",
            "README verification scope",
        ),
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
    print("updated volume 42 checkpoint")


if __name__ == "__main__":
    main()
