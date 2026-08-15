#!/usr/bin/env python3
"""Verify the source-free autonomy and legal-pluralism correction."""

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
    unit = rows(ROOT / "COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-EVIDENCE-LEDGER.csv")
    expected = [f"F-{number:03d}" for number in range(1, 193)]
    unit_ids = [f"F-{number:03d}" for number in range(187, 193)]
    assert [row["finding_id"] for row in ledger] == expected
    assert [row["finding_id"] for row in unit] == unit_ids
    assert ledger[-6:] == unit
    assert all(row["supporting_excerpt"] == "" for row in unit)
    assert [row["confidence"] for row in unit] == [
        "high", "medium-high", "medium-high", "high", "medium-high", "high"
    ]
    assert [row["article_gap_status"] for row in unit] == ["D", "D", "B", "D", "D", "D"]
    assert "state monopoly" in unit[0]["what_source_establishes"].lower()
    assert "full control is too strong" in unit[1]["what_source_establishes"].lower()
    assert "worldwide-innovation criterion" in unit[2]["what_source_establishes"].lower()
    assert "neither a state-dependence case nor a no-state case" in unit[3]["what_source_establishes"].lower()
    assert "isolated-local sufficiency" in unit[4]["what_source_establishes"].lower()
    assert "human-rights constraint" in unit[5]["what_source_establishes"].lower()

    cumulative_sources = rows(ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv")
    unit_sources = rows(ROOT / "COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-SOURCE-INVENTORY.csv")
    source_ids = [f"LP-{number:03d}" for number in range(1, 10)]
    assert [row["record_id"] for row in unit_sources] == source_ids
    assert cumulative_sources[-9:] == unit_sources
    assert [row["disposition"] for row in unit_sources] == [
        "F-187 promoted",
        "F-187 corroboration; no separate finding",
        "F-188 promoted",
        "F-187 and F-188 corroboration; no separate finding",
        "F-189 promoted",
        "F-190 promoted",
        "F-190 official corroboration; no separate finding",
        "F-191 promoted",
        "F-192 promoted",
    ]
    assert all(row["accessed_on"] == "2026-08-15" for row in unit_sources)
    assert "enlacezapatista" in unit_sources[0]["canonical_url"]
    assert "te.gob.mx" in unit_sources[6]["canonical_url"]
    assert unit_sources[7]["doi"] == "10.25222/larr.377"
    assert "normative declaration" in unit_sources[8]["sequence_later_outcome"]

    crosswalk = rows(ROOT / "COMMUNITIES-SYNTHESIS-CROSSWALK.csv")
    assert [row["finding_id"] for row in crosswalk] == expected
    assert Counter(row["primary_theme_id"] for row in crosswalk)["T-13"] == 6
    assert all(row["primary_theme_id"] == "T-13" for row in crosswalk[-6:])
    claims = {
        claim
        for row in crosswalk
        for claim in row["synthesis_claim_ids"].split(";")
        if claim
    }
    assert "S-16" in claims and "S-17" in claims
    assert all("G-019" in row["article_gap_refs"] for row in crosswalk[-6:])
    assert all(
        row["primary_theme"] == "independent correction, legal pluralism, and professional boundaries"
        for row in crosswalk
        if row["primary_theme_id"] == "T-09"
    )

    gap = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    gap_rows = re.findall(r"^\| G-\d{3} \| ([BCD]) \|", gap, flags=re.MULTILINE)
    assert Counter(gap_rows) == Counter({"B": 8, "C": 7, "D": 4})
    assert gap.count("| G-019 |") == 1
    assert all(finding_id in next(line for line in gap.splitlines() if line.startswith("| G-019 |")) for finding_id in unit_ids)
    assert "state-monopoly inference" in next(line for line in gap.splitlines() if line.startswith("| G-013 |"))

    report = (ROOT / "COMMUNITIES-FINAL-SYNTHESIS-REPORT.md").read_text(encoding="utf-8")
    report_lower = report.lower()
    for required in [
        "evidence base: 192 findings, f-001 through f-192",
        "t-13 autonomy, legal pluralism, and translocal federation",
        "independent correction is a relationship, not a geography",
        "state externality is contingent",
        "outside the autonomous movement",
        "full sovereign control",
        "person -> immediate community -> autonomous intercommunity review",
        "everything learned can be compressed into thirteen decisive conclusions",
    ]:
        assert required in report_lower, required
    for prohibited in [
        "professional, judicial, or public layer must retain",
        "community members retain ordinary legal powers",
        "do not inherit police, court, clinical, custody, restraint, seclusion, licensing, or regulatory powers",
        "outside correction is necessary, function-specific",
    ]:
        assert prohibited not in report_lower, prohibited

    unit_report = (ROOT / "COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md").read_text(encoding="utf-8")
    unit_lower = unit_report.lower()
    for heading in [
        "## direct answer",
        "## the corrected rule",
        "## what the zapatista case changes",
        "## why zapatismo fits the worldwide-innovation criterion",
        "## cheran: the hybrid case",
        "## crac-pc: why the village alone is not enough",
        "## rights boundary",
        "## corrected control map",
        "## bottom line",
    ]:
        assert heading in unit_lower, heading
    for finding_id in unit_ids:
        assert finding_id.lower() in unit_lower
    assert "not full sovereignty" in unit_lower
    assert "external to the village but internal to a regional indigenous order" in unit_lower
    assert "does not count all adaptations" in unit_lower

    state = (ROOT / "COMMUNITIES-RESEARCH-STATE.md").read_text(encoding="utf-8")
    readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
    index = (REPOSITORY / "docs" / "INDEX.md").read_text(encoding="utf-8")
    agents = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
    plan = (
        REPOSITORY
        / "docs"
        / "superpowers"
        / "plans"
        / "2026-08-15-autonomy-legal-pluralism-correction.md"
    ).read_text(encoding="utf-8")
    assert "**192 findings** (`F-001` through `F-192`)" in state
    assert "all 192 findings mapped across 13 themes" in readme
    assert "COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md" in index
    assert "test_autonomy_legal_pluralism_workflow.py" in agents
    assert "## What is falsified, qualified, and retained" in plan

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

    print("autonomy/legal-pluralism correction verification: PASS")


if __name__ == "__main__":
    main()
