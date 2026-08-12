from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"


FIELDNAMES = [
    "finding_id", "track", "source_record_id", "source_file",
    "journal_volume_issue_year", "article_title", "author", "community_group",
    "page_locator", "printed_page_number", "supporting_excerpt", "source_access",
    "evidence_type", "exact_factual_observation", "what_source_establishes",
    "what_source_does_not_establish", "author_interpretation",
    "alternative_interpretation", "response_process", "outcome", "transferability",
    "article_gap_status", "likely_article_destination", "confidence",
    "external_verification_needed", "notes",
]


def row(*values: str) -> dict[str, str]:
    assert len(values) == len(FIELDNAMES), (len(values), len(FIELDNAMES))
    return dict(zip(FIELDNAMES, values))


NEW_ROWS = [
    row(
        "F-065", "Track A direct", "M-0520",
        "004-etienne-cabet-icaria-s-paradoxical-papa.pdf", "Vol. 22, no. 1 (2002)",
        "Etienne Cabet: Icaria's Paradoxical ‘Papa’", "Robert P. Sutton", "Icaria at Nauvoo",
        "PDF pp. 7-8; printed pp. 6-7", "6-7", "", "full text",
        "historical case study drawing on Icarian documents and later scholarship",
        "During the 1856 factional crisis, Cabet's supporters seized communal buildings and nearly strangled an opposition leader while Cabet watched. After a later school confrontation frightened children and drew townspeople's attention, outsiders called the sheriff, who restored order. The majority subsequently voted to expel Cabet and his supporters, listed charges publicly, and the factions separated amid food, clothing, equity, and dissolution disputes.",
        "A founder challenge reached an effective boundary only after factional violence, outside law enforcement, collective expulsion, and physical separation; delayed correction endangered people and communal assets.",
        "It does not independently adjudicate every factional allegation, show a neutral internal investigation, establish that the expulsion was procedurally fair, or isolate Cabet as the sole cause of collapse.",
        "The author presents Cabet as paradoxically democratic and authoritarian and treats his increasingly rigid leadership as central to Icaria's disintegration.",
        "The majority also used force and denied necessities; the episode was a civil conflict between organized factions rather than a simple community-versus-bad-founder case.",
        "Factional seizure, violence, sheriff intervention, majority expulsion vote, published charges, relocation, and dissolution filing followed in sequence; no neutral internal adjudicator appears.",
        "Cabet's faction left for St. Louis, Cabet died shortly afterward, and the Nauvoo community split; equity and dissolution remained contested.",
        "High for early founder-removal, violence-response, independent adjudication, protected necessities, and prewritten factional separation; zero for copying the historical expulsion process.",
        "C", "Founderism / fair separation / outside response / money and land", "high", "yes",
        "Verify the factional documents and legal dissolution history before naming violent conduct in article prose. DOI: https://doi.org/10.9707/0739-1250.1658",
    ),
    row(
        "F-066", "Track A procedural contrast", "M-0520",
        "004-etienne-cabet-icaria-s-paradoxical-papa.pdf", "Vol. 22, no. 1 (2002)",
        "Etienne Cabet: Icaria's Paradoxical ‘Papa’", "Robert P. Sutton", "Icaria at Nauvoo",
        "PDF pp. 6-7; printed pp. 5-6", "5-6", "", "full text",
        "historical case study drawing on Icarian documents and later scholarship",
        "The General Assembly tried two accused sexual-rule violators and expelled them with a ten-dollar allowance. In a later accusation, both accused denied intercourse, the Assembly acquitted them, and then evicted the two women who had reported the allegation for what it called vicious slander. Cabet responded by restricting recruitment of several broad marital-status categories.",
        "An internal assembly could reject an allegation instead of automatically punishing the accused, but it then severely punished the reporters and widened exclusion through category-based recruitment rules.",
        "It does not supply a transcript, evidence standard, notice, recusal, appeal, protection against retaliation, or enough information to determine whether either decision was correct.",
        "The author uses the episodes to illustrate Cabet's increasingly intrusive moral control and conflict with women.",
        "The reporters may have knowingly lied, and the recruitment change may have aimed to reduce recurring conflict; the source cannot distinguish justified sanction from retaliation.",
        "Accusation, testimony before the Assembly, acquittal, punishment of reporters, and broad recruitment restriction are described; independent review is absent.",
        "The accused remained; the reporters were evicted; later recruitment narrowed. Longer-term effects of this particular case are not reported.",
        "High for reporter protection, proportionate sanctions, appeal, and auditing category exclusions; low for judging the underlying allegation.",
        "B", "Fair separation / evidence protocol / membership pipeline", "medium", "yes",
        "Do not call the reporters malicious or the accused innocent beyond the Assembly's verdict without additional evidence. DOI: https://doi.org/10.9707/0739-1250.1658",
    ),
    row(
        "F-067", "Track A direct", "M-0527",
        "011-between-zion-and-babylon-the-application-of-the-total-institution-model-to-a-christian-charismatic-community-t.pdf",
        "Vol. 22, no. 1 (2002)",
        "Between Zion and Babylon: The Case of the Jesus Fellowship", "Stephen Hunt",
        "Jesus Fellowship / New Creation Christian Community", "PDF p. 12; printed p. 109", "109", "", "full text",
        "participant observation, movement literature, and sociological analysis",
        "The author reports that everyday dissidence was handled within the community house; unacceptable behavior drew a warning and ultimately an obligation to leave. Leaving also meant losing food, shelter, and clothing supplied through membership, while the outside world was framed as evil ‘Babylon’ and departure as equivalent to leaving the faith.",
        "A nominally voluntary warning-and-expulsion process can become coercive when the same institution controls necessities and defines exit as spiritual betrayal.",
        "It does not document a specific dangerous-member case, the content or number of warnings, evidence standards, appeal, emergency protection, or post-exit outcomes.",
        "The author applies a modified total-institution model and emphasizes moral compliance more than overt force.",
        "Members may have sincerely accepted covenant obligations and the community may have needed a final response to repeated disruption; loss of benefits alone does not prove unlawful coercion.",
        "Household handling, warning, and required departure are identified, but no independent adjudication or transition process is described.",
        "No case-specific outcome is supplied.",
        "High for separating necessities and faith from discipline, written thresholds, independent appeal, and funded safe exit; low for judging any individual sanction.",
        "C", "Fair separation / non-waivable rights / selecting legal couplings", "high", "yes",
        "The article predates later public investigations of the Jesus Fellowship; current and case-specific evidence is required before naming allegations. DOI: https://doi.org/10.9707/0739-1250.1665",
    ),
    row(
        "F-068", "Track A protective adaptation", "M-0527",
        "011-between-zion-and-babylon-the-application-of-the-total-institution-model-to-a-christian-charismatic-community-t.pdf",
        "Vol. 22, no. 1 (2002)",
        "Between Zion and Babylon: The Case of the Jesus Fellowship", "Stephen Hunt",
        "Jesus Fellowship / New Creation Christian Community", "PDF pp. 24 and 26; printed pp. 121 and 123", "121, 123", "", "full text",
        "participant observation, movement literature, and sociological analysis",
        "The fellowship developed several membership styles, allowing a person to change level of involvement without leaving the church; residential community members had become less than one-third of total membership. A note states that capital assets placed in the Community Trust Fund could be refunded when a member left.",
        "Graduated belonging and portable capital can turn an all-or-nothing exit into a reversible reduction of institutional exposure.",
        "It does not state exact refund rules, timeliness, independent valuation, whether debts or appreciation were included, or whether members could change status freely during conflict.",
        "The author sees differentiated membership as both an adaptation that supported growth and a dilution of residential communal distinctiveness.",
        "Membership tiers may also create unequal voice or a low-commitment periphery; the source does not evaluate that risk.",
        "Status change and asset refund are described as established options; no dispute case tests their practical availability.",
        "The movement persisted and grew while the residential core proportion declined.",
        "High for graduated membership, time-away options, and portable equity; requires precise contemporary contract design.",
        "B", "Membership pipeline / children and alumni / fair separation / money and land", "medium", "yes",
        "Verify historical trust documents and actual refund practice before treating the protection as proven. DOI: https://doi.org/10.9707/0739-1250.1665",
    ),
    row(
        "F-069", "Track A source-limited admission case", "M-0527",
        "011-between-zion-and-babylon-the-application-of-the-total-institution-model-to-a-christian-charismatic-community-t.pdf",
        "Vol. 22, no. 1 (2002)",
        "Between Zion and Babylon: The Case of the Jesus Fellowship", "Stephen Hunt",
        "Jesus Fellowship / New Creation Christian Community", "PDF pp. 22-23; printed pp. 119-120", "119-120", "", "full text",
        "participant observation, movement literature, and sociological analysis",
        "The author reports high turnover among newer non-community members and describes a weakly integrated faction of recruits with substance use or emotional difficulties who could be disruptive, steal, use the community temporarily for necessities, and leave. The established residential-member dropout rate was reported as under ten percent, versus thirty percent for baptized non-community members.",
        "High-need recruitment can produce real disruption and opportunistic use, but this source shows no conduct-specific assessment, graduated support plan, protection process, or tracked reintegration outcome.",
        "It does not establish diagnoses, danger, prevalence of theft, whether descriptions came from leaders or direct observation, or whether community conditions contributed to the behavior.",
        "The author treats the transitory constituency as an underlife that never consolidated into a stable counterculture.",
        "Leaders may have interpreted ordinary ambivalence, poverty, relapse, or unmet needs as opportunism; the language may reproduce class and mental-health stigma.",
        "Recruitment from the street, welfare provision, weak integration, disruption or theft, temporary residence, and departure are described in aggregate; no individual case review is supplied.",
        "High turnover continued while new recruitment still produced net growth.",
        "Moderate for staged admission, explicit capacity limits, individualized support, conduct-specific response, and non-stigmatizing outcome tracking.",
        "B", "Math of absorption / membership pipeline / fair separation", "medium", "yes",
        "Do not convert ‘emotionally disturbed,’ substance use, homelessness, or poverty into danger proxies. DOI: https://doi.org/10.9707/0739-1250.1665",
    ),
    row(
        "F-070", "Track A corrective-channel contrast", "M-0550",
        "009-the-male-work-ethic-was-busted-black-bear-ranch-1968-1974.pdf", "Vol. 23, no. 1 (2003)",
        "The Male Work Ethic Was Busted: Black Bear Ranch, 1968-1974", "Tim Hodgdon", "Black Bear Ranch",
        "PDF pp. 11 and 13-14; printed pp. 104 and 106-107", "104, 106-107", "", "full text",
        "historical analysis using interviews, participant writings, and archival material",
        "During a coercive anti-monogamy campaign, some members ignored the rule or complied only outwardly. General redefinition proceeded through what an insider called group decision-making and bullying in which the loudest faction often prevailed. Later, separate women's meetings built enough solidarity for women to challenge gendered labor; their organized pressure increased men's household work and changed some attitudes.",
        "Consensus-like whole-group processes can hide bullying and false compliance, while an autonomous affinity channel can give a subordinated group enough backing to correct a normalized harm.",
        "It does not quantify coercion, show that women's meetings were protected by a rule, establish durable correction across all domains, or provide a dangerous-person response process.",
        "The author argues that feminist and gay-liberation agitation materially shifted debate and practice despite incomplete results.",
        "The affinity group also contributed to factional conflict, and some changes may have come from broader social movements or individual maturation rather than its meetings alone.",
        "Resistance, hidden noncompliance, factional decision conflict, separate meetings, public challenge, and practical labor changes are documented; formal appeal or protection is not.",
        "Household labor became less gendered and some men reported changed attitudes, while sexual and relational conflict remained unresolved and the commune dispersed in 1974.",
        "High for protected caucuses, confidential dissent, anti-retaliation, and checking whether consensus reflects safe disagreement; low for direct dangerous-actor management.",
        "B", "Dissent / evidence channels / governance / relational practice", "high", "no",
        "Preserve the source's mixed result: useful correction arose inside a conflictual process and did not resolve every inequality. DOI: https://doi.org/10.9707/0739-1250.1558",
    ),
    row(
        "F-071", "Track A direct design", "M-0566",
        "009-searching-for-solidarity-in-uncharted-territory.pdf", "Vol. 24, no. 1 (2004)",
        "Searching for Solidarity in Uncharted Territory", "Lawrence Schein and Rose Schein", "Grasmere",
        "PDF pp. 3 and 9; printed pp. 112 and 118", "112, 118", "", "full text",
        "participant retrospective by two members with a 26-year communal archive",
        "Grasmere barred automatic inheritance of membership so adults would not be forced to accept mature children they considered disruptive and the children would not face a later rejection. New families underwent an interview, a weekend visit, and a six-month probation before mutual final admission; some were declined or withdrew over sharing, communication, intrusiveness, or diffuse authority.",
        "A community can protect belonging to family without turning kinship into automatic adult governance rights, and can use a mutual probationary process that produces observable conduct before admission.",
        "It does not define disruptive behavior, report an appeal, test malicious exclusion, or show that probation identifies skilled deceivers or future danger.",
        "The authors present these rules as pragmatic solutions for a multigenerational part-time community.",
        "Excluding adult children from ownership can also weaken their security and voice; financial barriers narrowed the applicant pool.",
        "Non-inheritance, preferred-guest status, staged interviews and visits, six-month probation, and mutual final choice formed the process.",
        "The commune operated for 26 years and dissolved unanimously; no dangerous-member test of the admission process is reported.",
        "High for separating family connection from governance rights and for staged mutual admission; low as proof of bad-faith screening efficacy.",
        "B", "Children / membership pipeline / money and land", "high", "no",
        "The phrase ‘disruptive’ is the authors' hypothetical criterion, not a documented case or diagnosis. DOI: https://doi.org/10.9707/0739-1250.1590",
    ),
    row(
        "F-072", "Track A direct design", "M-0566",
        "009-searching-for-solidarity-in-uncharted-territory.pdf", "Vol. 24, no. 1 (2004)",
        "Searching for Solidarity in Uncharted Territory", "Lawrence Schein and Rose Schein", "Grasmere",
        "PDF p. 8; printed p. 117", "117", "", "full text",
        "participant retrospective by two members with a 26-year communal archive",
        "For disputed business issues, every adult spoke in a go-round; strong disagreement led to deferral or a time-limited experiment followed by evaluation. Separate communal-living meetings addressed exclusion, anger, perceived unfairness, hurt, and rejection. Rotating chairs and secretaries and written minutes supported equal participation. The authors report these meetings usually restored relations but did not resolve bitterness over dissolution.",
        "Deferral, reversible trials, mandatory review, a separate relationship forum, role rotation, and durable records can reduce pressure to force premature consensus and preserve later audit.",
        "It does not show confidentiality, recusal, emergency safety procedures, independent appeal, protection from a determined bad actor, or success in the dissolution conflict.",
        "The authors call the meetings a safety valve aimed at behavior change without violating dignity.",
        "Frequent multi-hour meetings may favor stamina, status, or verbal skill, and apparent restored relations may include silent accommodation.",
        "Go-round, deferral or reversible experiment, evaluation, a separate living-conflict meeting, rotating facilitation, and minutes formed the process.",
        "Most routine conflicts were reported as resolved; dissolution left lingering bitterness.",
        "High for reversible decisions, scheduled review, procedural records, and separating operational from relational conflict; incomplete for severe danger.",
        "B", "Governance / conflict architecture / evidence protocol", "high", "no",
        "Do not generalize from a small, affluent, part-time kin-based community to a residential high-risk setting without stress tests. DOI: https://doi.org/10.9707/0739-1250.1590",
    ),
    row(
        "F-073", "Track A governance challenge", "M-0561",
        "004-god-and-gender-structures-of-opportunity-in-an-american-yogic-community.pdf", "Vol. 24, no. 1 (2004)",
        "God and Gender: Structures of Opportunity in an American Yogic Community", "Susan Love Brown", "Ananda Village",
        "PDF pp. 12-14 and 20; printed pp. 11-13 and 19", "11-13, 19", "", "full text",
        "participant observation, leader interviews, community survey, and retrospective update",
        "Ananda had an elected Village Council and committees, but an informal council directed both legal entities and constituted the highest authority. Founder Kriyananda held exceptional authority; longevity, service, positive attitude, spiritual progress, and attunement with him helped determine power. The article later notes a costly sexual-harassment scandal but does not describe its handling.",
        "Formal elected bodies can coexist with a shadow authority system whose spiritual status tests and founder exception control consequential decisions.",
        "It does not establish that the informal council caused or mishandled harassment, identify complainants, give legal findings, or show that every decision bypassed elected governance.",
        "The author emphasizes women's access to leadership while acknowledging founder exception and informal control.",
        "The informal council may have supplied expertise and continuity, and women shared many senior positions; the scandal reference alone cannot establish governance failure.",
        "Elected governance, committees, counseling by managers, informal supreme direction, and founder exception are described; the allegation-response process is absent.",
        "The community survived lawsuits and a costly harassment scandal, expanded geographically, and changed formal spiritual leaders while Kriyananda remained its spiritual center.",
        "High for mapping practical authority, rejecting longevity or attunement as safety proxies, and routing founder allegations outside informal spiritual control.",
        "C", "Founderism / governance / evidence channels / safety proxies", "high", "yes",
        "Verify the harassment litigation and later governance changes independently before naming the case in article prose. DOI: https://doi.org/10.9707/0739-1250.1630",
    ),
    row(
        "F-074", "Track A source-method warning", "M-0579",
        "006-basic-sense-the-more-philosophy-of-victor-baranco-and-the-institute-of-human-abilities.pdf", "Vol. 25, no. 1 (2005)",
        "Basic Sense: The More Philosophy of Victor Baranco and the Institute of Human Abilities", "Laurie Rivlin Heller", "Morehouse / Institute of Human Abilities",
        "PDF pp. 9 and 12; printed pp. 36 and 39", "36, 39", "", "full text",
        "historical and interpretive synthesis using movement publications, courses, journalism, and secondary sources",
        "Morehouse trained non-therapists to lead intense encounter exercises and framed participants as able to lie, answer, or refuse while the leader manipulated emotional highs and lows. Its philosophy also taught that perceived deprivation reflected a victim stance and that individuals create their experience. The article supplies no participant-harm case or independent outcome study for these practices.",
        "Peer-led transformational practice can combine unqualified authority, deliberately intensified emotion, and a worldview that makes harmed people responsible for their own experience.",
        "It does not establish coercion in each group, diagnose the founder, show that refusal was punished, quantify harm, or prove that the philosophy caused later casualties mentioned generally by the author.",
        "The author interprets the movement as secular religion and argues that relativism and weak social controls contributed to failure.",
        "Participants may have experienced the exercises as voluntary education, and the article's later cultural critique is polemical and relies heavily on secondary commentary.",
        "Training and group exercises are described, but licensing, screening, confidentiality, adverse-event response, and independent review are not.",
        "The organization declined as many participants aged and returned to conventional lives; no practice-specific outcome is established.",
        "Moderate for a firewall between peer care and governance, competent supervision, informed consent, stop rights, adverse-event review, and rejection of victim-blaming.",
        "B", "Community as therapist / non-waivable rights / safety and evidence", "medium", "yes",
        "Use as a mechanism warning, not proof of abuse or therapeutic inefficacy. DOI: https://doi.org/10.9707/0739-1250.1575",
    ),
    row(
        "F-075", "Track A child context", "M-0583",
        "010-dating-and-educational-behaviors-of-hutterian-youth.pdf", "Vol. 25, no. 1 (2005)",
        "Dating and Educational Behaviors of Hutterian Youth", "Suzanne R. Smith and Bron B. Ingoldsby", "Hutterite colonies",
        "PDF pp. 3, 5, and 12; printed pp. 114, 116, and 123", "114, 116, 123", "", "full text",
        "ethnographic synthesis and a small survey of outside teachers",
        "The article says authority figures control children's conduct through praise and punishment, including corporal punishment by German teachers acting with parental authority. It reports serious youth violence and drug use as practically nonexistent while minor rule-breaking was unofficially tolerated. Some outside teachers described lying, cheating, or stealing as wrong mainly when detected and expected children to reproduce the discipline they had experienced.",
        "A punishment-centered system may suppress visible serious misconduct while leaving moral reasoning externalized around authority and detection; low observed violence does not validate the discipline model.",
        "It does not measure violence prevalence, verify every teacher claim, establish effects of corporal punishment, document a persistently dangerous child, or provide allegation-to-outcome cases.",
        "The authors use Kohlbergian moral-development theory and suggest restrictive parenting may intensify some rebellion.",
        "Outside teachers may misunderstand Hutterite moral reasoning, and low serious violence may reflect strong peer monitoring, cohesion, opportunity limits, or underreporting.",
        "Adult and peer monitoring, punishment, tolerated minor deviation, and detection-based correction are described in aggregate; assessment, review, and individual outcomes are absent.",
        "Serious violence and drug use were reported as rare; some young men left and minor covert violations persisted.",
        "Moderate for distinguishing behavioral suppression from internalized accountability and requiring nonviolent discipline, confidential reporting, and independent child advocacy.",
        "B", "Children / school / discipline / safety metrics", "medium", "yes",
        "Historical and culturally specific evidence; current safeguarding standards and direct Hutterite perspectives are required before recommendation. DOI: https://doi.org/10.9707/0739-1250.1579",
    ),
    row(
        "F-076", "Track A child negative result", "", "Volumes 21-25 discovery corpus",
        "Volumes 21-25 (2001-2005)", "Cumulative targeted search and issue-by-issue discovery scan", "Research checkpoint",
        "Communal Societies volumes 21-25", "97 PDFs; 28 relevant or contextual close reads", "", "", "full extracted corpus",
        "systematic bounded search result",
        "Across all 97 PDFs, complete title triage, targeted vocabulary search, proximity inspection, and relevant-source close reads found youth violence described as rare, ordinary rule-breaking and theft, corporal punishment, peer monitoring, child autonomy, and children exposed to adult factional conflict. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        "The specified dangerous-child evidence pattern is absent from this completed chunk under the recorded search and close-read procedure.",
        "It does not prove that no such case exists in volumes 26-45, standalone sources, different terminology, unpublished records, or communities outside the journal.",
        "Not applicable.",
        "The journal may avoid private child cases, describe them euphemistically, or route them into education, medicine, juvenile law, family history, or book-length sources.",
        "Not applicable.", "Bounded null for volumes 21-25.",
        "High for this chunk; none for the full literature until remaining sources and standalone books are processed.",
        "F", "Research/school function / dangerous-child branch", "high", "no",
        "Child victims, ordinary rebellion, aggregate claims, adult danger near child terms, and punishment without a dangerous-child actor were excluded.",
    ),
]


with LEDGER.open(newline="", encoding="utf-8-sig") as handle:
    existing = list(csv.DictReader(handle))
ids = {r["finding_id"] for r in existing}
assert ids.isdisjoint(r["finding_id"] for r in NEW_ROWS), "new finding IDs already present"
with LEDGER.open("a", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
    writer.writerows(NEW_ROWS)


with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
    inventory_rows = list(csv.DictReader(handle))
    inventory_fields = handle.readline if False else None
fieldnames = list(inventory_rows[0])
count = 0
for item in inventory_rows:
    if item["record_type"] == "archive_pdf" and item["volume"].isdigit() and 21 <= int(item["volume"]) <= 25:
        kind = item["notes"].removeprefix("kind=")
        if kind in {"front_matter", "contents", "table_of_contents", "editorial", "back_matter"}:
            item["research_status"] = "metadata triaged"
        elif item["record_id"] in {r["source_record_id"] for r in NEW_ROWS if r["source_record_id"]}:
            item["research_status"] = "close read; finding promoted"
        else:
            item["research_status"] = "title and keyword triaged"
        count += 1
assert count == 97, count
with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(inventory_rows)


text = GAP_BANK.read_text(encoding="utf-8")
text = text.replace("Checkpoint: *Communal Societies* volumes 1-20", "Checkpoint: *Communal Societies* volumes 1-25")
text = text.replace("After reconciling the volume 16-20 findings", "After reconciling the volume 21-25 findings")
updates = {
    "F-050, F-051, F-053, F-061 |": "F-050, F-051, F-053, F-061, F-065, F-066, F-067 |",
    "F-007, F-008, F-056, F-057, F-063 |": "F-007, F-008, F-056, F-057, F-063, F-074 |",
    "F-050, F-055, F-061 |": "F-050, F-055, F-061, F-065, F-070, F-073 |",
    "F-052, F-061, F-063 |": "F-052, F-061, F-063, F-065, F-073 |",
    "F-051, F-056, F-057, F-063 |": "F-051, F-056, F-057, F-063, F-067, F-074, F-075 |",
    "F-056, F-058, F-059, F-060, F-063 |": "F-056, F-058, F-059, F-060, F-063, F-067, F-070, F-073 |",
    "F-016, F-018, F-043, F-044, F-051 |": "F-016, F-018, F-043, F-044, F-051, F-068, F-071 |",
    "F-017, F-043, F-049 |": "F-017, F-043, F-049, F-071, F-075 |",
    "F-019, F-033, F-045, F-059, F-060 |": "F-019, F-033, F-045, F-059, F-060, F-066, F-069, F-071 |",
    "F-020, F-061 |": "F-020, F-061, F-072 |",
    "F-054, F-061 |": "F-054, F-061, F-065, F-068, F-071 |",
    "F-053, F-057, F-062 |": "F-053, F-057, F-062, F-065, F-067, F-075 |",
    "F-013, F-028 |": "F-013, F-028, F-069 |",
    "F-024, F-025, F-026, F-033 |": "F-024, F-025, F-026, F-033, F-069 |",
    "F-060, F-063 |": "F-060, F-063, F-066, F-069, F-071, F-073, F-075 |",
}
for old, new in updates.items():
    assert old in text, old
    text = text.replace(old, new, 1)
text = text.replace(
    "The volume 1-20 dangerous-child searches (F-031, F-048, F-064)",
    "The volume 1-25 dangerous-child searches (F-031, F-048, F-064, F-076)",
)
text = text.replace(
    "- **F status:** current interest in intentional community requires contemporary evidence; the historical corpus only establishes earlier waves.",
    "- **F status:** verify Icaria's factional violence and dissolution in primary records before naming it; the article establishes the mechanism but represents competing factions through a secondary synthesis.\n"
    "- **F status:** retrieve the Jesus Fellowship's historical trust rules and later official investigation record before treating graduated membership, refunds, or warnings as effective safeguards.\n"
    "- **F status:** verify Ananda's harassment litigation and later governance changes before connecting the scandal to the informal council or founder exception.\n"
    "- **F status:** current interest in intentional community requires contemporary evidence; the historical corpus only establishes earlier waves.",
)
GAP_BANK.write_text(text, encoding="utf-8")

print(f"appended={len(NEW_ROWS)} inventory_updated={count}")
