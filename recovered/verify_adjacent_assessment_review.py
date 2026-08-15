#!/usr/bin/env python3
"""Verify the source-free adjacent assessment and review checkpoint."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        loaded = list(reader)
    assert all(None not in row for row in loaded), f"extra CSV fields in {path.name}"
    assert all(None not in row.values() for row in loaded), f"missing CSV fields in {path.name}"
    return loaded


def main() -> None:
    ledger = rows(ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv")
    expected_ids = [f"F-{number:03d}" for number in range(1, 176)]
    assert [row["finding_id"] for row in ledger] == expected_ids

    unit = rows(ROOT / "COMMUNITIES-ADJACENT-ASSESSMENT-EVIDENCE-LEDGER.csv")
    unit_ids = ["F-172", "F-173", "F-174", "F-175"]
    assert [row["finding_id"] for row in unit] == unit_ids
    assert {row["finding_id"]: row for row in ledger[-4:]} == {
        row["finding_id"]: row for row in unit
    }
    assert [row["source_record_id"] for row in unit] == [
        "B-001", "B-002", "B-003", "B-004"
    ]
    assert [row["article_gap_status"] for row in unit] == ["C", "C", "C", "C"]
    assert all(row["supporting_excerpt"] == "" for row in unit)
    assert "current authoritative" in unit[0]["evidence_type"]
    assert "six-month" in unit[1]["evidence_type"]
    assert "prospective field" in unit[2]["evidence_type"]
    assert "quality-improvement" in unit[3]["evidence_type"]
    assert "no significant reduction" in unit[3]["outcome"].lower()

    cumulative_sources = rows(ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv")
    unit_sources = rows(ROOT / "COMMUNITIES-ADJACENT-ASSESSMENT-SOURCE-INVENTORY.csv")
    assert [row["record_id"] for row in cumulative_sources] == [
        "A-001", "A-002", "A-003", "A-004", "A-005",
        "B-001", "B-002", "B-003", "B-004",
    ]
    assert [row["record_id"] for row in unit_sources] == [
        "B-001", "B-002", "B-003", "B-004"
    ]
    assert cumulative_sources[-4:] == unit_sources
    for row in unit_sources:
        assert row["accessed_on"] == "2026-08-15"
        assert row["disposition"].endswith("promoted")
        if row["doi"]:
            assert row["canonical_url"] == "https://doi.org/" + row["doi"]
    assert "official recommendations" in unit_sources[0]["access_status"]
    assert "fully updating" in unit_sources[0]["notes"]
    assert "no significant change" in unit_sources[3]["sequence_later_outcome"]

    gap = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    gap_rows = re.findall(r"^\| G-\d{3} \| ([BCD]) \|", gap, flags=re.MULTILINE)
    assert Counter(gap_rows) == Counter({"B": 8, "C": 7, "D": 3})
    assert "adjacent child-response and assessment/review units" in gap
    expected_gap_refs = {
        "G-001": ["F-172", "F-175"],
        "G-002": ["F-172"],
        "G-005": ["F-172"],
        "G-006": ["F-173", "F-174", "F-175"],
        "G-009": ["F-172", "F-175"],
        "G-018": ["F-173", "F-174"],
    }
    for gap_id, finding_ids in expected_gap_refs.items():
        line = next(item for item in gap.splitlines() if item.startswith(f"| {gap_id} |"))
        for finding_id in finding_ids:
            assert finding_id in line
    for finding_id in unit_ids:
        assert finding_id in gap
    assert "produced no community screening instrument" in gap

    report = (ROOT / "COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md").read_text(encoding="utf-8")
    for finding_id in unit_ids:
        assert finding_id in report
    for doi in [
        "10.1080/14789940802114475",
        "10.1177/10731911211063228",
        "10.1136/bmjoq-2023-002704",
    ]:
        assert doi in report
    for heading in [
        "### Observable and preservable by ordinary residents",
        "### Requires independent qualified assessment",
        "### Requires lawful emergency or statutory authority",
    ]:
        assert heading in report
    assert "No community screening instrument was created" in report
    assert "Neither event rate nor severity decreased significantly" in report
    assert "provisional update materials are not final guidance" in report
    assert "still does not supply the complete case history" in report

    roadmap = (
        REPOSITORY
        / "docs"
        / "superpowers"
        / "plans"
        / "2026-08-15-adjacent-source-roadmap.md"
    ).read_text(encoding="utf-8")
    assert roadmap.count("Status: completed") == 2
    assert "COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md" in roadmap
    assert "the exact next boundary is Unit C" in roadmap
    for doi in [
        "10.1080/14789940802114475",
        "10.1177/10731911211063228",
        "10.1136/bmjoq-2023-002704",
    ]:
        assert doi in roadmap

    state = (ROOT / "COMMUNITIES-RESEARCH-STATE.md").read_text(encoding="utf-8")
    readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
    index = (REPOSITORY / "docs" / "INDEX.md").read_text(encoding="utf-8")
    agents = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
    assert "**175 findings** (`F-001` through `F-175`)" in state
    assert "The next bounded unit is Unit C" in state
    assert "**175** evidence findings (`F-001` through `F-175`)" in readme
    assert "COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md" in readme
    assert "COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md" in index
    assert "test_adjacent_assessment_review_workflow.py" in agents
    assert "verify_adjacent_assessment_review.py" in agents

    forbidden_suffixes = {".pdf", ".epub", ".zip"}
    forbidden_dirs = {"corpus-adjacent", "adjacent-full-text", "source-downloads"}
    local_source_roots = {"corpus-v45", "corpus-standalone"}
    for path in REPOSITORY.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(REPOSITORY)
        if (
            len(relative.parts) > 1
            and relative.parts[0] == "recovered"
            and relative.parts[1] in local_source_roots
        ):
            continue
        assert path.suffix.lower() not in forbidden_suffixes, f"source binary present: {path}"
        assert not forbidden_dirs.intersection(path.parts), f"source directory present: {path}"

    combined = "\n".join(
        row["notes"]
        + " "
        + row["what_source_establishes"]
        + " "
        + row["what_source_does_not_establish"]
        + " "
        + row["transferability"]
        for row in unit
    ).lower()
    for prohibited in [
        "should execute",
        "forced assimilation",
        "remove the child permanently",
        "community psychopathy screen",
    ]:
        assert prohibited not in combined
    assert "zero for a lay-created screen" in combined
    assert "not independent external review" in combined

    print("adjacent assessment and review verification: PASS")


if __name__ == "__main__":
    main()
