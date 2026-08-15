#!/usr/bin/env python3
"""Verify the source-free final cross-corpus synthesis checkpoint."""

from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

import verify_adjacent_fair_separation as prior


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent

LOCKED_HASHES = {
    "COMMUNITIES-EVIDENCE-LEDGER.csv": "f6e50d9ae5402d185361986d0d15e08399c94b8ef188354c20aee4167b013d05",
    "COMMUNITIES-ARTICLE-GAP-BANK.md": "d2da9f741b6842466bf424567f907947bb253408144598a0cd652c71d7634854",
    "COMMUNITIES-SOURCE-INVENTORY.csv": "a4c5d2f99f1acb77d235f2ac857f2b40a7f7ed44fa2b4f72a3a30eed86fe4282",
    "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv": "8b20911faf4569cd74a21f219afa61683951e1df845ba8bd60a211f109c20a27",
}

THEME_COUNTS = Counter(
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
        "T-10": 9,
        "T-11": 11,
        "T-12": 33,
    }
)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        loaded = list(reader)
    assert all(None not in row for row in loaded), f"extra CSV fields in {path.name}"
    assert all(None not in row.values() for row in loaded), f"missing CSV fields in {path.name}"
    return loaded


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_gap_refs() -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    text = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        match = re.match(r"^\| (G-\d{3}) \|", line)
        if not match:
            continue
        gap_id = match.group(1)
        for finding_id in sorted(set(re.findall(r"F-\d{3}", line))):
            result[finding_id].append(gap_id)
    return result


def main() -> None:
    prior.main()

    for name, expected in LOCKED_HASHES.items():
        assert sha256(ROOT / name) == expected, f"synthesis mutated locked input: {name}"

    ledger = rows(ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv")
    crosswalk = rows(ROOT / "COMMUNITIES-SYNTHESIS-CROSSWALK.csv")
    expected_ids = [f"F-{number:03d}" for number in range(1, 187)]
    assert [row["finding_id"] for row in ledger] == expected_ids
    assert [row["finding_id"] for row in crosswalk] == expected_ids
    assert len({row["finding_id"] for row in crosswalk}) == 186

    assert Counter(row["primary_theme_id"] for row in crosswalk) == THEME_COUNTS
    assert {row["primary_theme_id"] for row in crosswalk} == {
        f"T-{number:02d}" for number in range(1, 13)
    }
    crosswalk_claims = {
        claim
        for row in crosswalk
        for claim in row["synthesis_claim_ids"].split(";")
        if claim
    }
    assert crosswalk_claims == {f"S-{number:02d}" for number in range(1, 15)}
    assert all("S-15" not in row["synthesis_claim_ids"] for row in crosswalk)
    assert all(row["synthesis_claim_ids"] for row in crosswalk)

    ledger_by_id = {row["finding_id"]: row for row in ledger}
    gap_refs = expected_gap_refs()
    for row in crosswalk:
        source = ledger_by_id[row["finding_id"]]
        assert row["community_or_group"] == source["community_group"]
        assert row["confidence"] == source["confidence"]
        assert row["external_verification_needed"] == source["external_verification_needed"]
        expected = ";".join(gap_refs.get(row["finding_id"], []))
        assert row["article_gap_refs"] == expected
        assert row["source_lane"]
        assert row["primary_theme"]
        assert row["evidence_role"]

    row_referenced = set(gap_refs)
    assert len(row_referenced) == 177
    assert set(expected_ids) - row_referenced == {
        "F-027", "F-030", "F-031", "F-032", "F-048", "F-064",
        "F-076", "F-090", "F-100",
    }
    gap_text = (ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md").read_text(encoding="utf-8")
    all_gap_referenced = set(re.findall(r"F-\d{3}", gap_text))
    assert len(re.findall(r"F-\d{3}", gap_text)) == 660
    assert len(all_gap_referenced) == 183
    assert set(expected_ids) - all_gap_referenced == {"F-027", "F-030", "F-032"}
    by_id = {row["finding_id"]: row for row in crosswalk}
    assert by_id["F-027"]["primary_theme_id"] == "T-06"
    assert by_id["F-030"]["primary_theme_id"] == "T-10"
    assert by_id["F-032"]["primary_theme_id"] == "T-10"
    assert all(by_id[finding_id]["article_gap_refs"] == "" for finding_id in ["F-027", "F-030", "F-032"])

    child_null_ids = [
        "F-031", "F-048", "F-064", "F-076", "F-090", "F-100",
        "F-105", "F-111", "F-115", "F-118", "F-121", "F-125",
        "F-131", "F-138", "F-142", "F-146", "F-148", "F-151",
        "F-154", "F-158", "F-162", "F-168",
    ]
    assert all(by_id[finding_id]["primary_theme_id"] == "T-12" for finding_id in child_null_ids)
    assert all("S-14" in by_id[finding_id]["synthesis_claim_ids"] for finding_id in child_null_ids)
    assert all(
        by_id[f"F-{number:03d}"]["source_lane"]
        == "adjacent child-response/professional evidence"
        for number in range(169, 180)
    )

    report = (ROOT / "COMMUNITIES-FINAL-SYNTHESIS-REPORT.md").read_text(encoding="utf-8")
    report_lower = report.lower()
    for theme_id in [f"T-{number:02d}" for number in range(1, 13)]:
        assert theme_id in report
    for claim_id in [f"S-{number:02d}" for number in range(1, 16)]:
        assert claim_id in report
    for heading in [
        "## Direct answer: the gap bank was not the final report",
        "## Executive synthesis",
        "## Cross-theme tensions that must not be flattened",
        "## The combined architecture — S-15",
        "## What this means for Joel's article and thesis",
        "## What remains unknown",
        "## Final conclusions",
    ]:
        assert heading in report
    for required in [
        "all 186 findings",
        "f-027",
        "f-030",
        "f-032",
        "twenty-two findings",
        "model-assisted",
        "no source in this corpus validates the whole package",
        "finding counts in this report show coded coverage",
        "community members retain ordinary legal powers",
        "do not inherit police, court, clinical, custody, restraint, seclusion, licensing, or regulatory powers",
        "the intentional-community corpus does not answer",
        "the article-gap bank should therefore remain the change specification",
    ]:
        assert required in report_lower
    for prohibited in [
        "the corpus proves communal living",
        "communities should diagnose",
        "communities should restrain children",
        "a validated community danger screen",
        "centralization is always harmful",
        "outside intervention is always correct",
    ]:
        assert prohibited not in report_lower

    method = (
        REPOSITORY
        / "docs"
        / "superpowers"
        / "plans"
        / "2026-08-15-final-synthesis-pass.md"
    ).read_text(encoding="utf-8")
    for required in [
        "## Decision",
        "## Horizontal questions",
        "## Theme architecture",
        "## Claim-status rubric",
        "## Completeness controls",
        "F-027, F-030, and F-032",
    ]:
        assert required in method

    state = (ROOT / "COMMUNITIES-RESEARCH-STATE.md").read_text(encoding="utf-8")
    readme = (REPOSITORY / "README.md").read_text(encoding="utf-8")
    index = (REPOSITORY / "docs" / "INDEX.md").read_text(encoding="utf-8")
    agents = (REPOSITORY / "AGENTS.md").read_text(encoding="utf-8")
    assert "COMMUNITIES-FINAL-SYNTHESIS-REPORT.md" in state
    assert "Every finding is mapped" in state
    assert "all 186 findings mapped" in readme
    assert "COMMUNITIES-SYNTHESIS-CROSSWALK.csv" in readme
    assert "COMMUNITIES-FINAL-SYNTHESIS-REPORT.md" in index
    assert "2026-08-15-final-synthesis-pass.md" in index
    assert "test_final_synthesis_workflow.py" in agents
    assert "verify_final_synthesis.py" in agents

    print("final cross-corpus synthesis verification: PASS")


if __name__ == "__main__":
    main()
