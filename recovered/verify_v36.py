#!/usr/bin/env python3
"""Fresh structural verification for the completed volume 36 checkpoint."""

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
REPORT = ROOT / "COMMUNITIES-V36-RESEARCH-REPORT.md"
RANKING = ROOT / "V36-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v36-child-danger-contexts.txt"
CORPUS = ROOT / "corpus-v36"
ARCHIVE = REPOSITORY / "raw" / "vol35-40.zip"
README = REPOSITORY / "README.md"

ARCHIVE_RECORD_ID = "D-017"
ARCHIVE_SIZE = 78_015_463
SAVED_ARCHIVE_SHA256 = "95f87d2210fc829ca76b7b495e24d9057db5d4acefe4c055c4f8d41bc32afb39"
ARCHIVE_STATUS = "not processed"
ARCHIVE_LOCAL_PATH = "raw/vol35-40.zip"
ARCHIVE_NOTE = "Drive inventory row; archive downloaded and integrity-tested; members follow"


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

volume_rows = [row for row in inventory_rows if row["volume"] == "36"]
assert len(volume_rows) == 21
assert Counter(row["issue"] for row in volume_rows) == Counter({"1": 10, "2": 11})
assert Counter(row["notes"] for row in volume_rows) == Counter({
    "kind=book_review": 11,
    "kind=article": 6,
    "kind=contents": 2,
    "kind=editorial": 2,
})
assert Counter(row["research_status"] for row in volume_rows) == Counter({
    "contextual close read; no distinct finding": 14,
    "metadata triaged": 4,
    "close read; finding promoted": 3,
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
    assert row["local_path"] == f"recovered/corpus-v36/{row['internal_filename']}"
    assert row["text_path"] == f"recovered/corpus-v36/{row['internal_filename'][:-4]}.txt"

with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    ledger_rows = list(csv.DictReader(handle))
assert len(ledger_rows) == 125
expected_ids = [f"F-{number:03d}" for number in range(1, 126)]
assert [row["finding_id"] for row in ledger_rows] == expected_ids
assert [row["finding_id"] for row in ledger_rows[-4:]] == ["F-122", "F-123", "F-124", "F-125"]
assert Counter(row["article_gap_status"] for row in ledger_rows[-4:]) == Counter({"C": 2, "D": 1, "F": 1})
assert [row["source_record_id"] for row in ledger_rows[-4:]] == ["M-0892", "M-0896", "M-0906", ""]

gap_text = GAP_BANK.read_text(encoding="utf-8")
gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
assert len(gap_lines) == 18
assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({"B": 8, "C": 7, "D": 3})
assert "Checkpoint: *Communal Societies* volumes 1-36" in gap_text
assert "through volume 36" in gap_text
assert "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125" in gap_text
ledger_ids = set(expected_ids)
gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
assert gap_references <= ledger_ids, sorted(gap_references - ledger_ids)

with RANKING.open(newline="", encoding="utf-8-sig") as handle:
    ranking_rows = list(csv.DictReader(handle))
assert len(ranking_rows) == 21
metadata_kinds = {"contents", "editorial"}
assert sum(row["kind"] not in metadata_kinds for row in ranking_rows) == 17
child_headers = re.findall(r"^===== M-\d{4}\b", CHILD_CONTEXTS.read_text(encoding="utf-8"), re.MULTILINE)
assert len(child_headers) == 6

state = STATE.read_text(encoding="utf-8")
for required in [
    "volumes **1-36**",
    "**777 journal PDFs**",
    "293 close-read",
    "207 title/keyword-triaged",
    "277 metadata-triaged",
    "**125 findings** (`F-001` through `F-125`)",
    "Volumes **37-45** have not been processed: **207 journal PDFs**",
    "volume **37: 26 PDFs**",
]:
    assert required in state, required
assert "Do not repeat volumes 1-36" in state

report = REPORT.read_text(encoding="utf-8")
for required in [
    "All **21 PDFs** in volume 36 were processed",
    "**17** relevant or contextual close reads",
    "**0** additional articles or reviews left at title-and-keyword triage",
    "**4** contents and editorial metadata triages",
    "**4 new findings, F-122 through F-125**",
    "All 21 publisher PDFs matched the pre-existing archive-member SHA-256 values",
    "not locally present or reverified in this checkpoint",
    "**volume 37: 26 PDFs**",
]:
    assert required in report, required
report_ids = set(re.findall(r"^\| (M-\d{4}) \|", report, re.MULTILINE))
expected_report_ids = {
    row["record_id"]
    for row in volume_rows
    if row["notes"] not in {"kind=contents", "kind=editorial"}
}
assert report_ids == expected_report_ids, sorted(expected_report_ids - report_ids)

readme = README.read_text(encoding="utf-8")
for required in [
    "Volumes **1-36** complete",
    "**777** journal PDFs triaged",
    "**293** relevant or contextual close reads",
    "**125** evidence findings (`F-001` through `F-125`)",
    "Next unit: **volume 37, 26 PDFs** (16 in issue 1; 10 in issue 2)",
    "recovered/COMMUNITIES-V36-RESEARCH-REPORT.md",
    "recovered/corpus-v36/",
    "python recovered/test_v36_workflow.py",
    "python recovered/verify_v36.py",
]:
    assert required in readme, required

tracked = subprocess.run(
    ["git", "ls-files"],
    cwd=REPOSITORY,
    check=True,
    capture_output=True,
    text=True,
).stdout.splitlines()
assert not any(path.startswith("recovered/corpus-v36/") for path in tracked)
assert not any(path.endswith((".pdf", ".zip", ".png")) for path in tracked)
assert not any("v36-keyword-contexts" in path or "v36-child-danger-contexts" in path for path in tracked)

volume_37_rows = [row for row in inventory_rows if row["volume"] == "37"]
assert len(volume_37_rows) == 26
assert Counter(row["issue"] for row in volume_37_rows) == Counter({"1": 16, "2": 10})
assert all(row["research_status"] == "not processed" for row in volume_37_rows)
remaining_rows = [
    row for row in inventory_rows
    if row["record_type"] == "archive_pdf" and row["volume"].isdigit() and int(row["volume"]) >= 37
]
assert len(remaining_rows) == 207

print("PASS volume36_publisher_member_hashes=21 pages_verified=21 text_nonempty=21 shared_archive_reverified=0")
print("PASS inventory_dispositions promoted_sources=3 contextual=14 title=0 metadata=4")
print("PASS ledger_rows=125 sequential_ids=125 new_statuses=C2,D1,F1")
print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
print("PASS discovery_rows=21 nonmetadata=17 child_candidate_files=6")
print("PASS report_close_read_rows=17 state_boundary=volumes_1_36")
print("PASS next_boundary=volume37 pdfs=26 issue1=16 issue2=10 remaining_37_45=207")
