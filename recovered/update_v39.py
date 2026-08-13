#!/usr/bin/env python3
"""Apply the completed volume 39 checkpoint to cumulative research artifacts."""

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

PROMOTED_IDS = {"M-0960", "M-0970", "M-0972"}
FUNCTIONAL_METADATA_IDS = {
    "M-0956",
    "M-0957",
    "M-0958",
    "M-0966",
    "M-0967",
    "M-0968",
    "M-0969",
    "M-0978",
}
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
    if old in text:
        return text.replace(old, new, 1)
    assert new in text, f"missing update anchor: {label}"
    return text


def validate_reconciled_evidence() -> None:
    """Require the completed finding and gap work before cumulative mutation."""
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    expected_ids = [f"F-{number:03d}" for number in range(1, 143)]
    assert [row["finding_id"] for row in rows] == expected_ids
    new_rows = rows[-4:]
    assert [row["source_record_id"] for row in new_rows] == [
        "M-0960", "M-0970", "M-0972", ""
    ]
    assert Counter(row["article_gap_status"] for row in new_rows) == Counter({
        "B": 2,
        "C": 1,
        "F": 1,
    })

    gap_text = GAP_BANK.read_text(encoding="utf-8")
    gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
        "B": 8,
        "C": 7,
        "D": 3,
    })
    assert "Checkpoint: *Communal Societies* volumes 1-39" in gap_text
    references = set(re.findall(r"\bF-\d{3}\b", gap_text))
    assert references <= set(expected_ids), sorted(references - set(expected_ids))


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
        if row["record_type"] != "archive_pdf" or row["volume"] != "39":
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
        row["local_path"] = f"recovered/corpus-v39/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v39/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1

    assert seen == {f"M-{number:04d}" for number in range(956, 979)}
    assert dispositions == Counter({"contextual": 12, "metadata": 8, "promoted": 3})
    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed during update: {field}"

    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = [
        ("volumes **1-38**", "volumes **1-39**", "state completed boundary"),
        (
            "**823 journal PDFs** were triaged: 326 close-read as relevant or contextual, 207 title/keyword-triaged, and 290 metadata-triaged.",
            "**846 journal PDFs** were triaged: 341 close-read as relevant or contextual, 207 title/keyword-triaged, and 298 metadata-triaged.",
            "state counts",
        ),
        (
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **138 findings** (`F-001` through `F-138`). Volume 38 added seven findings: four C, two B, and one F-status bounded negative.",
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **142 findings** (`F-001` through `F-142`). Volume 39 added four findings: two B, one C, and one F-status bounded negative.",
            "state findings",
        ),
        (
            "`COMMUNITIES-V38-RESEARCH-REPORT.md` records the completed 20-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "`COMMUNITIES-V39-RESEARCH-REPORT.md` records the completed 23-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "state report",
        ),
        (
            "Every one of the 20 volume 38 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text.",
            "Every one of the 23 volume 39 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text.",
            "state corpus verification",
        ),
        (
            "Volumes **39-45** have not been processed: **161 journal PDFs**.",
            "Volumes **40-45** have not been processed: **138 journal PDFs**.",
            "state remaining boundary",
        ),
        (
            "The next bounded journal unit is volume **39: 23 PDFs**—11 in issue 1 and 12 in issue 2.",
            "The next bounded journal unit is volume **40: 9 PDFs**, all in issue 1.",
            "state next unit",
        ),
        (
            "Volume 38 adds: named operational ownership across partner boundaries; protection against compelled assent and irreversible testimony; external-dependency tests for material autonomy; verified title and registration before pooled-fund release; source-coverage audits against population, labor, authority, and survival; conflict review for reputation and investigation channels; and another bounded dangerous-child null.",
            "Volume 39 adds: a completed transition from founder-owned land to enforceable institutional occupancy and purchase rights; an explicit warning that additive success scores cannot subtract harm or missing data; a case in which communal doctrine overrode a requested physical safeguard and independent child-consent protections; and another bounded dangerous-child null.",
            "state evidence summary",
        ),
        ("Do not repeat volumes 1-38.", "Do not repeat volumes 1-39.", "state resume boundary"),
        (
            "Retrieve and verify the 23 volume 39 publisher PDFs; they are the next exact bounded journal unit.",
            "Retrieve and verify the 9 volume 40 publisher PDFs; they are all in issue 1 and form the next exact bounded journal unit.",
            "state resume next unit",
        ),
        (
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 23 extracted texts.",
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 9 extracted texts.",
            "state resume corpus size",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = [
        ("Volumes **1-38** complete", "Volumes **1-39** complete", "README boundary"),
        ("**823** journal PDFs triaged", "**846** journal PDFs triaged", "README PDF count"),
        ("**326** relevant or contextual close reads", "**341** relevant or contextual close reads", "README close reads"),
        ("**138** evidence findings (`F-001` through `F-138`)", "**142** evidence findings (`F-001` through `F-142`)", "README findings"),
        (
            "Next unit: **volume 39, 23 PDFs** (11 in issue 1; 12 in issue 2)",
            "Next unit: **volume 40, 9 PDFs** (all in issue 1)",
            "README next unit",
        ),
        (
            "[`recovered/COMMUNITIES-V38-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V38-RESEARCH-REPORT.md)",
            "[`recovered/COMMUNITIES-V39-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V39-RESEARCH-REPORT.md)",
            "README report link",
        ),
        ("`recovered/corpus-v38/`", "`recovered/corpus-v39/`", "README corpus path"),
        ("python recovered/test_v38_workflow.py", "python recovered/test_v39_workflow.py", "README tests"),
        ("python recovered/verify_v38.py", "python recovered/verify_v39.py", "README verifier"),
        ("all 20 PDF hashes", "all 23 PDF hashes", "README verified PDFs"),
        ("the volume-39 boundary", "the volume-40 boundary", "README next-boundary check"),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    README.write_text(text, encoding="utf-8")


def main() -> None:
    validate_reconciled_evidence()
    update_inventory()
    update_state()
    update_readme()
    print("updated volume39 findings=4 promoted_sources=3 contextual=12 metadata=8")


if __name__ == "__main__":
    main()
