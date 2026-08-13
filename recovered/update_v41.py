#!/usr/bin/env python3
"""Apply the completed volume 41 checkpoint to cumulative research artifacts."""

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
REPORT = ROOT / "COMMUNITIES-V41-RESEARCH-REPORT.md"

PROMOTED_IDS = {"M-0018"}
FUNCTIONAL_METADATA_IDS = {"M-0004", "M-0019", "M-0020", "M-0021"}
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
    expected_ids = [f"F-{number:03d}" for number in range(1, 149)]
    assert [row["finding_id"] for row in rows] == expected_ids
    new_rows = rows[-2:]
    assert [row["source_record_id"] for row in new_rows] == ["M-0018", ""]
    assert Counter(row["article_gap_status"] for row in new_rows) == Counter({
        "C": 1,
        "F": 1,
    })
    assert REPORT.is_file()
    report = REPORT.read_text(encoding="utf-8")
    assert "**2 new findings, F-147 through F-148**" in report


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
        if row["record_type"] != "archive_pdf" or row["volume"] != "41":
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
        row["local_path"] = f"recovered/corpus-v41/{relative.as_posix()}"
        row["text_path"] = f"recovered/corpus-v41/{relative.with_suffix('.txt').as_posix()}"
        dispositions[disposition] += 1

    assert seen == {f"M-{number:04d}" for number in range(2, 22)}
    assert dispositions == Counter({"contextual": 15, "metadata": 4, "promoted": 1})
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
            "Checkpoint: *Communal Societies* volumes 1-40",
            "Checkpoint: *Communal Societies* volumes 1-41",
            "gap completed boundary",
        ),
        (
            "After reconciling the volume 40 findings rather than inflating the list",
            "After reconciling the volume 41 findings rather than inflating the list",
            "gap checkpoint description",
        ),
        (
            "No processed journal evidence through volume 40 validates six months of inner work as a reliable con-artist filter.",
            "No processed journal evidence through volume 41 validates six months of inner work as a reliable con-artist filter.",
            "G-018 cumulative boundary",
        ),
        (
            "F-007, F-008, F-056, F-057, F-063, F-074 |",
            "F-007, F-008, F-056, F-057, F-063, F-074, F-147 |",
            "G-002 evidence",
        ),
        (
            "F-136, F-137, F-145 |",
            "F-136, F-137, F-145, F-147 |",
            "G-003 evidence",
        ),
        (
            "F-135, F-136, F-137, F-139, F-143, F-144 |",
            "F-135, F-136, F-137, F-139, F-143, F-144, F-147 |",
            "G-004 evidence",
        ),
        (
            "F-117, F-130, F-133 |",
            "F-117, F-130, F-133, F-147 |",
            "G-007 evidence",
        ),
        (
            "F-137, F-144, F-145 |",
            "F-137, F-144, F-145, F-147 |",
            "G-013 evidence",
        ),
        (
            "Volume 40 again found neither validation of the filter nor a complete dangerous-child actor response sequence; lifetime commitment, symbolic co-trusteeship, and a civil 'lunacy' petition against a reformer were not safety evidence.",
            "Volume 40 again found neither validation of the filter nor a complete dangerous-child actor response sequence; lifetime commitment, symbolic co-trusteeship, and a civil 'lunacy' petition against a reformer were not safety evidence. Volume 41 again found neither validation of the filter nor a complete dangerous-child actor response sequence; a mandatory complaint forum, outward conformity, and managed answers to an outside psychologist were not safety evidence.",
            "G-018 volume 41 result",
        ),
        (
            "F-143, F-144, F-145, F-146 |",
            "F-143, F-144, F-145, F-146, F-147, F-148 |",
            "G-018 evidence",
        ),
        (
            "The volume 1-40 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146) are bounded negative results",
            "The volume 1-41 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148) are bounded negative results",
            "bounded dangerous-child sequence",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)

    prose_extensions = [
        (
            "independent appeal, clinical authority, and right to withdraw.",
            " A mandatory complaint-and-growth forum also needs confidential participation boundaries, a route around any challenged leader, and protection against using disclosed feelings as discipline.",
            "G-002 captured growth forum",
        ),
        (
            "A civil or clinical route requested by leaders who oppose the dissent is not independent unless intake, evidence, assessment, and review are protected from that conflict.",
            " A complaint forum can itself be captured, and an outside evaluator needs private, independently selected access, anti-retaliation, discrepant-account handling, and a later correction route.",
            "G-003 evaluation access",
        ),
        (
            "Map authority separately across household, intimate relationship, employment, ownership, and executive domains; a nominal co-trustee or professional drafter is not independent when interests or beneficiary status conflict.",
            " Audit control of complaint sessions, participant access, and evaluator-facing narratives as practical founder powers too.",
            "G-004 grievance and evaluation control",
        ),
        (
            "Public unanimity, bodily ritual intensity, submission, and a covenant never to deny a shared experience are not independent evidence of belief or safety when doubt itself carries spiritual or social punishment.",
            " Neither are outward conformity or apparently candid evaluator interviews when members fear that disagreement will return through a leader-controlled forum.",
            "G-007 managed agreement",
        ),
        (
            "Community principle cannot disable lawful recourse against an adverse fiduciary.",
            " External researchers and evaluators need direct private access, confidentiality limits, retaliation-safe follow-up, and a way to preserve and correct discrepant accounts.",
            "G-013 evaluator protocol",
        ),
    ]
    for anchor, addition, label in prose_extensions:
        text = extend_once_or_confirm(text, anchor, addition, label)

    verification_anchor = (
        "- **F status:** inspect the Nashoba Book entries, Wright and Richardson correspondence, deed, contemporary reactions, Josephine Prevot records, and accounts by or about enslaved members and descendants before stating conduct or motive beyond Coulthard's attributed reconstruction."
    )
    verification_new = verification_anchor + (
        "\n- **F status:** inspect Kerista's Gestalt-o-Rama rules and records, participant accounts across positions and periods, the psychologist's book and interview materials, confidentiality conditions, and later corrections before assigning conduct, motive, prevalence, or research fault."
    )
    text = replace_once_or_confirm(text, verification_anchor, verification_new, "F-147 verification queue")

    final_old = "- The remaining volume 40 records are functional metadata and supply no further distinct response mechanism or outcome."
    final_new = final_old + "\n" + "\n".join([
        "- F-147 is limited to the reported capture of Gestalt-o-Rama and contamination of an outside interview stream; it does not prove that every session failed, every member lied, or the psychologist knowingly presented managed evidence.",
        "- Amana's outside-contact limits, quantitative out-migration, personal exit accounts, member vote, and Great Change materially corroborate F-016, F-080, G-006, and G-008 rather than creating a duplicate finding.",
        "- The Kibbutz artists' association paired meaningful resource and time rights with duties to serve movement ideology, but the source documents no denied benefit, sanction, appeal, or later corrective outcome; it remains a protected-work and expression lead.",
        "- The Nauvoo review's reported destruction of a dissenting press corroborates F-037, F-113, and F-145; inspect the reviewed book and underlying records before treating the compressed account as a distinct adjudicated sequence.",
        "- The three volume 41 child-danger candidates concern students, dependents, subjects of adult governance, later adult leavers, family-form language, and unrelated lexical proximity—not a persistently dangerous child actor with assessment, intervention, review, and later outcome.",
        "- The remaining volume 41 articles and reviews supply exit, succession, labor, material-culture, governance, disability, heritage, external-context, or source-method corroboration without a further materially distinct response mechanism and outcome; four records are functional metadata.",
    ])
    text = replace_once_or_confirm(text, final_old, final_new, "volume 41 non-promotions")

    gap_lines = [line for line in text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
        "B": 8,
        "C": 7,
        "D": 3,
    })
    references = set(re.findall(r"\bF-\d{3}\b", text))
    assert references <= {f"F-{number:03d}" for number in range(1, 149)}
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = [
        ("volumes **1-40**", "volumes **1-41**", "state completed boundary"),
        (
            "**855 journal PDFs** were triaged: 346 close-read as relevant or contextual, 207 title/keyword-triaged, and 302 metadata-triaged.",
            "**875 journal PDFs** were triaged: 362 close-read as relevant or contextual, 207 title/keyword-triaged, and 306 metadata-triaged.",
            "state counts",
        ),
        (
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **146 findings** (`F-001` through `F-146`). Volume 40 added four findings: three C and one F-status bounded negative.",
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **148 findings** (`F-001` through `F-148`). Volume 41 added two findings: one C and one F-status bounded negative.",
            "state findings",
        ),
        (
            "`COMMUNITIES-V40-RESEARCH-REPORT.md` records the completed 9-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "`COMMUNITIES-V41-RESEARCH-REPORT.md` records the completed 20-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "state report",
        ),
        (
            "Every one of the 9 volume 40 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `vol35-40.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
            "Every one of the 20 volume 41 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `COMMUNAL-SOCIETIES-v41-v45.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
            "state corpus verification",
        ),
        (
            "Volumes **41-45** have not been processed: **129 journal PDFs**.",
            "Volumes **42-45** have not been processed: **109 journal PDFs**.",
            "state remaining boundary",
        ),
        (
            "The next bounded journal unit is volume **41: 20 PDFs**, all in issue 1.",
            "The next bounded journal unit is volume **42: 24 PDFs**, split evenly across issues 1 and 2.",
            "state next unit",
        ),
        (
            "Volume 40 adds: cross-domain authority and conflict rules where communal partners are also business supervisors and executives; conflict-qualified fiduciary and deed review rather than symbolic co-trusteeship; protection against civil or clinical processes initiated to silence dissent; and another bounded dangerous-child null.",
            "Volume 41 adds: protection against a required complaint-and-growth forum becoming a founder's discipline channel; independent participant access and correction safeguards for outside evaluation; and another bounded dangerous-child null.",
            "state evidence summary",
        ),
        ("Do not repeat volumes 1-40.", "Do not repeat volumes 1-41.", "state resume boundary"),
        (
            "Retrieve and verify the 20 volume 41 publisher PDFs; they are all in issue 1 and form the next exact bounded journal unit.",
            "Retrieve and verify the 24 volume 42 publisher PDFs; 12 are in issue 1 and 12 are in issue 2, together forming the next exact bounded journal unit.",
            "state resume next unit",
        ),
        (
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 20 extracted texts.",
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 24 extracted texts.",
            "state resume corpus size",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = [
        ("Volumes **1-40** complete", "Volumes **1-41** complete", "README completed boundary"),
        ("**855** journal PDFs triaged", "**875** journal PDFs triaged", "README total"),
        (
            "**346** relevant or contextual close reads",
            "**362** relevant or contextual close reads",
            "README close reads",
        ),
        (
            "**146** evidence findings (`F-001` through `F-146`)",
            "**148** evidence findings (`F-001` through `F-148`)",
            "README findings",
        ),
        (
            "Next unit: **volume 41, 20 PDFs** (all in issue 1)",
            "Next unit: **volume 42, 24 PDFs** (12 in issue 1; 12 in issue 2)",
            "README next unit",
        ),
        (
            "[`recovered/COMMUNITIES-V40-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V40-RESEARCH-REPORT.md)",
            "[`recovered/COMMUNITIES-V41-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V41-RESEARCH-REPORT.md)",
            "README latest report",
        ),
        (
            "With the exact local source corpus restored beneath `recovered/corpus-v40/`, run:",
            "With the exact local source corpus restored beneath `recovered/corpus-v41/`, run:",
            "README corpus path",
        ),
        ("python recovered/test_v40_workflow.py", "python recovered/test_v41_workflow.py", "README tests"),
        ("python recovered/verify_v40.py", "python recovered/verify_v41.py", "README verifier"),
        (
            "The verifier checks all 9 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, and the volume-41 boundary.",
            "The verifier checks all 20 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-42 boundary.",
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
    print("updated volume 41 checkpoint")


if __name__ == "__main__":
    main()
