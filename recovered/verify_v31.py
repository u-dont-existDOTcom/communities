#!/usr/bin/env python3
"""Fresh structural verification for the completed volume 31 checkpoint."""

from __future__ import annotations

import csv
import hashlib
import re
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
REPORT = ROOT / "COMMUNITIES-V31-RESEARCH-REPORT.md"
RANKING = ROOT / "V31-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v31-child-danger-contexts.txt"
ARCHIVE = ROOT / "vol31.zip"
CORPUS = ROOT / "corpus-v31"


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

volume_rows = [row for row in inventory_rows if row["volume"] == "31"]
assert len(volume_rows) == 31
assert Counter(row["notes"] for row in volume_rows) == Counter({
    "kind=book_review": 15,
    "kind=article": 8,
    "kind=front_matter": 2,
    "kind=contents": 2,
    "kind=editorial": 2,
    "kind=back_matter": 2,
})
assert Counter(row["research_status"] for row in volume_rows) == Counter({
    "contextual close read; no distinct finding": 14,
    "metadata triaged": 8,
    "title and keyword triaged": 7,
    "close read; finding promoted": 2,
})
assert all(row["text_extraction_status"] == "extracted" for row in volume_rows)

archive_row = next(row for row in inventory_rows if row["record_id"] == "D-012")
expected_archive_hash = "639c898fdb05d822850bd2bed975e8e6c6dd76d69515f6f0aeb2ffb6cee0933e"
assert archive_row["sha256"] == expected_archive_hash
assert archive_row["research_status"] == "container processed; 31 member PDFs triaged"
assert archive_row["local_path"] == "recovered/vol31.zip"
assert ARCHIVE.stat().st_size == 25_501_927
assert sha256(ARCHIVE) == expected_archive_hash

with zipfile.ZipFile(ARCHIVE) as archive:
    assert archive.testzip() is None
    zip_pdfs = {name for name in archive.namelist() if name.lower().endswith(".pdf")}
assert zip_pdfs == {row["internal_filename"] for row in volume_rows}

for row in volume_rows:
    pdf = CORPUS / row["internal_filename"]
    text = pdf.with_suffix(".txt")
    assert pdf.is_file() and pdf.stat().st_size > 0, row["record_id"]
    assert text.is_file() and text.stat().st_size > 0, row["record_id"]
    assert sha256(pdf) == row["sha256"], row["record_id"]
    assert row["local_path"] == f"recovered/corpus-v31/{row['internal_filename']}"
    assert row["text_path"] == f"recovered/corpus-v31/{row['internal_filename'][:-4]}.txt"

with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    ledger_reader = csv.DictReader(handle)
    ledger_rows = list(ledger_reader)
assert len(ledger_rows) == 105
expected_ids = [f"F-{number:03d}" for number in range(1, 106)]
assert [row["finding_id"] for row in ledger_rows] == expected_ids
assert Counter(row["article_gap_status"] for row in ledger_rows[-5:]) == Counter({"B": 2, "C": 2, "F": 1})
assert [row["finding_id"] for row in ledger_rows[-5:]] == ["F-101", "F-102", "F-103", "F-104", "F-105"]
assert {row["source_record_id"] for row in ledger_rows[-5:-1]} == {"M-0749", "M-0759"}
assert ledger_rows[-1]["source_record_id"] == ""

gap_text = GAP_BANK.read_text(encoding="utf-8")
gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
assert len(gap_lines) == 18
assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({"B": 8, "C": 7, "D": 3})
assert "Checkpoint: *Communal Societies* volumes 1-31" in gap_text
assert "through volume 31" in gap_text
assert "F-031, F-048, F-064, F-076, F-090, F-100, F-105" in gap_text
ledger_ids = set(expected_ids)
gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
assert gap_references <= ledger_ids, sorted(gap_references - ledger_ids)

with RANKING.open(newline="", encoding="utf-8-sig") as handle:
    ranking_rows = list(csv.DictReader(handle))
assert len(ranking_rows) == 31
metadata_kinds = {"front_matter", "contents", "editorial", "back_matter"}
assert sum(row["kind"] not in metadata_kinds for row in ranking_rows) == 23
child_headers = re.findall(r"^===== M-\d{4}\b", CHILD_CONTEXTS.read_text(encoding="utf-8"), re.MULTILINE)
assert len(child_headers) == 10

state = STATE.read_text(encoding="utf-8")
for required in [
    "volumes **1-31**",
    "**638 journal PDFs**",
    "186 close-read",
    "207 title/keyword-triaged",
    "245 metadata-triaged",
    "**105 findings** (`F-001` through `F-105`)",
    "Volumes **32-45** have not been processed: **346 journal PDFs**",
    "volume **32: 27 PDFs**",
]:
    assert required in state, required
assert "Do not repeat volumes 1-31" in state

report = REPORT.read_text(encoding="utf-8")
for required in [
    "All **31 PDFs** in volume 31 were processed",
    "**16** relevant or contextual close reads",
    "**7** additional articles or reviews title- and keyword-triaged",
    "**8** front matter, contents, editorials, and back matter metadata-triaged",
    "**5 new findings, F-101 through F-105**",
    "**volume 32: 27 PDFs**",
]:
    assert required in report, required
assert len(re.findall(r"^\| M-\d{4} \|", report, re.MULTILINE)) == 16

volume_32_rows = [row for row in inventory_rows if row["volume"] == "32"]
assert len(volume_32_rows) == 27
assert Counter(row["issue"] for row in volume_32_rows) == Counter({"1": 13, "2": 14})
assert all(row["research_status"] == "not processed" for row in volume_32_rows)

print("PASS archive_sha256_and_zip_integrity=1")
print("PASS volume31_pdf_hashes=31 text_nonempty=31")
print("PASS inventory_dispositions promoted=2 contextual=14 title=7 metadata=8")
print("PASS ledger_rows=105 sequential_ids=105 new_statuses=B2,C2,F1")
print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
print("PASS discovery_rows=31 nonmetadata=23 child_candidate_files=10")
print("PASS report_close_read_rows=16 state_boundary=volumes_1_31")
print("PASS next_boundary=volume32 pdfs=27 issue1=13 issue2=14 remaining_32_45=346")
