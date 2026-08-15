#!/usr/bin/env python3
"""Apply the completed volume 45 checkpoint to cumulative research artifacts."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"
AGENTS = REPOSITORY / "AGENTS.md"
REPORT = ROOT / "COMMUNITIES-V45-RESEARCH-REPORT.md"

PROMOTED_IDS = {"M-0119", "M-0120"}
FUNCTIONAL_METADATA_IDS = {"M-0116", "M-0117", "M-0118", "M-0130"}
EXPECTED_VOLUME_IDS = {f"M-{number:04d}" for number in range(116, 131)}

ARCHIVE_RAW_ROW = (
    "D-003,drive_archive,REDACTED,COMMUNAL-SOCIETIES-v41-v45.zip,application/zip,"
    "55770584,COMMUNAL-SOCIETIES-v41-v45.zip,,,,,,,,,,"
    "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c,"
    "not_applicable,not processed,raw/COMMUNAL-SOCIETIES-v41-v45.zip,,"
    "Drive inventory row; archive downloaded and integrity-tested; members follow"
)

NEW_FINDINGS = [
    {
        "finding_id": "F-159",
        "track": "Track A health outcome, work exposure, and housing conditions",
        "source_record_id": "M-0119",
        "source_file": "004-health-and-health-care-in-intentional-communities.pdf",
        "journal_volume_issue_year": "Vol. 45, no. 1 (2025)",
        "article_title": "Health and Health Care in Intentional Communities",
        "author": "Lyman Tower Sargent",
        "community_group": "Shaker societies",
        "page_locator": "PDF p. 4 of article file, duplicated as PDF p. 5; printed p. 4",
        "printed_page_number": "4",
        "supporting_excerpt": "",
        "source_access": "full text; historical synthesis citing John E. Murray's tuberculosis mortality study",
        "evidence_type": "historical mortality, work-exposure, and housing-practice synthesis",
        "exact_factual_observation": "Sargent reports that nineteenth-century Shaker tuberculosis mortality was significantly higher than non-Shaker mortality, that young Shakers working indoors died at a higher rate than those working outdoors, and that Shaker sisters, who mostly worked indoors, died at a much higher rate than brothers, who mostly worked outdoors. He says the difference was most likely related to failure to use established isolation and rest practices: sick Shakers continued working and remained in ordinary dwellings that were generally overcrowded, some extremely so.",
        "what_source_establishes": "At synthesis level, communal medical knowledge coexisted with adverse mortality differences by work setting and gendered work allocation and with reported failure to protect isolation and rest. Health claims need subgroup outcomes, work and housing exposure measures, protected rest and isolation, independent medical access, and an external public-health route.",
        "what_source_does_not_establish": "It does not reproduce Murray's dataset or model, establish individual diagnoses and exposures, separate age, selection, sex, occupation, crowding, ventilation, treatment, and reporting effects, quantify each mechanism, or show that every Shaker family or community followed the same practice. The page itself notes conflicting ventilation evidence.",
        "author_interpretation": "Sargent treats the mortality differences as evidence of the complexity of communal health care and says the most likely explanation was continued work and ordinary overcrowded housing rather than established isolation and rest.",
        "alternative_interpretation": "Population selection, age structure, sex-specific exposure, diagnostic practice, community differences, and other unmeasured conditions may explain part of the mortality pattern; recorded indoor work may proxy for several exposures rather than identify a single cause.",
        "response_process": "Tuberculosis illness; continued work rather than protected rest; residence in ordinary often overcrowded dwellings rather than systematic isolation; differential mortality reported across Shakers and non-Shakers, indoor and outdoor workers, and sisters and brothers. No internal review or correction sequence is described.",
        "outcome": "The cited evidence reports higher Shaker mortality and higher mortality among indoor workers and sisters. It does not report a later policy correction, recurrence trend, or community-by-community outcome.",
        "transferability": "High for separating community-care reputation from subgroup health outcomes and for protecting independent medical judgment, rest, isolation, ventilation, occupancy limits, and occupational exposure review. Medium for causal claims until the underlying data and alternative explanations are checked.",
        "article_gap_status": "C",
        "likely_article_destination": "Community as therapist / medicine / outcome dashboard / site capacity",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "Inspect Murray's data and methods, Shaker population and work records, housing and ventilation records, diagnostic practice, treatment and isolation rules, and competing demographic explanations before assigning causal shares. The source PDF duplicates this printed spread on consecutive physical pages.",
    },
    {
        "finding_id": "F-160",
        "track": "Track B pooled catastrophic-health reserve",
        "source_record_id": "M-0119",
        "source_file": "004-health-and-health-care-in-intentional-communities.pdf",
        "journal_volume_issue_year": "Vol. 45, no. 1 (2025)",
        "article_title": "Health and Health Care in Intentional Communities",
        "author": "Lyman Tower Sargent",
        "community_group": "Fellowship of Egalitarian Communities; PEACH",
        "page_locator": "PDF p. 10 of article file, duplicated as PDF p. 11; printed p. 9, note 27",
        "printed_page_number": "9",
        "supporting_excerpt": "",
        "source_access": "full text; footnote synthesis of reports by Kat Kinkade and Laird Schaub",
        "evidence_type": "historical cross-community catastrophic-health fund rules and claimed outcome",
        "exact_factual_observation": "Sargent's note describes PEACH, a Fellowship of Egalitarian Communities fund. Communities initially paid $10 per member per month, later $12.50 and then $15. The fund began helping after $5,000 per incident, paid 90 percent of a covered expense, never paid more than half of the fund, and imposed a two-year wait for a new member's full coverage. A cited 2009 account said that after 23 years PEACH held more than $500,000 and had paid every submitted claim in full. Sargent says he could not determine the current situation.",
        "what_source_establishes": "At historical synthesis level, a federation used an explicit contribution rule, attachment threshold, coinsurance rate, reserve cap, waiting period, and contribution adjustment, with a cited long-run asset and payment claim. A pooled reserve can make catastrophic-health risk allocation and preservation rules visible across communities.",
        "what_source_does_not_establish": "It does not establish PEACH's current operation or legal status, supply governing documents or audited accounts, define covered and excluded expenses completely, report enrollment, incidents, denials, delays, hardship, risk selection, or claim denominators, or compare the fund with alternatives. Paying every submitted claim does not show that every need was submitted or covered.",
        "author_interpretation": "Sargent presents PEACH as one way intentional communities shared medical risk and explicitly states that he could not determine its current status.",
        "alternative_interpretation": "The reported payment record may reflect narrow coverage, few claims, selection, informal supplementation, or publication bias as well as sound reserve design; the two-year wait may preserve solvency while creating a protection gap for new members.",
        "response_process": "Per-member contributions; an incident-level attachment point; payment of 90 percent of covered expense subject to a half-fund reserve cap; two-year vesting for full coverage; contribution increases; cited accumulation and claim payment. No denial, appeal, audit, portability, or current-status process is reported.",
        "outcome": "A cited 2009 account reported assets above $500,000 after 23 years and full payment of every claim presented. The source supplies no audit, later outcome, current balance, or claimant-level result.",
        "transferability": "High for explicitly specifying contributions, attachment, coinsurance, reserve protection, vesting, adjustments, audited claims and denials, hardship and appeal, and current-status review. Medium for treating PEACH itself as a validated or current model until records are checked.",
        "article_gap_status": "B",
        "likely_article_destination": "Medicine / money and land / external couplings / site capacity",
        "confidence": "medium",
        "external_verification_needed": "yes",
        "notes": "Retrieve the cited Kinkade and Schaub articles, PEACH governing documents, contribution and claim records, audits, coverage definitions, denial and appeal records, current legal status, and member accounts. The source PDF duplicates this printed spread on consecutive physical pages.",
    },
    {
        "finding_id": "F-161",
        "track": "Track B planned colony fission and continuity",
        "source_record_id": "M-0120",
        "source_file": "005-from-cloistered-courts-to-prairie-colonies-five-centuries-of-hutterite-communal-architecture.pdf",
        "journal_volume_issue_year": "Vol. 45, no. 1 (2025)",
        "article_title": "From Cloistered Courts to Prairie Colonies: Five Centuries of Hutterite Communal Architecture",
        "author": "Sibylle Becker-Kilian",
        "community_group": "Hutterite colonies; James Valley and Starlite",
        "page_locator": "PDF p. 36 of article file, duplicated as PDF p. 37; printed pp. 59-60",
        "printed_page_number": "59-60",
        "supporting_excerpt": "",
        "source_access": "full text; historical and architectural synthesis with cited studies and personal observation",
        "evidence_type": "planned population-threshold fission, member and asset division, and parity-renovation process",
        "exact_factual_observation": "Becker-Kilian reports that Hutterite colonies typically begin a structured division at about 120 to 150 people. Forming a daughter colony can take years. At completion, human and material assets are divided as equitably as possible, approximately half the members relocate, and mother and daughter operate as separate self-sustaining financial entities responsible for their own expenses, debts, and loans. After a daughter colony opens with modern facilities, the older mother colony enters renovation intended to reduce disparities in living conditions, although rising costs can constrain the work.",
        "what_source_establishes": "A community tradition used a population trigger, multiyear capital preparation, planned member and material-asset division, independent post-split finances, and a parity-oriented renovation obligation to the originating colony. Fission can be treated as continuity infrastructure rather than an improvised response after conflict or collapse.",
        "what_source_does_not_establish": "It does not provide individual consent and dissent procedures, decision thresholds, member-selection rules, valuation or debt formulas, legal instruments, conflict and appeal records, equality for each person, completion rates, comparative post-split outcomes, or proof that every Hutterite branch follows the same process.",
        "author_interpretation": "Becker-Kilian links division to administrative and social challenges and surplus labor at larger scale and says mother-colony renewal supports morale and continuity while acknowledging rising-cost constraints.",
        "alternative_interpretation": "The threshold may encode religious tradition, household structure, land and labor economics, or governance convenience rather than a universal scale limit; an approximately equal aggregate split may still constrain individual choice or distribute valued assets and debt unevenly.",
        "response_process": "Population approaches a customary threshold; years of capital accumulation and site planning; municipal and neighbor constraints; daughter-colony construction; approximately equal member and asset division; independent finances; later renovation at the mother colony to reduce disparity.",
        "outcome": "Mother and daughter colonies become separate financial entities and the older colony is described as entering a parity-oriented renovation period. The article supplies no systematic comparative outcome, dissent record, or long-term financial and member-wellbeing follow-up.",
        "transferability": "High for predefining scale triggers, preparation runway, voluntary and fair member allocation, transparent asset and debt division, independent successor finances, and parity review after a fork. Medium for direct transfer because Hutterite demography, law, religion, and property practice are specific.",
        "article_gap_status": "B",
        "likely_article_destination": "Forks are the immune system / money and land / site capacity / outcome dashboard",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "Inspect colony agreements, member and asset lists, valuation and debt records, decision and dissent procedures, municipal records, renovation accounts, and comparative later outcomes. The source PDF duplicates this printed spread on consecutive physical pages.",
    },
    {
        "finding_id": "F-162",
        "track": "Track A child negative result",
        "source_record_id": "",
        "source_file": "Volume 45 discovery corpus",
        "journal_volume_issue_year": "Volume 45 (2025)",
        "article_title": "Cumulative targeted search and issue-by-issue discovery scan",
        "author": "Research checkpoint",
        "community_group": "Communal Societies volume 45",
        "page_locator": "15 PDFs; 11 substantive close reads; 4 child-danger proximity candidates",
        "printed_page_number": "",
        "supporting_excerpt": "",
        "source_access": "full extracted corpus",
        "evidence_type": "systematic bounded search result",
        "exact_factual_observation": "Across all 15 PDFs, complete title triage, locked six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 11 substantive close reads produced four proximity candidates. They concerned parents' remembered fear of childhood polio near discussion of adult mental-health admission, state school and language policy described as a cultural threat, survivor accounts of harmful religious organizations, and fictional girls, sexism, spanking threats, and sexual conduct. No intentional-community source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        "what_source_establishes": "The specified dangerous-child evidence pattern is absent from volume 45 under the recorded search, proximity, exclusion, and close-read procedure. The current inventory's journal stream is now complete through volume 45.",
        "what_source_does_not_establish": "It does not prove that no such case exists in the eight standalone sources, the books and media reviewed in volume 45, different terminology, unpublished or protected records, juvenile, educational, medical, disability, family, or animal-welfare systems, other journals, or communities outside the corpus.",
        "author_interpretation": "Not applicable.",
        "alternative_interpretation": "Privacy, euphemism, aggregate reporting, review-level compression, source destruction, and routing into professional, family, juvenile, educational, disability, animal-welfare, or medical systems may hide relevant cases from a communal-history journal.",
        "response_process": "Not applicable.",
        "outcome": "Bounded null for volume 45 and completion of the current 984-PDF journal stream; the standalone evidence stream remains open.",
        "transferability": "High for this completed journal unit and cumulative journal boundary; none for the full literature until standalone and adjacent sources are processed.",
        "article_gap_status": "F",
        "likely_article_destination": "Research/school function / dangerous-child branch",
        "confidence": "high",
        "external_verification_needed": "no",
        "notes": "The cumulative bounded null now covers volumes 1-45. Adult mental-health admission, childhood disease, cultural threats to schooling, survivor accounts, and fictional gender or sexual material were excluded from the child-as-dangerous-actor result.",
    },
]


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old in text:
        return text.replace(old, new, 1)
    raise AssertionError(f"missing update anchor: {label}")


def append_sentence_once(text: str, sentence: str, addition: str) -> str:
    combined = sentence + addition
    if combined in text:
        return text
    assert sentence in text, f"missing sentence anchor: {sentence[:60]}"
    return text.replace(sentence, combined, 1)


def ensure_ledger_findings() -> None:
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    assert [row["finding_id"] for row in rows] == [
        f"F-{number:03d}" for number in range(1, len(rows) + 1)
    ]
    assert all(set(finding) == set(fieldnames) for finding in NEW_FINDINGS)

    if len(rows) == 158:
        assert rows[-1]["finding_id"] == "F-158"
        with LEDGER.open("a", newline="", encoding="utf-8") as handle:
            csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n").writerows(
                NEW_FINDINGS
            )
    else:
        assert len(rows) == 162
        assert rows[-4:] == NEW_FINDINGS


def update_inventory() -> None:
    raw_before = INVENTORY.read_text(encoding="utf-8-sig")
    assert raw_before.splitlines().count(ARCHIVE_RAW_ROW) == 1

    with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None

    seen: set[str] = set()
    dispositions: Counter[str] = Counter()
    for row in rows:
        if row["drive_file_id"]:
            row["drive_file_id"] = "REDACTED"
        if row["record_type"] != "archive_pdf" or row["volume"] != "45":
            continue
        record_id = row["record_id"]
        seen.add(record_id)
        if record_id in PROMOTED_IDS:
            row["research_status"] = "close read; finding promoted"
            dispositions["promoted"] += 1
        elif record_id in FUNCTIONAL_METADATA_IDS:
            row["research_status"] = "metadata triaged"
            dispositions["metadata"] += 1
        else:
            row["research_status"] = "contextual close read; no distinct finding"
            dispositions["contextual"] += 1
        relative = Path(row["internal_filename"]).relative_to("archive")
        row["text_extraction_status"] = "extracted"
        row["local_path"] = f"recovered/corpus-v45/{relative.as_posix()}"
        row["text_path"] = f"recovered/corpus-v45/{relative.with_suffix('.txt').as_posix()}"

    assert seen == EXPECTED_VOLUME_IDS
    assert dispositions == Counter({"contextual": 9, "metadata": 4, "promoted": 2})

    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    raw_after = INVENTORY.read_text(encoding="utf-8-sig")
    assert raw_after.splitlines().count(ARCHIVE_RAW_ROW) == 1, "D-003 row changed byte-for-byte"


GAP_ADDITIONS = {
    "G-002": (
        " Community provision also needs an occupational and public-health firewall: independent medical judgment, protected rest and isolation, exposure controls, and subgroup outcome review must override work or housing custom when needed.",
        ["F-159"],
    ),
    "G-005": (
        " Independent medical access includes protected rest and isolation when clinically indicated. A pooled health reserve also needs transparent eligibility, denial, hardship, and appeal rules so vesting or solvency controls do not silently erase care.",
        ["F-159", "F-160"],
    ),
    "G-006": (
        " Report health outcomes by subgroup, work exposure, housing and care practice rather than treating communal expertise as an outcome. For pooled health funds, report claims, denials, delay, hardship, reserves, portability, and later status; for a planned fork, report consent, allocation, debt, parity, and both successors' later outcomes.",
        ["F-159", "F-160", "F-161"],
    ),
    "G-012": (
        " A pooled catastrophic-health reserve needs visible contributions, attachment and payout rules, a protected reserve, audited claims and denials, vesting safeguards, portability, and an appeal route. A planned fission needs transparent member choice and valuation, fair asset and debt division, independent accounts, and parity review after the split.",
        ["F-160", "F-161"],
    ),
    "G-013": (
        " The external map must preserve independent medical and public-health authority over work, isolation, occupancy, and exposure decisions, and verify whether a pooled health fund is legally and operationally current rather than inferring protection from a historical payment claim.",
        ["F-159", "F-160"],
    ),
    "G-015": (
        " Health capacity includes protected sick leave, isolation space, ventilation, occupancy, occupational exposure controls, and subgroup monitoring. Fork capacity includes a demographic trigger, years of capital runway, a feasible site, transparent debt and asset allocation, and resources to prevent the originating community from becoming the neglected half.",
        ["F-159", "F-160", "F-161"],
    ),
    "G-016": (
        " A fork can be prepared before rupture: define a scale trigger, multiyear runway, member choice, equitable people-and-asset division, independent successor finances, and a parity obligation to the originating community.",
        ["F-161"],
    ),
    "G-018": (
        " Volume 45 again found neither validation of the filter nor a complete dangerous-child actor response sequence; communal medical expertise, survival, publisher selection, survivor testimony, and fictional gender or harm language were not validated danger filters or complete child-response evidence.",
        ["F-159", "F-160", "F-161", "F-162"],
    ),
}


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-44",
        "Checkpoint: *Communal Societies* volumes 1-45",
        "gap completed boundary",
    )
    text = replace_once_or_confirm(
        text,
        "After reconciling the volume 44 findings rather than inflating the list",
        "After reconciling the volume 45 findings rather than inflating the list",
        "gap checkpoint description",
    )
    text = replace_once_or_confirm(
        text,
        "No processed journal evidence through volume 44 validates six months of inner work as a reliable con-artist filter.",
        "No processed journal evidence through volume 45 validates six months of inner work as a reliable con-artist filter.",
        "G-018 cumulative boundary",
    )

    updated_lines: list[str] = []
    for line in text.splitlines():
        if not line.startswith("| G-"):
            updated_lines.append(line)
            continue
        cells = line.split("|")
        gap_id = cells[1].strip()
        if gap_id not in GAP_ADDITIONS:
            updated_lines.append(line)
            continue
        addition, finding_ids = GAP_ADDITIONS[gap_id]
        if addition.strip() not in cells[4]:
            cells[4] = cells[4].rstrip() + addition + " "
        evidence = cells[7].strip()
        existing = [part.strip() for part in evidence.split(",") if part.strip()]
        for finding_id in finding_ids:
            if finding_id not in existing:
                existing.append(finding_id)
        cells[7] = " " + ", ".join(existing) + " "
        updated_lines.append("|".join(cells))
    text = "\n".join(updated_lines) + "\n"

    old_sequence = (
        "The volume 1-44 dangerous-child searches (F-031, F-048, F-064, F-076, "
        "F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, "
        "F-138, F-142, F-146, F-148, F-151, F-154, F-158) are bounded negative results"
    )
    new_sequence = (
        "The volume 1-45 dangerous-child searches (F-031, F-048, F-064, F-076, "
        "F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, "
        "F-138, F-142, F-146, F-148, F-151, F-154, F-158, F-162) are bounded negative results"
    )
    text = replace_once_or_confirm(text, old_sequence, new_sequence, "bounded child sequence")

    verification_anchor = (
        "- **F status:** verify Metcalf's 1982 agency intake, later conviction and charging records, investigative status, survivor accounts, and Gloriavale's response; preserve the distinction between his direct visit/report account and his review of Pratt, and do not repeat diagnostic labels."
    )
    verification_addition = "\n" + "\n".join([
        "- **F status:** inspect Murray's tuberculosis data and methods, Shaker population and work records, housing and ventilation conditions, diagnostic practice, and competing explanations before assigning causal shares to continued work, failed isolation, or overcrowding.",
        "- **F status:** retrieve PEACH's governing documents, contribution and claim records, audits, coverage and exclusion rules, denials, appeals, member accounts, and current legal and operational status before presenting it as a validated or current health-finance model.",
        "- **F status:** inspect Hutterite colony agreements, member and asset lists, valuation and debt records, decision and dissent procedures, renovation accounts, and comparative later outcomes before treating the described fission process as universal or individually equitable.",
    ])
    text = append_sentence_once(text, verification_anchor, verification_addition)

    final_anchor = "- The remaining volume 44 records are functional metadata and supply no further distinct response mechanism or outcome."
    final_addition = "\n" + "\n".join([
        "- F-159 preserves Sargent's synthesis-level attribution and conflicting ventilation evidence; it does not infer individual causation or treat communal medical knowledge as proof of safety.",
        "- F-160 preserves the historical, secondary, and current-status-unknown limits of the PEACH account; the claimed full-payment record is not an audit or proof that every need was covered.",
        "- F-161 does not convert an approximately equal aggregate division into proof of individual consent or fairness and does not generalize one described Hutterite process to every colony or modern community.",
        "- The remaining volume 45 reviews provide media, category, archive, survivor-source, succession, belief, material-culture, or fiction context without a further materially distinct response mechanism and later outcome.",
        "- The four volume 45 child-danger candidates concern childhood disease, state schooling policy, survivor accounts of adult organizations, and fictional girls or harm language—not a persistently dangerous child actor with assessment, intervention, review, and later outcome.",
        "- The remaining volume 45 records are functional metadata and supply no further distinct response mechanism or outcome.",
    ])
    text = append_sentence_once(text, final_anchor, final_addition)

    gap_lines = [line for line in text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter(
        {"B": 8, "C": 7, "D": 3}
    )
    references = set(re.findall(r"\bF-\d{3}\b", text))
    assert references <= {f"F-{number:03d}" for number in range(1, 163)}
    for finding_id in ("F-159", "F-160", "F-161", "F-162"):
        assert finding_id in text
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = [
        ("volumes **1-44**", "volumes **1-45**", "state completed boundary"),
        (
            "**969 journal PDFs** were triaged: 432 close-read as relevant or contextual, 207 title/keyword-triaged, and 330 metadata-triaged.",
            "**984 journal PDFs** were triaged: 443 close-read as relevant or contextual, 207 title/keyword-triaged, and 334 metadata-triaged.",
            "state counts",
        ),
        (
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **158 findings** (`F-001` through `F-158`). Volume 44 added four findings: three C and one F-status bounded negative.",
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **162 findings** (`F-001` through `F-162`). Volume 45 added four findings: two B, one C, and one F-status bounded negative.",
            "state findings",
        ),
        (
            "`COMMUNITIES-V44-RESEARCH-REPORT.md` records the completed 33-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "`COMMUNITIES-V45-RESEARCH-REPORT.md` records the completed 15-PDF boundary, close-read disposition, discovery and child-search method, cautions, and completion of the current journal stream.",
            "state report",
        ),
        (
            "All 984 journal PDFs have extracted text. Every one of the 33 volume 44 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `COMMUNAL-SOCIETIES-v41-v45.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
            "All 984 journal PDFs have extracted text. The Google Drive `vol41-45.zip` object matched the saved D-003 size and SHA-256 exactly, passed a ZIP integrity test, and supplied all 15 volume 45 PDFs. Each volume 45 member matched both the archive manifest and its pre-existing inventory SHA-256, matched its inventoried page count, and has nonempty extracted text. The source container and full text remain outside Git.",
            "state corpus verification",
        ),
        (
            "Volume 44 adds: a child-centered stop rule for placement programs whose institutional-succession purpose fails; independent court and professional routes around therapist-controlled family separation; inclusive external intake for credible disclosed harm; and another bounded dangerous-child null.",
            "Volume 45 adds: subgroup health outcomes and exposure controls that override communal-care reputation; explicit pooled catastrophic-health reserve rules with current-status and audit limits; planned fission with a scale trigger, fair member and asset division, independent successor finances, and mother-colony parity review; and the final journal-volume dangerous-child bounded null.",
            "state evidence summary",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)

    pending = re.compile(r"## Exact pending boundary\n\n.*?\n## Current evidence picture", re.DOTALL)
    pending_new = """## Exact pending boundary

- The current journal stream is complete: **984 of 984 journal PDFs** across volumes 1-45 have been triaged, with no journal PDFs remaining.
- Eight standalone Drive sources are inventoried but not yet represented by durable local text or close-read findings:
  1. *The Riddle of Amish Culture* (EPUB)
  2. *Alienation and Charisma*
  3. *Commitment and Community*
  4. *The Mountain People*
  5. *The !Kung San*
  6. Richard Wrangham, “Targeted conspiratorial killing, human self-domestication and the evolution of groupishness”
  7. `Zarpentinedissertation.pdf`
  8. *Evil Genes*
- The downloaded ZIPs are source containers, not additional substantive documents.

## Current evidence picture"""
    text, count = pending.subn(pending_new, text, count=1)
    assert count == 1 or pending_new in text

    resume = re.compile(r"## Resume procedure\n\n.*?\n## Stop conditions", re.DOTALL)
    resume_new = """## Resume procedure

1. Do not repeat volumes 1-45; the current journal stream is complete.
2. Recover the eight standalone sources and record source access, hashes, extraction state, and provenance without folding them into the 984-PDF journal count.
3. Run title and keyword discovery, process-family screening, and the separate dangerous-child actor search across the recovered standalone texts.
4. Close-read every source that may bear on admission, predation, violence, discipline, expulsion, ostracism, schism, grievance, child conduct, child protection, leader capture, dissent, reintegration, outside intervention, or outcome.
5. Append only materially distinct findings and preserve source access, what the source does not establish, alternative interpretation, process, outcome, transferability, and verification needs.
6. Reconcile findings into the existing 18-item gap bank; do not create a new gap merely for corroboration.
7. Keep traditional-society, clinical, legal, and intentional-community evidence separate until a transfer argument is made.
8. After each bounded standalone unit, update this state file before further work.

## Stop conditions"""
    text, count = resume.subn(resume_new, text, count=1)
    assert count == 1 or resume_new in text
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = [
        ("Volumes **1-44** complete", "Volumes **1-45** complete", "README boundary"),
        ("**969** journal PDFs triaged", "**984** journal PDFs triaged", "README total"),
        ("**432** relevant or contextual close reads", "**443** relevant or contextual close reads", "README close reads"),
        ("**158** evidence findings (`F-001` through `F-158`)", "**162** evidence findings (`F-001` through `F-162`)", "README findings"),
        ("Next unit: **volume 45, 15 PDFs** (all in issue 1)", "Journal stream: **complete, 984 of 984 PDFs**; eight standalone sources remain separate", "README next unit"),
        ("recovered/COMMUNITIES-V44-RESEARCH-REPORT.md", "recovered/COMMUNITIES-V45-RESEARCH-REPORT.md", "README latest report"),
        ("](recovered/COMMUNITIES-V44-RESEARCH-REPORT.md)", "](recovered/COMMUNITIES-V45-RESEARCH-REPORT.md)", "README latest report link target"),
        ("recovered/corpus-v44/", "recovered/corpus-v45/", "README corpus"),
        ("python recovered/test_v44_workflow.py", "python recovered/test_v45_workflow.py", "README tests"),
        ("python recovered/verify_v44.py", "python recovered/verify_v45.py", "README verifier"),
        (
            "The verifier checks all 33 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-45 boundary.",
            "The verifier checks all 15 PDF hashes, page counts, and text extractions, the optional local source-container hash and ZIP integrity, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and completion of the 984-PDF journal boundary.",
            "README verification scope",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    README.write_text(text, encoding="utf-8")


def update_agents() -> None:
    text = AGENTS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "python recovered/test_v44_workflow.py",
        "python recovered/test_v45_workflow.py",
        "AGENTS regression command",
    )
    text = replace_once_or_confirm(
        text,
        "python recovered/verify_v44.py",
        "python recovered/verify_v45.py",
        "AGENTS verifier command",
    )
    AGENTS.write_text(text, encoding="utf-8")


def validate_checkpoint() -> None:
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        ledger_rows = list(csv.DictReader(handle))
    assert [row["finding_id"] for row in ledger_rows] == [
        f"F-{number:03d}" for number in range(1, 163)
    ]
    assert ledger_rows[-4:] == NEW_FINDINGS
    assert [row["source_record_id"] for row in ledger_rows[-4:]] == [
        "M-0119", "M-0119", "M-0120", ""
    ]
    assert Counter(row["article_gap_status"] for row in ledger_rows[-4:]) == Counter(
        {"B": 2, "C": 1, "F": 1}
    )
    assert all(row["supporting_excerpt"] == "" for row in ledger_rows[-4:])
    report = REPORT.read_text(encoding="utf-8")
    assert "**4 new findings, F-159 through F-162**" in report


def main() -> None:
    ensure_ledger_findings()
    update_inventory()
    update_gap_bank()
    update_state()
    update_readme()
    update_agents()
    validate_checkpoint()
    print("updated volume 45 checkpoint")


if __name__ == "__main__":
    main()
