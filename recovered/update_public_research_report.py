#!/usr/bin/env python3
"""Refresh the deterministic statistics block in the public research report.

This updater does not alter research findings, article prose, or narrative conclusions.
It recomputes only the delimited public-summary counts from canonical repository
artifacts and is intentionally byte-idempotent.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
CROSSWALK = ROOT / "COMMUNITIES-SYNTHESIS-CROSSWALK.csv"
ADJACENT = ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
REPORT = REPOSITORY / "docs" / "PUBLIC-RESEARCH-REPORT.md"

BEGIN = "<!-- BEGIN AUTO-STATS -->"
END = "<!-- END AUTO-STATS -->"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def state_count(pattern: str, state: str, label: str) -> int:
    match = re.search(pattern, state, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Could not derive {label} from research state")
    return int(match.group(1).replace(",", ""))


def derive() -> dict[str, object]:
    ledger = read_rows(LEDGER)
    crosswalk = read_rows(CROSSWALK)
    adjacent = read_rows(ADJACENT)
    state = STATE.read_text(encoding="utf-8")
    gap = GAP_BANK.read_text(encoding="utf-8")

    expected = [f"F-{number:03d}" for number in range(1, 199)]
    ledger_ids = [row["finding_id"] for row in ledger]
    crosswalk_ids = [row["finding_id"] for row in crosswalk]
    if ledger_ids != expected:
        raise ValueError("Evidence ledger is not sequential F-001 through F-198")
    if crosswalk_ids != expected:
        raise ValueError("Synthesis crosswalk is not sequential F-001 through F-198")

    confidence = Counter(row["confidence"] for row in ledger)
    verification = Counter(row["external_verification_needed"] for row in ledger)
    gap_classes = Counter(
        re.findall(r"^\| G-\d{3} \| ([BCD]) \|", gap, flags=re.MULTILINE)
    )
    theme_ids = {row["primary_theme_id"] for row in crosswalk}

    return {
        "volumes_start": 1,
        "volumes_end": 45,
        "journal_pdfs": state_count(r"\*\*(\d[\d,]*) journal PDFs\*\* were triaged", state, "journal PDF count"),
        "close_reads": state_count(r"(\d[\d,]*) close-read as relevant or contextual", state, "close-read count"),
        "standalone": state_count(r"\*\*(\d+) of 8 standalone substantive sources\*\*", state, "standalone count"),
        "adjacent": len(adjacent),
        "findings": len(ledger),
        "themes": len(theme_ids),
        "gaps": sum(gap_classes.values()),
        "gap_b": gap_classes["B"],
        "gap_c": gap_classes["C"],
        "gap_d": gap_classes["D"],
        "confidence": confidence,
        "verification": verification,
    }


def render_block(values: dict[str, object]) -> str:
    confidence: Counter[str] = values["confidence"]  # type: ignore[assignment]
    verification: Counter[str] = values["verification"]  # type: ignore[assignment]
    return "\n".join(
        [
            BEGIN,
            f"- *Communal Societies* volumes reviewed: **{values['volumes_start']}–{values['volumes_end']}**",
            f"- Journal PDFs triaged: **{values['journal_pdfs']:,}**",
            f"- Relevant or contextual journal close reads: **{values['close_reads']:,}**",
            f"- Standalone substantive sources: **{values['standalone']} of 8 completed**",
            f"- Bounded adjacent/public records: **{values['adjacent']}**",
            f"- Promoted findings: **{values['findings']}**, F-001 through F-198",
            f"- Synthesis themes: **{values['themes']}**",
            f"- Article-facing research gaps: **{values['gaps']}** — {values['gap_b']} partially present (B), {values['gap_c']} apparently missing (C), {values['gap_d']} challenges (D)",
            "- Confidence coding: "
            f"**{confidence['high']} high**, **{confidence['medium-high']} medium-high**, "
            f"**{confidence['medium']} medium**, **{confidence['medium-low']} medium-low**, "
            f"**{confidence['low-medium']} low-medium**, **{confidence['low']} low**",
            f"- External-verification flag: **{verification['yes']} yes**, **{verification['no']} no**",
            END,
        ]
    )


def update() -> None:
    text = REPORT.read_text(encoding="utf-8")
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError("Public report must contain exactly one auto-statistics marker pair")
    start = text.index(BEGIN)
    end = text.index(END, start) + len(END)
    replacement = render_block(derive())
    revised = text[:start] + replacement + text[end:]
    REPORT.write_text(revised, encoding="utf-8")
    print("Public research report statistics update: PASS")


if __name__ == "__main__":
    update()
