#!/usr/bin/env python3
"""Apply the completed adjacent durable-treatment and transition checkpoint."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
UNIT_LEDGER = ROOT / "COMMUNITIES-ADJACENT-DURABLE-EVIDENCE-LEDGER.csv"
SOURCE_INVENTORY = ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv"
UNIT_SOURCE_INVENTORY = ROOT / "COMMUNITIES-ADJACENT-DURABLE-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"
AGENTS = REPOSITORY / "AGENTS.md"
INDEX = REPOSITORY / "docs" / "INDEX.md"
ROADMAP = (
    REPOSITORY
    / "docs"
    / "superpowers"
    / "plans"
    / "2026-08-15-adjacent-source-roadmap.md"
)


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
        ["F-176", "F-177", "F-178", "F-179"],
    )
    merge_unit_csv(
        SOURCE_INVENTORY,
        UNIT_SOURCE_INVENTORY,
        "record_id",
        ["C-001", "C-002", "C-003", "C-004"],
    )


GAP_ADDITIONS = {
    "G-002": (
        "Unit C rejects a generic claim that the community is the therapist. The favorable MST and treatment-foster-care results arose inside trained, supervised systems spanning family, school, clinical, and official-record functions, while current FFT and residential iCBT trials found no statistically significant advantage over active care. A model name, family-style household, in-program improvement, or written relapse plan cannot replace qualified service infrastructure or comparative later outcomes (F-176 through F-179).",
        ["F-176", "F-177", "F-178", "F-179"],
    ),
    "G-005": (
        "Durable-treatment evidence does not make rights contingent on clinical response, completion, conviction, or service assignment. Family involvement, school continuity, independent care, confidentiality, and lawful external records remained functions of professional systems; poor response or dropout did not authorize community coercion or loss of contact, necessities, reply, or appeal (F-177 through F-179).",
        ["F-177", "F-178", "F-179"],
    ),
    "G-006": (
        "Unit C adds a release-anchored durability panel: comparison condition; baseline severity; actual treatment dose, fidelity, crossover and completion; treatment or placement end; continuing services actually received; time at risk; conduct-specific recurrence; record jurisdiction; victim safety; child wellbeing; caregiver burden; restrictions and placement disruption; missing cases; and fixed post-support intervals. An in-program change, treatment plan, or conviction count cannot stand for the whole outcome (F-176 through F-179).",
        ["F-176", "F-177", "F-178", "F-179"],
    ),
    "G-009": (
        "The favorable family-style placement result depended on state-certified foster parents, daily case data, weekly supervision, family-of-origin therapy, school coordination, on-call consultation, and external follow-up. Collective childrearing does not inherit those capacities merely by resembling a household, and the bundled trial does not identify residence form as the active ingredient (F-178).",
        ["F-178"],
    ),
    "G-018": (
        "Unit C supplies no admission or danger filter. Trial averages, criminal records, treatment assignment, apparent in-program response, completion, and dropout are outcome and implementation data, not stable personality evidence. Positive and null results varied across severity, services, comparators, jurisdictions, and follow-up windows and cannot classify an individual child or applicant (F-176 through F-179).",
        ["F-176", "F-177", "F-178", "F-179"],
    ),
}


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response and assessment/review units",
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response, assessment/review, and durable treatment/transition units",
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
        "- **F status:** independently replicate and transport the 21.9-year MST result; audit trial allocation, developer role, record coverage across jurisdictions, later services, subgroup outcomes, victim safety, wellbeing, family burden, and the mechanism connecting adolescent treatment to middle-adult records.\n"
        "- **F status:** replicate the Norwegian FFT effectiveness trial with planned power, stable eligibility and comparator rules, complete registry linkage, service-dose accounting, and separate lower-severity prevention and serious-recidivism populations; the current null result does not establish exact equivalence.\n"
        "- **F status:** independently replicate treatment foster care against defined group-care alternatives; measure crossover, post-placement services, victim safety, wellbeing, family burden, placement experience, and adulthood outcomes before attributing the bundle to household form or a single component.\n"
        "- **F status:** test any residential transition intervention only after feasibility, fidelity, completion, and delivered aftercare are measurable; retain release-indexed victim, wellbeing, family, and reconviction outcomes and do not replace intent-to-treat results with selected completer comparisons.\n"
    )
    if verification not in text:
        text = text.replace("## Explicit non-promotions\n", verification + "\n## Explicit non-promotions\n", 1)

    nonpromotion = (
        "- Unit C produced no treatment-derived screen or community treatment mandate. Criminal history, service assignment, apparent response, completion, dropout, family form, and official outcomes remain conduct, implementation, and group-level evidence; none was converted into a diagnosis, admission rule, membership decision, custody power, or punishment rule.\n"
    )
    if nonpromotion not in text:
        text = text.rstrip() + "\n" + nonpromotion

    GAP_BANK.write_text(text, encoding="utf-8")


def update_roadmap() -> None:
    text = ROADMAP.read_text(encoding="utf-8")
    completed = (
        "Selected sources:\n\n"
        "- Sawyer and Borduin (2011), 21.9-year MST follow-up, DOI 10.1037/a0024862.\n"
        "- Olseth, Høstmælingen, and Bjørnebekk (2026), Norwegian FFT registry effectiveness trial, DOI 10.1007/s11292-026-09736-6.\n"
        "- Chamberlain, Leve, and DeGarmo (2007), treatment foster care versus group care at 24 months, DOI 10.1037/0022-006X.75.1.187.\n"
        "- Lardén, Högström, and Långström (2021), residential iCBT add-on with 24-month post-release follow-up, DOI 10.3389/fpsyt.2021.670957.\n\n"
        "Status: completed in `COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md`. The two family/community and two residential/group-care studies remain separate; the exact next boundary is Unit D.\n"
    )
    if completed not in text:
        anchor = (
            "Stop after four studies or when two independent high-quality studies converge on the same transfer limit.\n"
        )
        assert anchor in text
        text = text.replace(anchor, anchor + "\n" + completed, 1)
    ROADMAP.write_text(text, encoding="utf-8")


def update_handoffs() -> None:
    text = STATE.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **175 findings** (`F-001` through `F-175`). The assessment/review unit added four findings in explicitly separate authoritative clinical, forensic, secure youth-care, and inpatient quality-improvement lanes.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **179 findings** (`F-001` through `F-179`). The durable-treatment unit added four comparative findings in explicitly separate family/community, treatment-foster-care, and residential forensic lanes.",
        "state finding count",
    )
    durable = "- `COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md` completes the four-study durable-treatment and transition unit. It preserves two favorable and two null comparative results, release-anchored follow-up, active-comparator and completion limits, developer disclosures, and separate family/community and residential/group-care lanes.\n"
    if durable not in text:
        anchor = "- `COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md` completes the four-source assessment, immediate-safety, and review unit. It preserves the current-guidance update flag, group-prediction and reliability limits, the distinction between prediction and management effect, and the negative event-rate result for internal staff debriefing.\n"
        assert anchor in text
        text = text.replace(anchor, anchor + durable, 1)
    text = replace_once_or_confirm(
        text,
        "- The four-source assessment, immediate-safety, and review unit is complete. The next bounded unit is Unit C in `docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`: four comparative studies on durable treatment and transition beyond the active treatment window.",
        "- The four-study durable-treatment and transition unit is complete. The next bounded unit is Unit D in `docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`: three official correction records for communal child safeguarding, with children kept in the alleged-victim rather than dangerous-actor lane.",
        "state next unit",
    )
    evidence = "- The durable-treatment unit adds two favorable and two null comparisons. One developer-led MST trial found lower official criminal and civil outcomes 21.9 years after treatment; a current Norwegian FFT effectiveness trial found no significant advantage over active care; one small treatment-foster-care trial found better 24-month delinquency outcomes than group care; and a Swedish residential iCBT add-on found no significant post-release benefit beyond active care. The shared transfer rule is release-anchored, comparator-aware measurement of actual service dose, completion, transition support, recurrence, victim safety, wellbeing, and family burden—not treatment-name prestige or in-program change.\n"
    if evidence not in text:
        anchor = "- The assessment/review unit adds a professional process boundary: developmentally informed assessment, safeguarding, de-escalation, least-restrictive lawful action, immediate debrief, external review, plan correction, and governing oversight are separate functions. SAVRY and START:AV findings show group-level and outcome-specific predictive value with material error, reliability, history, and implementation limits. A staff debrief implementation reported learning and care-plan discussion but no significant reduction in behavioral-event rate or severity. None creates a lay danger screen or transfers clinical and statutory powers to a private community.\n"
        assert anchor in text
        text = text.replace(anchor, anchor + evidence, 1)
    text = replace_once_or_confirm(
        text,
        "2. Continue with Unit C in the adjacent-source roadmap; stop after four primary comparative studies on durable treatment and transition, keeping family/community and residential/group-care lanes separate.",
        "2. Continue with Unit D in the adjacent-source roadmap; stop after three official correction records for communal child safeguarding and keep alleged child victims separate from the dangerous-child actor branch.",
        "state resume step",
    )
    STATE.write_text(text, encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "- **175** evidence findings (`F-001` through `F-175`)",
        "- **179** evidence findings (`F-001` through `F-179`)",
        "README count",
    )
    text = replace_once_or_confirm(
        text,
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md`](recovered/COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "README latest report",
    )
    text = replace_once_or_confirm(
        text,
        "python recovered/test_adjacent_assessment_review_workflow.py\npython recovered/verify_adjacent_assessment_review.py",
        "python recovered/test_adjacent_durable_transition_workflow.py\npython recovered/verify_adjacent_durable_transition.py",
        "README validation",
    )
    text = replace_once_or_confirm(
        text,
        "The current verifier checks sequential findings through F-175, the nine-record cumulative adjacent inventory, the four Unit B source dispositions, unchanged gap classes, boundary-map and report coverage, the Unit C handoff, and exclusion of source binaries outside known local-only corpus roots.",
        "The current verifier checks sequential findings through F-179, the 13-record cumulative adjacent inventory, the four Unit C source dispositions, unchanged gap classes, durable-transition and report coverage, the Unit D handoff, and exclusion of source binaries outside known local-only corpus roots.",
        "README verifier description",
    )
    README.write_text(text, encoding="utf-8")

    text = INDEX.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-ASSESSMENT-REVIEW-REPORT.md`",
        "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md`",
        "index latest report",
    )
    INDEX.write_text(text, encoding="utf-8")

    text = AGENTS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`python recovered/test_adjacent_assessment_review_workflow.py` (or the current bounded-unit successor)",
        "`python recovered/test_adjacent_durable_transition_workflow.py` (or the current bounded-unit successor)",
        "AGENTS regression",
    )
    text = replace_once_or_confirm(
        text,
        "`python recovered/verify_adjacent_assessment_review.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "`python recovered/verify_adjacent_durable_transition.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
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
