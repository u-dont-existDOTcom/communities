#!/usr/bin/env python3
"""Fresh structural verification for the completed volume 38 checkpoint."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
REPORT = ROOT / "COMMUNITIES-V38-RESEARCH-REPORT.md"
RANKING = ROOT / "V38-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v38-child-danger-contexts.txt"
CORPUS = ROOT / "corpus-v38"
ARCHIVE = REPOSITORY / "raw" / "vol35-40.zip"
README = REPOSITORY / "README.md"

ARCHIVE_RECORD_ID = "D-017"
ARCHIVE_SIZE = 78_015_463
SAVED_ARCHIVE_SHA256 = "95f87d2210fc829ca76b7b495e24d9057db5d4acefe4c055c4f8d41bc32afb39"
ARCHIVE_STATUS = "not processed"
ARCHIVE_LOCAL_PATH = "raw/vol35-40.zip"
ARCHIVE_NOTE = "Drive inventory row; archive downloaded and integrity-tested; members follow"

PROMOTED_IDS = {"M-0939", "M-0940", "M-0941", "M-0942", "M-0952", "M-0954"}
FUNCTIONAL_METADATA_IDS = {
    "M-0936",
    "M-0937",
    "M-0938",
    "M-0947",
    "M-0948",
    "M-0949",
    "M-0955",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_pages(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    assert match, path
    return int(match.group(1))


with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
    inventory_rows = list(csv.DictReader(handle))
assert len(inventory_rows) == 1005
assert Counter(row["record_type"] for row in inventory_rows)["archive_pdf"] == 984
assert all(row["drive_file_id"] in {"", "REDACTED"} for row in inventory_rows)
assert any(row["drive_file_id"] == "REDACTED" for row in inventory_rows)

volume_rows = [row for row in inventory_rows if row["volume"] == "38"]
assert len(volume_rows) == 20
assert Counter(row["issue"] for row in volume_rows) == Counter({"1": 11, "2": 9})
assert {row["record_id"] for row in volume_rows} == {
    f"M-{number:04d}" for number in range(936, 956)
}
assert Counter(row["notes"] for row in volume_rows) == Counter({
    "kind=article": 11,
    "kind=book_review": 4,
    "kind=editorial": 2,
    "kind=front_matter": 1,
    "kind=contents": 1,
    "kind=table_of_contents": 1,
})
assert Counter(row["research_status"] for row in volume_rows) == Counter({
    "metadata triaged": 7,
    "contextual close read; no distinct finding": 7,
    "close read; finding promoted": 6,
})
assert all(row["text_extraction_status"] == "extracted" for row in volume_rows)

archive_row = next(row for row in inventory_rows if row["record_id"] == ARCHIVE_RECORD_ID)
assert archive_row["drive_size_bytes"] == str(ARCHIVE_SIZE)
assert archive_row["sha256"] == SAVED_ARCHIVE_SHA256
assert archive_row["research_status"] == ARCHIVE_STATUS
assert archive_row["local_path"] == ARCHIVE_LOCAL_PATH
assert archive_row["notes"] == ARCHIVE_NOTE
assert not ARCHIVE.exists(), "shared volume 35-40 archive unexpectedly present; update provenance if materialized"

for row in volume_rows:
    pdf = CORPUS / row["internal_filename"]
    extracted = pdf.with_suffix(".txt")
    assert pdf.is_file() and pdf.stat().st_size > 0, row["record_id"]
    assert extracted.is_file() and extracted.stat().st_size > 0, row["record_id"]
    assert sha256(pdf) == row["sha256"], row["record_id"]
    assert pdf_pages(pdf) == int(row["pdf_pages"]), row["record_id"]
    assert row["local_path"] == f"recovered/corpus-v38/{row['internal_filename']}"
    assert row["text_path"] == f"recovered/corpus-v38/{row['internal_filename'][:-4]}.txt"
    if row["record_id"] in PROMOTED_IDS:
        assert row["research_status"] == "close read; finding promoted"
    elif row["record_id"] in FUNCTIONAL_METADATA_IDS:
        assert row["research_status"] == "metadata triaged"
    else:
        assert row["research_status"] == "contextual close read; no distinct finding"

with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    ledger_rows = list(csv.DictReader(handle))
assert len(ledger_rows) == 138
expected_ids = [f"F-{number:03d}" for number in range(1, 139)]
assert [row["finding_id"] for row in ledger_rows] == expected_ids
new_rows = ledger_rows[-7:]
assert [row["finding_id"] for row in new_rows] == [
    "F-132", "F-133", "F-134", "F-135", "F-136", "F-137", "F-138"
]
assert Counter(row["article_gap_status"] for row in new_rows) == Counter({
    "C": 4,
    "B": 2,
    "F": 1,
})
assert [row["source_record_id"] for row in new_rows] == [
    "M-0939", "M-0940", "M-0941", "M-0942", "M-0952", "M-0954", ""
]

gap_text = GAP_BANK.read_text(encoding="utf-8")
gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
assert len(gap_lines) == 18
assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
    "B": 8,
    "C": 7,
    "D": 3,
})
assert "Checkpoint: *Communal Societies* volumes 1-38" in gap_text
assert "through volume 38" in gap_text
assert (
    "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, "
    "F-115, F-118, F-121, F-125, F-131, F-138"
) in gap_text
ledger_ids = set(expected_ids)
gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
assert gap_references <= ledger_ids, sorted(gap_references - ledger_ids)

with RANKING.open(newline="", encoding="utf-8-sig") as handle:
    ranking_rows = list(csv.DictReader(handle))
assert len(ranking_rows) == 20
assert Counter(row["functional_class"] for row in ranking_rows) == Counter({
    "substantive": 13,
    "metadata": 7,
})
assert {
    row["record_id"] for row in ranking_rows if row["functional_class"] == "metadata"
} == FUNCTIONAL_METADATA_IDS
assert next(row for row in ranking_rows if row["record_id"] == "M-0949")["kind"] == "article"
assert next(row for row in ranking_rows if row["record_id"] == "M-0955")["kind"] == "article"
child_headers = re.findall(
    r"^===== M-\d{4}\b",
    CHILD_CONTEXTS.read_text(encoding="utf-8"),
    re.MULTILINE,
)
assert len(child_headers) == 8

state = STATE.read_text(encoding="utf-8")
for required in [
    "volumes **1-38**",
    "**823 journal PDFs**",
    "326 close-read",
    "207 title/keyword-triaged",
    "290 metadata-triaged",
    "**138 findings** (`F-001` through `F-138`)",
    "Volumes **39-45** have not been processed: **161 journal PDFs**",
    "volume **39: 23 PDFs**",
]:
    assert required in state, required
assert "Do not repeat volumes 1-38" in state

report = REPORT.read_text(encoding="utf-8")
for required in [
    "All **20 PDFs** in volume 38 were processed",
    "**13** relevant or contextual close reads",
    "**0** additional articles or reviews left at title-and-keyword triage",
    "**7** front-matter, contents, editorial, contributors, and bibliography metadata triages",
    "**7 new findings, F-132 through F-138**",
    "All 20 publisher PDFs matched the pre-existing archive-member SHA-256 values",
    "not locally present or reverified in this checkpoint",
    "**volume 39: 23 PDFs**",
]:
    assert required in report, required
report_ids = set(re.findall(r"^\| (M-\d{4}) \|", report, re.MULTILINE))
expected_report_ids = {
    row["record_id"] for row in volume_rows if row["record_id"] not in FUNCTIONAL_METADATA_IDS
}
assert report_ids == expected_report_ids, sorted(expected_report_ids - report_ids)

readme = README.read_text(encoding="utf-8")
for required in [
    "Volumes **1-38** complete",
    "**823** journal PDFs triaged",
    "**326** relevant or contextual close reads",
    "**138** evidence findings (`F-001` through `F-138`)",
    "Next unit: **volume 39, 23 PDFs** (11 in issue 1; 12 in issue 2)",
    "recovered/COMMUNITIES-V38-RESEARCH-REPORT.md",
    "recovered/corpus-v38/",
    "python recovered/test_v38_workflow.py",
    "python recovered/verify_v38.py",
]:
    assert required in readme, required

tracked = subprocess.run(
    ["git", "ls-files"],
    cwd=REPOSITORY,
    check=True,
    capture_output=True,
    text=True,
).stdout.splitlines()
assert not any(path.startswith("recovered/corpus-v38/") for path in tracked)
assert not any(path.endswith((".pdf", ".zip", ".png")) for path in tracked)
assert not any(
    "v38-keyword-contexts" in path or "v38-child-danger-contexts" in path
    for path in tracked
)

volume_39_rows = [row for row in inventory_rows if row["volume"] == "39"]
assert len(volume_39_rows) == 23
assert Counter(row["issue"] for row in volume_39_rows) == Counter({"1": 11, "2": 12})
assert all(row["research_status"] == "not processed" for row in volume_39_rows)
remaining_rows = [
    row
    for row in inventory_rows
    if row["record_type"] == "archive_pdf"
    and row["volume"].isdigit()
    and int(row["volume"]) >= 39
]
assert len(remaining_rows) == 161

print("PASS volume38_publisher_member_hashes=20 pages_verified=20 text_nonempty=20 shared_archive_reverified=0")
print("PASS inventory_dispositions promoted_sources=6 contextual=7 title=0 metadata=7")
print("PASS ledger_rows=138 sequential_ids=138 new_statuses=B2,C4,F1")
print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
print("PASS discovery_rows=20 substantive=13 metadata=7 child_candidate_files=8")
print("PASS report_close_read_rows=13 state_boundary=volumes_1_38")
print("PASS next_boundary=volume39 pdfs=23 issue1=11 issue2=12 remaining_39_45=161")
