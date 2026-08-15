#!/usr/bin/env python3
"""Apply the completed eight-source standalone checkpoint."""

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
INDEX = REPOSITORY / "docs" / "INDEX.md"
REPORT = ROOT / "COMMUNITIES-STANDALONE-RESEARCH-REPORT.md"

SOURCE_UPDATES = {
    "D-001": {
        "year": "1980",
        "article_title": "Alienation and Charisma: A Study of Contemporary American Communes",
        "author": "Benjamin D. Zablocki",
        "printed_page_range": "1-421",
        "pdf_pages": "488",
        "sha256": "ac1af0c28f1ed953dbb0c92db90f6aa9815309a230a28a51af019b062f653535",
        "research_status": "close read; findings promoted",
        "file_stem": "D-001-alienation-and-charisma",
        "extension": ".pdf",
        "notes": "Standalone book; exact Drive size and hash verified; full text close-read; F-163 and F-164 promoted; nonprobability sample and case limits preserved",
    },
    "D-002": {
        "year": "1972",
        "article_title": "Commitment and Community: Communes and Utopias in Sociological Perspective",
        "author": "Rosabeth Moss Kanter",
        "printed_page_range": "1-280",
        "pdf_pages": "324",
        "sha256": "02e6817cd2e8295e28aee842b95e496605f8624b136bb48844fc42080b4e0684",
        "research_status": "contextual close read; no distinct finding",
        "file_stem": "D-002-commitment-and-community",
        "extension": ".pdf",
        "notes": "Standalone book; exact Drive size and hash verified; full text close-read; longevity and retention are not safety outcomes; corroborates F-060 and F-012",
    },
    "D-004": {
        "year": "2008",
        "article_title": "Evil Genes: Why Rome Fell, Hitler Rose, Enron Failed, and My Sister Stole My Mother's Boyfriend",
        "author": "Barbara Oakley",
        "printed_page_range": "1-402",
        "pdf_pages": "427",
        "sha256": "fd5001e2af795928330791023547f5a03844042b5a3bc45f1d32db5e99b6bc98",
        "research_status": "contextual close read; no distinct finding",
        "file_stem": "D-004-evil-genes",
        "extension": ".pdf",
        "notes": "Standalone popular synthesis; exact Drive size and hash verified; full text close-read; retrospective diagnostic framing and historical biography not promoted as screening evidence",
    },
    "D-005": {
        "year": "2021",
        "article_title": "Targeted Conspiratorial Killing, Human Self-Domestication and the Evolution of Groupishness",
        "author": "Richard W. Wrangham",
        "printed_page_range": "1-21",
        "pdf_pages": "21",
        "sha256": "c0509337e38c00f37384c7b1255cf2e37432642ec174928d7fe096360cd0b0fd",
        "research_status": "contextual close read; no distinct finding",
        "file_stem": "D-005-wrangham-targeted-conspiratorial-killing",
        "extension": ".pdf",
        "notes": "Standalone open-access theory article; exact Drive size and hash verified; full text close-read; hypothesis and lethal mechanism explicitly excluded from modern recommendations; DOI 10.1017/ehs.2021.20",
    },
    "D-006": {
        "year": "1979",
        "article_title": "The !Kung San: Men, Women, and Work in a Foraging Society",
        "author": "Richard B. Lee",
        "printed_page_range": "1-526",
        "pdf_pages": "564",
        "sha256": "ca821f84da90e7475ff1d919935a14d0ba4fbdcc263296a83385351aeea2bc97",
        "research_status": "close read; findings promoted",
        "file_stem": "D-006-the-kung-san",
        "extension": ".pdf",
        "notes": "Standalone ethnography; exact Drive size and hash verified; full text close-read; F-165 and F-166 promoted in a separate traditional-society evidence lane; killings excluded from recommendations",
    },
    "D-007": {
        "year": "1972",
        "article_title": "The Mountain People",
        "author": "Colin M. Turnbull",
        "printed_page_range": "1-298",
        "pdf_pages": "324",
        "sha256": "c34bc1a621a214725ecd89c0c2d100ffb83adda6dcba21c24dc998830094b6f3",
        "research_status": "contextual close read; no distinct finding",
        "file_stem": "D-007-the-mountain-people",
        "extension": ".pdf",
        "notes": "Standalone contested ethnography; exact Drive size and hash verified; full text close-read; later scholarship checked; coercive dispersal, child removal, assimilation, and extinction proposals explicitly rejected",
    },
    "D-008": {
        "year": "2001",
        "article_title": "The Riddle of Amish Culture, Revised Edition",
        "author": "Donald B. Kraybill",
        "printed_page_range": "1-371",
        "pdf_pages": "",
        "sha256": "6b79ab85b331e106f2fea62da75f955604370570cc394638e8ad1cfd119c8557",
        "research_status": "close read; findings promoted",
        "file_stem": "D-008-the-riddle-of-amish-culture",
        "extension": ".epub",
        "notes": "Standalone EPUB; exact Drive size and hash verified; ZIP integrity passed; full text close-read; F-167 promoted with district-specific and independence limits",
    },
    "D-018": {
        "year": "2011",
        "article_title": "The Fragmentation of Moral Psychology: Reason, Emotion, Motivation and Moral Judgment in Ethics and Science",
        "author": "Christopher Zarpentine",
        "printed_page_range": "1-270",
        "pdf_pages": "317",
        "sha256": "5eb136c64c1922dd53fac829e473167030071a6101521f6c260468968ec15065",
        "research_status": "contextual close read; no distinct finding",
        "file_stem": "D-018-zarpentine-dissertation",
        "extension": ".pdf",
        "notes": "Standalone philosophy dissertation; exact Drive size and hash verified; full text close-read; DSM-IV-era psychopathy discussion is not a community screening or governance protocol",
    },
}

NEW_FINDINGS = [
    {
        "finding_id": "F-163",
        "track": "Track A adult dangerous conduct and failed separation authority",
        "source_record_id": "D-001",
        "source_file": "D-001-alienation-and-charisma.pdf",
        "journal_volume_issue_year": "Standalone book (1980)",
        "article_title": "Alienation and Charisma: A Study of Contemporary American Communes",
        "author": "Benjamin D. Zablocki",
        "community_group": "120 contemporary United States communes; rural anarchistic case",
        "page_locator": "PDF pp. 166-168 and 311-316; printed pp. 138-140 and 283-288",
        "printed_page_number": "138-140; 283-288",
        "supporting_excerpt": "",
        "source_access": "full text; book-length comparative commune study",
        "evidence_type": "nonprobability comparative study with interviews, observation, aggregate response repertoire, and one conduct-specific case",
        "exact_factual_observation": "Across the 120-commune sample, Table 6-11 reports methods ever used: discussion by the people involved 88 percent, group meeting 76 percent, mutual criticism 75 percent, expulsion or threat 44 percent, removal from office 40 percent, membership tribunal 31 percent, therapeutic counseling 24 percent, temporary exile 4 percent, activity exclusion 4 percent, and withdrawal of privileges 1 percent. Separately, about one-quarter of rural communes denied any authority to expel. In one rural anarchistic commune an adult described behaviorally as drinking heavily, bullying, stealing, abusing others, and sometimes becoming violent remained despite members' fear and weak requests that he leave; other men sometimes beat him, children mocked him, and members subjected him to cruel practical jokes.",
        "what_source_establishes": "The source documents both a discussion-heavy response repertoire and a case in which the absence of clear separation authority coexisted with continuing dangerous conduct and retaliatory cruelty. A modern design needs conduct thresholds, immediate protection, explicit decision authority, notice, evidence review, recusal, appeal, and fair property settlement rather than assuming discussion or informal pressure will resolve every case.",
        "what_source_does_not_establish": "The table records whether a method was ever used, not its frequency, fairness, effectiveness, or danger-specific outcome. The case does not establish prevalence, an independent account, a diagnosis, motive, responsibility for every incident, a formal allegation sequence, or what happened later. It does not show that expulsion alone would have produced safety.",
        "author_interpretation": "Zablocki interprets expulsion crises as important to the routinization of communal social control and speculates that outcasts may function as scapegoats or tension outlets.",
        "alternative_interpretation": "Open-admission norms, weak authority, intoxication, poverty, interpersonal escalation, retaliation, leadership style, and selection into the observed case may all have shaped the outcome. The author's diagnostic and scapegoat speculation is not needed for the conduct-specific finding.",
        "response_process": "Aggregate methods included dyadic discussion, group meetings, criticism, removal, tribunals, counseling, and expulsion. In the focal case the group had no effective formal expulsion route, used weak requests to leave, and members and children retaliated informally while the adult remained.",
        "outcome": "In the reported observation the adult remained and both the described conduct and cruel retaliation persisted. No later separation, review, repair, recurrence rate, victim outcome, or member-wellbeing follow-up is supplied.",
        "transferability": "High for the need to define separation authority and due process before a crisis. Medium for the response menu. Low for generalizing the single case or using the author's diagnostic and functional speculation.",
        "article_gap_status": "C",
        "likely_article_destination": "Membership and fair separation / conflict architecture / external response",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "Inspect study instruments, case notes, member accounts, any incident or property records, and later outcomes. Do not repeat the source's retrospective diagnosis or infer a scapegoat motive. Discussion prevalence is not effectiveness evidence.",
    },
    {
        "finding_id": "F-164",
        "track": "Track A applicant role-specific child-access gating",
        "source_record_id": "D-001",
        "source_file": "D-001-alienation-and-charisma.pdf",
        "journal_volume_issue_year": "Standalone book (1980)",
        "article_title": "Alienation and Charisma: A Study of Contemporary American Communes",
        "author": "Benjamin D. Zablocki",
        "community_group": "One consensual noncharismatic commune in Atlanta",
        "page_locator": "PDF p. 141; printed p. 113",
        "printed_page_number": "113",
        "supporting_excerpt": "",
        "source_access": "full text; one participant account within a comparative study",
        "evidence_type": "single admission-process example",
        "exact_factual_observation": "A participant said a new resident was placed on an informal probation, did not initially attend meetings, and did not initially perform childcare because the commune wanted to observe the resident's relationship with children. The account says access expanded when the group judged the relationship and readiness for long-term commitment acceptable.",
        "what_source_establishes": "The account documents that one commune separated residence from immediate access to meetings and childcare. It is a precedent for staging role-specific authority during provisional membership instead of treating admission as an all-access switch.",
        "what_source_does_not_establish": "It supplies no written criteria, child or parent input, observation method, allegation or incident, reviewer independence, time limit, appeal, false-positive or false-negative rate, comparator, safety outcome, or later follow-up. It does not validate intuition, relationship fit, or commitment as a danger screen.",
        "author_interpretation": "Zablocki presents the account as an example of consensual admission decision-making rather than as a tested safeguarding protocol.",
        "alternative_interpretation": "The delay may have reflected general integration, convenience, trust, or informal preference rather than a deliberate child-safety design; consensus can also reproduce bias unless criteria and review are recorded.",
        "response_process": "Informal probation; temporary exclusion from meetings and childcare; observation of the resident's relationship with children; later expansion of access after group consensus.",
        "outcome": "The resident was admitted for long-term participation. No child-safety, incident, retention, grievance, or later role-performance outcome is reported.",
        "transferability": "Medium-high for separating residence, governance, childcare, finances, transport, and other sensitive roles during a provisional period. Low for the source's informal decision rule as a validated screen.",
        "article_gap_status": "B",
        "likely_article_destination": "From visitor to member / children and safeguarding",
        "confidence": "medium",
        "external_verification_needed": "yes",
        "notes": "Verify the original interview and any admission or childcare records. A modern version needs written conduct-based criteria, named supervisors, child and parent voice, access logs, time-bound review, appeal, and a route for later concerns.",
    },
    {
        "finding_id": "F-165",
        "track": "Track C traditional-society allocation and anti-capture mechanism",
        "source_record_id": "D-006",
        "source_file": "D-006-the-kung-san.pdf",
        "journal_volume_issue_year": "Standalone ethnography (1979)",
        "article_title": "The !Kung San: Men, Women, and Work in a Foraging Society",
        "author": "Richard B. Lee",
        "community_group": "Dobe-area !Kung San",
        "page_locator": "PDF pp. 274-279; printed pp. 244-249",
        "printed_page_number": "244-249",
        "supporting_excerpt": "",
        "source_access": "full text; book-length ethnography based on fieldwork in 1963-1964 and 1967-1969",
        "evidence_type": "ethnographic observation, retrospective hunting records, distribution rules, and a four-person quiver check",
        "exact_factual_observation": "Lee's Table 8.6 reports that 34 percent of hunters accounted for 79 percent of recorded kudu kills while 66 percent accounted for 21 percent. Under the described rule, the owner of the first arrow to strike the animal, not necessarily the hunter, held the formal right and burden to distribute the meat. Arrows circulated through hxaro exchange: in a 1964 check of four men's quivers, three carried arrows from four to six other men and two carried none of their own.",
        "what_source_establishes": "In this setting, productive skill, formal allocation authority, and public credit were partly decoupled through circulated arrow ownership. The mechanism made high productivity less automatically convertible into sole distribution control and spread both prestige and the burden of contested allocation.",
        "what_source_does_not_establish": "It does not establish a controlled causal effect on dominance, violence, equality, nutrition, or long-run group survival; universal compliance; the representativeness of four quivers; an absence of gender or status inequality; or direct portability to money, employment, property, or modern law.",
        "author_interpretation": "Lee interprets arrow circulation and disparagement of successful hunters as practices that diffuse prestige, responsibility, and hostility and inhibit self-aggrandizement.",
        "alternative_interpretation": "Kinship, hxaro reciprocity, ecology, ownership symbolism, sharing obligations, or allocation risk may explain the rule without proving an anti-capture effect. Ridicule and food taboos are culturally specific and are not necessary to preserve the structural observation.",
        "response_process": "Highly unequal hunting production; circulation of arrows among exchange partners; allocation right assigned to the arrow owner; formal meat distribution by that owner; reciprocal sharing and later hosting obligations.",
        "outcome": "The source reports distributed ownership and credit despite unequal production, but supplies no comparison group, pre-policy baseline, quantified authority outcome, or individual wellbeing follow-up.",
        "transferability": "Medium for the abstract design question of whether contribution, credit, allocation authority, and oversight should be separated. Low for direct transfer of ridicule, taboo, kinship exchange, or arrow rules. Traditional-society evidence remains separate until a modern legal and ethical transfer argument is made.",
        "article_gap_status": "B",
        "likely_article_destination": "Founderism / math of absorption / economic-role design",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "Check field records, sampling and kill estimates, women's participation and allocation accounts, later ethnography, and competing interpretations. Do not recommend humiliation or treat productivity as a safety proxy.",
    },
    {
        "finding_id": "F-166",
        "track": "Track C traditional-society conflict response and external adjudication",
        "source_record_id": "D-006",
        "source_file": "D-006-the-kung-san.pdf",
        "journal_volume_issue_year": "Standalone ethnography (1979)",
        "article_title": "The !Kung San: Men, Women, and Work in a Foraging Society",
        "author": "Richard B. Lee",
        "community_group": "Dobe, Nyae Nyae, and /Du/da-region !Kung San",
        "page_locator": "PDF pp. 400-412 and 425-429; printed pp. 370-382 and 395-399",
        "printed_page_number": "370-382; 395-399",
        "supporting_excerpt": "",
        "source_access": "full text; ethnographic observation and retrospective case histories",
        "evidence_type": "observed fights, retrospective homicide accounts, conflict cases, group fission, and outside-court adoption",
        "exact_factual_observation": "Across three years of fieldwork Lee recorded 58 arguments and fights, 34 involving blows. He also tabulated 22 confirmed homicides and at least 15 woundings from 1920-1955 in a base population he estimated near 1,500; all homicide accounts were retrospective and the best were corroborated by multiple informants. After blows, third parties commonly restrained and separated combatants. Principals sometimes left for cooling-off periods, groups split and later recombined, and elders could direct opposing parties to separate n!ores for periods said to last up to 20 years. Serious disputes increasingly went to a Tswana court, which the source says was popular and offered relief and some protection, although two homicides followed the headman's appointment and one offender was killed after imprisonment.",
        "what_source_establishes": "The source documents a layered response repertoire: third-party interruption, temporary cooling and mobility, longer structural separation, and an external adjudication route. It also shows that informal egalitarian intervention can expose bystanders and that outside law did not eliminate violence.",
        "what_source_does_not_establish": "It does not establish causal effectiveness of any step, complete event ascertainment, fair process, individual consent, victim outcomes, an appeal system, modern legal validity, or that reported post-1955 decline resulted from the court. The source's homicide-rate comparison and evolutionary discussion require separate scrutiny.",
        "author_interpretation": "Lee treats group fission as a major conflict-resolution and spacing mechanism and the Tswana court as relieving the burden of retaliation-prone internal settlement, while saying both internal and outside mechanisms were imperfect.",
        "alternative_interpretation": "Mobility, changing settlement patterns, colonial authority, policing, reporting, medical access, weapons, ecology, demographic change, and fear of coercive punishment may explain part of the observed sequence. A popular outside forum is not necessarily independent, fair, or safe.",
        "response_process": "Argument; attempted de-escalation; third-party restraint after blows; cooling-off departure or camp split; in grave cases longer territorial separation; increasing referral of serious disputes to an outside customary-law forum. Community-sanctioned killings, feud retaliation, summary execution, and coercive colonial punishment are excluded from the transferable process.",
        "outcome": "The source reports recurrent nonlethal fights, historical homicides, periods of successful separation and recombination, and no reported killings after 1955, but provides no causal design and records serious failures after outside authority arrived.",
        "transferability": "Medium for designing a nonlethal ladder that separates immediate interruption, cooling space, longer housing separation, and independent adjudication. Low for direct transfer because mobility, kinship, subsistence, colonial law, and threat environment differ. Lethal punishment is not a recommendation.",
        "article_gap_status": "C",
        "likely_article_destination": "Conflict architecture / external couplings / planned forks",
        "confidence": "medium",
        "external_verification_needed": "yes",
        "notes": "Inspect field notes, independent participant accounts, court and headman records, later scholarship, demographic denominators, and post-1955 reporting. Never translate executions, retaliatory killing, banishment, or colonial coercion into a modern recommendation.",
    },
    {
        "finding_id": "F-167",
        "track": "Track C religious-district disciplinary ladder and captured review",
        "source_record_id": "D-008",
        "source_file": "D-008-the-riddle-of-amish-culture.epub",
        "journal_volume_issue_year": "Standalone book, revised edition (2001)",
        "article_title": "The Riddle of Amish Culture, Revised Edition",
        "author": "Donald B. Kraybill",
        "community_group": "Old Order Amish church districts, with Lancaster County examples",
        "page_locator": "EPUB ops/xhtml/ch05.html; printed pp. 131-139; anchors page_131 through page_139",
        "printed_page_number": "131-139",
        "supporting_excerpt": "",
        "source_access": "full EPUB text; ethnographic synthesis with interviews, observation, primary documents, and a methods appendix",
        "evidence_type": "district-level disciplinary procedure, member and leader accounts, and conflict-of-interest example",
        "exact_factual_observation": "Kraybill describes requested and voluntary confessions with four graduated levels. Reports or observation go to ordained leaders; a bishop may send a deacon and minister for a private visit; serious matters move to a members' meeting where the accused may explain; ministers propose a sanction; the congregation votes and generally affirms the bishop; a six-week temporary ban ends in review and possible reinstatement; refusal to submit can lead to excommunication and shunning. The same chapter reports a member pressing action against a bishop's son and the bishop later threatening that member with excommunication over a telephone.",
        "what_source_establishes": "The source documents an internally graduated sequence with private resolution, a hearing, a time-bounded sanction, review, and a reintegration path. It simultaneously documents that proposal and information control remained leader-centered, congregation review was usually affirming, and a conflict involving a bishop could contaminate enforcement.",
        "what_source_does_not_establish": "It does not establish independent adjudication, recusal, appeal, proportionality, consistent application, member or family freedom from coercion, safety effectiveness, incident denominators, false-positive rates, or later wellbeing. Most examples concern religious and technological conformity, not dangerous conduct, and the source says practice varies by district.",
        "author_interpretation": "Kraybill describes confession as both social control and a reintegrative ritual, notes strong pressure and humiliation, and presents the bishop retaliation example as a petty conflict that can sour the process.",
        "alternative_interpretation": "A time-bounded ladder can reduce arbitrary escalation, but confession and unanimous assent under strong social pressure may record submission rather than factual agreement. Congregational voting is not independent review when leaders select the charge, evidence, and proposed sanction.",
        "response_process": "Observation or report; leader intake; private visit for minor matters; public member meeting for serious matters; opportunity to explain; minister-proposed sanction; congregational vote; six-week ban; return review and reinstatement on confession, or escalation to excommunication and shunning.",
        "outcome": "The source reports some reinstatements and member descriptions of catharsis, but gives no denominator, independent fairness or safety measure, recurrence result, appeal outcome, or later wellbeing. The conflict-of-interest example has no recorded correction.",
        "transferability": "Medium-high for distinguishing graduated steps, a written time limit, review, and reintegration from permanent exclusion. Low for public humiliation, compelled confession, shunning, leader-centered evidence, and conformity enforcement. A modern process needs independent intake, recusal, appeal, and non-waivable rights.",
        "article_gap_status": "C",
        "likely_article_destination": "Fair separation / founderism / conflict architecture",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "Inspect district rules, case records, participant and former-member accounts, variation across affiliations, recusal practice, and later outcomes. Do not endorse humiliation, confession under pressure, shunning, or conformity sanctions as safety mechanisms.",
    },
    {
        "finding_id": "F-168",
        "track": "Track A child negative result",
        "source_record_id": "",
        "source_file": "Standalone discovery corpus",
        "journal_volume_issue_year": "Eight standalone sources (1972-2021 publications and editions)",
        "article_title": "Cumulative standalone discovery, process screening, and close-read audit",
        "author": "Research checkpoint",
        "community_group": "Eight intentional-community, traditional-society, theory, clinical, and philosophical sources",
        "page_locator": "8 substantive sources; 8 full-text close reads; child-danger proximity candidates in all 8",
        "printed_page_number": "",
        "supporting_excerpt": "",
        "source_access": "full extracted corpus; seven PDFs and one EPUB",
        "evidence_type": "systematic bounded search result with source-by-source close reading",
        "exact_factual_observation": "Complete title triage, the locked six-family keyword scoring, five-family process screening, child-danger proximity inspection, and eight full-text close reads found no intentional-community case documenting a child who remained gravely dangerous together with allegation, assessment, intervention, review, and later outcome. Turnbull reports alleged child-on-child cruelty under displacement and famine, but provides no individual persistence tracking, adult assessment, structured intervention, review, or later outcome; the source's sweeping account and proposals are contested. Other candidates concerned child victims, policy subjects, clinical or developmental theory, biographies, hypotheticals, or unrelated lexical proximity.",
        "what_source_establishes": "The specified dangerous-child actor sequence is absent from the eight-source standalone unit under the recorded search, proximity, exclusion, and close-read procedure. Combined with F-162, the current assigned primary corpus is complete without such a sequence.",
        "what_source_does_not_establish": "It does not prove historical absence or absence in other books, articles, unpublished or protected records, different terminology, schools, families, clinical settings, juvenile systems, disability services, child welfare, animal-welfare reports, or communities outside the assigned corpus.",
        "author_interpretation": "Not applicable.",
        "alternative_interpretation": "Privacy, euphemism, aggregate reporting, missing records, source controversy, and routing into family, school, medical, disability, juvenile, child-welfare, or animal-welfare systems may hide relevant sequences from the processed sources.",
        "response_process": "Not applicable.",
        "outcome": "Bounded null across eight standalone sources and completion of the assigned 984-journal-PDF plus eight-standalone substantive corpus. No article prose was changed.",
        "transferability": "High for the completed standalone search unit; none for the wider literature. The result supports an explicit evidence gap and adjacent-source research plan, not a claim of absence.",
        "article_gap_status": "F",
        "likely_article_destination": "Research or school function / dangerous-child branch",
        "confidence": "high",
        "external_verification_needed": "no",
        "notes": "The cumulative bounded null now covers Communal Societies volumes 1-45 plus the eight assigned standalone sources. Turnbull's child-harm descriptions lack the required process and outcome sequence and do not rescue the gap.",
    },
]


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old in text:
        return text.replace(old, new, 1)
    raise AssertionError(f"missing update anchor: {label}")


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
    if len(rows) == 162:
        with LEDGER.open("a", newline="", encoding="utf-8") as handle:
            csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n").writerows(
                NEW_FINDINGS
            )
    else:
        assert len(rows) == 168
        assert rows[-6:] == NEW_FINDINGS


def update_inventory() -> None:
    with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    seen: set[str] = set()
    for row in rows:
        if row["drive_file_id"]:
            row["drive_file_id"] = "REDACTED"
        update = SOURCE_UPDATES.get(row["record_id"])
        if update is None:
            continue
        seen.add(row["record_id"])
        for field in (
            "year",
            "article_title",
            "author",
            "printed_page_range",
            "pdf_pages",
            "sha256",
            "research_status",
            "notes",
        ):
            row[field] = update[field]
        stem = update["file_stem"]
        row["text_extraction_status"] = "extracted"
        row["local_path"] = f"recovered/corpus-standalone/{stem}{update['extension']}"
        row["text_path"] = f"recovered/corpus-standalone/{stem}.txt"
    assert seen == set(SOURCE_UPDATES)
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-001": (
        " Discussion-heavy conflict handling is not enough when no one has clear authority to order a fair separation: define the threshold, decision maker, review, appeal, immediate protection, and property settlement before danger and retaliation coexist. A graduated internal ladder still needs recusal and an independent route when its leader controls the allegation and proposed sanction.",
        ["F-163", "F-167"],
    ),
    "G-003": (
        " Congregational assent is not independent review when a conflicted leader controls the charge, evidence, and recommended sanction; require recusal, a route outside the district, and a correction record.",
        ["F-167"],
    ),
    "G-004": (
        " Separate productive skill and public credit from allocation authority and oversight so a high contributor does not automatically become the distribution gatekeeper.",
        ["F-165"],
    ),
    "G-010": (
        " Gate sensitive roles separately during provisional membership: residence need not imply immediate childcare, governance, financial, transport, or records access. The gate needs conduct-based criteria, named supervisors, affected-person voice, logs, a time limit, and review rather than informal fit alone.",
        ["F-164"],
    ),
    "G-011": (
        " Distinguish immediate third-party interruption, voluntary cooling space, longer housing separation, and independent adjudication. Internal graduated discipline can add a time-bounded review and reintegration step, but leader-controlled evidence and sanctions still require recusal and external appeal.",
        ["F-166", "F-167"],
    ),
    "G-016": (
        " Conflict-triggered fission is not the same as a planned fork: preassign voluntary cooling space and reversible housing separation so mobility does not become informal banishment or permanent loss of rights.",
        ["F-166"],
    ),
    "G-018": (
        " The standalone unit again found no validated personality, commitment, productivity, or dangerous-child filter. Admission severity correlated with stability but also with difficulty leaving; staged childcare access was only an anecdote; productive skill was deliberately separated from allocation credit in one traditional-society setting; and the child search remained a bounded null.",
        ["F-163", "F-164", "F-165", "F-168"],
    ),
}


VERIFICATION_LINES = [
    "- **F status:** inspect Zablocki's instruments, response and selection patterns, original case notes, participant accounts, incident and property records, and later outcomes before estimating prevalence or effectiveness; do not adopt the retrospective diagnosis or scapegoat speculation.",
    "- **F status:** verify the Atlanta admission interview and any childcare or access records before treating staged role access as more than a single informal example.",
    "- **F status:** inspect Lee's field notes, hunting and conflict case records, demographic denominators, Tswana court records, participant accounts, later ethnography, and competing interpretations before assigning causal effects to arrow circulation, fission, or outside adjudication.",
    "- **F status:** inspect Amish district rules, case records, member and former-member accounts, variation across affiliations, recusal practice, and later outcomes before treating the described ladder as fair or effective.",
]

NONPROMOTION_LINES = [
    "- F-163 preserves the difference between an aggregate ever-used response table and one failed-separation case. It does not diagnose the adult, infer a scapegoat function, or prove that expulsion alone would have produced safety.",
    "- F-164 is one informal admission account with no criteria, child input, error rate, or safety outcome. It supports role-specific staging, not intuition or commitment as a validated danger screen.",
    "- Kanter's successful-versus-unsuccessful commune comparison defines success by longevity and retention. Its commitment mechanisms and leader prerogatives corroborate F-060 and F-012 but do not establish safety, wellbeing, or causation.",
    "- Oakley's popular synthesis mixes science, biography, and family narrative and retrospectively applies diagnostic frames. It supplies no intentional-community screening protocol or outcome and is not promoted as clinical or historical diagnosis.",
    "- Wrangham's execution hypothesis is theory, acknowledges unknown Pleistocene execution frequency and unmodeled conditions, and supplies no modern community protocol or outcome. Planned killing, execution, and conformity pressure are explicitly not recommendations.",
    "- F-165 and F-166 remain in a separate traditional-society evidence lane. Arrow circulation and conflict fission are not direct modern prescriptions; ridicule, feud retaliation, community-sanctioned killing, summary execution, and colonial coercion are excluded.",
    "- Turnbull's Ik child-harm descriptions lack individual persistence tracking, adult assessment, structured intervention, review, and later outcome. His proposed roundup, random family separation, language loss, assimilation, infant removal, and hoped-for disappearance of the Ik are unethical, coercive, unsupported, and explicitly rejected. Later scholarship also disputes his sweeping characterization.",
    "- F-167 does not endorse public humiliation, compelled confession, shunning, or conformity enforcement. A time-bounded ladder and reintegration path do not cure leader control, social pressure, missing recusal, or missing appeal.",
    "- Zarpentine's dissertation is moral psychology and DSM-IV-era theory, not an intentional-community case or applicant screen. Psychopathy constructs and instruments cannot be inferred from historical conduct or used here as a community admission shortcut.",
    "- The eight-source child-danger search produced F-168, a bounded negative result. It does not establish that intentional communities never faced or managed a persistently dangerous child.",
]


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-45",
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources",
        "gap completed boundary",
    )
    text = replace_once_or_confirm(
        text,
        "After reconciling the volume 45 findings rather than inflating the list",
        "After reconciling the eight standalone-source findings rather than inflating the list",
        "gap checkpoint description",
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
        existing = [part.strip() for part in cells[7].strip().split(",") if part.strip()]
        for finding_id in finding_ids:
            if finding_id not in existing:
                existing.append(finding_id)
        cells[7] = " " + ", ".join(existing) + " "
        updated_lines.append("|".join(cells))
    text = "\n".join(updated_lines) + "\n"
    text = replace_once_or_confirm(
        text,
        "The volume 1-45 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148, F-151, F-154, F-158, F-162) are bounded negative results",
        "The volume 1-45 and standalone dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105, F-111, F-115, F-118, F-121, F-125, F-131, F-138, F-142, F-146, F-148, F-151, F-154, F-158, F-162, F-168) are bounded negative results",
        "bounded child sequence",
    )
    verification_anchor = "- **F status:** inspect Hutterite colony agreements, member and asset lists, valuation and debt records, decision and dissent procedures, renovation accounts, and comparative later outcomes before treating the described fission process as universal or individually equitable."
    verification_block = verification_anchor + "\n" + "\n".join(VERIFICATION_LINES)
    if VERIFICATION_LINES[0] not in text:
        assert verification_anchor in text
        text = text.replace(verification_anchor, verification_block, 1)
    nonpromotion_anchor = "- The remaining volume 45 records are functional metadata and supply no further distinct response mechanism or outcome."
    nonpromotion_block = nonpromotion_anchor + "\n" + "\n".join(NONPROMOTION_LINES)
    if NONPROMOTION_LINES[0] not in text:
        assert nonpromotion_anchor in text
        text = text.replace(nonpromotion_anchor, nonpromotion_block, 1)
    gap_lines = [line for line in text.splitlines() if line.startswith("| G-")]
    assert len(gap_lines) == 18
    assert Counter(line.split("|")[2].strip() for line in gap_lines) == Counter(
        {"B": 8, "C": 7, "D": 3}
    )
    references = set(re.findall(r"\bF-\d{3}\b", text))
    assert references <= {f"F-{number:03d}" for number in range(1, 169)}
    for finding_id in ("F-163", "F-164", "F-165", "F-166", "F-167", "F-168"):
        assert finding_id in text
    GAP_BANK.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **162 findings** (`F-001` through `F-162`). Volume 45 added four findings: two B, one C, and one F-status bounded negative.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **168 findings** (`F-001` through `F-168`). The standalone pass added six findings: two B, three C, and one F-status bounded negative.",
        "state finding total",
    )
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-V45-RESEARCH-REPORT.md` records the completed 15-PDF boundary, close-read disposition, discovery and child-search method, cautions, and completion of the current journal stream.",
        "`COMMUNITIES-STANDALONE-RESEARCH-REPORT.md` records recovery, exact source verification, all eight close-read dispositions, six promoted findings, source cautions, and completion of the assigned primary corpus.",
        "state report",
    )
    corpus_anchor = "- M-0398's pre-extracted text ended at printed page 107; printed pages 108-113 were inspected directly from the source PDF and the affected ledger row records that access path."
    corpus_addition = "\n- All eight standalone sources were recovered locally and matched their inventoried Drive sizes and saved SHA-256 values: seven PDFs with verified page counts and one EPUB with valid ZIP structure. Each has nonempty extracted text. These copyrighted source files and full-text derivatives remain outside Git."
    if corpus_addition.strip() not in text:
        assert corpus_anchor in text
        text = text.replace(corpus_anchor, corpus_anchor + corpus_addition, 1)
    pending = re.compile(r"## Exact pending boundary\n\n.*?\n## Current evidence picture", re.DOTALL)
    pending_new = """## Exact pending boundary

- The assigned primary corpus is complete: **984 of 984 journal PDFs** across volumes 1-45 and **8 of 8 standalone substantive sources** have been triaged and dispositioned.
- No journal PDF or assigned standalone source remains. The next unit must be explicitly bounded: either verify the underlying or adjacent sources named in the gap bank, add a newly authorized corpus, or pause P0 for an owner decision.
- Article drafting or revision remains outside scope unless separately authorized.

## Current evidence picture"""
    text, count = pending.subn(pending_new, text, count=1)
    assert count == 1 or pending_new in text
    volume_sentence = "- Volume 45 adds: subgroup health outcomes and exposure controls that override communal-care reputation; explicit pooled catastrophic-health reserve rules with current-status and audit limits; planned fission with a scale trigger, fair member and asset division, independent successor finances, and mother-colony parity review; and the final journal-volume dangerous-child bounded null."
    standalone_sentence = "\n- The standalone pass adds: an explicit-separation-authority failure paired with a response-repertoire table; one role-specific childcare gate during provisional admission; a traditional-society example separating productive skill from allocation authority; a traditional-society conflict ladder spanning interruption, cooling, fission, and outside court; an internally graduated Amish discipline and reintegration process with a documented capture weakness; and the bounded standalone dangerous-child null."
    if standalone_sentence.strip() not in text:
        assert volume_sentence in text
        text = text.replace(volume_sentence, volume_sentence + standalone_sentence, 1)
    resume = re.compile(r"## Resume procedure\n\n.*?\n## Stop conditions", re.DOTALL)
    resume_new = """## Resume procedure

1. Do not repeat volumes 1-45 or the eight standalone sources; the assigned primary corpus is complete.
2. If an adjacent-source verification unit is authorized, select a bounded subset from the F-status leads in `COMMUNITIES-ARTICLE-GAP-BANK.md` and record access, provenance, and why it changes a live uncertainty.
3. Preserve the existing discovery, process-screening, close-read, disposition, ledger, gap-reconciliation, and verification sequence.
4. Keep traditional-society, clinical, legal, and intentional-community evidence separate until a transfer argument is made.
5. Add findings only for materially distinct evidence; corroboration and theory receive explicit non-promotion dispositions.
6. Update this state file after each bounded unit. Do not draft or revise article prose without separate authorization.

## Stop conditions"""
    text, count = resume.subn(resume_new, text, count=1)
    assert count == 1 or resume_new in text
    STATE.write_text(text, encoding="utf-8")


def update_readme() -> None:
    text = README.read_text(encoding="utf-8")
    replacements = [
        ("**162** evidence findings (`F-001` through `F-162`)", "**168** evidence findings (`F-001` through `F-168`)", "README finding total"),
        ("Journal stream: **complete, 984 of 984 PDFs**; eight standalone sources remain separate", "Primary assigned corpus: **complete, 984 journal PDFs plus 8 standalone sources**", "README corpus boundary"),
        ("The latest source-level account is [`recovered/COMMUNITIES-V45-RESEARCH-REPORT.md`](recovered/COMMUNITIES-V45-RESEARCH-REPORT.md).", "The latest source-level account is [`recovered/COMMUNITIES-STANDALONE-RESEARCH-REPORT.md`](recovered/COMMUNITIES-STANDALONE-RESEARCH-REPORT.md).", "README report"),
        ("With the exact local source corpus restored beneath `recovered/corpus-v45/`, run:", "With the exact local source corpora restored beneath `recovered/corpus-v45/` and `recovered/corpus-standalone/`, run:", "README verification intro"),
        ("python recovered/test_v45_workflow.py\npython recovered/verify_v45.py", "python recovered/test_standalone_workflow.py\npython recovered/verify_standalone.py", "README commands"),
        ("The verifier checks all 15 PDF hashes, page counts, and text extractions, the optional local source-container hash and ZIP integrity, inventory dispositions, sequential finding IDs, gap references, report coverage, cumulative counts, byte-for-byte preservation of the shared archive row, and completion of the 984-PDF journal boundary.", "The verifier checks all eight standalone source sizes and hashes, seven PDF page counts, EPUB integrity, nonempty extracted text, inventory dispositions, sequential finding IDs, gap references, discovery coverage, report coverage, cumulative counts, preservation of all non-standalone inventory rows, and completion of the 984-journal-plus-8-standalone boundary.", "README verifier scope"),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    README.write_text(text, encoding="utf-8")


def update_agents_and_index() -> None:
    text = AGENTS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(text, "python recovered/test_v45_workflow.py", "python recovered/test_standalone_workflow.py", "AGENTS tests")
    text = replace_once_or_confirm(text, "python recovered/verify_v45.py", "python recovered/verify_standalone.py", "AGENTS verifier")
    AGENTS.write_text(text, encoding="utf-8")
    text = INDEX.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "3. the latest `../recovered/COMMUNITIES-V*-RESEARCH-REPORT.md`",
        "3. the latest bounded report, currently `../recovered/COMMUNITIES-STANDALONE-RESEARCH-REPORT.md`",
        "index report",
    )
    INDEX.write_text(text, encoding="utf-8")


def validate_checkpoint() -> None:
    with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 168
    assert rows[-6:] == NEW_FINDINGS
    assert Counter(row["article_gap_status"] for row in rows[-6:]) == Counter(
        {"B": 2, "C": 3, "F": 1}
    )
    assert REPORT.is_file()
    report = REPORT.read_text(encoding="utf-8")
    assert "6 new findings, F-163 through F-168" in report


def main() -> None:
    ensure_ledger_findings()
    update_inventory()
    update_gap_bank()
    update_state()
    update_readme()
    update_agents_and_index()
    validate_checkpoint()
    print("updated standalone checkpoint")


if __name__ == "__main__":
    main()
