#!/usr/bin/env python3
"""Verify the completed volume 41 checkpoint and exact volume 42 handoff."""

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
REPORT = ROOT / "COMMUNITIES-V41-RESEARCH-REPORT.md"
RANKING = ROOT / "V41-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v41-child-danger-contexts.txt"
CORPUS = ROOT / "corpus-v41"
ARCHIVE = REPOSITORY / "raw" / "COMMUNAL-SOCIETIES-v41-v45.zip"
README = REPOSITORY / "README.md"

ARCHIVE_RECORD_ID = "D-003"
ARCHIVE_SIZE = 55_770_584
SAVED_ARCHIVE_SHA256 = "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c"
ARCHIVE_STATUS = "not processed"
ARCHIVE_LOCAL_PATH = "raw/COMMUNAL-SOCIETIES-v41-v45.zip"
ARCHIVE_NOTE = "Drive inventory row; archive downloaded and integrity-tested; members follow"
ARCHIVE_RAW_ROW = (
    "D-003,drive_archive,REDACTED,COMMUNAL-SOCIETIES-v41-v45.zip,application/zip,"
    "55770584,COMMUNAL-SOCIETIES-v41-v45.zip,,,,,,,,,,"
    "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c,"
    "not_applicable,not processed,raw/COMMUNAL-SOCIETIES-v41-v45.zip,,"
    "Drive inventory row; archive downloaded and integrity-tested; members follow"
)

PROMOTED_IDS = {"M-0018"}
FUNCTIONAL_METADATA_IDS = {"M-0004", "M-0019", "M-0020", "M-0021"}
EXPECTED_VOLUME_IDS = {f"M-{number:04d}" for number in range(2, 22)}


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

volume_rows = [row for row in inventory_rows if row["volume"] == "41"]
assert len(volume_rows) == 20
assert Counter(row["issue"] for row in volume_rows) == Counter({"1": 20})
assert {row["record_id"] for row in volume_rows} == EXPECTED_VOLUME_IDS
assert Counter(row["notes"] for row in volume_rows) == Counter({
    "kind=article": 8,
    "kind=book_review": 8,
    "kind=front_matter": 1,
    "kind=table_of_contents": 1,
    "kind=editorial": 1,
    "kind=back_matter": 1,
})
assert Counter(row["research_status"] for row in volume_rows) == Counter({
    "metadata triaged": 4,
    "close read; finding promoted": 1,
    "contextual close read; no distinct finding": 15,
})
assert all(row["text_extraction_status"] == "extracted" for row in volume_rows)

archive_row = next(row for row in inventory_rows if row["record_id"] == ARCHIVE_RECORD_ID)
assert archive_row["drive_size_bytes"] == str(ARCHIVE_SIZE)
assert archive_row["sha256"] == SAVED_ARCHIVE_SHA256
assert archive_row["research_status"] == ARCHIVE_STATUS
assert archive_row["local_path"] == ARCHIVE_LOCAL_PATH
assert archive_row["notes"] == ARCHIVE_NOTE
raw_inventory_lines = INVENTORY.read_text(encoding="utf-8-sig").splitlines()
assert raw_inventory_lines.count(ARCHIVE_RAW_ROW) == 1, "D-003 row changed byte-for-byte"
assert not ARCHIVE.exists(), "shared volume 41-45 archive unexpectedly present; update provenance if materialized"

for row in volume_rows:
    relative = Path(row["internal_filename"]).relative_to("archive")
    pdf = CORPUS / relative
    extracted = pdf.with_suffix(".txt")
    assert pdf.is_file() and pdf.stat().st_size > 0, row["record_id"]
    assert extracted.is_file() and extracted.stat().st_size > 0, row["record_id"]
    assert sha256(pdf) == row["sha256"], row["record_id"]
    assert pdf_pages(pdf) == int(row["pdf_pages"]), row["record_id"]
    assert row["local_path"] == f"recovered/corpus-v41/{relative.as_posix()}"
    assert row["text_path"] == f"recovered/corpus-v41/{relative.with_suffix('.txt').as_posix()}"
    if row["record_id"] in PROMOTED_IDS:
        assert row["research_status"] == "close read; finding promoted"
    elif row["record_id"] in FUNCTIONAL_METADATA_IDS:
        assert row["research_status"] == "metadata triaged"
    else:
        assert row["research_status"] == "contextual close read; no distinct finding"

with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    ledger_rows = list(csv.DictReader(handle))
assert len(ledger_rows) == 148
expected_ids = [f"F-{number:03d}" for number in range(1, 149)]
assert [row["finding_id"] for row in ledger_rows] == expected_ids
new_rows = ledger_rows[-2:]
assert [row["finding_id"] for row in new_rows] == ["F-147", "F-148"]
assert Counter(row["article_gap_status"] for row in new_rows) == Counter({"C": 1, "F": 1})
assert [row["source_record_id"] for row in new_rows] == ["M-0018", ""]
assert all(row["supporting_excerpt"] == "" for row in new_rows)

gap_text = GAP_BANK.read_text(encoding="utf-8")
gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
assert len(gap_lines) == 18
assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
    "B": 8,
    "C": 7,
    "D": 3,
})
assert "Checkpoint: *Communal Societies* volumes 1-41" in gap_text
assert "through volume 41" in gap_text
assert (
    "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, "
    "F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148"
) in gap_text
ledger_ids = set(expected_ids)
gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
assert gap_references <= ledger_ids, sorted(gap_references - ledger_ids)
for finding_id in ("F-147", "F-148"):
    assert finding_id in gap_text

with RANKING.open(newline="", encoding="utf-8-sig") as handle:
    ranking_rows = list(csv.DictReader(handle))
assert len(ranking_rows) == 20
assert Counter(row["functional_class"] for row in ranking_rows) == Counter({
    "substantive": 16,
    "metadata": 4,
})
assert {
    row["record_id"] for row in ranking_rows if row["functional_class"] == "metadata"
} == FUNCTIONAL_METADATA_IDS
assert Counter(
    row["kind"] for row in ranking_rows if row["functional_class"] == "metadata"
) == Counter({
    "front_matter": 1,
    "table_of_contents": 1,
    "editorial": 1,
    "back_matter": 1,
})
child_headers = re.findall(
    r"^===== M-\d{4}\b",
    CHILD_CONTEXTS.read_text(encoding="utf-8"),
    re.MULTILINE,
)
assert len(child_headers) == 3

state = STATE.read_text(encoding="utf-8")
for required in [
    "volumes **1-41**",
    "**875 journal PDFs**",
    "362 close-read",
    "207 title/keyword-triaged",
    "306 metadata-triaged",
    "**148 findings** (`F-001` through `F-148`)",
    "Volumes **42-45** have not been processed: **109 journal PDFs**",
    "volume **42: 24 PDFs**",
]:
    assert required in state, required
assert "Do not repeat volumes 1-41" in state

report = REPORT.read_text(encoding="utf-8")
for required in [
    "All **20 PDFs** in volume 41 were processed",
    "**16** substantive close reads",
    "**0** additional articles left at title-and-keyword triage",
    "**4** front-matter, table-of-contents, editorial, and back-matter metadata triages",
    "**2 new findings, F-147 through F-148**",
    "All twenty publisher PDFs matched the pre-existing archive-member SHA-256 values",
    "not locally present or reverified in this checkpoint",
    "**volume 42: 24 PDFs**",
]:
    assert required in report, required
report_ids = set(re.findall(r"^\| (M-\d{4}) \|", report, re.MULTILINE))
assert report_ids == EXPECTED_VOLUME_IDS - FUNCTIONAL_METADATA_IDS

readme = README.read_text(encoding="utf-8")
for required in [
    "Volumes **1-41** complete",
    "**875** journal PDFs triaged",
    "**362** relevant or contextual close reads",
    "**148** evidence findings (`F-001` through `F-148`)",
    "Next unit: **volume 42, 24 PDFs** (12 in issue 1; 12 in issue 2)",
    "recovered/COMMUNITIES-V41-RESEARCH-REPORT.md",
    "recovered/corpus-v41/",
    "python recovered/test_v41_workflow.py",
    "python recovered/verify_v41.py",
]:
    assert required in readme, required

tracked = subprocess.run(
    ["git", "ls-files"],
    cwd=REPOSITORY,
    check=True,
    capture_output=True,
    text=True,
).stdout.splitlines()
assert not any(path.startswith("recovered/corpus-v41/") for path in tracked)
assert not any(path.endswith((".pdf", ".zip", ".png")) for path in tracked)
assert not any(
    "v41-keyword-contexts" in path or "v41-child-danger-contexts" in path
    for path in tracked
)

volume_42_rows = [row for row in inventory_rows if row["volume"] == "42"]
assert len(volume_42_rows) == 24
assert Counter(row["issue"] for row in volume_42_rows) == Counter({"1": 12, "2": 12})
assert all(row["research_status"] == "not processed" for row in volume_42_rows)
remaining_rows = [
    row
    for row in inventory_rows
    if row["record_type"] == "archive_pdf"
    and row["volume"].isdigit()
    and int(row["volume"]) >= 42
]
assert len(remaining_rows) == 109

print("PASS volume41_publisher_member_hashes=20 pages_verified=20 text_nonempty=20 shared_archive_reverified=0")
print("PASS inventory_dispositions promoted_sources=1 contextual=15 title=0 metadata=4")
print("PASS ledger_rows=148 sequential_ids=148 new_statuses=C1,F1")
print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
print("PASS discovery_rows=20 substantive=16 metadata=4 child_candidate_files=3")
print("PASS report_close_read_rows=16 state_boundary=volumes_1_41")
print("PASS next_boundary=volume42 pdfs=24 issue1=12 issue2=12 remaining_42_45=109")
