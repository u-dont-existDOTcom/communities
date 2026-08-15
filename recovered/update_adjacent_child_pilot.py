#!/usr/bin/env python3
"""Apply the completed adjacent child-response pilot checkpoint."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
UNIT_LEDGER = ROOT / "COMMUNITIES-ADJACENT-EVIDENCE-LEDGER.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"
AGENTS = REPOSITORY / "AGENTS.md"
INDEX = REPOSITORY / "docs" / "INDEX.md"


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old in text:
        return text.replace(old, new, 1)
    raise AssertionError(f"missing update anchor: {label}")


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        return list(reader.fieldnames), list(reader)


def merge_findings() -> None:
    fields, rows = load_csv(LEDGER)
    unit_fields, unit_rows = load_csv(UNIT_LEDGER)
    assert fields == unit_fields
    assert [row["finding_id"] for row in unit_rows] == ["F-169", "F-170", "F-171"]

    by_id = {row["finding_id"]: row for row in rows}
    for unit_row in unit_rows:
        finding_id = unit_row["finding_id"]
        if finding_id in by_id:
            assert by_id[finding_id] == unit_row, f"conflicting existing row: {finding_id}"
        else:
            rows.append(unit_row)

    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-002": (
        "Adjacent child-response evidence sharpens the boundary: a family-style residential model improved measured criminal conduct only during residence (F-169); a trained, coached setting-level model reduced some incident categories but not all and supplied no post-exit outcome (F-170); and a randomized child-plus-caregiver program used trained providers and continuing individualized services rather than peer therapy alone (F-171).",
        ["F-169", "F-170", "F-171"],
    ),
    "G-005": (
        "The adjacent clinical trial also requires independent child assessment, caregiver participation, trained providers, continuing individualized support, and repeated review outside membership discipline; treatment response is not a danger screen (F-171).",
        ["F-171"],
    ),
    "G-006": (
        "Adjacent child-response studies require separate fields for conduct during residence and after exit, each serious incident category, service exposure, continuing-treatment status, victim outcomes, and later child wellbeing; an in-program gain cannot be counted as durable recovery (F-169 through F-171).",
        ["F-169", "F-170", "F-171"],
    ),
    "G-009": (
        "Adjacent residential and clinical evidence adds developmentally focused caregiving, family involvement, trained support, separate peer-aggression measurement, and repeated child outcomes without authorizing collective diagnosis or discipline (F-170, F-171).",
        ["F-170", "F-171"],
    ),
    "G-018": (
        "The first adjacent child-response pilot still found no validated personality, commitment, productivity, therapeutic-fluency, or residence-duration screen. Its useful evidence came from conduct records, structured measures, comparison conditions, implementation review, and follow-up; none of the three evaluations completed the requested individual allegation-to-later-outcome sequence for a persistently dangerous child (F-169 through F-171).",
        ["F-169", "F-170", "F-171"],
    ),
}


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources",
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response pilot",
        "gap checkpoint",
    )

    output: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        matched = None
        for gap_id in GAP_ADDITIONS:
            if line.startswith(f"| {gap_id} |"):
                matched = gap_id
                break
        if matched is None:
            output.append(line)
            continue

        cells = line.split("|")
        assert len(cells) == 9, f"unexpected gap-table shape for {matched}"
        addition, finding_ids = GAP_ADDITIONS[matched]
        if addition not in cells[4]:
            cells[4] = cells[4].rstrip() + " " + addition + " "
        for finding_id in finding_ids:
            evidence = [item.strip() for item in cells[7].split(",") if item.strip()]
            if finding_id not in evidence:
                evidence.append(finding_id)
            cells[7] = " " + ", ".join(evidence) + " "
        output.append("|".join(cells))
        seen.add(matched)

    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(output) + "\n"

    verification = (
        "- **F status:** inspect Teaching-Family admission criteria, program-fidelity records, complete court and police files, resident and victim accounts, transition supports, and longer follow-up before assigning causal or durable effects; the reported post-treatment null has been disputed and is not proof of no effect.\n"
        "- **F status:** inspect CARE incident definitions, raw agency series, reporting changes, implementation records, child and family accounts, independent replication, and post-exit outcomes before treating falling reports as complete safety or wellbeing evidence.\n"
        "- **F status:** inspect SNAP intake, fidelity, service-use, blinded or multi-informant outcomes, subgroup results, rare-event records, outcomes for girls and adolescents, and follow-up after services cease before generalizing the trial or treating severity response as a screen.\n"
    )
    if verification not in text:
        text = text.replace("## Explicit non-promotions\n", verification + "\n## Explicit non-promotions\n", 1)

    nonpromotion = (
        "- Brown's 1996 Indiana University dissertation remains a retrieval lead. Its exact citation was verified from the 2023 reflection, but no lawful public full text or stable catalog record was located in the pilot; the reflection's 80-percent persistence statement is not promoted as a case process or validated outcome.\n"
    )
    if nonpromotion not in text:
        text = text.rstrip() + "\n" + nonpromotion

    GAP_BANK.write_text(text, encoding="utf-8")


def update_handoffs() -> None:
    text = STATE.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Updated: 2026-08-14 (Africa/Dakar)",
        "Updated: 2026-08-15 (Africa/Dakar)",
        "state date",
    )
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **168 findings** (`F-001` through `F-168`). The standalone pass added six findings: two B, three C, and one F-status bounded negative.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **171 findings** (`F-001` through `F-171`). The adjacent child-response pilot added three findings in explicitly separate residential and clinical lanes.",
        "state finding count",
    )
    durable = "- `COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md` completes the first five-record adjacent unit. The Brown dissertation remains an access-limited retrieval lead; three primary evaluations produced F-169 through F-171 without supplying the complete individual dangerous-child sequence.\n"
    if durable not in text:
        text = text.replace(
            "- `COMMUNITIES-STANDALONE-RESEARCH-REPORT.md` records recovery, exact source verification, all eight close-read dispositions, six promoted findings, source cautions, and completion of the assigned primary corpus.\n",
            "- `COMMUNITIES-STANDALONE-RESEARCH-REPORT.md` records recovery, exact source verification, all eight close-read dispositions, six promoted findings, source cautions, and completion of the assigned primary corpus.\n" + durable,
            1,
        )
    text = replace_once_or_confirm(
        text,
        "- No journal PDF or assigned standalone source remains. The next unit must be explicitly bounded: either verify the underlying or adjacent sources named in the gap bank, add a newly authorized corpus, or pause P0 for an owner decision.",
        "- The first five-record adjacent child-response pilot is complete. The next bounded unit is Unit B in `docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`: four sources on assessment, immediate safety, and independent review.",
        "state next unit",
    )
    evidence = "- The adjacent child-response pilot adds three bounded contrasts: family-style residential gains that did not remain statistically significant one year after exit; setting-level residential reductions in some but not all incident categories; and randomized child-plus-caregiver improvements during a period that included continuing individualized services. None is an intentional-community case or a validated danger screen.\n"
    if evidence not in text:
        text = text.replace(
            "- The standalone pass adds: an explicit-separation-authority failure paired with a response-repertoire table; one role-specific childcare gate during provisional admission; a traditional-society example separating productive skill from allocation authority; a traditional-society conflict ladder spanning interruption, cooling, fission, and outside court; an internally graduated Amish discipline and reintegration process with a documented capture weakness; and the bounded standalone dangerous-child null.\n",
            "- The standalone pass adds: an explicit-separation-authority failure paired with a response-repertoire table; one role-specific childcare gate during provisional admission; a traditional-society example separating productive skill from allocation authority; a traditional-society conflict ladder spanning interruption, cooling, fission, and outside court; an internally graduated Amish discipline and reintegration process with a documented capture weakness; and the bounded standalone dangerous-child null.\n" + evidence,
            1,
        )
    text = replace_once_or_confirm(
        text,
        "2. If an adjacent-source verification unit is authorized, select a bounded subset from the F-status leads in `COMMUNITIES-ARTICLE-GAP-BANK.md` and record access, provenance, and why it changes a live uncertainty.",
        "2. Continue with Unit B in the adjacent-source roadmap; stop after one current authoritative practice guideline, two prospective structured-professional-judgment validation studies, and one primary implementation study.",
        "state resume step",
    )
    STATE.write_text(text, encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    text = replace_once_or_confirm(text, "- **168** evidence findings (`F-001` through `F-168`)", "- **171** evidence findings (`F-001` through `F-171`)", "README count")
    text = replace_once_or_confirm(
        text,
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-STANDALONE-RESEARCH-REPORT.md`](recovered/COMMUNITIES-STANDALONE-RESEARCH-REPORT.md).",
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md`](recovered/COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "README latest report",
    )
    text = replace_once_or_confirm(text, "python recovered/test_standalone_workflow.py\npython recovered/verify_standalone.py", "python recovered/test_adjacent_child_pilot_workflow.py\npython recovered/verify_adjacent_child_pilot.py", "README validation")
    README.write_text(text, encoding="utf-8")

    text = INDEX.read_text(encoding="utf-8")
    text = replace_once_or_confirm(text, "the latest bounded report, currently `../recovered/COMMUNITIES-STANDALONE-RESEARCH-REPORT.md`", "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md`", "index latest report")
    index_note = "\nThe post-corpus queue is finite and recorded in `superpowers/plans/2026-08-15-adjacent-source-roadmap.md`. Adjacent web and publication records are kept in `../recovered/COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv`; they do not change the 984-journal-PDF or eight-standalone primary-corpus counts.\n"
    if index_note.strip() not in text:
        text = text.replace("## Evidence classes\n", index_note + "\n## Evidence classes\n", 1)
    INDEX.write_text(text, encoding="utf-8")

    text = AGENTS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(text, "`python recovered/test_standalone_workflow.py` (or the current volume-specific successor)", "`python recovered/test_adjacent_child_pilot_workflow.py` (or the current bounded-unit successor)", "AGENTS regression")
    text = replace_once_or_confirm(text, "`python recovered/verify_standalone.py` with the exact local corpus restored", "`python recovered/verify_adjacent_child_pilot.py`; run source-dependent predecessor checks only when their exact local corpora are restored", "AGENTS verification")
    AGENTS.write_text(text, encoding="utf-8")


def main() -> None:
    merge_findings()
    update_gap_bank()
    update_handoffs()


if __name__ == "__main__":
    main()
