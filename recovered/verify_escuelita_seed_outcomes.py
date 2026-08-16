#!/usr/bin/env python3
"""Verify the repository-contained Escuelita descendant audit."""

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
    unit = rows(ROOT / "COMMUNITIES-ESCUELITA-SEED-OUTCOMES-EVIDENCE-LEDGER.csv")
    expected = [f"F-{number:03d}" for number in range(1, 199)]
    unit_ids = [f"F-{number:03d}" for number in range(193, 199)]
    assert [row["finding_id"] for row in ledger] == expected
    assert [row["finding_id"] for row in unit] == unit_ids
    assert ledger[-6:] == unit
    assert all(row["supporting_excerpt"] == "" for row in unit)
    assert [row["confidence"] for row in unit] == [
        "medium-high", "medium", "medium-high", "medium", "high", "medium-high"
    ]
    assert all(row["article_gap_status"] == "B" for row in unit)
    assert [row["external_verification_needed"] for row in unit] == [
        "yes", "yes", "yes", "yes", "no", "yes"
    ]
    assert Counter(row["confidence"] for row in ledger) == Counter(
        {
            "high": 92,
            "medium-high": 28,
            "medium": 69,
            "low-medium": 3,
            "medium-low": 2,
            "low": 4,
        }
    )
    assert Counter(row["external_verification_needed"] for row in ledger) == Counter(
        {"yes": 133, "no": 65}
    )
    assert "lineage level 2" in unit[0]["what_source_establishes"]
    assert "lineage-level-3" in unit[1]["what_source_establishes"]
    assert "lineage-level-4" in unit[2]["what_source_establishes"]
    assert "named individual trace" in unit[3]["what_source_establishes"]
    assert "existing transnational Zapatista ecology" in unit[4]["what_source_establishes"]
    assert "evidence ceiling is lineage level 4" in unit[5]["what_source_establishes"]
    assert "not proof that no Escuelita descendant exists" in unit[5]["notes"]

    cumulative_sources = rows(ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv")
    unit_sources = rows(ROOT / "COMMUNITIES-ESCUELITA-SEED-OUTCOMES-SOURCE-INVENTORY.csv")
    prior_unit_sources = rows(ROOT / "COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-SOURCE-INVENTORY.csv")
    assert len(cumulative_sources) == 47
    assert [row["record_id"] for row in unit_sources] == [
        f"ES-{number:03d}" for number in range(1, 19)
    ]
    assert cumulative_sources[-18:] == unit_sources
    assert cumulative_sources[-27:-18] == prior_unit_sources
    assert all(row["accessed_on"] == "2026-08-15" for row in unit_sources)
    assert all(row["canonical_url"].startswith("https://") for row in unit_sources)
    assert [row["disposition"] for row in unit_sources] == [
        "F-198 search-frame context; no separate finding",
        "F-198 search-frame context; no separate finding",
        "F-193 promoted",
        "F-193 promoted",
        "F-193 promoted",
        "F-193 promoted",
        "F-195 promoted",
        "F-195 persistence corroboration; no separate finding",
        "F-195 persistence corroboration; no separate finding",
        "F-195 persistence corroboration; no separate finding",
        "F-194 promoted",
        "F-194 promoted",
        "F-194 promoted",
        "F-196 promoted",
        "F-196 promoted",
        "F-197 promoted",
        "F-197 promoted",
        "F-197 promoted",
    ]
    assert "enlacezapatista" in unit_sources[0]["canonical_url"]
    assert "congresonacionalindigena" in unit_sources[9]["canonical_url"]
    assert unit_sources[12]["doi"] == "10.1177/0094582X241288861"
    assert unit_sources[15]["year"] == "2011"
    assert unit_sources[17]["year"] == "2012"

    crosswalk = rows(ROOT / "COMMUNITIES-SYNTHESIS-CROSSWALK.csv")
    assert [row["finding_id"] for row in crosswalk] == expected
    assert Counter(row["primary_theme_id"] for row in crosswalk) == Counter(
        {
            "T-01": 20,
            "T-02": 13,
            "T-03": 17,
            "T-04": 14,
            "T-05": 8,
            "T-06": 14,
            "T-07": 21,
            "T-08": 7,
            "T-09": 19,
            "T-10": 11,
            "T-11": 13,
            "T-12": 33,
            "T-13": 8,
        }
    )
    assert [row["primary_theme_id"] for row in crosswalk[-6:]] == [
        "T-11", "T-13", "T-11", "T-13", "T-10", "T-10"
    ]
    claims = {
        claim
        for row in crosswalk
        for claim in row["synthesis_claim_ids"].split(";")
        if claim
    }
    assert claims == {f"S-{number:02d}" for number in range(1, 19)}
    assert all(row["article_gap_refs"] == "G-020" for row in crosswalk[-6:])

    gap = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    gap_rows = re.findall(r"^\| G-\d{3} \| ([BCD]) \|", gap, flags=re.MULTILINE)
    assert Counter(gap_rows) == Counter({"B": 9, "C": 7, "D": 4})
    assert set(expected) - set(re.findall(r"F-\d{3}", gap)) == {
        "F-027", "F-030", "F-032"
    }
    assert gap.count("| G-020 |") == 1
    gap_020 = next(line for line in gap.splitlines() if line.startswith("| G-020 |"))
    assert all(finding_id in gap_020 for finding_id in unit_ids)
    assert "20 material items: **9 B, 7 C, and 4 D**" in gap
    assert "bounded search found no alumni registry" in gap_020

    report = (ROOT / "COMMUNITIES-FINAL-SYNTHESIS-REPORT.md").read_text(encoding="utf-8")
    report_lower = report.lower()
    for required in [
        "evidence base: 198 findings, f-001 through f-198",
        "47 bounded adjacent records",
        "92 findings high confidence, 28 medium-high, 69 medium",
        "133 for external verification and 65 as not needing it",
        "outward diffusion needs a lineage ladder",
        "espacio de coordinacion grietas en el muro",
        "pre-2013 controls prevent false credit",
        "s-18 is therefore the diffusion rule",
        "everything learned can be compressed into thirteen decisive conclusions",
    ]:
        assert required in report_lower, required
    for synthesis_claim in [f"s-{number:02d}" for number in range(1, 19)]:
        assert synthesis_claim in report_lower, synthesis_claim
    numbered = re.findall(r"^## (\d+)\. ", report, flags=re.MULTILINE)
    assert numbered == [str(number) for number in range(1, 14)]
    assert report.count("## 11. Success is a vector, not a score — T-10, S-11") == 1
    assert "## 10. Success is a vector, not a score" not in report

    unit_report = (ROOT / "COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md").read_text(
        encoding="utf-8"
    )
    unit_lower = unit_report.lower()
    for heading in [
        "## direct answer",
        "## what counts as a sprout",
        "## the escuelita was designed to travel",
        "## sprout 1: alumni became an organizational identity",
        "## sprout 2: participants report carrying practices home",
        "## sprout 3: grietas en el muro is the strongest durable candidate",
        "## sprout 4: one traceable individual pathway",
        "## what must be excluded from escuelita-specific credit",
        "## what the bounded search did not find",
        "## what this means for the worldwide-innovation thesis",
        "## bottom line",
    ]:
        assert heading in unit_lower, heading
    for finding_id in unit_ids:
        assert finding_id.lower() in unit_lower
    for boundary in [
        "the seeds demonstrably germinated",
        "the evidence does not yet show a transplanted forest",
        "grafting into existing root systems",
        "movement school and network generator",
        "bounded null, not a historical claim",
    ]:
        assert boundary in unit_lower, boundary
    assert unit_report.count("https://") >= 16

    state = (ROOT / "COMMUNITIES-RESEARCH-STATE.md").read_text(encoding="utf-8")
    readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
    index = (REPOSITORY / "docs" / "INDEX.md").read_text(encoding="utf-8")
    handoff = (REPOSITORY / "docs" / "FRESH-CONVERSATION-HANDOFF.md").read_text(
        encoding="utf-8"
    )
    agents = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
    plan = (
        REPOSITORY
        / "docs"
        / "superpowers"
        / "plans"
        / "2026-08-15-escuelita-seed-outcomes.md"
    ).read_text(encoding="utf-8")
    assert "**198 findings** (`F-001` through `F-198`)" in state
    assert "20 reconciled article-gap items: 9 partially present" in state
    assert "47 bounded adjacent records" in state
    assert "all 198 findings mapped across 13 themes" in readme
    assert "one-row-per-finding map from all 198 findings" in readme
    assert "thirteen-theme and eighteen-claim report architecture" in readme
    assert "docs/FRESH-CONVERSATION-HANDOFF.md" in readme
    assert "1. `FRESH-CONVERSATION-HANDOFF.md`" in index
    assert "COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md" in index
    assert "test_escuelita_seed_outcomes_workflow.py" in agents
    assert "## Seed lineage ladder" in plan
    assert "pre-2013" in plan
    for required in [
        "communal living is a return to our evolved ancestral pattern",
        "large societies breed anomie and capture by psychopaths",
        "movement school and network generator",
        "there is no silently authorized unfinished research lane",
        "do not begin article revision",
    ]:
        assert required in handoff.lower(), required
    lessons_path = REPOSITORY / "COMMUNITY-DEVELOPMENT-LESSONS.md"
    if lessons_path.exists():
        lessons = lessons_path.read_text(encoding="utf-8")
        assert "**Related:** F-189; F-193–F-198" in lessons
        assert "one durable mixed-lineage coordination candidate" in lessons
        assert "not automatically a successful communal-replication engine" in lessons

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

    print("Escuelita seed-outcomes verification: PASS")


if __name__ == "__main__":
    main()
