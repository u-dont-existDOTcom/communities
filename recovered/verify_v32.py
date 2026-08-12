#!/usr/bin/env python3
"""Fresh structural verification for the completed volume 32 checkpoint."""

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
REPORT = ROOT / "COMMUNITIES-V32-RESEARCH-REPORT.md"
RANKING = ROOT / "V32-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v32-child-danger-contexts.txt"
CORPUS = ROOT / "corpus-v32"

ARCHIVES = {
    "1": {
        "record_id": "D-013",
        "path": ROOT / "vol32-iss1.zip",
        "size": 52_973_234,
        "sha256": "d110decb49fdb935cee2f94a14055e52de3ab8fc6119e3734a0f908aab8ab7f9",
        "count": 13,
    },
    "2": {
        "record_id": "D-014",
        "path": ROOT / "vol32-iss2.zip",
        "size": 61_802_532,
        "sha256": "326193a31caa09ce1d9fd2d7908c445c31648df5f3f88f1f726b24b51307fbd5",
        "count": 14,
    },
}


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

volume_rows = [row for row in inventory_rows if row["volume"] == "32"]
assert len(volume_rows) == 27
assert Counter(row["issue"] for row in volume_rows) == Counter({"1": 13, "2": 14})
assert Counter(row["notes"] for row in volume_rows) == Counter({
    "kind=book_review": 11,
    "kind=article": 8,
    "kind=front_matter": 2,
    "kind=contents": 2,
    "kind=editorial": 2,
    "kind=back_matter": 2,
})
assert Counter(row["research_status"] for row in volume_rows) == Counter({
    "contextual close read; no distinct finding": 16,
    "metadata triaged": 8,
    "close read; finding promoted": 3,
})
assert all(row["text_extraction_status"] == "extracted" for row in volume_rows)

for issue, spec in ARCHIVES.items():
    archive_row = next(row for row in inventory_rows if row["record_id"] == spec["record_id"])
    assert archive_row["sha256"] == spec["sha256"]
    assert archive_row["research_status"] == f"container processed; {spec['count']} member PDFs triaged"
    assert archive_row["local_path"] == f"recovered/vol32-iss{issue}.zip"
    assert spec["path"].stat().st_size == spec["size"]
    assert sha256(spec["path"]) == spec["sha256"]
    with zipfile.ZipFile(spec["path"]) as archive:
        assert archive.testzip() is None
        zip_pdfs = {name for name in archive.namelist() if name.lower().endswith(".pdf")}
    issue_rows = [row for row in volume_rows if row["issue"] == issue]
    assert len(issue_rows) == spec["count"]
    assert zip_pdfs == {row["internal_filename"] for row in issue_rows}

for row in volume_rows:
    pdf = CORPUS / row["internal_filename"]
    text = pdf.with_suffix(".txt")
    assert pdf.is_file() and pdf.stat().st_size > 0, row["record_id"]
    assert text.is_file() and text.stat().st_size > 0, row["record_id"]
    assert sha256(pdf) == row["sha256"], row["record_id"]
    assert row["local_path"] == f"recovered/corpus-v32/{row['internal_filename']}"
    assert row["text_path"] == f"recovered/corpus-v32/{row['internal_filename'][:-4]}.txt"

with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    ledger_reader = csv.DictReader(handle)
    ledger_rows = list(ledger_reader)
assert len(ledger_rows) == 111
expected_ids = [f"F-{number:03d}" for number in range(1, 112)]
assert [row["finding_id"] for row in ledger_rows] == expected_ids
assert Counter(row["article_gap_status"] for row in ledger_rows[-6:]) == Counter({"B": 2, "C": 2, "D": 1, "F": 1})
assert [row["finding_id"] for row in ledger_rows[-6:]] == ["F-106", "F-107", "F-108", "F-109", "F-110", "F-111"]
assert {row["source_record_id"] for row in ledger_rows[-6:-1]} == {"M-0775", "M-0776", "M-0787"}
assert ledger_rows[-1]["source_record_id"] == ""

gap_text = GAP_BANK.read_text(encoding="utf-8")
gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
assert len(gap_lines) == 18
assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({"B": 8, "C": 7, "D": 3})
assert "Checkpoint: *Communal Societies* volumes 1-32" in gap_text
assert "through volume 32" in gap_text
assert "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111" in gap_text
ledger_ids = set(expected_ids)
gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
assert gap_references <= ledger_ids, sorted(gap_references - ledger_ids)

with RANKING.open(newline="", encoding="utf-8-sig") as handle:
    ranking_rows = list(csv.DictReader(handle))
assert len(ranking_rows) == 27
metadata_kinds = {"front_matter", "contents", "editorial", "back_matter"}
assert sum(row["kind"] not in metadata_kinds for row in ranking_rows) == 19
child_headers = re.findall(r"^===== M-\d{4}\b", CHILD_CONTEXTS.read_text(encoding="utf-8"), re.MULTILINE)
assert len(child_headers) == 9

state = STATE.read_text(encoding="utf-8")
for required in [
    "volumes **1-32**",
    "**665 journal PDFs**",
    "205 close-read",
    "207 title/keyword-triaged",
    "253 metadata-triaged",
    "**111 findings** (`F-001` through `F-111`)",
    "Volumes **33-45** have not been processed: **319 journal PDFs**",
    "volume **33: 36 PDFs**",
]:
    assert required in state, required
assert "Do not repeat volumes 1-32" in state

report = REPORT.read_text(encoding="utf-8")
for required in [
    "All **27 PDFs** in volume 32 were processed",
    "**19** relevant or contextual close reads",
    "**0** additional articles or reviews left at title-and-keyword triage",
    "**8** front matter, contents, editorials, and back matter metadata triages",
    "**6 new findings, F-106 through F-111**",
    "**volume 33: 36 PDFs**",
]:
    assert required in report, required
assert len(re.findall(r"^\| M-\d{4} \|", report, re.MULTILINE)) == 19

volume_33_rows = [row for row in inventory_rows if row["volume"] == "33"]
assert len(volume_33_rows) == 36
assert Counter(row["issue"] for row in volume_33_rows) == Counter({"1": 14, "2": 22})
assert all(row["research_status"] == "not processed" for row in volume_33_rows)
remaining_rows = [
    row for row in inventory_rows
    if row["record_type"] == "archive_pdf" and row["volume"].isdigit() and int(row["volume"]) >= 33
]
assert len(remaining_rows) == 319

print("PASS archive_sha256_and_zip_integrity=2")
print("PASS volume32_pdf_hashes=27 text_nonempty=27")
print("PASS inventory_dispositions promoted=3 contextual=16 title=0 metadata=8")
print("PASS ledger_rows=111 sequential_ids=111 new_statuses=B2,C2,D1,F1")
print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
print("PASS discovery_rows=27 nonmetadata=19 child_candidate_files=9")
print("PASS report_close_read_rows=19 state_boundary=volumes_1_32")
print("PASS next_boundary=volume33 pdfs=36 issue1=14 issue2=22 remaining_33_45=319")
