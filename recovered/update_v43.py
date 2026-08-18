#!/usr/bin/env python3
"""Apply the completed volume 43 checkpoint to cumulative research artifacts."""

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
REPORT = ROOT / "COMMUNITIES-V43-RESEARCH-REPORT.md"

PROMOTED_IDS = {"M-0070", "M-0075"}
FUNCTIONAL_METADATA_IDS = {
    "M-0046",
    "M-0047",
    "M-0048",
    "M-0065",
    "M-0066",
    "M-0067",
    "M-0081",
    "M-0082",
}
ARCHIVE_RECORD_ID = "D-003"
ARCHIVE_EXPECTED = {
    "drive_size_bytes": "55770584",
    "sha256": "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c",
    "research_status": "not processed",
    "local_path": "raw/COMMUNAL-SOCIETIES-v41-v45.zip",
    "notes": "Drive inventory row; archive downloaded and integrity-tested; members follow",
}
ARCHIVE_RAW_ROW = (
    "D-003,drive_archive,REDACTED,COMMUNAL-SOCIETIES-v41-v45.zip,application/zip,"
    "55770584,COMMUNAL-SOCIETIES-v41-v45.zip,,,,,,,,,,"
    "e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c,"
    "not_applicable,not processed,raw/COMMUNAL-SOCIETIES-v41-v45.zip,,"
    "Drive inventory row; archive downloaded and integrity-tested; members follow"
)

NEW_FINDINGS = [
    {
        "finding_id": "F-152",
        "track": "Track A child-policy dissent and nonimplementation",
        "source_record_id": "M-0070",
        "source_file": "005-living-in-disharmony-women-s-experiences-of-gendered-progress-and-failure-in-new-harmony-indiana-1824-1827.pdf",
        "journal_volume_issue_year": "Vol. 43, no. 2 (2023)",
        "article_title": "Living in Disharmony: Women's Experiences of Gendered Progress and Failure in New Harmony, Indiana, 1824-1827",
        "author": "Olivia Krall",
        "community_group": "New Harmony",
        "page_locator": "PDF p. 13 of article file; printed pp. 37-38",
        "printed_page_number": "37-38",
        "supporting_excerpt": "",
        "source_access": "full text; historical article using letters newspapers speeches and secondary scholarship",
        "evidence_type": "historical policy and dissent reconstruction",
        "exact_factual_observation": "Krall reports that New Harmony proposed removing children aged fourteen and older from their homes to communal boarding houses. Sarah Pears objected in a March 1826 letter to loss of parental care and household support; the article also records her labor complaints and her family's 1826 departure. Krall states that women's protests meant the child-removal plan was never implemented.",
        "what_source_establishes": "Affected women could oppose an announced communal child-placement policy, and the article reports nonimplementation rather than treating the proposal as completed practice. Protected objection, family contact, and a recorded implementation status belong in child-governance design.",
        "what_source_does_not_establish": "It does not reconstruct a formal proposal text, meeting, vote, decision maker, protest roster, children's own views, or independent causal test; it does not show that protest was the sole reason the plan ended or that Pears's departure itself caused the result.",
        "author_interpretation": "Krall argues that women exercised agency inside a system that undervalued their labor and that their protests prevented this proposed removal of older children from their homes.",
        "alternative_interpretation": "The plan may also have lapsed because of administrative weakness, financial or educational limits, the wider collapse of the experiment, or resistance not preserved in the cited record; Pears's objection mixed family attachment with loss of children's domestic labor.",
        "response_process": "Policy proposal; affected mother's written objection amid wider women's complaints; family departure; broader protests; reported nonimplementation.",
        "outcome": "The proposed boarding-house removal was reportedly never implemented; the Pears family returned to Philadelphia in 1826. The article records no formal repeal instrument or child follow-up.",
        "transferability": "High for notice, independent child and family representation, protected collective objection, preservation of family contact, credible exit, decision records, and implementation audits before compulsory communal child placement.",
        "article_gap_status": "C",
        "likely_article_destination": "Children section / protected dissent and family-bond safeguards",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "Inspect the Pears letters, New Harmony minutes, boarding plans, newspapers, family records, and other participant accounts before presenting a formal policy or causal precedent. DOI: https://doi.org/10.9707/0739-1250.1024",
    },
    {
        "finding_id": "F-153",
        "track": "Track A rule-averse admission and exit failure",
        "source_record_id": "M-0075",
        "source_file": "010-review-of-commune-chasing-a-utopian-dream-in-aotearoa.pdf",
        "journal_volume_issue_year": "Vol. 43, no. 2 (2023)",
        "article_title": "Review of Commune: Chasing a Utopian Dream in Aotearoa",
        "author": "William J. Metcalf",
        "community_group": "Graham Downs; Renaissance Community Trust",
        "page_locator": "PDF pp. 3 and 5 of review file; printed pp. 67-69",
        "printed_page_number": "67-69",
        "supporting_excerpt": "",
        "source_access": "full text; book review of a participant-scholar history",
        "evidence_type": "review-level autobiographical governance history",
        "exact_factual_observation": "Metcalf reports that Graham Downs resisted membership and governance structure in the name of anarchism and had little ability or willingness to refuse arrivals. The review attributes work refusal, drug and alcohol abuse, police attention, and some violence to later conditions; says founders felt unable to protect communal life; says trust ownership left some unhappy early members with nothing to sell; reports decline to six residents; and notes a later trustee-board takeover intended to change the laissez-faire culture.",
        "what_source_establishes": "At review level, the case connects open admission and rule resistance with disabled protection and exit, and it records a structural intervention—a new trustee board—while making clear that no repair outcome had yet been shown.",
        "what_source_does_not_establish": "It does not independently verify individual conduct, diagnoses, legal status, prevalence, incident chronology, police findings, trust obligations, valuation rights, board authority, current conditions, or whether the takeover improved safety or communal life.",
        "author_interpretation": "Metcalf accepts Jones's account that the community's anarchistic resistance to rules and control prevented it from protecting itself and contributed to its transformation from intentional community into a poor, dispersed rural neighborhood.",
        "alternative_interpretation": "Resource scarcity, poverty, land and housing limits, external stigma, ordinary lifecycle change, selection in a participant memoir, or trust design may explain part of the decline; open residence and support for homeless people are not themselves evidence of danger.",
        "response_process": "Open admission and informal governance; inability or unwillingness to refuse or regulate arrivals; increasing conflict and fragmentation into private homes; constrained exit under trust ownership; decline; later trustee-board takeover with a stated reform aim.",
        "outcome": "The review reports six residents and little communal activity, with some residents poor and unhappy. A new board took control, but the reviewer states only hope for renewal and supplies no evaluated later outcome.",
        "transferability": "High for conduct-specific admission and separation rules, protected emergency authority, neutral review, member-equity and exit terms, trustee accountability, and post-reform outcome checks; low for inferring danger from poverty, homelessness, substance use, mental-health labels, or anarchist identity.",
        "article_gap_status": "C",
        "likely_article_destination": "Membership pipeline / governance safeguards / usable exit",
        "confidence": "medium",
        "external_verification_needed": "yes",
        "notes": "Do not repeat the review's mental-health labels as diagnoses. Inspect Jones's book, the Renaissance trust deed, membership and trustee records, incident and police records, finances, resident and neighbor accounts, and later board actions. DOI: https://doi.org/10.9707/0739-1250.1029",
    },
    {
        "finding_id": "F-154",
        "track": "Track A child negative result",
        "source_record_id": "",
        "source_file": "Volume 43 discovery corpus",
        "journal_volume_issue_year": "Volume 43 (2023)",
        "article_title": "Cumulative targeted search and issue-by-issue discovery scan",
        "author": "Research checkpoint",
        "community_group": "Communal Societies volume 43",
        "page_locator": "37 PDFs; 29 substantive close reads; 10 child-danger proximity candidates",
        "printed_page_number": "",
        "supporting_excerpt": "",
        "source_access": "full extracted corpus",
        "evidence_type": "systematic bounded search result",
        "exact_factual_observation": "Across all 37 PDFs, complete title triage, locked six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 29 substantive close reads found children or young people as policy subjects, dependents, students, orphans, alleged victims, family members, biographical subjects, and participants in an adjacent school program. No intentional-community source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        "what_source_establishes": "The specified dangerous-child evidence pattern is absent from volume 43 under the recorded search, proximity, exclusion, and close-read procedure. Brown's adjacent school program is retained as a verification lead rather than converted into a responsive community case.",
        "what_source_does_not_establish": "It does not prove that no such case exists in volumes 44-45, standalone or book-length sources, Brown's dissertation, different terminology, unpublished or protected records, juvenile, educational, medical, disability, or family systems, or communities outside the journal.",
        "author_interpretation": "Not applicable.",
        "alternative_interpretation": "Privacy, euphemism, aggregate reporting, source destruction, review-level compression, and routing into professional, family, juvenile, educational, disability, or medical systems may hide relevant cases from a communal-history journal.",
        "response_process": "Not applicable.",
        "outcome": "Bounded null for volume 43; adjacent violent-student program flagged for dissertation-level verification.",
        "transferability": "High for this completed unit; none for the full literature until the remaining journal and standalone sources are processed.",
        "article_gap_status": "F",
        "likely_article_destination": "Research/school function / dangerous-child branch",
        "confidence": "high",
        "external_verification_needed": "no",
        "notes": "The cumulative bounded null now covers volumes 1-43. Children harmed, governed, educated, housed, represented, or described biographically were excluded from the child-as-dangerous-actor result; the adjacent school program lacks the required process and setting.",
    },
]


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    """Replace an old checkpoint anchor or confirm the new one is already present."""
    if new in text:
        return text
    if old in text:
        return text.replace(old, new, 1)
    raise AssertionError(f"missing update anchor: {label}")


def extend_once_or_confirm(text: str, anchor: str, addition: str, label: str) -> str:
    """Append to a unique prose anchor once while remaining idempotent."""
    new = anchor + addition
    if new in text:
        return text
    assert anchor in text, f"missing extension anchor: {label}"
    return text.replace(anchor, new, 1)


def ensure_ledger_findings() -> None:
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    assert [row["finding_id"] for row in rows] == [
        f"F-{number:03d}" for number in range(1, len(rows) + 1)
    ]

    if len(rows) == 151:
        assert rows[-1]["finding_id"] == "F-151"
        assert all(set(finding) == set(fieldnames) for finding in NEW_FINDINGS)
        # Preserve every prior finding byte-for-byte; only append the new checkpoint.
        with LEDGER.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writerows(NEW_FINDINGS)
    else:
        assert len(rows) == 154
        assert rows[-3:] == NEW_FINDINGS


def validate_reconciled_evidence() -> None:
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["finding_id"] for row in rows] == [
        f"F-{number:03d}" for number in range(1, 155)
    ]
    assert [row["source_record_id"] for row in rows[-3:]] == ["M-0070", "M-0075", ""]
    assert Counter(row["article_gap_status"] for row in rows[-3:]) == Counter({"C": 2, "F": 1})
    assert all(row["supporting_excerpt"] == "" for row in rows[-3:])
    assert REPORT.is_file()
    report = REPORT.read_text(encoding="utf-8")
    assert "**3 new findings, F-152 through F-154**" in report


def update_inventory() -> None:
    raw_before = INVENTORY.read_text(encoding="utf-8-sig")
    assert raw_before.splitlines().count(ARCHIVE_RAW_ROW) == 1

    with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None

    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed before update: {field}"

    dispositions: Counter[str] = Counter()
    seen: set[str] = set()
    for row in rows:
        if row["drive_file_id"]:
            row["drive_file_id"] = "REDACTED"
        if row["record_type"] != "archive_pdf" or row["volume"] != "43":
            continue
        record_id = row["record_id"]
        seen.add(record_id)
        if record_id in PROMOTED_IDS:
            status = "close read; finding promoted"
            disposition = "promoted"
        elif record_id in FUNCTIONAL_METADATA_IDS:
            status = "metadata triaged"
            disposition = "metadata"
        else:
            status = "contextual close read; no distinct finding"
            disposition = "contextual"
        relative = Path(row["internal_filename"]).relative_to("archive")
        row["text_extraction_status"] = "extracted"
        row["research_status"] = status
        row["local_path"] = f"recovered/corpus-v43/{relative.as_posix()}"
        row["text_path"] = f"recovered/corpus-v43/{relative.with_suffix('.txt').as_posix()}"
        dispositions[disposition] += 1

    assert seen == {f"M-{number:04d}" for number in range(46, 83)}
    assert dispositions == Counter({"contextual": 27, "metadata": 8, "promoted": 2})
    archive_row = next(row for row in rows if row["record_id"] == ARCHIVE_RECORD_ID)
    for field, value in ARCHIVE_EXPECTED.items():
        assert archive_row[field] == value, f"shared archive provenance changed during update: {field}"

    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    raw_after = INVENTORY.read_text(encoding="utf-8-sig")
    assert raw_after.splitlines().count(ARCHIVE_RAW_ROW) == 1, "D-003 row changed byte-for-byte"


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    replacements = [
        (
            "Checkpoint: *Communal Societies* volumes 1-42",
            "Checkpoint: *Communal Societies* volumes 1-43",
            "gap completed boundary",
        ),
        (
            "After reconciling the volume 42 findings rather than inflating the list",
            "After reconciling the volume 43 findings rather than inflating the list",
            "gap checkpoint description",
        ),
        (
            "No processed journal evidence through volume 42 validates six months of inner work as a reliable con-artist filter.",
            "No processed journal evidence through volume 43 validates six months of inner work as a reliable con-artist filter.",
            "G-018 cumulative boundary",
        ),
        ("F-128, F-130, F-145 |", "F-128, F-130, F-145, F-153 |", "G-001 evidence"),
        ("F-136, F-137, F-145, F-147 |", "F-136, F-137, F-145, F-147, F-152 |", "G-003 evidence"),
        ("F-139, F-143, F-144, F-147 |", "F-139, F-143, F-144, F-147, F-153 |", "G-004 evidence"),
        ("F-141, F-145, F-149, F-150 |", "F-141, F-145, F-149, F-150, F-152 |", "G-005 evidence"),
        ("F-140, F-141, F-143, F-150 |", "F-140, F-141, F-143, F-150, F-153 |", "G-006 evidence"),
        ("F-112, F-114, F-150 |", "F-112, F-114, F-150, F-152, F-153 |", "G-008 evidence"),
        ("F-126, F-141, F-149, F-150 |", "F-126, F-141, F-149, F-150, F-152 |", "G-009 evidence"),
        ("F-087, F-091, F-106 |", "F-087, F-091, F-106, F-153 |", "G-010 evidence"),
        ("F-069, F-083, F-088 |", "F-069, F-083, F-088, F-153 |", "G-014 evidence"),
        (
            "Volume 42 again found neither validation of the filter nor a complete dangerous-child actor response sequence; adult-defined openness, positive memories, and broad social-sustainability correlations were not safety evidence.",
            "Volume 42 again found neither validation of the filter nor a complete dangerous-child actor response sequence; adult-defined openness, positive memories, and broad social-sustainability correlations were not safety evidence. Volume 43 again found neither validation of the filter nor a complete dangerous-child actor response sequence; reported school persistence, successful protest, and a late board takeover were not validated danger filters or complete child-response evidence.",
            "G-018 volume 43 result",
        ),
        (
            "F-149, F-150, F-151 |",
            "F-149, F-150, F-151, F-152, F-153, F-154 |",
            "G-018 evidence",
        ),
        (
            "The volume 1-42 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148, F-151) are bounded negative results",
            "The volume 1-43 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148, F-151, F-154) are bounded negative results",
            "bounded dangerous-child sequence",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)

    prose_extensions = [
        (
            "A civil or competency petition initiated by implicated leaders also requires conduct-specific evidence and independent review.",
            " A community's resistance to formal rules cannot disable conduct thresholds, refusal, immediate protection, review, or fair separation when open admission stops being safe or workable.",
            "G-001 rule-averse separation",
        ),
        (
            "A complaint forum can itself be captured, and an outside evaluator needs private, independently selected access, anti-retaliation, discrepant-account handling, and a later correction route.",
            " Protected objection must also be able to pause a proposed child-placement policy until affected children and families have independent representation and the final decision is recorded.",
            "G-003 child-policy objection",
        ),
        (
            "Audit control of complaint sessions, participant access, and evaluator-facing narratives as practical founder powers too.",
            " When a replacement trustee board takes control after decline, verify its deed authority, resident voice, conflicts, implementation, and later outcomes rather than counting takeover alone as correction.",
            "G-004 board takeover",
        ),
        (
            "Protected dissent also includes freedom from competency or clinical retaliation initiated by the authority being challenged.",
            " Moving a child from family housing to collective boarding requires notice, lawful authority, age-appropriate assent, protected family contact, an independent objection route, and a verified implementation record.",
            "G-005 child placement",
        ),
        (
            "Report business solvency, ownership protection, participation, role conflicts, layoffs, and communal trust separately; an orderly liquidation is not a complete community outcome.",
            " Report decline into a residual neighborhood, resident poverty, usable exit, trust-asset condition, and performance after trustee replacement separately; neither continued occupancy nor a new board is itself recovery.",
            "G-006 residual neighborhood outcome",
        ),
        (
            "A leaver network can supply transition money, educational letters, emergency contacts, records, and a substitute social field; privacy protections may be essential where public participation threatens remaining family ties.",
            " Trust ownership must not make an unhappy resident's home investment unusable; valuation, payout, continued occupancy, hardship, and independent advice need written routes before conflict.",
            "G-008 trust exit",
        ),
        (
            "Safeguarding also requires child-controlled bathing and sleeping boundaries, named adult supervision, and a bar on using an older child as a substitute caregiver beyond age and capacity.",
            " A proposed collective boarding transfer also needs child and family notice, independent representation, protected objection, recorded authorization, and an implementation audit.",
            "G-009 collective boarding",
        ),
        (
            "A purposive study of already stable, normatively selected communities shows that long probation exists, but cannot establish predictive validity, false-positive rates, or a causal effect on safety or survival.",
            " An open-door philosophy must be tested against arrivals who cannot or will not meet conduct and contribution terms, with humane refusal and support routes that do not use poverty, homelessness, diagnosis, or police contact as automatic proxies.",
            "G-010 open admission stress test",
        ),
        (
            "Opaque 'unsuitable or unworthy' classifications can shift structural failure onto low-voice residents, while paid religious service can still be compulsory through institutional sanction.",
            " Open residence also needs explicit guest and member status, basic protections, duties, voice, review, and transition support so ambiguity does not erase either care or accountability.",
            "G-014 open resident roles",
        ),
    ]
    for anchor, addition, label in prose_extensions:
        text = extend_once_or_confirm(text, anchor, addition, label)

    verification_anchor = (
        "- **F status:** inspect Israel's memoir, diary provenance, interviews, other child and adult accounts, Love Family rules, school and health records, and official records before assigning group-wide prevalence, authority, motive, diagnosis, or causation."
    )
    verification_new = verification_anchor + "\n" + "\n".join([
        "- **F status:** inspect the Pears letters, New Harmony minutes, boarding plans, newspapers, family records, and other participant accounts before treating the proposed child transfer, protest constituency, causal claim, or nonimplementation as a formal policy precedent.",
        "- **F status:** inspect Jones's book, the Renaissance Community Trust deed, membership and trustee records, incident and police records, finances, resident and neighbor accounts, and later board actions before naming conduct, assigning diagnoses or prevalence, or claiming that trustee replacement repaired Graham Downs.",
    ])
    text = replace_once_or_confirm(text, verification_anchor, verification_new, "F-152 and F-153 verification queue")

    final_old = "- The remaining volume 42 records are functional metadata and supply no further distinct response mechanism or outcome."
    final_new = final_old + "\n" + "\n".join([
        "- F-152 is limited to Krall's documented proposal, Pears's objection and departure, and the article's conclusion that women's protests prevented implementation; it does not establish a formal veto procedure or the children's own views.",
        "- F-153 preserves the review-level status of Jones's participant history and does not convert poverty, homelessness, substance use, mental-health labels, police contact, or anarchist identity into danger proxies; the later board's outcome is unknown.",
        "- Brown's violent-or-difficult-student program is an adjacent school lead, not an intentional-community child case; its reported 80-percent persistence lacks the denominator, individual process, safety measures, comparator, recurrence, and long-term follow-up needed for promotion.",
        "- Developmental communalism, New Harmony's other gender and education material, Waco media, restorative theory, cohousing process, historiography, religious biography, and the remaining reviews supply corroboration or retrieval leads rather than additional materially distinct response mechanisms.",
        "- The ten volume 43 child-danger candidates concern an adjacent student program, policy subjects, dependents, orphans, alleged victims, family members, childhood biography, scholarly themes, and lexical proximity—not a persistently dangerous child actor in an intentional community with assessment, intervention, review, and later outcome.",
        "- The remaining volume 43 records are functional metadata and supply no further distinct response mechanism or outcome.",
    ])
    text = replace_once_or_confirm(text, final_old, final_new, "volume 43 non-promotions")

    gap_lines = [line for line in text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
        "B": 8,
        "C": 7,
        "D": 3,
    })
    references = set(re.findall(r"\bF-\d{3}\b", text))
    assert references <= {f"F-{number:03d}" for number in range(1, 155)}
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = [
        ("volumes **1-42**", "volumes **1-43**", "state completed boundary"),
        (
            "**899 journal PDFs** were triaged: 378 close-read as relevant or contextual, 207 title/keyword-triaged, and 314 metadata-triaged.",
            "**936 journal PDFs** were triaged: 407 close-read as relevant or contextual, 207 title/keyword-triaged, and 322 metadata-triaged.",
            "state counts",
        ),
        (
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **151 findings** (`F-001` through `F-151`). Volume 42 added three findings: two C and one F-status bounded negative.",
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **154 findings** (`F-001` through `F-154`). Volume 43 added three findings: two C and one F-status bounded negative.",
            "state findings",
        ),
        (
            "`COMMUNITIES-V42-RESEARCH-REPORT.md` records the completed 24-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "`COMMUNITIES-V43-RESEARCH-REPORT.md` records the completed 37-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "state report",
        ),
        (
            "Every one of the 24 volume 42 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `COMMUNAL-SOCIETIES-v41-v45.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
            "Every one of the 37 volume 43 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text. The shared `COMMUNAL-SOCIETIES-v41-v45.zip` archive container was not locally present or reverified in this checkpoint; its saved size, hash, local-path provenance, and prior integrity-test note remain unchanged.",
            "state corpus verification",
        ),
        (
            "Volumes **43-45** have not been processed: **85 journal PDFs**.",
            "Volumes **44-45** have not been processed: **48 journal PDFs**.",
            "state remaining boundary",
        ),
        (
            "The next bounded journal unit is volume **43: 37 PDFs**, with 20 in issue 1 and 17 in issue 2.",
            "The next bounded journal unit is volume **44: 33 PDFs**, with 20 in issue 1 and 13 in issue 2.",
            "state next unit",
        ),
        (
            "Volume 42 adds: child-controlled privacy and safeguarding-by-design for bathing and sleeping space; named adult accountability, age-appropriate limits, protected family bonds, and transition support in collective childrearing; and another bounded dangerous-child null.",
            "Volume 43 adds: protected objection and verified nonimplementation for an intrusive child-placement proposal; conduct-specific admission, protection, separation, property, and review procedures that remain operable under a rule-averse philosophy; and another bounded dangerous-child null.",
            "state evidence summary",
        ),
        ("Do not repeat volumes 1-42.", "Do not repeat volumes 1-43.", "state resume boundary"),
        (
            "Retrieve and verify the 37 volume 43 publisher PDFs; 20 are in issue 1 and 17 are in issue 2, together forming the next exact bounded journal unit.",
            "Retrieve and verify the 33 volume 44 publisher PDFs; 20 are in issue 1 and 13 are in issue 2, together forming the next exact bounded journal unit.",
            "state resume next unit",
        ),
        (
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 37 extracted texts.",
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 33 extracted texts.",
            "state resume corpus size",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = [
        ("Volumes **1-42** complete", "Volumes **1-43** complete", "README completed boundary"),
        ("**899** journal PDFs triaged", "**936** journal PDFs triaged", "README total"),
        ("**378** relevant or contextual close reads", "**407** relevant or contextual close reads", "README close reads"),
        ("**151** evidence findings (`F-001` through `F-151`)", "**154** evidence findings (`F-001` through `F-154`)", "README findings"),
        (
            "Next unit: **volume 43, 37 PDFs** (20 in issue 1; 17 in issue 2)",
            "Next unit: **volume 44, 33 PDFs** (20 in issue 1; 13 in issue 2)",
            "README next unit",
        ),
        (
            "[`recovered/COMMUNITIES-V42-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V42-RESEARCH-REPORT.md)",
            "[`recovered/COMMUNITIES-V43-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V43-RESEARCH-REPORT.md)",
            "README latest report",
        ),
        (
            "With the exact local source corpus restored beneath `recovered/corpus-v42/`, run:",
            "With the exact local source corpus restored beneath `recovered/corpus-v43/`, run:",
            "README corpus path",
        ),
        ("python recovered/test_v42_workflow.py", "python recovered/test_v43_workflow.py", "README tests"),
        ("python recovered/verify_v42.py", "python recovered/verify_v43.py", "README verifier"),
        (
            "The verifier checks all 24 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-43 boundary.",
            "The verifier checks all 37 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-44 boundary.",
            "README verification scope",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    README.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_ledger_findings()
    validate_reconciled_evidence()
    update_inventory()
    update_gap_bank()
    update_state()
    update_readme()
    print("updated volume 43 checkpoint")


if __name__ == "__main__":
    main()
