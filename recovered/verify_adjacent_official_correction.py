#!/usr/bin/env python3
"""Verify the source-free adjacent official-correction checkpoint."""

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
    expected_ids = [f"F-{number:03d}" for number in range(1, 183)]
    assert [row["finding_id"] for row in ledger] == expected_ids

    unit = rows(ROOT / "COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-EVIDENCE-LEDGER.csv")
    unit_ids = ["F-180", "F-181", "F-182"]
    assert [row["finding_id"] for row in unit] == unit_ids
    assert {row["finding_id"]: row for row in ledger[-3:]} == {
        row["finding_id"]: row for row in unit
    }
    assert [row["source_record_id"] for row in unit] == ["D-001", "D-002", "D-003"]
    assert [row["article_gap_status"] for row in unit] == ["C", "C", "C"]
    assert all(row["supporting_excerpt"] == "" for row in unit)
    assert all(row["external_verification_needed"] == "yes" for row in unit)
    assert "license dispositions" in unit[0]["evidence_type"]
    assert "royal-commission" in unit[1]["evidence_type"]
    assert "statutory inquiry" in unit[2]["evidence_type"]
    assert "not proof of recovery" in unit[0]["what_source_does_not_establish"]
    assert "does not demonstrate completed correction" in unit[1]["outcome"]
    assert "six perpetrators were convicted" in unit[2]["outcome"].lower()

    cumulative_sources = rows(ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv")
    unit_sources = rows(ROOT / "COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-SOURCE-INVENTORY.csv")
    assert [row["record_id"] for row in cumulative_sources] == [
        "A-001", "A-002", "A-003", "A-004", "A-005",
        "B-001", "B-002", "B-003", "B-004",
        "C-001", "C-002", "C-003", "C-004",
        "D-001", "D-002", "D-003",
    ]
    assert [row["record_id"] for row in unit_sources] == ["D-001", "D-002", "D-003"]
    assert cumulative_sources[-3:] == unit_sources
    assert [row["year"] for row in unit_sources] == ["1997", "2024", "2021"]
    for row in unit_sources:
        assert row["accessed_on"] == "2026-08-15"
        assert row["disposition"].endswith("promoted")
        assert row["doi"] == ""
    assert "op.nysed.gov" in unit_sources[0]["canonical_url"]
    assert "abuseincare.org.nz" in unit_sources[1]["canonical_url"]
    assert "iicsa.org.uk" in unit_sources[2]["canonical_url"]
    assert "no child" in unit_sources[0]["sequence_later_outcome"]
    assert "not proof" in unit_sources[1]["sequence_later_outcome"]
    assert "six convicted" in unit_sources[2]["sequence_later_outcome"]

    gap = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    gap_rows = re.findall(r"^\| G-\d{3} \| ([BCD]) \|", gap, flags=re.MULTILINE)
    assert Counter(gap_rows) == Counter({"B": 8, "C": 7, "D": 3})
    assert "official-correction units" in gap
    expected_gap_refs = {
        "G-003": unit_ids,
        "G-004": unit_ids,
        "G-005": unit_ids,
        "G-006": unit_ids,
        "G-009": ["F-181", "F-182"],
        "G-013": unit_ids,
    }
    for gap_id, finding_ids in expected_gap_refs.items():
        line = next(item for item in gap.splitlines() if item.startswith(f"| {gap_id} |"))
        for finding_id in finding_ids:
            assert finding_id in line
    for finding_id in unit_ids:
        assert finding_id in gap
    assert "produced no community investigative" in gap

    report = (
        ROOT / "COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md"
    ).read_text(encoding="utf-8")
    report_lower = report.lower()
    for finding_id in unit_ids:
        assert finding_id in report
    for domain in ["op.nysed.gov", "abuseincare.org.nz", "iicsa.org.uk"]:
        assert domain in report
    for heading in [
        "## Cross-record correction map",
        "## Independence, preservation, and recusal tests",
        "## Family contact and survivor support",
        "## Official-correction outcome rule",
        "## Transfer boundary",
    ]:
        assert heading in report
    assert "license revocation establishes removal of licensed authority" in report_lower
    assert "an inquiry finding establishes an authoritative public correction record" in report_lower
    assert "a conviction establishes criminal liability" in report_lower
    assert "No police, court, licensing, custody, child-protection, or inquiry power transfers" in report
    assert "Proceed to Unit E" in report

    roadmap = (
        REPOSITORY
        / "docs"
        / "superpowers"
        / "plans"
        / "2026-08-15-adjacent-source-roadmap.md"
    ).read_text(encoding="utf-8")
    assert roadmap.count("Status: completed") == 4
    assert "COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md" in roadmap
    assert "the exact next boundary is Unit E" in roadmap
    assert "New York State Office of the Professions" in roadmap
    assert "Whanaketia" in roadmap
    assert "Independent Inquiry into Child Sexual Abuse" in roadmap

    state = (ROOT / "COMMUNITIES-RESEARCH-STATE.md").read_text(encoding="utf-8")
    readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
    index = (REPOSITORY / "docs" / "INDEX.md").read_text(encoding="utf-8")
    agents = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
    assert "**182 findings** (`F-001` through `F-182`)" in state
    assert "The next bounded unit is Unit E" in state
    assert "fair separation, pooled risk, and planned fission" in state
    assert "**182** evidence findings (`F-001` through `F-182`)" in readme
    assert "COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md" in readme
    assert "COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md" in index
    assert "test_adjacent_official_correction_workflow.py" in agents
    assert "verify_adjacent_official_correction.py" in agents

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
    assert "zero for transferring licensing or custody power" in combined
    assert "does not authorize private investigation" in combined
    assert "zero for community-run criminal investigation" in combined

    print("adjacent official correction verification: PASS")


if __name__ == "__main__":
    main()
