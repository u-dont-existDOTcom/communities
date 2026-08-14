#!/usr/bin/env python3
"""Apply the completed volume 44 checkpoint to cumulative research artifacts."""

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
REPORT = ROOT / "COMMUNITIES-V44-RESEARCH-REPORT.md"

PROMOTED_IDS = {"M-0093", "M-0106", "M-0113"}
FUNCTIONAL_METADATA_IDS = {
    "M-0083",
    "M-0084",
    "M-0101",
    "M-0102",
    "M-0103",
    "M-0104",
    "M-0105",
    "M-0115",
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
        "finding_id": "F-155",
        "track": "Track A child-placement purpose and stop-rule failure",
        "source_record_id": "M-0106",
        "source_file": "004-counting-the-cost-shaker-celibacy.pdf",
        "journal_volume_issue_year": "Vol. 44, no. 2 (2024)",
        "article_title": "Counting the Cost: Shaker Celibacy",
        "author": "Mary Ann Haagen",
        "community_group": "Shaker societies",
        "page_locator": "PDF p. 12 of article file; printed pp. 11-12",
        "printed_page_number": "11-12",
        "supporting_excerpt": "",
        "source_access": "full text; historical article using Shaker correspondence manuscripts official reports and secondary scholarship",
        "evidence_type": "historical child-admission labor and aggregate-outcome analysis",
        "exact_factual_observation": "Haagen reports that after adult recruitment declined Shaker leaders accepted hundreds of unaccompanied and indentured children in hopes that they would become adult Believers. The children contributed substantially to agricultural and domestic labor. Some became lifelong members, but the article says the vast majority ran away, were dismissed, left at adulthood, or were taken away—sometimes against their will—by family. Haagen concludes that the strategy was ineffective for maintaining membership and continued despite shortcomings obvious to many.",
        "what_source_establishes": "A child-admission policy was used for institutional succession and labor and persisted after aggregate attrition showed that its stated membership purpose was not being met. Child placement needs a child-centered purpose, lawful authority, independent representation, capacity standards, cohort outcomes, and a recorded stop or redesign rule.",
        "what_source_does_not_establish": "It does not supply an entry or outcome denominator, each child's age or legal status, child or family accounts, placement-by-placement welfare, schooling and health outcomes, reasons for each departure, or a counterfactual showing what would have happened without the policy. It does not establish that every child was exploited or harmed.",
        "author_interpretation": "Haagen argues that accepting unaccompanied children failed as a demographic strategy even though Shaker societies continued investing resources and emotional energy in it; she treats celibacy's demographic consequences as a central cost.",
        "alternative_interpretation": "The communities may also have understood admission as refuge, education, or charity; some children became committed members, and family retrieval or ordinary maturation may explain departures better than institutional failure in individual cases. Aggregate nonretention does not by itself measure child wellbeing.",
        "response_process": "Declining adult recruitment; policy shift after 1821; admission and indenture of hundreds of children; work and religious socialization; mixed individual responses; running away, dismissal, adulthood departure, or family removal; continued institutional investment despite aggregate nonretention. No independent child review or formal stop rule is described.",
        "outcome": "Some admitted children became lifelong Shakers, but the article says the vast majority did not remain and that the strategy did not maintain or strengthen membership. No child-wellbeing cohort or later reintegration outcome is reported.",
        "transferability": "High for separating child welfare from demographic, labor, or institutional-survival goals; requiring lawful placement authority, child and family voice, capacity and education standards, protected contact, cohort reporting, and a stop or redesign rule. Low for judging individual Shaker placements without their records.",
        "article_gap_status": "C",
        "likely_article_destination": "Children / math of absorption / outcome dashboard",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "Inspect child-admission and indenture records, census and family records, labor and school records, dismissal and departure records, child accounts, and custody proceedings before estimating cohort size, retention, welfare, involuntariness, or causal effects. DOI: https://doi.org/10.9707/0739-1250.1519",
    },
    {
        "finding_id": "F-156",
        "track": "Track A therapist-controlled child separation and external correction",
        "source_record_id": "M-0113",
        "source_file": "011-review-of-the-sullivanians-sex-psychotherapy-and-the-wild-life-of-an-american-commune.pdf",
        "journal_volume_issue_year": "Vol. 44, no. 2 (2024)",
        "article_title": "Review of The Sullivanians: Sex, Psychotherapy, and the Wild Life of an American Commune",
        "author": "Susan Love Brown",
        "community_group": "Sullivan Institute; Sullivanians; Fourth Wall",
        "page_locator": "PDF p. 4 of review file; printed pp. 77-78",
        "printed_page_number": "77-78",
        "supporting_excerpt": "",
        "source_access": "full text; book review of a history built from interviews and documentary research",
        "evidence_type": "review-level family-separation custody and professional-discipline sequence",
        "exact_factual_observation": "Brown reports that Sullivanian therapists directed family severance, separated mothers from babies, sent children to boarding schools, and portrayed resisting parents as dangerous. In the review's account of Marice Pappo, group members removed her baby's belongings, denied access, and spread claims of alcohol and drug use. With legal advice and outside help Pappo took her daughter out of state. When the father sued for custody, testimony reportedly showed that members had lied about Pappo's substance use; he dropped the suit when the court appeared likely to favor her, and the parents reached a private partial-custody agreement. The review also says publicity preceded the loss of psychotherapy licenses by Joan Harvey, Helen Moses, and Ralph Klein for professional and sexual boundary violations it describes.",
        "what_source_establishes": "At review level, the case contrasts a therapist-controlled family and evidence system with outside counsel, custody-court testimony, and professional licensing review. Care authority, custody narratives, evidence, and professional discipline require independent routes outside the same therapist-leader chain.",
        "what_source_does_not_establish": "The review does not supply the custody pleadings, complete testimony, court findings, private agreement, licensing charges or dispositions, interview protocol, every participant's account, child-welfare records, or later outcomes for the child. It does not prove that publicity caused license loss or adjudicate every allegation in the reviewed book.",
        "author_interpretation": "Brown presents the Sullivanians as an initially liberating psychotherapeutic project that became authoritarian, harmed parents and children, and used secrecy and therapist power to prevent intervention.",
        "alternative_interpretation": "Some members experienced therapy and community as beneficial; the custody plaintiff may have dropped the case for reasons not preserved in the review; professional discipline may have rested on records or conduct independent of the Pappo dispute; and the private agreement may reflect negotiated parental interests rather than a complete institutional correction.",
        "response_process": "Therapist-directed family severance and mother-child separation; removal of the baby's belongings and denial of access; outside legal advice and assisted departure; custody filing; testimony contradicting attributed substance-use claims; dropped suit and private partial-custody agreement; publicity and later professional-license loss. No independent internal grievance or child advocate is described.",
        "outcome": "Pappo retained her daughter subject to a private partial-custody arrangement; the custody suit ended without a reported judgment. Three senior therapists reportedly lost their licenses. The review supplies no child follow-up, group-wide remedy, or causal allocation among court exposure, publicity, licensing evidence, and wider institutional collapse.",
        "transferability": "High for firewalls among therapy, parenting and custody, discipline, intimate relationships, evidence, and professional supervision; for outside counsel and courts; and for independent licensing review. Medium for the historical sequence until the book and underlying records are checked.",
        "article_gap_status": "C",
        "likely_article_destination": "Community as therapist / children / external couplings",
        "confidence": "medium",
        "external_verification_needed": "yes",
        "notes": "Inspect Stille's book and interview method, custody pleadings and testimony, the private agreement, licensing files and dispositions, school and child-welfare records, participant accounts across positions, and contemporaneous press before treating individual conduct or causal links as adjudicated. DOI: https://doi.org/10.9707/0739-1250.1526",
    },
    {
        "finding_id": "F-157",
        "track": "Track A external-report intake bottleneck and survivor response",
        "source_record_id": "M-0093",
        "source_file": "011-review-of-unveiled-a-story-of-surviving-gloriavale.pdf",
        "journal_volume_issue_year": "Vol. 44, no. 1 (2024)",
        "article_title": "Review of Unveiled: A Story of Surviving Gloriavale",
        "author": "William J. Metcalf",
        "community_group": "Cooperites; Gloriavale",
        "page_locator": "PDF pp. 2 and 4 of review file; printed pp. 65-68",
        "printed_page_number": "65-68",
        "supporting_excerpt": "",
        "source_access": "full text; book review combining the reviewer's 1982 research visit with summary of a survivor memoir",
        "evidence_type": "reviewer direct report plus review-level legal and survivor-response account",
        "exact_factual_observation": "Metcalf directly recounts that during a 1982 visit women and girls told him of routine sexual and physical abuse, Neville Cooper expelled him as an evil influence and spy, and he reported the disclosures to authorities. He says nothing happened because he had not personally observed the abuse. The review then summarizes Cooper's later conviction, other convictions and pending investigations described by Pratt, fear-related evidence withholding, Pratt's 2016 escape, survivor organizing, testimony to external bodies, and assistance to other leavers.",
        "what_source_establishes": "A reporting route can exist while its intake threshold excludes disclosed harm from a visitor who lacks direct observation. A usable route needs documented intake, lawful referral and evidence-preservation rules, protection from retaliation, reasons for screening, survivor support distinct from evidence testing, and review when later information emerges.",
        "what_source_does_not_establish": "It does not supply the 1982 agency report or intake standard, identify the authority, show that the authority acted unlawfully, prove what evidence was then available, connect each later case to the disclosures Metcalf heard, verify the review's later counts as a current official register, or establish that every allegation was substantiated.",
        "author_interpretation": "Metcalf treats the initial inaction, later prosecutions and investigations, ongoing fear, and survivor organizing as evidence of long-running abuse protected by isolation and authoritarian control.",
        "alternative_interpretation": "The unidentified authority may have lacked jurisdiction, particulars, willing witnesses, or a lawful investigative predicate in 1982; later cases may concern different people and events; and fear, evidentiary limits, resources, or legal standards may each explain delay. None of these possibilities makes a disclosure-only intake route unnecessary.",
        "response_process": "Private disclosures to an outside visitor; leader expulsion of the visitor; report to unidentified authorities; stated no-action result for lack of direct observation; later criminal and investigative activity summarized by the review; survivor escape, organizing, public testimony, evidence gathering, and leaver support.",
        "outcome": "The 1982 report produced no action according to Metcalf. The review reports later convictions, charges, investigations, survivor advocacy, and continuing difficulty obtaining evidence; it supplies no unified case file, institutional closure, or group-wide safety outcome.",
        "transferability": "High for inclusive and documented external intake, anti-retaliation, preserved screening reasons, later-information review, survivor support, and leaver assistance; medium for the historical enforcement chronology until official records are checked.",
        "article_gap_status": "C",
        "likely_article_destination": "Protected reporting / children / external legal couplings",
        "confidence": "medium",
        "external_verification_needed": "yes",
        "notes": "Verify agency intake, conviction and charging records, investigative status, survivor accounts, and Gloriavale's response before treating later counts or procedural status as current or complete. Preserve the distinction between Metcalf's direct visit/report account and his review of Pratt. Do not repeat the reviewer's diagnostic labels. DOI: https://doi.org/10.9707/0739-1250.1010",
    },
    {
        "finding_id": "F-158",
        "track": "Track A child negative result",
        "source_record_id": "",
        "source_file": "Volume 44 discovery corpus",
        "journal_volume_issue_year": "Volume 44 (2024)",
        "article_title": "Cumulative targeted search and issue-by-issue discovery scan",
        "author": "Research checkpoint",
        "community_group": "Communal Societies volume 44",
        "page_locator": "33 PDFs; 25 substantive close reads; 11 child-danger proximity candidates",
        "printed_page_number": "",
        "supporting_excerpt": "",
        "source_access": "full extracted corpus",
        "evidence_type": "systematic bounded search result",
        "exact_factual_observation": "Across all 33 PDFs, complete title triage, locked six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 25 substantive close reads found children or young people as alleged victims, separated family members, boarding-school residents, unaccompanied or indentured entrants, labor contributors, students, biographical subjects, and participants in adult scandals. One review says some boys bullied animals but supplies no individual allegation, persistence standard, assessment, intervention, review, or later outcome. No intentional-community source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        "what_source_establishes": "The specified dangerous-child evidence pattern is absent from volume 44 under the recorded search, proximity, exclusion, and close-read procedure. The boys-and-animals reference is retained as an incomplete verification lead rather than converted into a responsive child case.",
        "what_source_does_not_establish": "It does not prove that no such case exists in volume 45, standalone or book-length sources, the reviewed books, different terminology, unpublished or protected records, juvenile, educational, medical, disability, animal-welfare, or family systems, or communities outside the journal.",
        "author_interpretation": "Not applicable.",
        "alternative_interpretation": "Privacy, euphemism, aggregate reporting, review-level compression, source destruction, and routing into professional, family, juvenile, educational, disability, animal-welfare, or medical systems may hide relevant cases from a communal-history journal.",
        "response_process": "Not applicable.",
        "outcome": "Bounded null for volume 44; incomplete peer-bullying and animal-harm reference flagged without promotion.",
        "transferability": "High for this completed unit; none for the full literature until volume 45 and the standalone sources are processed.",
        "article_gap_status": "F",
        "likely_article_destination": "Research/school function / dangerous-child branch",
        "confidence": "high",
        "external_verification_needed": "no",
        "notes": "The cumulative bounded null now covers volumes 1-44. Children harmed, separated, boarded, admitted, indentured, employed, educated, or discussed through adult scandals were excluded from the child-as-dangerous-actor result; the brief animal-harm statement lacks the required process and outcome.",
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

    if len(rows) == 154:
        assert rows[-1]["finding_id"] == "F-154"
        assert all(set(finding) == set(fieldnames) for finding in NEW_FINDINGS)
        with LEDGER.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
            writer.writerows(NEW_FINDINGS)
    else:
        assert len(rows) == 158
        assert rows[-4:] == NEW_FINDINGS


def validate_reconciled_evidence() -> None:
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["finding_id"] for row in rows] == [
        f"F-{number:03d}" for number in range(1, 159)
    ]
    assert [row["source_record_id"] for row in rows[-4:]] == [
        "M-0106", "M-0113", "M-0093", ""
    ]
    assert Counter(row["article_gap_status"] for row in rows[-4:]) == Counter({
        "C": 3,
        "F": 1,
    })
    assert all(row["supporting_excerpt"] == "" for row in rows[-4:])
    assert REPORT.is_file()
    assert "**4 new findings, F-155 through F-158**" in REPORT.read_text(encoding="utf-8")


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
        if row["record_type"] != "archive_pdf" or row["volume"] != "44":
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
        row["local_path"] = f"recovered/corpus-v44/{relative.as_posix()}"
        row["text_path"] = f"recovered/corpus-v44/{relative.with_suffix('.txt').as_posix()}"
        dispositions[disposition] += 1

    assert seen == {f"M-{number:04d}" for number in range(83, 116)}
    assert dispositions == Counter({"contextual": 22, "metadata": 8, "promoted": 3})
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
            "Checkpoint: *Communal Societies* volumes 1-43",
            "Checkpoint: *Communal Societies* volumes 1-44",
            "gap completed boundary",
        ),
        (
            "After reconciling the volume 43 findings rather than inflating the list",
            "After reconciling the volume 44 findings rather than inflating the list",
            "gap checkpoint description",
        ),
        (
            "No processed journal evidence through volume 43 validates six months of inner work as a reliable con-artist filter.",
            "No processed journal evidence through volume 44 validates six months of inner work as a reliable con-artist filter.",
            "G-018 cumulative boundary",
        ),
        ("F-145, F-153 |", "F-145, F-153, F-156 |", "G-001 evidence"),
        ("F-063, F-074, F-147 |", "F-063, F-074, F-147, F-156 |", "G-002 evidence"),
        ("F-145, F-147, F-152 |", "F-145, F-147, F-152, F-155, F-156, F-157 |", "G-003 evidence"),
        ("F-144, F-147, F-153 |", "F-144, F-147, F-153, F-156 |", "G-004 evidence"),
        ("F-149, F-150, F-152 |", "F-149, F-150, F-152, F-155, F-156, F-157 |", "G-005 evidence"),
        ("F-141, F-143, F-150, F-153 |", "F-141, F-143, F-150, F-153, F-155, F-156 |", "G-006 evidence"),
        ("F-150, F-152, F-153 |", "F-150, F-152, F-153, F-155, F-156, F-157 |", "G-008 evidence"),
        ("F-149, F-150, F-152 |", "F-149, F-150, F-152, F-155, F-156, F-157 |", "G-009 evidence"),
        ("F-127, F-132, F-143 |", "F-127, F-132, F-143, F-156, F-157 |", "G-011 evidence"),
        ("F-145, F-147, F-149 |", "F-145, F-147, F-149, F-156, F-157 |", "G-013 evidence"),
        ("F-069, F-083, F-088, F-153 |", "F-069, F-083, F-088, F-153, F-155 |", "G-014 evidence"),
        ("F-069, F-083, F-134 |", "F-069, F-083, F-134, F-155 |", "G-015 evidence"),
        ("F-029, F-043, F-084, F-150 |", "F-029, F-043, F-084, F-150, F-155 |", "G-017 evidence"),
        (
            "Volume 43 again found neither validation of the filter nor a complete dangerous-child actor response sequence; reported school persistence, successful protest, and a late board takeover were not validated danger filters or complete child-response evidence.",
            "Volume 43 again found neither validation of the filter nor a complete dangerous-child actor response sequence; reported school persistence, successful protest, and a late board takeover were not validated danger filters or complete child-response evidence. Volume 44 again found neither validation of the filter nor a complete dangerous-child actor response sequence; child-placement attrition, adult custody correction, abuse reporting, and a brief animal-harm statement were not a validated danger filter or complete child-actor response.",
            "G-018 volume 44 result",
        ),
        (
            "F-149, F-150, F-151, F-152, F-153, F-154 |",
            "F-149, F-150, F-151, F-152, F-153, F-154, F-155, F-156, F-157, F-158 |",
            "G-018 evidence",
        ),
        (
            "The volume 1-43 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148, F-151, F-154) are bounded negative results",
            "The volume 1-44 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148, F-151, F-154, F-158) are bounded negative results",
            "bounded dangerous-child sequence",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)

    prose_extensions = [
        (
            "A community's resistance to formal rules cannot disable conduct thresholds, refusal, immediate protection, review, or fair separation when open admission stops being safe or workable.",
            " When care authorities generate or control a child-custody narrative, the separated parent and child need independent counsel, preserved evidence, family contact, and external review.",
            "G-001 therapy custody",
        ),
        (
            "A mandatory complaint-and-growth forum also needs confidential participation boundaries, a route around any challenged leader, and protection against using disclosed feelings as discipline.",
            " A therapist-directed community also needs firewalls between treatment, parenting and custody, intimate relationships, professional supervision, and evidence used in court or discipline.",
            "G-002 therapy firewalls",
        ),
        (
            "Protected objection must also be able to pause a proposed child-placement policy until affected children and families have independent representation and the final decision is recorded.",
            " The same protection must be able to stop or redesign an implemented child-admission strategy when child-wellbeing and retention evidence contradict its institutional purpose. Outside intake must preserve credible disclosed harm even when the reporter lacks direct observation, record why a report was screened out, and reopen when later evidence appears. Court and professional-review routes must remain independent of any therapist-leader chain that generated the family or custody allegation.",
            "G-003 reporting and child stop rule",
        ),
        (
            "When a replacement trustee board takes control after decline, verify its deed authority, resident voice, conflicts, implementation, and later outcomes rather than counting takeover alone as correction.",
            " Audit therapist control over family separation, custody allegations, court-facing evidence, and professional supervision as practical gatekeeper powers too.",
            "G-004 therapist gatekeeper",
        ),
        (
            "Moving a child from family housing to collective boarding requires notice, lawful authority, age-appropriate assent, protected family contact, an independent objection route, and a verified implementation record.",
            " Neither institutional succession nor child labor is a sufficient child benefit; an implemented placement program needs child-centered capacity, independent advocacy, periodic wellbeing review, and a stop rule. A report of harm and support for a separated parent must have a route outside the authority chain that controls treatment, family contact, or evidence.",
            "G-005 child purpose and report",
        ),
        (
            "Report decline into a residual neighborhood, resident poverty, usable exit, trust-asset condition, and performance after trustee replacement separately; neither continued occupancy nor a new board is itself recovery.",
            " For child-admission cohorts, report lawful placement, capacity, education, labor burden, family contact, voluntary retention, reasons for departure, wellbeing, and performance after a stop or redesign decision. For custody or professional correction, report the child's later outcome separately from the end of litigation or loss of a license.",
            "G-006 child cohort and correction outcomes",
        ),
        (
            "Trust ownership must not make an unhappy resident's home investment unusable; valuation, payout, continued occupancy, hardship, and independent advice need written routes before conflict.",
            " For children admitted without a resident parent, the outward door also requires preserved identity and custody records, protected family contact, portable schooling and health records, independent departure review, and reintegration support. A parent-child exit must not depend on accepting therapist-generated allegations or surrendering outside counsel.",
            "G-008 admitted child exit",
        ),
        (
            "A proposed collective boarding transfer also needs child and family notice, independent representation, protected objection, recorded authorization, and an implementation audit.",
            " An implemented admission or indenture program additionally needs a child-centered purpose, capacity and labor limits, cohort outcomes, and a stop or redesign rule when institutional succession fails. Confidential child and survivor disclosures must be intake-capable even when the first outside reporter did not witness the harm directly.",
            "G-009 placement and intake",
        ),
        (
            "A home/work split also fails when the same people are lovers, supervisors, and executives; preassign decision rights, recusal, affected-member voice, records, and appeal across both domains.",
            " A custody dispute or screened-out abuse report also needs an outside case owner, preserved reasons and evidence, a later-information review trigger, and survivor support that remains distinct from adjudication.",
            "G-011 outside case owner",
        ),
        (
            "Child-protection and housing review should audit private bathing and sleeping space and access boundaries rather than assume adult collective consent governs minors.",
            " Map the evidence threshold and reopening rule for disclosure-only reports, and keep custody courts and professional licensing review independent from therapist-controlled treatment, family, and disciplinary records.",
            "G-013 intake and licensing map",
        ),
        (
            "Open residence also needs explicit guest and member status, basic protections, duties, voice, review, and transition support so ambiguity does not erase either care or accountability.",
            " Unaccompanied or indentured children need child-specific status, lawful authority, age-appropriate labor limits, independent grievance access, and a route to family or supported exit rather than being counted mainly as future members or workers.",
            "G-014 child role",
        ),
        (
            "Include legal capacity, transport, utilities, schools, markets, ownership of each external choke point, alternative suppliers, and the consequences of discriminatory or ordinary service withdrawal.",
            " Child-placement capacity must include qualified caregivers, schooling, health care, family contact, records, independent advocacy, and a stop or redesign threshold before admissions scale.",
            "G-015 child capacity",
        ),
        (
            "The implementation audit should include adequate schooling and continuity when a minor leaves, not only written standards.",
            " It should also publish cohort-level admission, retention, departure reason, education, labor, family-contact, and wellbeing outcomes without treating institutional survival as the child's success measure.",
            "G-017 child cohort audit",
        ),
    ]
    for anchor, addition, label in prose_extensions:
        text = extend_once_or_confirm(text, anchor, addition, label)

    verification_anchor = (
        "- **F status:** inspect Jones's book, the Renaissance Community Trust deed, membership and trustee records, incident and police records, finances, resident and neighbor accounts, and later board actions before naming conduct, assigning diagnoses or prevalence, or claiming that trustee replacement repaired Graham Downs."
    )
    verification_new = verification_anchor + "\n" + "\n".join([
        "- **F status:** inspect Shaker child-admission and indenture records, census and family records, labor and school records, dismissal and departure records, child accounts, and custody proceedings before estimating cohort size, retention, welfare, involuntariness, or causal effects.",
        "- **F status:** inspect Stille's book and interview method, the Pappo custody pleadings and testimony, private agreement, licensing files and dispositions, school and child-welfare records, participant accounts, and contemporaneous press before treating the Sullivanian sequence as adjudicated or causal.",
        "- **F status:** verify Metcalf's 1982 agency intake, later conviction and charging records, investigative status, survivor accounts, and Gloriavale's response; preserve the distinction between his direct visit/report account and his review of Pratt, and do not repeat diagnostic labels.",
    ])
    text = replace_once_or_confirm(
        text,
        verification_anchor,
        verification_new,
        "F-155 through F-157 verification queue",
    )

    final_anchor = "- The remaining volume 43 records are functional metadata and supply no further distinct response mechanism or outcome."
    final_new = final_anchor + "\n" + "\n".join([
        "- F-155 is limited to Haagen's aggregate Shaker child-admission, labor, attrition, and policy-persistence account; it does not generalize harm to every placement or treat nonretention alone as a child-wellbeing measure.",
        "- F-156 remains a review-level custody and professional-correction sequence; ending litigation and losing licenses do not by themselves establish the child's later wellbeing or prove every allegation.",
        "- F-157 separates Metcalf's direct 1982 visit and report from his summary of Pratt's memoir and later legal developments; the review's later counts are not a current official case register.",
        "- The Oneida podcast review, Nashoba synthesis, historical-abuse credibility review, Fuller biography, Warren article, and remaining sources corroborate existing findings or supply method and retrieval leads rather than additional materially distinct mechanisms.",
        "- The eleven volume 44 child-danger candidates concern alleged victims, separated or boarded children, unaccompanied entrants, labor contributors, students, adult scandals, incidental language, and one undeveloped statement about boys harming animals—not a persistently dangerous child actor with assessment, intervention, review, and later outcome.",
        "- The remaining volume 44 records are functional metadata and supply no further distinct response mechanism or outcome.",
    ])
    text = replace_once_or_confirm(text, final_anchor, final_new, "volume 44 non-promotions")

    gap_lines = [line for line in text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter({
        "B": 8,
        "C": 7,
        "D": 3,
    })
    references = set(re.findall(r"\bF-\d{3}\b", text))
    assert references <= {f"F-{number:03d}" for number in range(1, 159)}
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    replacements = [
        ("Updated: 2026-08-13 (Africa/Dakar)", "Updated: 2026-08-14 (Africa/Dakar)", "state date"),
        ("volumes **1-43**", "volumes **1-44**", "state completed boundary"),
        (
            "**936 journal PDFs** were triaged: 407 close-read as relevant or contextual, 207 title/keyword-triaged, and 322 metadata-triaged.",
            "**969 journal PDFs** were triaged: 432 close-read as relevant or contextual, 207 title/keyword-triaged, and 330 metadata-triaged.",
            "state counts",
        ),
        (
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **154 findings** (`F-001` through `F-154`). Volume 43 added three findings: two C and one F-status bounded negative.",
            "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **158 findings** (`F-001` through `F-158`). Volume 44 added four findings: three C and one F-status bounded negative.",
            "state findings",
        ),
        (
            "`COMMUNITIES-V43-RESEARCH-REPORT.md` records the completed 37-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "`COMMUNITIES-V44-RESEARCH-REPORT.md` records the completed 33-PDF boundary, close-read disposition, discovery and child-search method, cautions, and exact next unit.",
            "state report",
        ),
        (
            "Every one of the 37 volume 43 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text.",
            "Every one of the 33 volume 44 PDFs was independently recovered from the journal's primary publisher, matched its pre-existing archive-member SHA-256 value in the inventory, matched its inventoried page count, and has nonempty extracted text.",
            "state corpus verification",
        ),
        (
            "Volumes **44-45** have not been processed: **48 journal PDFs**.",
            "Volume **45** has not been processed: **15 journal PDFs**.",
            "state remaining boundary",
        ),
        (
            "The next bounded journal unit is volume **44: 33 PDFs**, with 20 in issue 1 and 13 in issue 2.",
            "The next bounded journal unit is volume **45: 15 PDFs**, all in issue 1.",
            "state next unit",
        ),
        (
            "Volume 43 adds: protected objection and verified nonimplementation for an intrusive child-placement proposal; conduct-specific admission, protection, separation, property, and review procedures that remain operable under a rule-averse philosophy; and another bounded dangerous-child null.",
            "Volume 44 adds: a child-centered stop rule for placement programs whose institutional-succession purpose fails; independent court and professional routes around therapist-controlled family separation; inclusive external intake for credible disclosed harm; and another bounded dangerous-child null.",
            "state evidence summary",
        ),
        ("Do not repeat volumes 1-43.", "Do not repeat volumes 1-44.", "state resume boundary"),
        (
            "Retrieve and verify the 33 volume 44 publisher PDFs; 20 are in issue 1 and 13 are in issue 2, together forming the next exact bounded journal unit.",
            "Retrieve and verify the 15 volume 45 publisher PDFs; all are in issue 1 and together form the final bounded journal unit in the current inventory.",
            "state resume next unit",
        ),
        (
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 33 extracted texts.",
            "Run complete title and keyword discovery, process-family screening, and the separate dangerous-child actor search across all 15 extracted texts.",
            "state resume corpus size",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = [
        ("Volumes **1-43** complete", "Volumes **1-44** complete", "README completed boundary"),
        ("**936** journal PDFs triaged", "**969** journal PDFs triaged", "README total"),
        ("**407** relevant or contextual close reads", "**432** relevant or contextual close reads", "README close reads"),
        ("**154** evidence findings (`F-001` through `F-154`)", "**158** evidence findings (`F-001` through `F-158`)", "README findings"),
        (
            "Next unit: **volume 44, 33 PDFs** (20 in issue 1; 13 in issue 2)",
            "Next unit: **volume 45, 15 PDFs** (all in issue 1)",
            "README next unit",
        ),
        (
            "[`recovered/COMMUNITIES-V43-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V43-RESEARCH-REPORT.md)",
            "[`recovered/COMMUNITIES-V44-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V44-RESEARCH-REPORT.md)",
            "README latest report",
        ),
        (
            "With the exact local source corpus restored beneath `recovered/corpus-v43/`, run:",
            "With the exact local source corpus restored beneath `recovered/corpus-v44/`, run:",
            "README corpus path",
        ),
        ("python recovered/test_v43_workflow.py", "python recovered/test_v44_workflow.py", "README tests"),
        ("python recovered/verify_v43.py", "python recovered/verify_v44.py", "README verifier"),
        (
            "The verifier checks all 37 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-44 boundary.",
            "The verifier checks all 33 PDF hashes, page counts, and text extractions, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and the volume-45 boundary.",
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
    print("updated volume 44 checkpoint")


if __name__ == "__main__":
    main()
