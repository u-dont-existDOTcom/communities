#!/usr/bin/env python3
"""Build and apply the final cross-corpus synthesis checkpoint.

This pass does not add, remove, or edit evidence findings. It maps the existing
186 findings into a corpus-directed synthesis and updates the durable handoff.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
CROSSWALK = ROOT / "COMMUNITIES-SYNTHESIS-CROSSWALK.csv"
REPORT = ROOT / "COMMUNITIES-FINAL-SYNTHESIS-REPORT.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"
AGENTS = REPOSITORY / "AGENTS.md"
INDEX = REPOSITORY / "docs" / "INDEX.md"


THEMES = {
    "T-01": "authority, role fusion, and capture",
    "T-02": "participation, dissent, reporting, and evidence",
    "T-03": "membership, classification, and safety prediction",
    "T-04": "conflict, bounded separation, and remedy",
    "T-05": "care, medicine, therapy, and governance firewalls",
    "T-06": "children, family, education, and direct rights",
    "T-07": "assets, exit, records, and material security",
    "T-08": "capacity, infrastructure, labor, and external dependence",
    "T-09": "external correction, law, and professional boundaries",
    "T-10": "success, outcomes, source quality, and measurement",
    "T-11": "succession, fission, and movement continuity",
    "T-12": "dangerous-child bounded null and adjacent response evidence",
}

CLAIMS = {
    "S-01": "Authority must be decomposed by function and made replaceable.",
    "S-02": "Formal participation is not practical override or independent review.",
    "S-03": "Communities need bounded, conduct-specific separation authority.",
    "S-04": "Commitment, productivity, conformity, and labels are not validated danger screens.",
    "S-05": "Peer support cannot inherit clinical, custody, disciplinary, or evidentiary power.",
    "S-06": "Children need direct non-waivable rights and independent advocacy.",
    "S-07": "Exit must be legally permitted and materially, relationally, and procedurally usable.",
    "S-08": "Title, accounts, records, appointment power, and liquidity determine real control.",
    "S-09": "Dissent, evidence, reporting, appeal, and preservation need independent routes.",
    "S-10": "External correction is necessary for some functions but narrow, fallible, and incomplete.",
    "S-11": "Survival, cohesion, process completion, and in-program improvement are not human outcomes.",
    "S-12": "Material capacity and external dependencies constrain autonomy before character does.",
    "S-13": "Transformation, migration, alumni support, and planned fission can preserve continuity.",
    "S-14": "The intentional-community corpus does not answer the persistent-dangerous-child question.",
    "S-15": "Function-specific subsidiarity with direct individual routes is the combined model-assisted synthesis.",
}


def expand(spec: str) -> list[str]:
    """Expand a compact numeric finding specification into F-IDs."""
    values: list[int] = []
    for part in spec.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            start, end = (int(item) for item in part.split("-", 1))
            values.extend(range(start, end + 1))
        else:
            values.append(int(part))
    return [f"F-{value:03d}" for value in values]


# This is a partition: every finding has one primary corpus theme. Secondary
# relationships are represented by the synthesis-claim map and article-gap refs.
PRIMARY_THEME_SPECS = {
    "T-01": "4,6,9,34,35,52,61,63,73,84,88,89,95,97,101,109,110,117,143,165",
    "T-02": "10,37,55,70,81,85,113,122,124,133,136,137,147",
    "T-03": "3,12,13,33,38,45,58,59,69,71,75,83,87,91,106,153,164",
    "T-04": "1,2,20,39,46,66,72,77,82,93,130,163,166,167",
    "T-05": "7,8,40,56,57,74,156,159",
    "T-06": "17,27,29,43,49,51,99,104,116,141,149,150,152,155",
    "T-07": "5,18,21,42,44,47,54,67,78,92,96,107,112,120,135,139,144,160,183,184,186",
    "T-08": "24,25,26,28,129,132,134",
    "T-09": "11,36,50,53,62,65,86,94,102,119,123,126,127,128,145,157,180,181,182",
    "T-10": "14,15,19,30,32,41,60,108,140",
    "T-11": "16,22,23,68,79,80,98,103,114,161,185",
    "T-12": "31,48,64,76,90,100,105,111,115,118,121,125,131,138,142,146,148,151,154,158,162,168-179",
}

THEME_DEFAULT_CLAIMS = {
    "T-01": ["S-01", "S-02"],
    "T-02": ["S-02", "S-09"],
    "T-03": ["S-03", "S-04"],
    "T-04": ["S-03", "S-09"],
    "T-05": ["S-05"],
    "T-06": ["S-06"],
    "T-07": ["S-07", "S-08"],
    "T-08": ["S-12"],
    "T-09": ["S-09", "S-10"],
    "T-10": ["S-11"],
    "T-11": ["S-13"],
    "T-12": ["S-14"],
}

ADDITIONAL_CLAIM_SPECS = {
    "S-03": "3,39,59,66,72,77,82,93,109,130,153,163,166,167",
    "S-04": "12,13,38,45,58,59,69,71,75,83,87,91,106,140,164,169-179",
    "S-05": "40,43,49,74,86,94,116,119,126,141,147,149,150,156,159,169-180",
    "S-06": "11,17,27,29,43,49,51,75,84,86,99,104,116,122,126-128,141,149,150,152,155-159,169-182,184-186",
    "S-07": "5,16,18,21-23,42,44,50,51,54,61,67,68,71,77,78,92,96,99,103,107-114,119,120,135,139,144,153,160,161,183-186",
    "S-08": "4,21,34,35,42,44,47,50,52,54,61,78,84,88,89,92,95,96,101,107-110,112,117,120,124,129,135,139,143,144,160,161,183-186",
    "S-09": "10,30,37,41,55,62,70,74,81,85,86,91,94,97,102,104,107,109,113,114,122-128,132,133,136,137,145,147,156,157,167,172,175,180-182,186",
    "S-10": "11,20,36,44,50,53,62,65,78,86,94,102,104,107,109,116,119,120,123,126-128,132,134,135,137,144,145,156,157,159,169-186",
    "S-11": "14-17,19,22-30,32,38,40,41,44,45,47,48,54,58-60,64,68,69,71,72,75,76,81,83-87,90,92,93,95,98-100,105,106,108-111,114,115,118,121,123-125,127,129,131-140,142,146,148,151,154,155,158-162,168-186",
    "S-12": "3,19,24-28,33,43,47,52,54,59,60,69,71,75,83,87,92,106,108,112,116,129,132,134,140,150,153,155,159-161,183-185",
    "S-13": "16,18,22,23,44,54,61,68,79,80,84,95,98,99,103,108,110,114,124,129,135,139,152,155,160,161,183-186",
}

CHILD_NULL_IDS = set(expand("31,48,64,76,90,100,105,111,115,118,121,125,131,138,142,146,148,151,154,158,162,168"))
ADJACENT_RESPONSE_IDS = set(expand("169-179"))
OFFICIAL_CORRECTION_IDS = set(expand("180-182"))
INSTRUMENT_IDS = set(expand("183-186"))
METHOD_IDS = set(expand("12,14,15,30,32,38,40,41,45,58,60,75,81,87,106,108,123,136,137,140,164"))
DESIGN_IDS = set(expand("16,18-23,29,33,44,47,54,68,71,72,79,80,92,95,96,98,99,103,113,114,122,129,135,139,160,161,165-167"))
MIXED_IDS = set(expand("3,17,24-28,52,59,62,69,82-86,93,107,109,110,119,120,124,127,128,130,132-135,141,143,144,149,150,152,153,155,159,163"))


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        loaded = list(reader)
    assert all(None not in row for row in loaded)
    assert all(None not in row.values() for row in loaded)
    return loaded


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    """Replace one predecessor string, or confirm the successor is present."""
    if old in text:
        assert text.count(old) == 1, f"ambiguous replacement for {label}"
        return text.replace(old, new, 1)
    assert new in text, f"missing predecessor and successor for {label}"
    return text


def primary_theme_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for theme_id, spec in PRIMARY_THEME_SPECS.items():
        for finding_id in expand(spec):
            assert finding_id not in result, f"duplicate primary theme for {finding_id}"
            result[finding_id] = theme_id
    expected = {f"F-{number:03d}" for number in range(1, 187)}
    assert set(result) == expected, f"primary-theme coverage mismatch: {expected ^ set(result)}"
    return result


def claim_map(themes_by_finding: dict[str, str]) -> dict[str, list[str]]:
    result = {
        finding_id: list(THEME_DEFAULT_CLAIMS[theme_id])
        for finding_id, theme_id in themes_by_finding.items()
    }
    # Adjacent child-response sources replace the corpus-null claim with the
    # professional-boundary claims they actually support.
    for finding_id in ADJACENT_RESPONSE_IDS:
        result[finding_id] = ["S-04", "S-05", "S-06", "S-11"]
    for claim_id, spec in ADDITIONAL_CLAIM_SPECS.items():
        for finding_id in expand(spec):
            if claim_id not in result[finding_id]:
                result[finding_id].append(claim_id)
    for finding_id in result:
        result[finding_id].sort()
    assert all("S-15" not in claim_ids for claim_ids in result.values())
    return result


def gap_references() -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    for line in GAP_BANK.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\| (G-\d{3}) \|", line)
        if not match:
            continue
        gap_id = match.group(1)
        for finding_id in sorted(set(re.findall(r"F-\d{3}", line))):
            result[finding_id].append(gap_id)
    return result


def source_lane(finding_id: str) -> str:
    if finding_id in CHILD_NULL_IDS:
        return "bounded primary-corpus search"
    number = int(finding_id[-3:])
    if 165 <= number <= 167:
        return "traditional-society comparison"
    if finding_id in ADJACENT_RESPONSE_IDS:
        return "adjacent child-response/professional evidence"
    if finding_id in OFFICIAL_CORRECTION_IDS:
        return "adjacent official correction record"
    if finding_id in INSTRUMENT_IDS:
        return "adjacent governance instrument/primary record"
    return "intentional-community and communal-history corpus"


def evidence_role(finding_id: str) -> str:
    if finding_id in CHILD_NULL_IDS or finding_id == "F-032":
        return "bounded or unresolved null"
    if finding_id in ADJACENT_RESPONSE_IDS:
        return "adjacent comparative, validation, or guidance boundary"
    if finding_id in OFFICIAL_CORRECTION_IDS:
        return "official correction record; endpoint incomplete"
    if finding_id in INSTRUMENT_IDS:
        return "instrument or primary architecture; implementation incomplete"
    if finding_id in METHOD_IDS:
        return "method, source-quality, or measurement boundary"
    if finding_id in DESIGN_IDS:
        return "protective design or remedy component"
    if finding_id in MIXED_IDS:
        return "mixed mechanism, counterevidence, or boundary case"
    return "harm, failure, or capture mechanism case"


def write_crosswalk() -> None:
    ledger = load_rows(LEDGER)
    themes_by_finding = primary_theme_map()
    claims_by_finding = claim_map(themes_by_finding)
    gaps_by_finding = gap_references()
    fieldnames = [
        "finding_id",
        "source_lane",
        "community_or_group",
        "primary_theme_id",
        "primary_theme",
        "synthesis_claim_ids",
        "evidence_role",
        "confidence",
        "external_verification_needed",
        "article_gap_refs",
    ]
    with CROSSWALK.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in ledger:
            finding_id = row["finding_id"]
            theme_id = themes_by_finding[finding_id]
            writer.writerow(
                {
                    "finding_id": finding_id,
                    "source_lane": source_lane(finding_id),
                    "community_or_group": row["community_group"],
                    "primary_theme_id": theme_id,
                    "primary_theme": THEMES[theme_id],
                    "synthesis_claim_ids": ";".join(claims_by_finding[finding_id]),
                    "evidence_role": evidence_role(finding_id),
                    "confidence": row["confidence"],
                    "external_verification_needed": row["external_verification_needed"],
                    "article_gap_refs": ";".join(gaps_by_finding.get(finding_id, [])),
                }
            )


def update_handoffs() -> None:
    text = STATE.read_text(encoding="utf-8")
    report_line = (
        "- `COMMUNITIES-FINAL-SYNTHESIS-REPORT.md` is the corpus-directed final report. It horizontally synthesizes all 186 findings across twelve themes, preserves counterevidence and transfer limits, and keeps the combined subsidiarity architecture explicitly model-assisted rather than source-validated.\n"
    )
    if report_line not in text:
        anchor = (
            "- `COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md` completes the four-record fair-separation, pooled-risk, and planned-fission unit. It separates permission from usable exit, institutional equity from individual entitlement, aggregate parity from consent, court finality from pre-crisis exit, and procedure from later human outcomes.\n"
        )
        assert anchor in text
        text = text.replace(anchor, anchor + report_line, 1)
    boundary = (
        "- The post-corpus horizontal synthesis is complete. Every finding is mapped in `COMMUNITIES-SYNTHESIS-CROSSWALK.csv`; the synthesis adds no evidence rows and does not replace the article-directed gap bank.\n"
    )
    if boundary not in text:
        anchor = (
            "- The four-record fair-separation, pooled-risk, and planned-fission unit is complete. The assigned primary corpus and all five units in the finite adjacent-source roadmap are complete. There is no next research unit in the accepted roadmap.\n"
        )
        assert anchor in text
        text = text.replace(anchor, anchor + boundary, 1)
    picture = (
        "- The final horizontal synthesis identifies one recurring system failure across otherwise different cases: legitimate authority in one domain becomes unreviewable control over other domains, captures the evidence and remedy channels, makes exit costly, and can turn cohesion or survival into a false success signal. The counterdesign is bounded and replaceable authority, direct rights, independent reporting and review, usable exit and fission, and later human-outcome measurement. This assembled architecture is model-assisted; no source validates it as a complete package.\n"
    )
    if picture not in text:
        anchor = "## Current evidence picture\n\n"
        assert anchor in text
        text = text.replace(anchor, anchor + picture, 1)
    text = replace_once_or_confirm(
        text,
        "1. Do not repeat volumes 1-45 or the eight standalone sources; the assigned primary corpus is complete.",
        "1. Start with `COMMUNITIES-FINAL-SYNTHESIS-REPORT.md` and `COMMUNITIES-SYNTHESIS-CROSSWALK.csv`; do not repeat volumes 1-45 or the eight standalone sources.",
        "state synthesis resume step",
    )
    STATE.write_text(text, encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    checkpoint = "- Final cross-corpus synthesis: **complete; all 186 findings mapped**\n"
    if checkpoint not in text:
        anchor = "- Primary assigned corpus: **complete, 984 journal PDFs plus 8 standalone sources**\n"
        assert anchor in text
        text = text.replace(anchor, anchor + checkpoint, 1)
    text = replace_once_or_confirm(
        text,
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The latest source-level account is [`recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md); the completed finite roadmap is [`docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md`](docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md).",
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The corpus-wide conclusion is [`recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`](recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md), with finding-level coverage in [`recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`](recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv). The latest bounded source report remains [`recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md).",
        "README synthesis links",
    )
    layout = (
        "- `recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md` — corpus-directed conclusions, tensions, boundaries, and remaining unknowns\n"
        "- `recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv` — one-row-per-finding map from all 186 findings to synthesis themes, claims, evidence roles, and article gaps\n"
    )
    if layout not in text:
        anchor = "- `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv` — finding-level evidence, source limits, alternative interpretations, outcomes, and verification needs\n"
        assert anchor in text
        text = text.replace(anchor, anchor + layout, 1)
    text = replace_once_or_confirm(
        text,
        "python recovered/test_adjacent_fair_separation_workflow.py\npython recovered/verify_adjacent_fair_separation.py",
        "python recovered/test_final_synthesis_workflow.py\npython recovered/verify_final_synthesis.py",
        "README synthesis validation",
    )
    text = replace_once_or_confirm(
        text,
        "The current verifier checks sequential findings through F-186, the 20-record cumulative adjacent inventory, the four Unit E source dispositions, unchanged gap classes, fair-separation report coverage, finite-roadmap completion, and exclusion of source binaries outside known local-only corpus roots.",
        "The current verifier retains all Unit E checks, locks the evidence ledger and article-gap bank against synthesis-time mutation, requires one crosswalk row for every finding, verifies the twelve-theme and fifteen-claim architecture, confirms the three gap-unreferenced findings are nevertheless synthesized, and checks the final report's epistemic and transfer boundaries.",
        "README synthesis verifier",
    )
    README.write_text(text, encoding="utf-8")

    text = INDEX.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "3. the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`\n4. `../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`\n5. `../recovered/COMMUNITIES-SOURCE-INVENTORY.csv`\n6. `../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`\n7. current discovery, update, test, and verification scripts",
        "3. `../recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`\n4. `../recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`\n5. the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`\n6. `../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`\n7. `../recovered/COMMUNITIES-SOURCE-INVENTORY.csv`\n8. `../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`\n9. current discovery, update, test, and verification scripts",
        "index synthesis read order",
    )
    plan_note = (
        "The corpus-directed synthesis method is recorded in `superpowers/plans/2026-08-15-final-synthesis-pass.md`. The gap bank remains the article-change specification; it is not the final research report.\n\n"
    )
    if plan_note not in text:
        anchor = "The post-corpus queue is finite and recorded in `superpowers/plans/2026-08-15-adjacent-source-roadmap.md`."
        assert anchor in text
        text = text.replace(anchor, plan_note + anchor, 1)
    INDEX.write_text(text, encoding="utf-8")

    text = AGENTS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`python recovered/test_adjacent_fair_separation_workflow.py` (or the current bounded-unit successor)",
        "`python recovered/test_final_synthesis_workflow.py` (or the current bounded-unit successor)",
        "AGENTS synthesis regression",
    )
    text = replace_once_or_confirm(
        text,
        "`python recovered/verify_adjacent_fair_separation.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "`python recovered/verify_final_synthesis.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "AGENTS synthesis verification",
    )
    AGENTS.write_text(text, encoding="utf-8")


def main() -> None:
    assert REPORT.exists(), f"missing synthesis report: {REPORT}"
    write_crosswalk()
    update_handoffs()


if __name__ == "__main__":
    main()
