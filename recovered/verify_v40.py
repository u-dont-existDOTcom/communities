#!/usr/bin/env python3
"""Verify the completed volume 40 checkpoint and exact volume 41 handoff."""

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
REPORT = ROOT / "COMMUNITIES-V40-RESEARCH-REPORT.md"
RANKING = ROOT / "V40-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v40-child-danger-contexts.txt"
CORPUS = ROOT / "corpus-v40"
ARCHIVE = REPOSITORY / "raw" / "vol35-40.zip"
README = REPOSITORY / "README.md"

ARCHIVE_RECORD_ID = "D-017"
ARCHIVE_SIZE = 78_015_463
SAVED_ARCHIVE_SHA256 = "95f87d2210fc829ca76b7b495e24d9057db5d4acefe4c055c4f8d41bc32afb39"
ARCHIVE_STATUS = "not processed"
ARCHIVE_LOCAL_PATH = "raw/vol35-40.zip"
ARCHIVE_NOTE = "Drive inventory row; archive downloaded and integrity-tested; members follow"

PROMOTED_IDS = {"M-0983", "M-0985", "M-0986"}
FUNCTIONAL_METADATA_IDS = {"M-0979", "M-0980", "M-0981", "M-0987"}


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

volume_rows = [row for row in inventory_rows if row["volume"] == "40"]
assert len(volume_rows) == 9
assert Counter(row["issue"] for row in volume_rows) == Counter({"1": 9})
assert {row["record_id"] for row in volume_rows} == {
    f"M-{number:04d}" for number in range(979, 988)
}
assert Counter(row["notes"] for row in volume_rows) == Counter({
    "kind=article": 5,
    "kind=front_matter": 1,
    "kind=table_of_contents": 1,
    "kind=editorial": 1,
    "kind=back_matter": 1,
})
assert Counter(row["research_status"] for row in volume_rows) == Counter({
    "metadata triaged": 4,
    "close read; finding promoted": 3,
    "contextual close read; no distinct finding": 2,
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
    assert row["local_path"] == f"recovered/corpus-v40/{row['internal_filename']}"
    assert row["text_path"] == f"recovered/corpus-v40/{row['internal_filename'][:-4]}.txt"
    if row["record_id"] in PROMOTED_IDS:
        assert row["research_status"] == "close read; finding promoted"
    elif row["record_id"] in FUNCTIONAL_METADATA_IDS:
        assert row["research_status"] == "metadata triaged"
    else:
        assert row["research_status"] == "contextual close read; no distinct finding"

with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    ledger_rows = list(csv.DictReader(handle))
assert len(ledger_rows) == 146
expected_ids = [f"F-{number:03d}" for number in range(1, 147)]
assert [row["finding_id"] for row in ledger_rows] == expected_ids
new_rows = ledger_rows[-4:]
assert [row["finding_id"] for row in new_rows] == [
    "F-143", "F-144", "F-145", "F-146"
]
assert Counter(row["article_gap_status"] for row in new_rows) == Counter({
    "C": 3,
    "F": 1,
})
assert [row["source_record_id"] for row in new_rows] == [
    "M-0983", "M-0985", "M-0986", ""
]
assert all(row["supporting_excerpt"] == "" for row in new_rows)

gap_text = GAP_BANK.read_text(encoding="utf-8")
gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
assert len(gap_lines) == 18
assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
    "B": 8,
    "C": 7,
    "D": 3,
})
assert "Checkpoint: *Communal Societies* volumes 1-40" in gap_text
assert "through volume 40" in gap_text
assert (
    "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, "
    "F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146"
) in gap_text
ledger_ids = set(expected_ids)
gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
assert gap_references <= ledger_ids, sorted(gap_references - ledger_ids)
for finding_id in ("F-143", "F-144", "F-145", "F-146"):
    assert finding_id in gap_text

with RANKING.open(newline="", encoding="utf-8-sig") as handle:
    ranking_rows = list(csv.DictReader(handle))
assert len(ranking_rows) == 9
assert Counter(row["functional_class"] for row in ranking_rows) == Counter({
    "substantive": 5,
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
    "volumes **1-40**",
    "**855 journal PDFs**",
    "346 close-read",
    "207 title/keyword-triaged",
    "302 metadata-triaged",
    "**146 findings** (`F-001` through `F-146`)",
    "Volumes **41-45** have not been processed: **129 journal PDFs**",
    "volume **41: 20 PDFs**",
]:
    assert required in state, required
assert "Do not repeat volumes 1-40" in state

report = REPORT.read_text(encoding="utf-8")
for required in [
    "All **9 PDFs** in volume 40 were processed",
    "**5** substantive close reads",
    "**0** additional articles left at title-and-keyword triage",
    "**4** front-matter, table-of-contents, editorial, and back-matter metadata triages",
    "**4 new findings, F-143 through F-146**",
    "All nine publisher PDFs matched the pre-existing archive-member SHA-256 values",
    "not locally present or reverified in this checkpoint",
    "**volume 41: 20 PDFs**",
]:
    assert required in report, required
report_ids = set(re.findall(r"^\| (M-\d{4}) \|", report, re.MULTILINE))
expected_report_ids = {
    row["record_id"] for row in volume_rows if row["record_id"] not in FUNCTIONAL_METADATA_IDS
}
assert report_ids == expected_report_ids, sorted(expected_report_ids - report_ids)

readme = README.read_text(encoding="utf-8")
for required in [
    "Volumes **1-40** complete",
    "**855** journal PDFs triaged",
    "**346** relevant or contextual close reads",
    "**146** evidence findings (`F-001` through `F-146`)",
    "Next unit: **volume 41, 20 PDFs** (all in issue 1)",
    "recovered/COMMUNITIES-V40-RESEARCH-REPORT.md",
    "recovered/corpus-v40/",
    "python recovered/test_v40_workflow.py",
    "python recovered/verify_v40.py",
]:
    assert required in readme, required

tracked = subprocess.run(
    ["git", "ls-files"],
    cwd=REPOSITORY,
    check=True,
    capture_output=True,
    text=True,
).stdout.splitlines()
assert not any(path.startswith("recovered/corpus-v40/") for path in tracked)
assert not any(path.endswith((".pdf", ".zip", ".png")) for path in tracked)
assert not any(
    "v40-keyword-contexts" in path or "v40-child-danger-contexts" in path
    for path in tracked
)

volume_41_rows = [row for row in inventory_rows if row["volume"] == "41"]
assert len(volume_41_rows) == 20
assert Counter(row["issue"] for row in volume_41_rows) == Counter({"1": 20})
assert all(row["research_status"] == "not processed" for row in volume_41_rows)
remaining_rows = [
    row
    for row in inventory_rows
    if row["record_type"] == "archive_pdf"
    and row["volume"].isdigit()
    and int(row["volume"]) >= 41
]
assert len(remaining_rows) == 129

print("PASS volume40_publisher_member_hashes=9 pages_verified=9 text_nonempty=9 shared_archive_reverified=0")
print("PASS inventory_dispositions promoted_sources=3 contextual=2 title=0 metadata=4")
print("PASS ledger_rows=146 sequential_ids=146 new_statuses=C3,F1")
print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
print("PASS discovery_rows=9 substantive=5 metadata=4 child_candidate_files=3")
print("PASS report_close_read_rows=5 state_boundary=volumes_1_40")
print("PASS next_boundary=volume41 pdfs=20 issue1=20 remaining_41_45=129")
