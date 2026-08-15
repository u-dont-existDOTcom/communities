#!/usr/bin/env python3
"""Verify the source-free adjacent child-response pilot checkpoint."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    ledger = rows(ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv")
    expected_ids = [f"F-{number:03d}" for number in range(1, 172)]
    actual_ids = [row["finding_id"] for row in ledger]
    assert actual_ids == expected_ids, "ledger IDs must be sequential through F-171"

    unit = rows(ROOT / "COMMUNITIES-ADJACENT-EVIDENCE-LEDGER.csv")
    assert [row["finding_id"] for row in unit] == ["F-169", "F-170", "F-171"]
    assert {row["finding_id"]: row for row in ledger if row["finding_id"] >= "F-169"} == {
        row["finding_id"]: row for row in unit
    }
    assert unit[0]["track"].startswith("Track D adjacent residential")
    assert unit[1]["track"].startswith("Track D adjacent residential")
    assert unit[2]["track"].startswith("Track E adjacent clinical")
    assert [row["article_gap_status"] for row in unit] == ["D", "C", "C"]

    inventory = rows(ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv")
    assert [row["record_id"] for row in inventory] == ["A-001", "A-002", "A-003", "A-004", "A-005"]
    assert inventory[1]["access_status"] == "citation verified; full text not located"
    assert [row["disposition"] for row in inventory[2:]] == ["F-169 promoted", "F-170 promoted", "F-171 promoted"]
    for row in inventory:
        if row["doi"]:
            assert row["canonical_url"] == "https://doi.org/" + row["doi"]
        assert row["accessed_on"] == "2026-08-15"

    gap = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    gap_rows = re.findall(r"^\| G-\d{3} \| ([BCD]) \|", gap, flags=re.MULTILINE)
    assert Counter(gap_rows) == Counter({"B": 8, "C": 7, "D": 3})
    for gap_id in ["G-002", "G-005", "G-006", "G-009", "G-018"]:
        line = next(item for item in gap.splitlines() if item.startswith(f"| {gap_id} |"))
        assert "F-17" in line or (gap_id == "G-002" and "F-169" in line)
    for finding_id in ["F-169", "F-170", "F-171"]:
        assert finding_id in gap

    report = (ROOT / "COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md").read_text(encoding="utf-8")
    for finding_id in ["F-169", "F-170", "F-171"]:
        assert finding_id in report
    for doi in ["10.1901/jaba.1982.15-1", "10.1007/s11121-016-0649-0", "10.1007/s11121-014-0490-2"]:
        assert doi in report
    assert "does not supply the requested complete individual sequence" in report
    assert "not evidence about intentional-community prevalence or practice" in report

    roadmap = (REPOSITORY / "docs" / "superpowers" / "plans" / "2026-08-15-adjacent-source-roadmap.md").read_text(encoding="utf-8")
    for unit_name in ["Unit A", "Unit B", "Unit C", "Unit D", "Unit E"]:
        assert unit_name in roadmap
    assert "Status: completed" in roadmap

    state = (ROOT / "COMMUNITIES-RESEARCH-STATE.md").read_text(encoding="utf-8")
    readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
    index = (REPOSITORY / "docs" / "INDEX.md").read_text(encoding="utf-8")
    assert "**171 findings** (`F-001` through `F-171`)" in state
    assert "Unit B" in state
    assert "**171** evidence findings (`F-001` through `F-171`)" in readme
    assert "COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md" in readme
    assert "COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md" in index

    forbidden_suffixes = {".pdf", ".epub", ".zip"}
    forbidden_dirs = {"corpus-adjacent", "adjacent-full-text", "source-downloads"}
    local_source_roots = {"corpus-v45", "corpus-standalone"}
    for path in REPOSITORY.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(REPOSITORY)
        if len(relative.parts) > 1 and relative.parts[0] == "recovered" and relative.parts[1] in local_source_roots:
            continue
        assert path.suffix.lower() not in forbidden_suffixes, f"source binary committed: {path}"
        assert not forbidden_dirs.intersection(path.parts), f"source directory committed: {path}"

    combined = "\n".join(row["notes"] + " " + row["what_source_establishes"] for row in unit).lower()
    for prohibited in ["should execute", "forced assimilation", "remove the child permanently", "psychopath screen"]:
        assert prohibited not in combined

    print("adjacent child-response pilot verification: PASS")


if __name__ == "__main__":
    main()
