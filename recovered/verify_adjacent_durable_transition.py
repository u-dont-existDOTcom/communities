#!/usr/bin/env python3
"""Verify the source-free adjacent durable-treatment checkpoint."""

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
    expected_ids = [f"F-{number:03d}" for number in range(1, 180)]
    assert [row["finding_id"] for row in ledger] == expected_ids

    unit = rows(ROOT / "COMMUNITIES-ADJACENT-DURABLE-EVIDENCE-LEDGER.csv")
    unit_ids = ["F-176", "F-177", "F-178", "F-179"]
    assert [row["finding_id"] for row in unit] == unit_ids
    assert {row["finding_id"]: row for row in ledger[-4:]} == {
        row["finding_id"]: row for row in unit
    }
    assert [row["source_record_id"] for row in unit] == [
        "C-001", "C-002", "C-003", "C-004"
    ]
    assert [row["article_gap_status"] for row in unit] == ["C", "D", "C", "D"]
    assert all(row["supporting_excerpt"] == "" for row in unit)
    assert "21.9 years" in unit[0]["evidence_type"]
    assert "national-registry" in unit[1]["evidence_type"]
    assert "24 months" in unit[2]["evidence_type"]
    assert "post-release" in unit[3]["transferability"]
    assert "no statistically significant" in unit[1]["outcome"].lower()
    assert "no significant" in unit[3]["outcome"].lower()

    cumulative_sources = rows(ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv")
    unit_sources = rows(ROOT / "COMMUNITIES-ADJACENT-DURABLE-SOURCE-INVENTORY.csv")
    assert [row["record_id"] for row in cumulative_sources] == [
        "A-001", "A-002", "A-003", "A-004", "A-005",
        "B-001", "B-002", "B-003", "B-004",
        "C-001", "C-002", "C-003", "C-004",
    ]
    assert [row["record_id"] for row in unit_sources] == [
        "C-001", "C-002", "C-003", "C-004"
    ]
    assert cumulative_sources[-4:] == unit_sources
    assert [row["year"] for row in unit_sources] == ["2011", "2026", "2007", "2021"]
    for row in unit_sources:
        assert row["accessed_on"] == "2026-08-15"
        assert row["disposition"].endswith("promoted")
        assert row["canonical_url"] == "https://doi.org/" + row["doi"]
    assert "21.9 years after treatment" in unit_sources[0]["evidence_scope"]
    assert "40.7% of TAU received MST" in unit_sources[1]["notes"]
    assert "174 days" in unit_sources[2]["notes"]
    assert "12 and 24 months after release" in unit_sources[3]["evidence_scope"]

    gap = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    gap_rows = re.findall(r"^\| G-\d{3} \| ([BCD]) \|", gap, flags=re.MULTILINE)
    assert Counter(gap_rows) == Counter({"B": 8, "C": 7, "D": 3})
    assert "durable treatment/transition units" in gap
    expected_gap_refs = {
        "G-002": unit_ids,
        "G-005": ["F-177", "F-178", "F-179"],
        "G-006": unit_ids,
        "G-009": ["F-178"],
        "G-018": unit_ids,
    }
    for gap_id, finding_ids in expected_gap_refs.items():
        line = next(item for item in gap.splitlines() if item.startswith(f"| {gap_id} |"))
        for finding_id in finding_ids:
            assert finding_id in line
    for finding_id in unit_ids:
        assert finding_id in gap
    assert "produced no treatment-derived screen" in gap

    report = (
        ROOT / "COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md"
    ).read_text(encoding="utf-8")
    for finding_id in unit_ids:
        assert finding_id in report
    for doi in [
        "10.1037/a0024862",
        "10.1007/s11292-026-09736-6",
        "10.1037/0022-006X.75.1.187",
        "10.3389/fpsyt.2021.670957",
    ]:
        assert doi in report
    for heading in [
        "### Do gains persist after dense treatment or staff support ends?",
        "### What follow-on contact, caregiver training, school coordination, and measurement appear necessary?",
        "### Which results concern lower-level conduct and which concern serious or repeated violence?",
        "### Are victim safety, recurrence, child wellbeing, and family burden measured separately?",
    ]:
        assert heading in report
    assert "two favorable and two null comparative results" in report
    assert "still does not supply the requested individual case sequence" in report
    assert "A treatment plan is not delivered aftercare" in report
    assert "exact next boundary is Unit D" not in report
    assert "Proceed to Unit D" in report

    roadmap = (
        REPOSITORY
        / "docs"
        / "superpowers"
        / "plans"
        / "2026-08-15-adjacent-source-roadmap.md"
    ).read_text(encoding="utf-8")
    assert roadmap.count("Status: completed") == 3
    assert "COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md" in roadmap
    assert "the exact next boundary is Unit D" in roadmap
    for doi in [
        "10.1037/a0024862",
        "10.1007/s11292-026-09736-6",
        "10.1037/0022-006X.75.1.187",
        "10.3389/fpsyt.2021.670957",
    ]:
        assert doi in roadmap

    state = (ROOT / "COMMUNITIES-RESEARCH-STATE.md").read_text(encoding="utf-8")
    readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
    index = (REPOSITORY / "docs" / "INDEX.md").read_text(encoding="utf-8")
    agents = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
    assert "**179 findings** (`F-001` through `F-179`)" in state
    assert "The next bounded unit is Unit D" in state
    assert "children kept in the alleged-victim rather than dangerous-actor lane" in state
    assert "**179** evidence findings (`F-001` through `F-179`)" in readme
    assert "COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md" in readme
    assert "COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md" in index
    assert "test_adjacent_durable_transition_workflow.py" in agents
    assert "verify_adjacent_durable_transition.py" in agents

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
    assert "not an individual prognosis or screen" in combined
    assert "does not support diagnosis, coercion" in combined

    print("adjacent durable treatment and transition verification: PASS")


if __name__ == "__main__":
    main()
