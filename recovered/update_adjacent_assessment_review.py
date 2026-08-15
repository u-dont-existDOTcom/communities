#!/usr/bin/env python3
"""Apply the completed adjacent assessment and review checkpoint."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
UNIT_LEDGER = ROOT / "COMMUNITIES-ADJACENT-ASSESSMENT-EVIDENCE-LEDGER.csv"
SOURCE_INVENTORY = ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv"
UNIT_SOURCE_INVENTORY = ROOT / "COMMUNITIES-ADJACENT-ASSESSMENT-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"
AGENTS = REPOSITORY / "AGENTS.md"
INDEX = REPOSITORY / "docs" / "INDEX.md"
ROADMAP = REPOSITORY / "docs" / "superpowers" / "plans" / "2026-08-15-adjacent-source-roadmap.md"


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


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def merge_unit_csv(
    cumulative_path: Path,
    unit_path: Path,
    id_field: str,
    expected_ids: list[str],
) -> None:
    fields, rows = load_csv(cumulative_path)
    unit_fields, unit_rows = load_csv(unit_path)
    assert fields == unit_fields
    assert [row[id_field] for row in unit_rows] == expected_ids

    by_id = {row[id_field]: row for row in rows}
    for unit_row in unit_rows:
        record_id = unit_row[id_field]
        if record_id in by_id:
            assert by_id[record_id] == unit_row, f"conflicting existing row: {record_id}"
        else:
            rows.append(unit_row)
    write_csv(cumulative_path, fields, rows)


def merge_findings_and_sources() -> None:
    merge_unit_csv(
        LEDGER,
        UNIT_LEDGER,
        "finding_id",
        ["F-172", "F-173", "F-174", "F-175"],
    )
    merge_unit_csv(
        SOURCE_INVENTORY,
        UNIT_SOURCE_INVENTORY,
        "record_id",
        ["B-001", "B-002", "B-003", "B-004"],
    )


GAP_ADDITIONS = {
    "G-001": (
        "Unit B separates internal support from neutral correction: current NICE guidance distinguishes immediate debrief after harm is contained from a service-user-led external review with staff from outside the ward within 72 hours, while the TALK implementation remained staff-initiated and internal, changed some care-plan discussions, and did not reduce event rate or severity. Debrief is not independent adjudication or completed correction (F-172, F-175).",
        ["F-172", "F-175"],
    ),
    "G-002": (
        "The current child-aggression guidance places assessment, safeguarding, restrictive intervention, medication, monitoring, and review inside trained professional and statutory systems and prohibits using family contact, social interaction, food, or fluids to force compliance; peer therapy or membership authority cannot inherit those powers (F-172).",
        ["F-172"],
    ),
    "G-005": (
        "Unit B makes the child-rights floor operational: developmental participation, safeguarding, parental involvement, dignity, continuous wellbeing monitoring, least-restrictive response, nonpunitive necessities and contact, external review, and governing oversight persist even when conduct is dangerous (F-172).",
        ["F-172"],
    ),
    "G-006": (
        "Assessment and review now require separate dashboard fields for outcome-specific discrimination, calibration and base rate, interrater reliability, false positives and negatives, subgroup performance, missing and excluded cases, reassessment interval, management effect, debrief fidelity, action completion, child voice, staff impact, event rate, and event severity. Prediction and supportive review are not safety outcomes by themselves (F-173 through F-175).",
        ["F-173", "F-174", "F-175"],
    ),
    "G-009": (
        "Collective childrearing does not create authority to diagnose, restrain, seclude, medicate, investigate, or decide custody. It needs a conduct-record route to qualified assessment and lawful safeguarding plus child participation, family involvement, nonpunitive contact, external review, and separately measured child outcomes (F-172, F-175).",
        ["F-172", "F-175"],
    ),
    "G-018": (
        "Unit B found no lay danger filter. Even professional structured judgment was outcome-specific, time-limited, information-dependent, and fallible: SAVRY separated institutional-violence groups but did not supply individual certainty or a management-effect test (F-173), while START:AV field ratings had poor reliability for total scores, partial outcome validity, no tested incremental value over lifetime history, and no evidence that use reduced incidents or restrictions (F-174).",
        ["F-173", "F-174"],
    ),
}


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response pilot",
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response and assessment/review units",
        "gap checkpoint",
    )

    output: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        matched = next(
            (gap_id for gap_id in GAP_ADDITIONS if line.startswith(f"| {gap_id} |")),
            None,
        )
        if matched is None:
            output.append(line)
            continue

        cells = line.split("|")
        assert len(cells) == 9, f"unexpected gap-table shape for {matched}"
        addition, finding_ids = GAP_ADDITIONS[matched]
        if addition not in cells[4]:
            cells[4] = cells[4].rstrip() + " " + addition + " "
        evidence = [item.strip() for item in cells[7].split(",") if item.strip()]
        for finding_id in finding_ids:
            if finding_id not in evidence:
                evidence.append(finding_id)
        cells[7] = " " + ", ".join(evidence) + " "
        output.append("|".join(cells))
        seen.add(matched)

    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(output) + "\n"

    verification = (
        "- **F status:** re-check NICE NG10 after the expected 28 January 2027 replacement; inspect the applicable law, service capacity, professional standards, child and family participation, advocacy, external-review independence, implementation fidelity, and outcomes before translating its current process guidance.\n"
        "- **F status:** inspect the complete Gammelgård article, SAVRY manual and training requirements, event base rates, calibration, full error table, subgroup performance, record quality, intervention use, and later outcomes before professional application; relative odds are not individual certainty.\n"
        "- **F status:** replicate START:AV field performance across services and subgroups; audit evaluator information, agreement, exclusions, outcome definitions, dynamic reassessment, decision effects, incidents, wellbeing, and liberty restrictions before claiming clinical utility or fair classification.\n"
        "- **F status:** verify TALK debrief frequency, participants, action completion, child and affected-person accounts, staff outcomes, care-plan changes, independent review, and longer event outcomes; the reported internal staff debrief did not reduce event rate or severity.\n"
    )
    if verification not in text:
        text = text.replace("## Explicit non-promotions\n", verification + "\n## Explicit non-promotions\n", 1)

    nonpromotion = (
        "- Unit B produced no community screening instrument. SAVRY and START:AV results remain professional, outcome-specific validation evidence; no odds ratio, AUC, total score, summary category, diagnosis, record, or historical act was converted into a personality, admission, membership, productivity, or punishment rule.\n"
    )
    if nonpromotion not in text:
        text = text.rstrip() + "\n" + nonpromotion

    GAP_BANK.write_text(text, encoding="utf-8")


def update_roadmap() -> None:
    text = ROADMAP.read_text(encoding="utf-8")
    completed = (
        "Selected sources:\n\n"
        "- NICE guideline NG10, current published recommendations plus its active full-update status.\n"
        "- Gammelgård et al. (2008), six-month SAVRY validation in 208 institutionalized adolescents, DOI 10.1080/14789940802114475.\n"
        "- De Beuf et al. (2023), prospective START:AV field validation in 106 secure-care adolescents, DOI 10.1177/10731911211063228.\n"
        "- Shepherd et al. (2024), TALK post-event debrief implementation in acute child and adolescent mental-health units, DOI 10.1136/bmjoq-2023-002704.\n\n"
        "Status: completed in `COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md`. No lay screening tool was produced; the exact next boundary is Unit C.\n"
    )
    if completed not in text:
        anchor = (
            "Stop after four sources. Do not produce a community screening instrument. The output is a boundary map: what residents can observe and document, what requires independent professional assessment, and what requires lawful emergency action.\n"
        )
        assert anchor in text
        text = text.replace(anchor, anchor + "\n" + completed, 1)
    ROADMAP.write_text(text, encoding="utf-8")


def update_handoffs() -> None:
    text = STATE.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **171 findings** (`F-001` through `F-171`). The adjacent child-response pilot added three findings in explicitly separate residential and clinical lanes.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **175 findings** (`F-001` through `F-175`). The assessment/review unit added four findings in explicitly separate authoritative clinical, forensic, secure youth-care, and inpatient quality-improvement lanes.",
        "state finding count",
    )
    durable = "- `COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md` completes the four-source assessment, immediate-safety, and review unit. It preserves the current-guidance update flag, group-prediction and reliability limits, the distinction between prediction and management effect, and the negative event-rate result for internal staff debriefing.\n"
    if durable not in text:
        anchor = "- `COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md` completes the first five-record adjacent unit. The Brown dissertation remains an access-limited retrieval lead; three primary evaluations produced F-169 through F-171 without supplying the complete individual dangerous-child sequence.\n"
        assert anchor in text
        text = text.replace(anchor, anchor + durable, 1)
    text = replace_once_or_confirm(
        text,
        "- The first five-record adjacent child-response pilot is complete. The next bounded unit is Unit B in `docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`: four sources on assessment, immediate safety, and independent review.",
        "- The four-source assessment, immediate-safety, and review unit is complete. The next bounded unit is Unit C in `docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`: four comparative studies on durable treatment and transition beyond the active treatment window.",
        "state next unit",
    )
    evidence = "- The assessment/review unit adds a professional process boundary: developmentally informed assessment, safeguarding, de-escalation, least-restrictive lawful action, immediate debrief, external review, plan correction, and governing oversight are separate functions. SAVRY and START:AV findings show group-level and outcome-specific predictive value with material error, reliability, history, and implementation limits. A staff debrief implementation reported learning and care-plan discussion but no significant reduction in behavioral-event rate or severity. None creates a lay danger screen or transfers clinical and statutory powers to a private community.\n"
    if evidence not in text:
        anchor = "- The adjacent child-response pilot adds three bounded contrasts: family-style residential gains that did not remain statistically significant one year after exit; setting-level residential reductions in some but not all incident categories; and randomized child-plus-caregiver improvements during a period that included continuing individualized services. None is an intentional-community case or a validated danger screen.\n"
        assert anchor in text
        text = text.replace(anchor, anchor + evidence, 1)
    text = replace_once_or_confirm(
        text,
        "2. Continue with Unit B in the adjacent-source roadmap; stop after one current authoritative practice guideline, two prospective structured-professional-judgment validation studies, and one primary implementation study.",
        "2. Continue with Unit C in the adjacent-source roadmap; stop after four primary comparative studies on durable treatment and transition, keeping family/community and residential/group-care lanes separate.",
        "state resume step",
    )
    STATE.write_text(text, encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "- **171** evidence findings (`F-001` through `F-171`)",
        "- **175** evidence findings (`F-001` through `F-175`)",
        "README count",
    )
    text = replace_once_or_confirm(
        text,
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md`](recovered/COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md`](recovered/COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "README latest report",
    )
    text = replace_once_or_confirm(
        text,
        "python recovered/test_adjacent_child_pilot_workflow.py\npython recovered/verify_adjacent_child_pilot.py",
        "python recovered/test_adjacent_assessment_review_workflow.py\npython recovered/verify_adjacent_assessment_review.py",
        "README validation",
    )
    text = replace_once_or_confirm(
        text,
        "The verifier checks all eight standalone source sizes and hashes, seven PDF page counts, EPUB integrity, nonempty extracted text, inventory dispositions, sequential finding IDs, gap references, discovery coverage, report coverage, cumulative counts, preservation of all non-standalone inventory rows, and completion of the 984-journal-plus-8-standalone boundary.",
        "The current verifier checks sequential findings through F-175, the nine-record cumulative adjacent inventory, the four Unit B source dispositions, unchanged gap classes, boundary-map and report coverage, the Unit C handoff, and exclusion of source binaries outside known local-only corpus roots.",
        "README verifier description",
    )
    README.write_text(text, encoding="utf-8")

    text = INDEX.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-CHILD-PILOT-REPORT.md`",
        "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md`",
        "index latest report",
    )
    INDEX.write_text(text, encoding="utf-8")

    text = AGENTS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`python recovered/test_adjacent_child_pilot_workflow.py` (or the current bounded-unit successor)",
        "`python recovered/test_adjacent_assessment_review_workflow.py` (or the current bounded-unit successor)",
        "AGENTS regression",
    )
    text = replace_once_or_confirm(
        text,
        "`python recovered/verify_adjacent_child_pilot.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "`python recovered/verify_adjacent_assessment_review.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "AGENTS verification",
    )
    AGENTS.write_text(text, encoding="utf-8")


def main() -> None:
    merge_findings_and_sources()
    update_gap_bank()
    update_roadmap()
    update_handoffs()


if __name__ == "__main__":
    main()
