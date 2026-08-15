#!/usr/bin/env python3
"""Apply the completed adjacent fair-separation checkpoint."""

from __future__ import annotations

from pathlib import Path

import update_adjacent_official_correction as prior


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
UNIT_LEDGER = ROOT / "COMMUNITIES-ADJACENT-FAIR-SEPARATION-EVIDENCE-LEDGER.csv"
SOURCE_INVENTORY = ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv"
UNIT_SOURCE_INVENTORY = ROOT / "COMMUNITIES-ADJACENT-FAIR-SEPARATION-SOURCE-INVENTORY.csv"
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


def merge_findings_and_sources() -> None:
    prior.merge_unit_csv(
        LEDGER,
        UNIT_LEDGER,
        "finding_id",
        ["F-183", "F-184", "F-185", "F-186"],
    )
    prior.merge_unit_csv(
        SOURCE_INVENTORY,
        UNIT_SOURCE_INVENTORY,
        "record_id",
        ["E-001", "E-002", "E-003", "E-004"],
    )


GAP_ADDITIONS = {
    "G-001": (
        "Unit E separates permission to leave from usable exit: a draft instrument ring-fences a two-business-day Leaving Fund but leaves a later benefit nonvested or discounted, while the JFCT closure record shows that late claims can depend on archived records, deadlines, self-funded advice, trustee classification, and beneficiary votes. Write the right, reserve, deadline, former-member records, neutral review, household transition, and safety exception before crisis (F-183, F-186).",
        ["F-183", "F-186"],
    ),
    "G-005": (
        "Pooled protection and planned fission must reach the individual. PEACH's community-level structure gave no direct individual entitlement in the inspected account, and the Hutterite public record allows household assignment by lot even when aggregate assets are divided. Preserve direct medical access, individual appeal, refusal, family contact, and necessities across pooled claims and forks (F-184, F-185).",
        ["F-184", "F-185"],
    ),
    "G-006": (
        "Unit E reports instrument existence, adoption, reserve funding, claims submitted or denied, actual payout, voluntary allocation, debt, successor viability, closure distributions, family continuity, and later wellbeing separately. A draft clause, historical payment assertion, balanced asset split, court allocation, or completed claims cut-off is not a later outcome (F-183 through F-186).",
        ["F-183", "F-184", "F-185", "F-186"],
    ),
    "G-008": (
        "An outward door needs immediate and sufficient household liquidity, vested later benefits, record access after membership, housing and care continuity, protected family contact, and affordable independent review. A small rapid fund, a retrospective closure payment, or a right that depends on a vote does not establish a usable family exit (F-183, F-186).",
        ["F-183", "F-186"],
    ),
    "G-012": (
        "Unit E turns exit and fission clauses into auditable controls: reserve all-member exit liquidity; separate and vest each benefit; publish valuation and debt schedules; preserve former-member records; use independent escrow and review; give an individual route around a home-community claim gate; and audit both successors. Aggregate equity between institutions cannot substitute for an individual right (F-183 through F-186).",
        ["F-183", "F-184", "F-185", "F-186"],
    ),
    "G-013": (
        "Map the legal and operational status of pooled-risk and trust arrangements, who may file, who screens, who pays first, who funds advice, what deadline binds, and which forum hears review. A court claims procedure, arbitration clause, or federation board answers a defined dispute; none supplies ordinary medical, family, housing, or safeguarding authority (F-183, F-184, F-186).",
        ["F-183", "F-184", "F-186"],
    ),
    "G-016": (
        "Planned fission must separate aggregate parity from individual consent. The Hutterite public account supplies a scale trigger and asset division but also volunteer-or-lot allocation; the Felger judgment supplies a post-breakdown allocation, not a voluntary fork. Require refusal rights, household and child voice, debt schedules, family contact, appeal, and both-successor outcome review (F-185).",
        ["F-185"],
    ),
}


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = prior.replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response, assessment/review, durable treatment/transition, and official-correction units",
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response, assessment/review, durable treatment/transition, official-correction, and fair-separation/pooled-risk/planned-fission units",
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
        "- **F status:** retrieve the executed final Mothership agreement, amendments, reserve statements, actual exit payouts, former-member record access, disputes, and household outcomes; preserve the draft status meanwhile.\n"
        "- **F status:** retrieve PEACH's governing rules, current legal status, reserve audit, coverage and denial ledger, filed and unfiled need denominator, individual notice and appeal, hardship route, and later patient outcomes.\n"
        "- **F status:** retrieve the Felger trust agreement and trial reasons plus a signed Hutterite daughter-colony division schedule, valuation and debt ledger, refusal or dissent record, family-contact plan, and both-successor accounts.\n"
        "- **F status:** retrieve the full JFCT High Court Order and operative Trust Deed, notice and advice-access audit, classification and challenge outcomes, final votes and distributions, closure record, and later recipient and family outcomes.\n"
    )
    if verification not in text:
        text = text.replace(
            "## Explicit non-promotions\n",
            verification + "\n## Explicit non-promotions\n",
            1,
        )

    nonpromotion = (
        "- Unit E produced no forced relocation, family division, lot assignment as a general consent rule, community medical gate, private extinguishment of legal rights, or transfer of court, medical, insurance-regulatory, custody, or safeguarding power. Draft status, institutional equity, aggregate parity, court allocation, claim finality, and later human outcomes remain separate.\n"
    )
    if nonpromotion not in text:
        text = text.rstrip() + "\n" + nonpromotion

    GAP_BANK.write_text(text, encoding="utf-8")


def update_roadmap() -> None:
    text = ROADMAP.read_text(encoding="utf-8")
    completed = (
        "Selected records:\n\n"
        "- The Mothership LLC operating agreement, explicitly labelled draft dated March 20, 2016.\n"
        "- PEACH's current official governance page and a 2013 first-person administrator claim account.\n"
        "- *Walter Estate v. Walter* and the Hutterites.org member-managed Daughter Colony record, kept in separate dissolution and planned-fission lanes.\n"
        "- Jesus Fellowship Community Trust Schedule 1A Notice under the July 25, 2025 High Court order and current closure-phase records.\n\n"
        "Status: completed in `COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`. Permission, usable liquidity, individual entitlement, aggregate parity, neutral review, claim finality, and later human outcomes remain separate. This completes the finite adjacent-source roadmap; no article drafting or revision is authorized by this research checkpoint.\n"
    )
    if completed not in text:
        anchor = "- Are later outcomes reported rather than inferred from legal survival?\n"
        assert anchor in text
        text = text.replace(anchor, anchor + "\n" + completed, 1)
    ROADMAP.write_text(text, encoding="utf-8")


def update_handoffs() -> None:
    text = STATE.read_text(encoding="utf-8")
    text = prior.replace_once_or_confirm(
        text,
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **182 findings** (`F-001` through `F-182`). The official-correction unit added three findings in explicitly separate professional-licensing, royal-commission, and statutory-inquiry lanes.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **186 findings** (`F-001` through `F-186`). The fair-separation unit added four findings in explicitly separate draft exit-instrument, pooled-risk, planned-fission/allocation, and court-supervised trust-closure lanes.",
        "state finding count",
    )
    report = (
        "- `COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md` completes the four-record fair-separation, pooled-risk, and planned-fission unit. It separates permission from usable exit, institutional equity from individual entitlement, aggregate parity from consent, court finality from pre-crisis exit, and procedure from later human outcomes.\n"
    )
    if report not in text:
        anchor = (
            "- `COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md` completes the three-record official-correction unit. It separates professional authority removal, inquiry findings and recommendations, police and court outcomes, survivor support, implementation, family contact, child wellbeing, and later institutional safety.\n"
        )
        assert anchor in text
        text = text.replace(anchor, anchor + report, 1)
    text = prior.replace_once_or_confirm(
        text,
        "- The three-record official-correction unit is complete. The next bounded unit is Unit E in `docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`: four underlying instruments or primary records on fair separation, pooled risk, and planned fission.",
        "- The four-record fair-separation, pooled-risk, and planned-fission unit is complete. The assigned primary corpus and all five units in the finite adjacent-source roadmap are complete. There is no next research unit in the accepted roadmap.",
        "state finite boundary",
    )
    evidence = (
        "- The fair-separation unit adds four control boundaries. An unsigned draft pairs a two-business-day Leaving Fund with a later nonvested or discounted benefit. PEACH's inspected account protects participating-community equity but supplies no direct individual entitlement. The Hutterite records distinguish a post-breakdown court allocation from a planned daughter split whose aggregate asset parity can coexist with household assignment by lot. The JFCT record supplies court-supervised claim finality after collapse, not an ordinary pre-crisis exit. None reports the complete chain from adopted right through household usability and later wellbeing.\n"
    )
    if evidence not in text:
        anchor = (
            "- The official-correction unit adds three endpoint warnings. New York license revocations removed professional authority but did not report family repair or child and patient outcomes. The New Zealand Royal Commission documented blocked reporting and required ongoing government safety action at Gloriavale but did not prove implementation. IICSA linked Jesus Fellowship disclosures to police investigation and six convictions relating to 11 children while distinguishing internal discipline, external adjudication, survivor support, and later institutional safety. None transfers state or professional power to a private community.\n"
        )
        assert anchor in text
        text = text.replace(anchor, anchor + evidence, 1)
    text = prior.replace_once_or_confirm(
        text,
        "2. Continue with Unit E in the adjacent-source roadmap; stop after four underlying instruments or primary records on fair separation, pooled risk, and planned fission.",
        "2. The finite adjacent-source roadmap is complete. Do not invent another research unit; await explicit authority for article editing or a new bounded research question.",
        "state resume step",
    )
    STATE.write_text(text, encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    text = prior.replace_once_or_confirm(
        text,
        "- **182** evidence findings (`F-001` through `F-182`)",
        "- **186** evidence findings (`F-001` through `F-186`)",
        "README count",
    )
    text = prior.replace_once_or_confirm(
        text,
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md); the finite continuation queue is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md); the completed finite roadmap is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "README latest report",
    )
    text = prior.replace_once_or_confirm(
        text,
        "python recovered/test_adjacent_official_correction_workflow.py\npython recovered/verify_adjacent_official_correction.py",
        "python recovered/test_adjacent_fair_separation_workflow.py\npython recovered/verify_adjacent_fair_separation.py",
        "README validation",
    )
    text = prior.replace_once_or_confirm(
        text,
        "The current verifier checks sequential findings through F-182, the 16-record cumulative adjacent inventory, the three Unit D official-record dispositions, unchanged gap classes, official-correction and report coverage, the Unit E handoff, and exclusion of source binaries outside known local-only corpus roots.",
        "The current verifier checks sequential findings through F-186, the 20-record cumulative adjacent inventory, the four Unit E source dispositions, unchanged gap classes, fair-separation report coverage, finite-roadmap completion, and exclusion of source binaries outside known local-only corpus roots.",
        "README verifier description",
    )
    README.write_text(text, encoding="utf-8")

    text = INDEX.read_text(encoding="utf-8")
    text = prior.replace_once_or_confirm(
        text,
        "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-OFFICIAL-CORRECTION-REPORT.md`",
        "the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`",
        "index latest report",
    )
    INDEX.write_text(text, encoding="utf-8")

    text = AGENTS.read_text(encoding="utf-8")
    text = prior.replace_once_or_confirm(
        text,
        "`python recovered/test_adjacent_official_correction_workflow.py` (or the current bounded-unit successor)",
        "`python recovered/test_adjacent_fair_separation_workflow.py` (or the current bounded-unit successor)",
        "AGENTS regression",
    )
    text = prior.replace_once_or_confirm(
        text,
        "`python recovered/verify_adjacent_official_correction.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "`python recovered/verify_adjacent_fair_separation.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
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
