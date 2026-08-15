#!/usr/bin/env python3
"""Verify the completed eight-source standalone checkpoint."""

from __future__ import annotations

import csv
import hashlib
import io
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
CORPUS = ROOT / "corpus-standalone"
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
REPORT = ROOT / "COMMUNITIES-STANDALONE-RESEARCH-REPORT.md"
RANKING = ROOT / "STANDALONE-DISCOVERY-RANKING.csv"
KEYWORD_CONTEXTS = ROOT / "standalone-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "standalone-child-danger-contexts.txt"
README = REPOSITORY / "README.md"
AGENTS = REPOSITORY / "AGENTS.md"
INDEX = REPOSITORY / "docs" / "INDEX.md"
PLAN = REPOSITORY / "docs" / "superpowers" / "plans" / "2026-08-14-standalone-research.md"

LEDGER_PREFIX_SHA256 = "6ed0657ec35bc5d56d0ad3f22ddfdc8853a5bccd3424ee9279f3c9dcc4be1541"
NON_STANDALONE_INVENTORY_SHA256 = "335821a605fd17269acc0882a1d462b55a5b3ad0c08a974baa7ca19ec02027c9"

SOURCES = {
    "D-001": ("D-001-alienation-and-charisma.pdf", 23_783_671, 488, "ac1af0c28f1ed953dbb0c92db90f6aa9815309a230a28a51af019b062f653535"),
    "D-002": ("D-002-commitment-and-community.pdf", 15_933_042, 324, "02e6817cd2e8295e28aee842b95e496605f8624b136bb48844fc42080b4e0684"),
    "D-004": ("D-004-evil-genes.pdf", 5_518_847, 427, "fd5001e2af795928330791023547f5a03844042b5a3bc45f1d32db5e99b6bc98"),
    "D-005": ("D-005-wrangham-targeted-conspiratorial-killing.pdf", 375_081, 21, "c0509337e38c00f37384c7b1255cf2e37432642ec174928d7fe096360cd0b0fd"),
    "D-006": ("D-006-the-kung-san.pdf", 32_740_431, 564, "ca821f84da90e7475ff1d919935a14d0ba4fbdcc263296a83385351aeea2bc97"),
    "D-007": ("D-007-the-mountain-people.pdf", 17_300_144, 324, "c34bc1a621a214725ecd89c0c2d100ffb83adda6dcba21c24dc998830094b6f3"),
    "D-008": ("D-008-the-riddle-of-amish-culture.epub", 10_492_959, None, "6b79ab85b331e106f2fea62da75f955604370570cc394638e8ad1cfd119c8557"),
    "D-018": ("D-018-zarpentine-dissertation.pdf", 1_736_362, 317, "5eb136c64c1922dd53fac829e473167030071a6101521f6c260468968ec15065"),
}

PROMOTED = {"D-001", "D-006", "D-008"}
CONTEXTUAL = set(SOURCES) - PROMOTED


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


def canonical_inventory_hash(
    fieldnames: list[str], rows: list[dict[str, str]]
) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return hashlib.sha256(output.getvalue().encode("utf-8")).hexdigest()


def verify_sources(rows_by_id: dict[str, dict[str, str]]) -> None:
    for record_id, (filename, size, pages, expected_hash) in SOURCES.items():
        row = rows_by_id[record_id]
        source = CORPUS / filename
        text_path = source.with_suffix(".txt")
        assert source.is_file() and source.stat().st_size == size, record_id
        assert sha256(source) == expected_hash, record_id
        assert text_path.is_file() and text_path.stat().st_size > 0, record_id
        assert row["drive_size_bytes"] == str(size), record_id
        assert row["sha256"] == expected_hash, record_id
        assert row["text_extraction_status"] == "extracted", record_id
        assert row["local_path"] == f"recovered/corpus-standalone/{filename}", record_id
        assert row["text_path"] == f"recovered/corpus-standalone/{text_path.name}", record_id
        if pages is None:
            assert row["pdf_pages"] == "", record_id
            with zipfile.ZipFile(source) as package:
                assert package.testzip() is None, record_id
                assert "mimetype" in package.namelist(), record_id
        else:
            assert row["pdf_pages"] == str(pages), record_id
            assert pdf_pages(source) == pages, record_id
        if record_id in PROMOTED:
            assert row["research_status"] == "close read; findings promoted", record_id
        else:
            assert row["research_status"] == "contextual close read; no distinct finding", record_id


def verify_checkpoint() -> None:
    with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        inventory_rows = list(reader)
    assert fieldnames is not None
    assert len(inventory_rows) == 1005
    assert Counter(row["record_type"] for row in inventory_rows)["archive_pdf"] == 984
    assert all(row["drive_file_id"] in {"", "REDACTED"} for row in inventory_rows)
    rows_by_id = {row["record_id"]: row for row in inventory_rows}
    assert set(SOURCES) <= set(rows_by_id)
    standalone_rows = [rows_by_id[record_id] for record_id in SOURCES]
    assert Counter(row["research_status"] for row in standalone_rows) == Counter({
        "close read; findings promoted": 3,
        "contextual close read; no distinct finding": 5,
    })
    non_standalone = [row for row in inventory_rows if row["record_id"] not in SOURCES]
    assert len(non_standalone) == 997
    assert canonical_inventory_hash(fieldnames, non_standalone) == NON_STANDALONE_INVENTORY_SHA256
    verify_sources(rows_by_id)

    ledger_bytes = LEDGER.read_bytes()
    marker = b"F-163,"
    assert ledger_bytes.count(marker) == 1
    assert hashlib.sha256(ledger_bytes.split(marker, 1)[0]).hexdigest() == LEDGER_PREFIX_SHA256
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        ledger_rows = list(csv.DictReader(handle))
    expected_ids = [f"F-{number:03d}" for number in range(1, 169)]
    assert len(ledger_rows) == 168
    assert [row["finding_id"] for row in ledger_rows] == expected_ids
    new_rows = ledger_rows[-6:]
    assert [row["finding_id"] for row in new_rows] == [
        "F-163", "F-164", "F-165", "F-166", "F-167", "F-168"
    ]
    assert [row["source_record_id"] for row in new_rows] == [
        "D-001", "D-001", "D-006", "D-006", "D-008", ""
    ]
    assert Counter(row["article_gap_status"] for row in new_rows) == Counter(
        {"B": 2, "C": 3, "F": 1}
    )
    assert all(row["supporting_excerpt"] == "" for row in new_rows)
    assert all(row["source_access"] for row in new_rows)
    assert all(row["what_source_does_not_establish"] for row in new_rows)
    assert all(row["alternative_interpretation"] for row in new_rows)
    assert all(row["response_process"] for row in new_rows)
    assert all(row["outcome"] for row in new_rows)
    assert all(row["transferability"] for row in new_rows)

    gap_text = GAP_BANK.read_text(encoding="utf-8")
    gap_lines = [line for line in gap_text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter(
        {"B": 8, "C": 7, "D": 3}
    )
    assert "volumes 1-45 plus eight standalone sources" in gap_text
    gap_references = set(re.findall(r"\bF-\d{3}\b", gap_text))
    assert gap_references <= set(expected_ids)
    for finding_id in expected_ids[-6:]:
        assert finding_id in gap_text
    for required in [
        "Wrangham's execution hypothesis is theory",
        "unethical, coercive, unsupported, and explicitly rejected",
        "traditional-society evidence lane",
        "bounded negative result",
    ]:
        assert required in gap_text, required

    with RANKING.open(newline="", encoding="utf-8-sig") as handle:
        ranking_rows = list(csv.DictReader(handle))
    assert len(ranking_rows) == 8
    assert {row["record_id"] for row in ranking_rows} == set(SOURCES)
    assert Counter(row["functional_class"] for row in ranking_rows) == Counter(
        {"substantive": 8}
    )
    required_families = {
        "danger", "sanction", "governance", "child", "exit", "clinical",
        "process_allegation", "process_assessment", "process_intervention",
        "process_review", "process_outcome", "process_families_present",
    }
    assert required_families <= set(ranking_rows[0])
    assert KEYWORD_CONTEXTS.is_file() and KEYWORD_CONTEXTS.stat().st_size > 0
    assert CHILD_CONTEXTS.is_file() and CHILD_CONTEXTS.stat().st_size > 0
    child_headers = re.findall(
        r"^===== (D-\d{3})\b",
        CHILD_CONTEXTS.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    assert len(child_headers) == 8
    assert set(child_headers) == set(SOURCES)

    state = STATE.read_text(encoding="utf-8")
    for required in [
        "**984 journal PDFs**",
        "**168 findings** (`F-001` through `F-168`)",
        "**8 of 8 standalone substantive sources**",
        "No journal PDF or assigned standalone source remains",
        "Article drafting or revision remains outside scope",
    ]:
        assert required in state, required

    report = REPORT.read_text(encoding="utf-8")
    for required in [
        "**8 of 8 substantive sources**",
        "**8 full-text close reads**",
        "**6 new findings, F-163 through F-168**",
        "**984 journal PDFs plus 8 standalone substantive sources**",
        "No assigned source remains",
        "No article prose was drafted or revised",
    ]:
        assert required in report, required
    report_ids = set(re.findall(r"^\| (D-\d{3}) \|", report, re.MULTILINE))
    assert report_ids == set(SOURCES)

    readme = README.read_text(encoding="utf-8")
    for required in [
        "**168** evidence findings (`F-001` through `F-168`)",
        "**complete, 984 journal PDFs plus 8 standalone sources**",
        "COMMUNITIES-STANDALONE-RESEARCH-REPORT.md",
        "python recovered/test_standalone_workflow.py",
        "python recovered/verify_standalone.py",
    ]:
        assert required in readme, required
    assert "test_standalone_workflow.py" in AGENTS.read_text(encoding="utf-8")
    assert "verify_standalone.py" in AGENTS.read_text(encoding="utf-8")
    assert "COMMUNITIES-STANDALONE-RESEARCH-REPORT.md" in INDEX.read_text(encoding="utf-8")
    assert PLAN.is_file()

    gitignore = (REPOSITORY / ".gitignore").read_text(encoding="utf-8")
    for required in [
        "recovered/corpus-standalone/",
        "recovered/standalone-keyword-contexts.txt",
        "recovered/standalone-child-danger-contexts.txt",
        "recovered/*.zip",
    ]:
        assert required in gitignore, required

    print(
        "verified standalone checkpoint: sources=8 close_reads=8 "
        "findings=168 gaps=18 journal_pdfs=984"
    )


if __name__ == "__main__":
    verify_checkpoint()
