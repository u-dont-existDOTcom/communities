#!/usr/bin/env python3
"""Verify the public research report without modifying it."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
REPORT = REPOSITORY / "docs" / "PUBLIC-RESEARCH-REPORT.md"
APPENDIX = REPOSITORY / "docs" / "ARTICLE-APPENDIX-RESEARCH-LINK.md"
UPDATER = ROOT / "update_public_research_report.py"

THESIS = "communal living is a return to our evolved ancestral pattern; large societies breed anomie and capture by psychopaths."


def load_updater():
    spec = importlib.util.spec_from_file_location("public_report_updater", UPDATER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not import public report updater")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    updater = load_updater()
    report = REPORT.read_text(encoding="utf-8")
    appendix = APPENDIX.read_text(encoding="utf-8")
    lower = report.lower()

    expected_block = updater.render_block(updater.derive())
    assert expected_block in report, "public statistics block is stale"
    assert report.count(updater.BEGIN) == 1
    assert report.count(updater.END) == 1

    assert THESIS in report
    for boundary in [
        "That is the author's thesis.",
        "not designed to test ancestral evolution, comparative anomie, the prevalence of psychopathy, or whether large societies are more capturable than small societies",
        "P0 research only; this report does not revise the published article",
        "small scale does not automatically eliminate capture",
        "bounded null",
        "not evidence that no community ever faced or managed such a child",
        "independent correction does not mean “the state”",
        "Zapatismo is well supported here as a movement school and network generator",
        "That is an evidence ceiling, not proof that no such descendants exist.",
        "S-15, model-assisted synthesis",
        "No source in this corpus validates that entire package as one tested system.",
        "not an authorization for an unbounded new research sweep",
        "This public report does **not** apply those edits.",
        "claim-selective",
    ]:
        assert boundary.lower() in lower, boundary

    required_links = [
        "../recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md",
        "../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv",
        "../recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv",
        "../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md",
        "../recovered/COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv",
        "../recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md",
        "../recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md",
        "../recovered/COMMUNITIES-RESEARCH-STATE.md",
        "../COMMUNITY-DEVELOPMENT-LESSONS.md",
    ]
    for relative in required_links:
        assert relative in report, relative
        assert (REPORT.parent / relative).resolve().is_file(), f"broken relative link: {relative}"

    unknowns = re.findall(r"^(\d+)\. ", report[report.index("## What the research still does not know"):], flags=re.MULTILINE)
    assert unknowns[:13] == [str(i) for i in range(1, 14)]

    assert "**not inserted into the published article**" in appendix
    assert "joel-articles` registry also currently has no canonical article package" in appendix
    assert "raw editor HTML" in appendix
    assert "https://github.com/u-dont-existDOTcom/communities/blob/main/docs/PUBLIC-RESEARCH-REPORT.md" in appendix
    assert "https://github.com/u-dont-existDOTcom/communities/blob/agent/final-research-synthesis/docs/PUBLIC-RESEARCH-REPORT.md" in appendix

    forbidden_claims = [
        "the article has been updated",
        "the published article now links",
        "the escuelita created replicated municipalities",
        "independent correction must be state-operated",
    ]
    for phrase in forbidden_claims:
        assert phrase not in lower, phrase

    print("Public research report verification: PASS")


if __name__ == "__main__":
    main()
