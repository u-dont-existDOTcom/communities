#!/usr/bin/env python3
"""Fresh structural verification for the completed volume 33 checkpoint."""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
REPORT = ROOT / "COMMUNITIES-V33-RESEARCH-REPORT.md"
RANKING = ROOT / "V33-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v33-child-danger-contexts.txt"
CORPUS = ROOT / "corpus-v33"
ARCHIVE = ROOT / "vol33.zip"

ARCHIVE_RECORD_ID = "D-015"
ARCHIVE_SIZE = 96_183_475
SAVED_ARCHIVE_SHA256 = "c8aca658bc7dfc344e75ca81dd3f16fb6f42ed374d09d0ae55e243b8edb41cbb"
ARCHIVE_STATUS = "container not locally materialized; 36 publisher member PDFs hash-verified and triaged"
ARCHIVE_NOTE = (
    "Drive inventory row; archive container not locally materialized in this checkpoint; "
    "all 36 member PDFs independently recovered from the primary publisher and matched "
    "saved inventory SHA-256 values"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
    inventory_rows = list(csv.DictReader(handle))
assert len(inventory_rows) == 1005
assert Counter(row["record_type"] for row in inventory_rows)["archive_pdf"] == 984
assert all(row["drive_file_id"] in {"", "REDACTED"} for row in inventory_rows)
assert any(row["drive_file_id"] == "REDACTED" for row in inventory_rows)

volume_rows = [row for row in inventory_rows if row["volume"] == "33"]
assert len(volume_rows) == 36
assert Counter(row["issue"] for row in volume_rows) == Counter({"1": 14, "2": 22})
assert Counter(row["notes"] for row in volume_rows) == Counter({
    "kind=book_review": 21,
    "kind=article": 7,
    "kind=front_matter": 2,
    "kind=contents": 2,
    "kind=editorial": 2,
    "kind=back_matter": 2,
})
assert Counter(row["research_status"] for row in volume_rows) == Counter({
    "contextual close read; no distinct finding": 25,
    "metadata triaged": 8,
    "close read; finding promoted": 3,
})
assert all(row["text_extraction_status"] == "extracted" for row in volume_rows)

archive_row = next(row for row in inventory_rows if row["record_id"] == ARCHIVE_RECORD_ID)
assert archive_row["drive_size_bytes"] == str(ARCHIVE_SIZE)
assert archive_row["sha256"] == SAVED_ARCHIVE_SHA256
assert archive_row["research_status"] == ARCHIVE_STATUS
assert archive_row["local_path"] == ""
assert archive_row["notes"] == ARCHIVE_NOTE
assert not ARCHIVE.exists(), "volume 33 archive unexpectedly present; update provenance if materialized"

for row in volume_rows:
    pdf = CORPUS / row["internal_filename"]
    text = pdf.with_suffix(".txt")
    assert pdf.is_file() and pdf.stat().st_size > 0, row["record_id"]
    assert text.is_file() and text.stat().st_size > 0, row["record_id"]
    assert sha256(pdf) == row["sha256"], row["record_id"]
    assert row["local_path"] == f"recovered/corpus-v33/{row['internal_filename']}"
    assert row["text_path"] == f"recovered/corpus-v33/{row['internal_filename'][:-4]}.txt"

with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    ledger_rows = list(csv.DictReader(handle))
assert len(ledger_rows) == 115
expected_ids = [f"F-{number:03d}" for number in range(1, 116)]
assert [row["finding_id"] for row in ledger_rows] == expected_ids
assert [row["finding_id"] for row in ledger_rows[-4:]] == ["F-112", "F-113", "F-114", "F-115"]
assert Counter(row["article_gap_status"] for row in ledger_rows[-4:]) == Counter({"C": 2, "B": 1, "F": 1})
assert {row["source_record_id"] for row in ledger_rows[-4:-1]} == {"M-0802", "M-0803", "M-0818"}
assert ledger_rows[-1]["source_record_id"] == ""

gap_text = GAP_BANK.read_text(encoding="utf-8")
gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
assert len(gap_lines) == 18
assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({"B": 8, "C": 7, "D": 3})
assert "Checkpoint: *Communal Societies* volumes 1-33" in gap_text
assert "through volume 33" in gap_text
assert "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115" in gap_text
ledger_ids = set(expected_ids)
gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
assert gap_references <= ledger_ids, sorted(gap_references - ledger_ids)

with RANKING.open(newline="", encoding="utf-8-sig") as handle:
    ranking_rows = list(csv.DictReader(handle))
assert len(ranking_rows) == 36
metadata_kinds = {"front_matter", "contents", "editorial", "back_matter"}
assert sum(row["kind"] not in metadata_kinds for row in ranking_rows) == 28
child_headers = re.findall(r"^===== M-\d{4}\b", CHILD_CONTEXTS.read_text(encoding="utf-8"), re.MULTILINE)
assert len(child_headers) == 9

state = STATE.read_text(encoding="utf-8")
for required in [
    "volumes **1-33**",
    "**701 journal PDFs**",
    "233 close-read",
    "207 title/keyword-triaged",
    "261 metadata-triaged",
    "**115 findings** (`F-001` through `F-115`)",
    "Volumes **34-45** have not been processed: **283 journal PDFs**",
    "volume **34: 29 PDFs**",
]:
    assert required in state, required
assert "Do not repeat volumes 1-33" in state

report = REPORT.read_text(encoding="utf-8")
for required in [
    "All **36 PDFs** in volume 33 were processed",
    "**28** relevant or contextual close reads",
    "**0** additional articles or reviews left at title-and-keyword triage",
    "**8** front matter, contents, editorials, and back matter metadata triages",
    "**4 new findings, F-112 through F-115**",
    "All 36 publisher PDFs matched the pre-existing archive-member SHA-256 values",
    "archive container itself was not locally materialized",
    "**volume 34: 29 PDFs**",
]:
    assert required in report, required
assert len(re.findall(r"^\| M-\d{4} \|", report, re.MULTILINE)) == 28

volume_34_rows = [row for row in inventory_rows if row["volume"] == "34"]
assert len(volume_34_rows) == 29
assert Counter(row["issue"] for row in volume_34_rows) == Counter({"1": 18, "2": 11})
assert all(row["research_status"] == "not processed" for row in volume_34_rows)
remaining_rows = [
    row for row in inventory_rows
    if row["record_type"] == "archive_pdf" and row["volume"].isdigit() and int(row["volume"]) >= 34
]
assert len(remaining_rows) == 283

print("PASS volume33_publisher_member_hashes=36 text_nonempty=36 archive_container_materialized=0")
print("PASS inventory_dispositions promoted=3 contextual=25 title=0 metadata=8")
print("PASS ledger_rows=115 sequential_ids=115 new_statuses=B1,C2,F1")
print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
print("PASS discovery_rows=36 nonmetadata=28 child_candidate_files=9")
print("PASS report_close_read_rows=28 state_boundary=volumes_1_33")
print("PASS next_boundary=volume34 pdfs=29 issue1=18 issue2=11 remaining_34_45=283")
