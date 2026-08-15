#!/usr/bin/env python3
"""Apply the completed adjacent official-correction checkpoint."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
UNIT_LEDGER = ROOT / "COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-EVIDENCE-LEDGER.csv"
SOURCE_INVENTORY = ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv"
UNIT_SOURCE_INVENTORY = ROOT / "COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-SOURCE-INVENTORY.csv"
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
        ["F-180", "F-181", "F-182"],
    )
    merge_unit_csv(
        SOURCE_INVENTORY,
        UNIT_SOURCE_INVENTORY,
        "record_id",
        ["D-001", "D-002", "D-003"],
    )


GAP_ADDITIONS = {
    "G-003": (
        "Unit D turns protected reporting into an external correction chain: preserve allegation, administrative finding, charge, conviction, support, recommendation, and later outcome as separate records; route evidence around the challenged therapist or leader; and do not let reputation, loyalty, forgiveness, or internal absolution stop lawful referral (F-180 through F-182).",
        ["F-180", "F-181", "F-182"],
    ),
    "G-004": (
        "The capture audit must now include control of professional supervision, complaint evidence, billing, family contact, child disclosures, referral decisions, and safeguarding records. A leader or therapist who controls one of those functions cannot select the reviewer or hear the appeal concerning it (F-180 through F-182).",
        ["F-180", "F-181", "F-182"],
    ),
    "G-005": (
        "Official correction does not make support or rights depend on case success. Lawful family contact, outside reporting, independent advice, survivor support, schooling, necessities, and protection from retaliation persist before and after a licensing action, inquiry, charge, conviction, acquittal, closure, or unproven report (F-180 through F-182).",
        ["F-180", "F-181", "F-182"],
    ),
    "G-006": (
        "Unit D separates authority removal, inquiry publication, prosecution, conviction, implementation, survivor recovery, child wellbeing, family repair, recurrence, institutional closure, redress, and successor-body compliance. No official procedural endpoint can stand for the whole correction outcome (F-180 through F-182).",
        ["F-180", "F-181", "F-182"],
    ),
    "G-009": (
        "Collective caregiving does not create authority to suppress a child's report, blame the child, relocate an accused person as the sole response, or adjudicate alleged abuse through prayer, forgiveness, reconciliation, or membership discipline. The child needs confidential external intake and continuing independent support (F-181, F-182).",
        ["F-181", "F-182"],
    ),
    "G-013": (
        "Unit D assigns distinct external functions: professional regulators remove licensed authority; police and courts investigate and adjudicate offences; child-protection bodies address immediate and continuing safety; inquiries preserve systemic evidence and recommend correction; and survivor services support without testing credibility. Each coupling needs a named trigger and later outcome review (F-180 through F-182).",
        ["F-180", "F-181", "F-182"],
    ),
}


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response, assessment/review, and durable treatment/transition units",
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response, assessment/review, durable treatment/transition, and official-correction units",
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
        "- **F status:** retrieve the complete New York professional-discipline charges, findings, hearing records, surrender records for other Sullivanian therapists, and appellate material; keep professional authority, custody, family contact, repair, and later child or patient outcomes separate.\n"
        "- **F status:** audit implementation of Gloriavale Recommendation 88 after the Royal Commission closed, including responsible agencies, monitoring continuity, confidential child access, family contact, survivor support, current risk, and published later outcomes; do not restate dated proceedings as current.\n"
        "- **F status:** reconcile the IICSA Jesus Fellowship record with police dispositions, the later redress record, institutional closure, successor bodies, survivor-reported experience, and later safeguarding outcomes without converting allegations, criminal history, or institutional labels into danger proxies.\n"
    )
    if verification not in text:
        text = text.replace("## Explicit non-promotions\n", verification + "\n## Explicit non-promotions\n", 1)

    nonpromotion = (
        "- Unit D produced no community investigative, licensing, custody, or punishment authority and no danger screen. Allegation, administrative finding, charge, conviction, sanction, recommendation, support, implementation, and later safety remain separate; official status does not make any one of them a complete outcome.\n"
    )
    if nonpromotion not in text:
        text = text.rstrip() + "\n" + nonpromotion

    GAP_BANK.write_text(text, encoding="utf-8")


def update_roadmap() -> None:
    text = ROADMAP.read_text(encoding="utf-8")
    completed = (
        "Selected official records:\n\n"
        "- New York State Office of the Professions and Board of Regents, June and July 1997 psychology enforcement-action summaries for Helen M. Fogarty (a/k/a Helen Moses) and Marc Rice.\n"
        "- New Zealand Royal Commission, *Whanaketia* final Gloriavale findings, government-response context, and Recommendation 88 (2024).\n"
        "- UK Independent Inquiry into Child Sexual Abuse, *Child protection in religious organisations and settings* investigation report, Jesus Fellowship evidence, conclusions, and recommendations (2021).\n\n"
        "Status: completed in `COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md`. Licensing, inquiry, police/court, survivor-support, and later-outcome functions remain separate; the exact next boundary is Unit E.\n"
    )
    if completed not in text:
        anchor = (
            "This unit concerns children as alleged victims and institutional correction, not dangerous child actors. Its purpose is to test independence, evidence preservation, recusal, professional discipline, family contact, and later safeguarding outcomes.\n"
        )
        assert anchor in text
        text = text.replace(anchor, anchor + "\n" + completed, 1)
    ROADMAP.write_text(text, encoding="utf-8")


def update_handoffs() -> None:
    text = STATE.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **179 findings** (`F-001` through `F-179`). The durable-treatment unit added four comparative findings in explicitly separate family/community, treatment-foster-care, and residential forensic lanes.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **182 findings** (`F-001` through `F-182`). The official-correction unit added three findings in explicitly separate professional-licensing, royal-commission, and statutory-inquiry lanes.",
        "state finding count",
    )
    official = "- `COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md` completes the three-record official-correction unit. It separates professional authority removal, inquiry findings and recommendations, police and court outcomes, survivor support, implementation, family contact, child wellbeing, and later institutional safety.\n"
    if official not in text:
        anchor = "- `COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md` completes the four-study durable-treatment and transition unit. It preserves two favorable and two null comparative results, release-anchored follow-up, active-comparator and completion limits, developer disclosures, and separate family/community and residential/group-care lanes.\n"
        assert anchor in text
        text = text.replace(anchor, anchor + official, 1)
    text = replace_once_or_confirm(
        text,
        "- The four-study durable-treatment and transition unit is complete. The next bounded unit is Unit D in `docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`: three official correction records for communal child safeguarding, with children kept in the alleged-victim rather than dangerous-actor lane.",
        "- The three-record official-correction unit is complete. The next bounded unit is Unit E in `docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`: four underlying instruments or primary records on fair separation, pooled risk, and planned fission.",
        "state next unit",
    )
    evidence = "- The official-correction unit adds three endpoint warnings. New York license revocations removed professional authority but did not report family repair or child and patient outcomes. The New Zealand Royal Commission documented blocked reporting and required ongoing government safety action at Gloriavale but did not prove implementation. IICSA linked Jesus Fellowship disclosures to police investigation and six convictions relating to 11 children while distinguishing internal discipline, external adjudication, survivor support, and later institutional safety. None transfers state or professional power to a private community.\n"
    if evidence not in text:
        anchor = "- The durable-treatment unit adds two favorable and two null comparisons. One developer-led MST trial found lower official criminal and civil outcomes 21.9 years after treatment; a current Norwegian FFT effectiveness trial found no significant advantage over active care; one small treatment-foster-care trial found better 24-month delinquency outcomes than group care; and a Swedish residential iCBT add-on found no significant post-release benefit beyond active care. The shared transfer rule is release-anchored, comparator-aware measurement of actual service dose, completion, transition support, recurrence, victim safety, wellbeing, and family burden—not treatment-name prestige or in-program change.\n"
        assert anchor in text
        text = text.replace(anchor, anchor + evidence, 1)
    text = replace_once_or_confirm(
        text,
        "2. Continue with Unit D in the adjacent-source roadmap; stop after three official correction records for communal child safeguarding and keep alleged child victims separate from the dangerous-child actor branch.",
        "2. Continue with Unit E in the adjacent-source roadmap; stop after four underlying instruments or primary records on fair separation, pooled risk, and planned fission.",
        "state resume step",
    )
    STATE.write_text(text, encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "- **179** evidence findings (`F-001` through `F-179`)",
        "- **182** evidence findings (`F-001` through `F-182`)",
        "README count",
    )
    text = replace_once_or_confirm(
        text,
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "README latest report",
    )
    text = replace_once_or_confirm(
        text,
        "python recovered/test_adjacent_durable_transition_workflow.py\npython recovered/verify_adjacent_durable_transition.py",
        "python recovered/test_adjacent_official_correction_workflow.py\npython recovered/verify_adjacent_official_correction.py",
        "README validation",
    )
    text = replace_once_or_confirm(
        text,
        "The current verifier checks sequential findings through F-179, the 13-record cumulative adjacent inventory, the four Unit C source dispositions, unchanged gap classes, durable-transition and report coverage, the Unit D handoff, and exclusion of source binaries outside known local-only corpus roots.",
        "The current verifier checks sequential findings through F-182, the 16-record cumulative adjacent inventory, the three Unit D official-record dispositions, unchanged gap classes, official-correction and report coverage, the Unit E handoff, and exclusion of source binaries outside known local-only corpus roots.",
        "README verifier description",
    )
    README.write_text(text, encoding="utf-8")

    text = INDEX.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-DURABLE-TRANSITION-REPORT.md`",
        "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md`",
        "index latest report",
    )
    INDEX.write_text(text, encoding="utf-8")

    text = AGENTS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`python recovered/test_adjacent_durable_transition_workflow.py` (or the current bounded-unit successor)",
        "`python recovered/test_adjacent_official_correction_workflow.py` (or the current bounded-unit successor)",
        "AGENTS regression",
    )
    text = replace_once_or_confirm(
        text,
        "`python recovered/verify_adjacent_durable_transition.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "`python recovered/verify_adjacent_official_correction.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
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
