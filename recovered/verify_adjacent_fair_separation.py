#!/usr/bin/env python3
"""Verify the source-free adjacent fair-separation checkpoint."""

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
    expected_ids = [f"F-{number:03d}" for number in range(1, 187)]
    assert [row["finding_id"] for row in ledger] == expected_ids

    unit = rows(ROOT / "COMMUNITIES-ADJACENT-FAIR-SEPARATION-EVIDENCE-LEDGER.csv")
    unit_ids = ["F-183", "F-184", "F-185", "F-186"]
    assert [row["finding_id"] for row in unit] == unit_ids
    assert {row["finding_id"]: row for row in ledger[-4:]} == {
        row["finding_id"]: row for row in unit
    }
    assert [row["source_record_id"] for row in unit] == [
        "E-001", "E-002", "E-003", "E-004"
    ]
    assert [row["article_gap_status"] for row in unit] == ["C", "B", "B", "C"]
    assert all(row["supporting_excerpt"] == "" for row in unit)
    assert all(row["external_verification_needed"] == "yes" for row in unit)
    assert "draft operating instrument" in unit[0]["evidence_type"]
    assert "no direct right to an individual" in unit[1]["exact_factual_observation"]
    assert "not a planned daughter split" in unit[2]["exact_factual_observation"]
    assert "judgment-derived claim notice" in unit[3]["evidence_type"]
    assert "explicitly a draft" in unit[0]["what_source_does_not_establish"]
    assert "aggregate parity" in unit[2]["what_source_establishes"]
    assert "do not establish completed trust closure" in unit[3]["what_source_does_not_establish"]

    cumulative_sources = rows(ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv")
    unit_sources = rows(ROOT / "COMMUNITIES-ADJACENT-FAIR-SEPARATION-SOURCE-INVENTORY.csv")
    assert [row["record_id"] for row in cumulative_sources] == [
        "A-001", "A-002", "A-003", "A-004", "A-005",
        "B-001", "B-002", "B-003", "B-004",
        "C-001", "C-002", "C-003", "C-004",
        "D-001", "D-002", "D-003",
        "E-001", "E-002", "E-003", "E-004",
    ]
    assert [row["record_id"] for row in unit_sources] == [
        "E-001", "E-002", "E-003", "E-004"
    ]
    assert cumulative_sources[-4:] == unit_sources
    assert [row["year"] for row in unit_sources] == ["2016", "2013", "1986", "2025"]
    for row in unit_sources:
        assert row["accessed_on"] == "2026-08-15"
        assert row["disposition"].endswith("promoted")
        assert row["doi"] == ""
    assert "thefec.org" in unit_sources[0]["canonical_url"]
    assert "thefec.org" in unit_sources[1]["canonical_url"]
    assert "vlex.com" in unit_sources[2]["canonical_url"]
    assert "jesus.org.uk" in unit_sources[3]["canonical_url"]
    assert "no signed final agreement" in unit_sources[0]["sequence_later_outcome"]
    assert "no audit" in unit_sources[1]["sequence_later_outcome"]
    assert "not member wellbeing" in unit_sources[2]["sequence_later_outcome"]
    assert "remain incomplete" in unit_sources[3]["sequence_later_outcome"]

    gap = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    gap_rows = re.findall(r"^\| G-\d{3} \| ([BCD]) \|", gap, flags=re.MULTILINE)
    assert Counter(gap_rows) == Counter({"B": 8, "C": 7, "D": 3})
    assert "fair-separation/pooled-risk/planned-fission units" in gap
    expected_gap_refs = {
        "G-001": ["F-183", "F-186"],
        "G-005": ["F-184", "F-185"],
        "G-006": unit_ids,
        "G-008": ["F-183", "F-186"],
        "G-012": unit_ids,
        "G-013": ["F-183", "F-184", "F-186"],
        "G-016": ["F-185"],
    }
    for gap_id, finding_ids in expected_gap_refs.items():
        line = next(item for item in gap.splitlines() if item.startswith(f"| {gap_id} |"))
        for finding_id in finding_ids:
            assert finding_id in line
    for finding_id in unit_ids:
        assert finding_id in gap
    assert "produced no forced relocation" in gap

    report = (
        ROOT / "COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md"
    ).read_text(encoding="utf-8")
    report_lower = report.lower()
    for finding_id in unit_ids:
        assert finding_id in report
    for domain in ["thefec.org", "geo.coop", "hutterites.org", "vlex.com", "jesus.org.uk"]:
        assert domain in report
    for heading in [
        "## Cross-record control map",
        "## Is exit usable before crisis?",
        "## Neutrality test",
        "## Planned-fission choice and viability",
        "## Later-outcome rule",
        "## Transfer boundary",
        "## Finite-roadmap completion",
    ]:
        assert heading in report
    assert "draft is not adoption" in report_lower
    assert "no direct right to an individual" in report_lower
    assert "aggregate parity" in report_lower and "individual consent" in report_lower
    assert "a claims cutoff is not a fair exit" in report_lower
    assert "there is no next research unit" in report_lower

    roadmap = (
        REPOSITORY
        / "docs"
        / "superpowers"
        / "plans"
        / "2026-08-15-adjacent-source-roadmap.md"
    ).read_text(encoding="utf-8")
    assert roadmap.count("Status: completed") == 5
    assert "COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md" in roadmap
    assert "completes the finite adjacent-source roadmap" in roadmap
    assert "The Mothership LLC operating agreement" in roadmap
    assert "PEACH's current official governance page" in roadmap
    assert "Walter Estate v. Walter" in roadmap
    assert "Jesus Fellowship Community Trust Schedule 1A" in roadmap

    state = (ROOT / "COMMUNITIES-RESEARCH-STATE.md").read_text(encoding="utf-8")
    readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
    index = (REPOSITORY / "docs" / "INDEX.md").read_text(encoding="utf-8")
    agents = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
    assert "**186 findings** (`F-001` through `F-186`)" in state
    assert "all five units in the finite adjacent-source roadmap are complete" in state
    assert "Do not invent another research unit" in state
    assert "**186** evidence findings (`F-001` through `F-186`)" in readme
    assert "COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md" in readme
    assert "COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md" in index
    assert "test_adjacent_fair_separation_workflow.py" in agents
    assert "verify_adjacent_fair_separation.py" in agents

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
    assert "zero for transferring medical decision authority" in combined
    assert "no forced relocation" in combined
    assert "zero for privately extinguishing legal rights" in combined

    print("adjacent fair separation verification: PASS")


if __name__ == "__main__":
    main()
