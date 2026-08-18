#!/usr/bin/env python3
"""Fresh structural verification for the completed volume 35 checkpoint."""

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
REPORT = ROOT / "COMMUNITIES-V35-RESEARCH-REPORT.md"
RANKING = ROOT / "V35-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v35-child-danger-contexts.txt"
CORPUS = ROOT / "corpus-v35"
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

volume_rows = [row for row in inventory_rows if row["volume"] == "35"]
assert len(volume_rows) == 26
assert Counter(row["issue"] for row in volume_rows) == Counter({"1": 12, "2": 14})
assert Counter(row["notes"] for row in volume_rows) == Counter({
    "kind=book_review": 14,
    "kind=article": 8,
    "kind=contents": 2,
    "kind=editorial": 2,
})
assert Counter(row["research_status"] for row in volume_rows) == Counter({
    "contextual close read; no distinct finding": 21,
    "metadata triaged": 4,
    "close read; finding promoted": 1,
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
    text = pdf.with_suffix(".txt")
    assert pdf.is_file() and pdf.stat().st_size > 0, row["record_id"]
    assert text.is_file() and text.stat().st_size > 0, row["record_id"]
    assert sha256(pdf) == row["sha256"], row["record_id"]
    assert pdf_pages(pdf) == int(row["pdf_pages"]), row["record_id"]
    assert row["local_path"] == f"recovered/corpus-v35/{row['internal_filename']}"
    assert row["text_path"] == f"recovered/corpus-v35/{row['internal_filename'][:-4]}.txt"

with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    ledger_rows = list(csv.DictReader(handle))
assert len(ledger_rows) == 121
expected_ids = [f"F-{number:03d}" for number in range(1, 122)]
assert [row["finding_id"] for row in ledger_rows] == expected_ids
assert [row["finding_id"] for row in ledger_rows[-3:]] == ["F-119", "F-120", "F-121"]
assert Counter(row["article_gap_status"] for row in ledger_rows[-3:]) == Counter({"C": 2, "F": 1})
assert [row["source_record_id"] for row in ledger_rows[-3:]] == ["M-0877", "M-0877", ""]

gap_text = GAP_BANK.read_text(encoding="utf-8")
gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
assert len(gap_lines) == 18
assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({"B": 8, "C": 7, "D": 3})
assert "Checkpoint: *Communal Societies* volumes 1-35" in gap_text
assert "through volume 35" in gap_text
assert "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121" in gap_text
ledger_ids = set(expected_ids)
gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
assert gap_references <= ledger_ids, sorted(gap_references - ledger_ids)

with RANKING.open(newline="", encoding="utf-8-sig") as handle:
    ranking_rows = list(csv.DictReader(handle))
assert len(ranking_rows) == 26
metadata_kinds = {"contents", "editorial"}
assert sum(row["kind"] not in metadata_kinds for row in ranking_rows) == 22
child_headers = re.findall(r"^===== M-\d{4}\b", CHILD_CONTEXTS.read_text(encoding="utf-8"), re.MULTILINE)
assert len(child_headers) == 10

state = STATE.read_text(encoding="utf-8")
for required in [
    "volumes **1-35**",
    "**756 journal PDFs**",
    "276 close-read",
    "207 title/keyword-triaged",
    "273 metadata-triaged",
    "**121 findings** (`F-001` through `F-121`)",
    "Volumes **36-45** have not been processed: **228 journal PDFs**",
    "volume **36: 21 PDFs**",
]:
    assert required in state, required
assert "Do not repeat volumes 1-35" in state

report = REPORT.read_text(encoding="utf-8")
for required in [
    "All **26 PDFs** in volume 35 were processed",
    "**22** relevant or contextual close reads",
    "**0** additional articles or reviews left at title-and-keyword triage",
    "**4** contents and editorial metadata triages",
    "**3 new findings, F-119 through F-121**",
    "All 26 publisher PDFs matched the pre-existing archive-member SHA-256 values",
    "not locally present or reverified in this checkpoint",
    "**volume 36: 21 PDFs**",
]:
    assert required in report, required
assert len(re.findall(r"^\| M-\d{4} \|", report, re.MULTILINE)) == 22

readme = README.read_text(encoding="utf-8")
for required in [
    "Volumes **1-35** complete",
    "**756** journal PDFs triaged",
    "**276** relevant or contextual close reads",
    "**121** evidence findings (`F-001` through `F-121`)",
    "Next unit: **volume 36, 21 PDFs** (10 in issue 1; 11 in issue 2)",
    "recovered/COMMUNITIES-V35-RESEARCH-REPORT.md",
    "recovered/corpus-v35/",
    "python recovered/test_v35_workflow.py",
    "python recovered/verify_v35.py",
]:
    assert required in readme, required

volume_36_rows = [row for row in inventory_rows if row["volume"] == "36"]
assert len(volume_36_rows) == 21
assert Counter(row["issue"] for row in volume_36_rows) == Counter({"1": 10, "2": 11})
assert all(row["research_status"] == "not processed" for row in volume_36_rows)
remaining_rows = [
    row for row in inventory_rows
    if row["record_type"] == "archive_pdf" and row["volume"].isdigit() and int(row["volume"]) >= 36
]
assert len(remaining_rows) == 228

print("PASS volume35_publisher_member_hashes=26 pages_verified=26 text_nonempty=26 shared_archive_reverified=0")
print("PASS inventory_dispositions promoted_sources=1 contextual=21 title=0 metadata=4")
print("PASS ledger_rows=121 sequential_ids=121 new_statuses=C2,F1")
print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
print("PASS discovery_rows=26 nonmetadata=22 child_candidate_files=10")
print("PASS report_close_read_rows=22 state_boundary=volumes_1_35")
print("PASS next_boundary=volume36 pdfs=21 issue1=10 issue2=11 remaining_36_45=228")
