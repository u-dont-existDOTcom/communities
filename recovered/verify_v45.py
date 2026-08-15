#!/usr/bin/env python3
"""Verify the completed volume 45 checkpoint and journal-stream boundary."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
REPORT = ROOT / "COMMUNITIES-V45-RESEARCH-REPORT.md"
RANKING = ROOT / "V45-DISCOVERY-RANKING.csv"
CHILD_CONTEXTS = ROOT / "v45-child-danger-contexts.txt"
CORPUS = ROOT / "corpus-v45"
README = REPOSITORY / "README.md"

ARCHIVE_RECORD_ID = "D-003"
ARCHIVE_SIZE = 55_770_584
ARCHIVE_SHA256 = "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c"
ARCHIVE_RAW_ROW = (
    "D-003,drive_archive,REDACTED,COMMUNAL-SOCIETIES-v41-v45.zip,application/zip,"
    "55770584,COMMUNAL-SOCIETIES-v41-v45.zip,,,,,,,,,,"
    "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c,"
    "not_applicable,not processed,raw/COMMUNAL-SOCIETIES-v41-v45.zip,,"
    "Drive inventory row; archive downloaded and integrity-tested; members follow"
)
LEDGER_PREFIX_SHA256 = "90574aeb08c4877af76149eaedc6689310003b6136f2b616a97bb97923cbc9f4"

PROMOTED_IDS = {"M-0119", "M-0120"}
FUNCTIONAL_METADATA_IDS = {"M-0116", "M-0117", "M-0118", "M-0130"}
EXPECTED_VOLUME_IDS = {f"M-{number:04d}" for number in range(116, 131)}


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    default_archive = os.environ.get("COMMUNITIES_V41_V45_ARCHIVE")
    parser.add_argument(
        "--archive",
        type=Path,
        default=Path(default_archive) if default_archive else None,
        help="optional local vol41-45 source ZIP to reverify",
    )
    return parser.parse_args()


def verify_archive(archive: Path, volume_rows: list[dict[str, str]]) -> None:
    assert archive.is_file(), archive
    assert archive.stat().st_size == ARCHIVE_SIZE
    assert sha256(archive) == ARCHIVE_SHA256
    with zipfile.ZipFile(archive) as package:
        bad = package.testzip()
        assert bad is None, bad
        manifest = package.read("SHA256SUMS.txt").decode("utf-8")
        manifest_rows = {
            name: digest
            for digest, name in (
                line.split(maxsplit=1)
                for line in manifest.splitlines()
                if line.strip()
            )
        }
        expected_names = {row["internal_filename"] for row in volume_rows}
        assert expected_names <= set(package.namelist())
        for row in volume_rows:
            name = row["internal_filename"]
            payload = package.read(name)
            digest = hashlib.sha256(payload).hexdigest()
            assert digest == manifest_rows[name] == row["sha256"], row["record_id"]


def verify_checkpoint(archive: Path | None) -> None:
    with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
        inventory_rows = list(csv.DictReader(handle))
    assert len(inventory_rows) == 1005
    assert Counter(row["record_type"] for row in inventory_rows)["archive_pdf"] == 984
    assert all(row["drive_file_id"] in {"", "REDACTED"} for row in inventory_rows)
    assert any(row["drive_file_id"] == "REDACTED" for row in inventory_rows)

    volume_rows = [row for row in inventory_rows if row["volume"] == "45"]
    assert len(volume_rows) == 15
    assert Counter(row["issue"] for row in volume_rows) == Counter({"1": 15})
    assert {row["record_id"] for row in volume_rows} == EXPECTED_VOLUME_IDS
    assert Counter(row["notes"] for row in volume_rows) == Counter({
        "kind=article": 2,
        "kind=book_review": 9,
        "kind=front_matter": 1,
        "kind=contents": 1,
        "kind=editorial": 1,
        "kind=back_matter": 1,
    })
    assert Counter(row["research_status"] for row in volume_rows) == Counter({
        "metadata triaged": 4,
        "close read; finding promoted": 2,
        "contextual close read; no distinct finding": 9,
    })
    assert all(row["text_extraction_status"] == "extracted" for row in volume_rows)

    archive_row = next(
        row for row in inventory_rows if row["record_id"] == ARCHIVE_RECORD_ID
    )
    assert archive_row["drive_size_bytes"] == str(ARCHIVE_SIZE)
    assert archive_row["sha256"] == ARCHIVE_SHA256
    assert archive_row["research_status"] == "not processed"
    assert archive_row["local_path"] == "raw/COMMUNAL-SOCIETIES-v41-v45.zip"
    assert archive_row["notes"] == (
        "Drive inventory row; archive downloaded and integrity-tested; members follow"
    )
    assert INVENTORY.read_text(encoding="utf-8-sig").splitlines().count(
        ARCHIVE_RAW_ROW
    ) == 1

    for row in volume_rows:
        relative = Path(row["internal_filename"]).relative_to("archive")
        pdf = CORPUS / relative
        extracted = pdf.with_suffix(".txt")
        assert pdf.is_file() and pdf.stat().st_size > 0, row["record_id"]
        assert extracted.is_file() and extracted.stat().st_size > 0, row["record_id"]
        assert sha256(pdf) == row["sha256"], row["record_id"]
        assert pdf_pages(pdf) == int(row["pdf_pages"]), row["record_id"]
        assert row["local_path"] == f"recovered/corpus-v45/{relative.as_posix()}"
        assert row["text_path"] == (
            f"recovered/corpus-v45/{relative.with_suffix('.txt').as_posix()}"
        )
        if row["record_id"] in PROMOTED_IDS:
            assert row["research_status"] == "close read; finding promoted"
        elif row["record_id"] in FUNCTIONAL_METADATA_IDS:
            assert row["research_status"] == "metadata triaged"
        else:
            assert row["research_status"] == "contextual close read; no distinct finding"

    if archive is not None:
        verify_archive(archive, volume_rows)

    ledger_bytes = LEDGER.read_bytes()
    marker = b"F-159,"
    assert ledger_bytes.count(marker) == 1
    ledger_prefix = ledger_bytes.split(marker, 1)[0]
    assert hashlib.sha256(ledger_prefix).hexdigest() == LEDGER_PREFIX_SHA256, (
        "pre-volume-45 evidence-ledger bytes changed"
    )
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        ledger_rows = list(csv.DictReader(handle))
    expected_ids = [f"F-{number:03d}" for number in range(1, 163)]
    assert len(ledger_rows) == 162
    assert [row["finding_id"] for row in ledger_rows] == expected_ids
    new_rows = ledger_rows[-4:]
    assert [row["finding_id"] for row in new_rows] == [
        "F-159", "F-160", "F-161", "F-162"
    ]
    assert [row["source_record_id"] for row in new_rows] == [
        "M-0119", "M-0119", "M-0120", ""
    ]
    assert Counter(row["article_gap_status"] for row in new_rows) == Counter(
        {"B": 2, "C": 1, "F": 1}
    )
    assert all(row["supporting_excerpt"] == "" for row in new_rows)

    gap_text = GAP_BANK.read_text(encoding="utf-8")
    gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter(
        {"B": 8, "C": 7, "D": 3}
    )
    assert "Checkpoint: *Communal Societies* volumes 1-45" in gap_text
    assert "through volume 45" in gap_text
    assert (
        "F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, "
        "F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, "
        "F-148, F-151, F-154, F-158, F-162"
    ) in gap_text
    gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
    assert gap_references <= set(expected_ids), sorted(gap_references - set(expected_ids))
    for finding_id in ("F-159", "F-160", "F-161", "F-162"):
        assert finding_id in gap_text

    with RANKING.open(newline="", encoding="utf-8-sig") as handle:
        ranking_rows = list(csv.DictReader(handle))
    assert len(ranking_rows) == 15
    assert {row["record_id"] for row in ranking_rows} == EXPECTED_VOLUME_IDS
    assert Counter(row["functional_class"] for row in ranking_rows) == Counter({
        "substantive": 11,
        "metadata": 4,
    })
    assert {
        row["record_id"]
        for row in ranking_rows
        if row["functional_class"] == "metadata"
    } == FUNCTIONAL_METADATA_IDS
    child_headers = re.findall(
        r"^===== M-\d{4}\b",
        CHILD_CONTEXTS.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    assert len(child_headers) == 4

    state = STATE.read_text(encoding="utf-8")
    for required in [
        "volumes **1-45**",
        "**984 journal PDFs**",
        "443 close-read",
        "207 title/keyword-triaged",
        "334 metadata-triaged",
        "**162 findings** (`F-001` through `F-162`)",
        "**984 of 984 journal PDFs**",
        "no journal PDFs remaining",
        "Do not repeat volumes 1-45",
    ]:
        assert required in state, required

    report = REPORT.read_text(encoding="utf-8")
    for required in [
        "All **15 PDFs** in volume 45 were processed",
        "**11** substantive close reads",
        "**0** additional articles left at title-and-keyword triage",
        "**4** front-matter, contents, editorial, and back-matter metadata triages",
        "**4 new findings, F-159 through F-162**",
        "exactly matching the saved D-003 container record",
        "**984 of 984 journal PDFs**",
    ]:
        assert required in report, required
    report_ids = set(re.findall(r"^\| (M-\d{4}) \|", report, re.MULTILINE))
    assert report_ids == EXPECTED_VOLUME_IDS - FUNCTIONAL_METADATA_IDS

    readme = README.read_text(encoding="utf-8")
    for required in [
        "Volumes **1-45** complete",
        "**984** journal PDFs triaged",
        "**443** relevant or contextual close reads",
        "**162** evidence findings (`F-001` through `F-162`)",
        "Journal stream: **complete, 984 of 984 PDFs**",
        "recovered/COMMUNITIES-V45-RESEARCH-REPORT.md",
        "recovered/corpus-v45/",
        "python recovered/test_v45_workflow.py",
        "python recovered/verify_v45.py",
    ]:
        assert required in readme, required

    remaining_journal = [
        row
        for row in inventory_rows
        if row["record_type"] == "archive_pdf"
        and row["research_status"] == "not processed"
    ]
    assert not remaining_journal

    git_check = "skipped_no_worktree"
    probe = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=REPOSITORY,
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode == 0 and probe.stdout.strip() == "true":
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=REPOSITORY,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        assert not any(path.startswith("recovered/corpus-v45/") for path in tracked)
        assert not any(path.endswith((".pdf", ".zip", ".png")) for path in tracked)
        assert not any(
            "v45-keyword-contexts" in path or "v45-child-danger-contexts" in path
            for path in tracked
        )
        git_check = "passed"

    archive_result = 1 if archive is not None else 0
    print(
        "PASS volume45_member_hashes=15 pages_verified=15 text_nonempty=15 "
        f"source_archive_reverified={archive_result}"
    )
    print("PASS inventory_dispositions promoted_sources=2 contextual=9 title=0 metadata=4")
    print("PASS ledger_rows=162 sequential_ids=162 new_statuses=B2,C1,F1")
    print("PASS gap_rows=18 classes=B8,C7,D3 references_valid=1")
    print("PASS discovery_rows=15 substantive=11 metadata=4 child_candidate_files=4")
    print("PASS report_close_read_rows=11 state_boundary=volumes_1_45")
    print("PASS journal_boundary=984_of_984 remaining_journal_pdfs=0")
    print(f"PASS source_exclusion_git_check={git_check}")


def main() -> None:
    args = parse_args()
    verify_checkpoint(args.archive)


if __name__ == "__main__":
    main()
