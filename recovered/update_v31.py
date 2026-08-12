#!/usr/bin/env python3
"""Apply the completed volume 31 checkpoint to the durable research artifacts."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"


def finding(**values: str) -> dict[str, str]:
    fields = [
        "finding_id",
        "track",
        "source_record_id",
        "source_file",
        "journal_volume_issue_year",
        "article_title",
        "author",
        "community_group",
        "page_locator",
        "printed_page_number",
        "supporting_excerpt",
        "source_access",
        "evidence_type",
        "exact_factual_observation",
        "what_source_establishes",
        "what_source_does_not_establish",
        "author_interpretation",
        "alternative_interpretation",
        "response_process",
        "outcome",
        "transferability",
        "article_gap_status",
        "likely_article_destination",
        "confidence",
        "external_verification_needed",
        "notes",
    ]
    row = {field: "" for field in fields}
    row.update(values)
    return row


NEW_FINDINGS = [
    finding(
        finding_id="F-101",
        track="Track A tested founder removal versus asset control",
        source_record_id="M-0759",
        source_file="004-zion-city-a-theocratic-municipality-with-a-coda-on-ave-maria.pdf",
        journal_volume_issue_year="Vol. 31, no. 2 (2011)",
        article_title="Zion City: A Theocratic Municipality, With a Coda on Ave Maria",
        author="Holly Folk",
        community_group="Christian Catholic Apostolic Church / Zion City",
        page_locator="PDF pp. 5-7; printed pp. 4-6",
        printed_page_number="4-6",
        source_access="full text",
        evidence_type="historical synthesis using church, municipal, dissertation, press, and local-history sources",
        exact_factual_observation="After the author reports financial mismanagement and rumors of sexual misconduct and proposed polygamy, John Alexander Dowie was deposed and ninety-five percent of church members voted to accept Wilbur Glenn Voliva as General Overseer. All church and Zion Industries assets had nevertheless been held in Dowie's name. Dowie sued over their transfer and the already-troubled businesses entered receivership. Between 1908 and 1911, adherents donated watches and jewelry and mortgaged their homes to finance reacquisition; the church also assumed a million-dollar mortgage. That mortgage remained a burden when the enterprises entered receivership again in 1933.",
        what_source_establishes="A founder-removal vote can work as a governance event while failing as an asset-control event. A practical override must automatically reach title, accounts, debt, contracts, and litigation authority without forcing members to repurchase common institutions through personal sacrifice.",
        what_source_does_not_establish="It does not prove the sexual rumors, establish every cause of Dowie's removal, show that the referendum was independently administered, quantify individual voluntariness in the asset drive, or show that the old mortgage alone caused the 1933 receivership.",
        author_interpretation="The author treats the removal and institutional reacquisition as evidence of an atypically resilient congregation whose commitment could survive a disgraced founder.",
        alternative_interpretation="The donations and mortgages may reflect genuine voluntary solidarity, while creditors, the Great Depression, business conditions, and later leadership decisions—not only founder title—shaped the two receiverships.",
        response_process="Founder deposition; member referendum; founder lawsuit; receivership; member donations and home mortgages; institutional reacquisition with a large mortgage; later receivership.",
        outcome="The founder lost office and the church recovered most assets, but only after receivership and member-financed reacquisition; inherited debt remained a later vulnerability.",
        transferability="High for pairing every removal clause with entity-owned title, automatic signatory transition, member-visible records, debt limits, litigation control, and a continuity plan that does not depend on emergency member pledges.",
        article_gap_status="B",
        likely_article_destination="Founderism / tested override / money and land",
        confidence="high",
        external_verification_needed="yes",
        notes="Confidence is high in the structural sequence, not in the misconduct rumors. DOI: https://doi.org/10.9707/0739-1250.1358",
    ),
    finding(
        finding_id="F-102",
        track="Track A migration of private sanctions into public institutions",
        source_record_id="M-0759",
        source_file="004-zion-city-a-theocratic-municipality-with-a-coda-on-ave-maria.pdf",
        journal_volume_issue_year="Vol. 31, no. 2 (2011)",
        article_title="Zion City: A Theocratic Municipality, With a Coda on Ave Maria",
        author="Holly Folk",
        community_group="Christian Catholic Apostolic Church / Zion City",
        page_locator="PDF pp. 7-10; printed pp. 6-9",
        printed_page_number="6-9",
        source_access="full text",
        evidence_type="historical synthesis using municipal codes, dissertations, court and press records, and church sources",
        exact_factual_observation="Christian Catholic Church members usually voted as a bloc. A contemporary observer saw no routine immediate compulsion but said Voliva's appeals functioned as instructions and his advice as commands, and believed critical disloyalty could bring suspension or expulsion. By 1914 Theocrats controlled the school board, city court, mayoralty, and nearly every local seat; Voliva held no office but selected electoral slates. The city enacted church-derived restrictions on tobacco, medicine, Sunday opening, pork, dress, and other conduct. Independents obtained an injunction against the tobacco ordinance, but Theocratic leaders declined to press the constitutional issue and left the code in place for church members. Later court records showed police arresting and fining outsider motorists for smoking while generally avoiding confrontations with residents.",
        what_source_establishes="A community's private sanction system can migrate into municipal law through bloc voting, candidate control, and overlapping personnel. Formal elections, sincere shared belief, nominal noncoercion, and inconsistent enforcement do not by themselves make the resulting power independent; an unlitigated or selectively enforced rule can still discipline members.",
        what_source_does_not_establish="It does not show that every vote was coerced, every officeholder lacked independence, every ordinance was unlawful, every member complied from fear, or the selective-enforcement pattern's frequency. It is not a statement of current constitutional law.",
        author_interpretation="The author describes a theocratic municipality in which religious adherents used civic infrastructure to apply church standards beyond the congregation, while noting sincere belief, partial nonenforcement, and some shared norms among opponents.",
        alternative_interpretation="Many residents may have freely supported the rules as ordinary local moral or health regulation; uneven enforcement and Independent agreement with some goals may indicate negotiated community norms as well as capture.",
        response_process="Bloc voting; leader-selected slates; overlapping church and municipal office; enactment of religious rules as ordinances; outsider challenge and injunction; strategic nonlitigation; selective police enforcement.",
        outcome="Church standards gained public-law reach and remained operative inside the membership even when their enforceability was contested; enforcement differed between outsiders and residents.",
        transferability="High for prohibiting leader control of public or quasi-public slates, requiring conflict disclosure and recusal, preserving independent courts and schools, auditing member/nonmember enforcement, and testing every external institution for capture rather than assuming public status equals independence.",
        article_gap_status="C",
        likely_article_destination="Founderism / non-waivable rights / selecting legal couplings",
        confidence="high",
        external_verification_needed="yes",
        notes="The finding concerns institutional control and enforcement, not the merits of any one tobacco, health, or Sunday rule. DOI: https://doi.org/10.9707/0739-1250.1358",
    ),
    finding(
        finding_id="F-103",
        track="Track A resident continuity and practical counter-power",
        source_record_id="M-0759",
        source_file="004-zion-city-a-theocratic-municipality-with-a-coda-on-ave-maria.pdf",
        journal_volume_issue_year="Vol. 31, no. 2 (2011)",
        article_title="Zion City: A Theocratic Municipality, With a Coda on Ave Maria",
        author="Holly Folk",
        community_group="Christian Catholic Apostolic Church / Zion City",
        page_locator="PDF pp. 5-6 and 13-15; printed pp. 4-5 and 12-14",
        printed_page_number="4-5, 12-14",
        source_access="full text",
        evidence_type="historical synthesis using municipal, church, press, dissertation, and local-history sources",
        exact_factual_observation="Some Doweites who opposed Voliva could not or did not leave their homes, jobs, and family ties. They left the church, remained in Zion, formed Grace Missionary Church, and joined a loose Independent coalition. In 1934 the Theocratic slate lost the school-board election for the first time in twenty-three years. Voliva retaliated by closing the parochial school to flood the public system with students, then quickly reversed. Residents won Sunday bus service by petition and elected an Independent judge. In 1935 six of seven Theocratic candidates lost and church members voted Voliva out as General Overseer. Leader removal did not erase shared norms: the incoming mayor promised to retain blue laws, voters kept the city dry, and a later purified-film ordinance was used against Voliva's own apocalyptic screenings.",
        what_source_establishes="Dissenters who can separate religious membership from residence, livelihood, family, association, and civic voice can become a durable counter-constituency. Petition, elections, parallel congregations, and the ability to withstand and reverse retaliation supplied a practical override; removing the leader did not automatically remove institutionalized norms or prevent old tools from being repurposed.",
        what_source_does_not_establish="It does not show that the counter-coalition was always peaceful or inclusive, that elections alone caused Voliva's fall, that every retaliatory act was unlawful, that the new order protected all rights, or that the surviving norms were imposed rather than broadly preferred.",
        author_interpretation="The author argues that the civic form which let the church extend its standards also made its domination vulnerable when demographics and voting blocs changed.",
        alternative_interpretation="The Depression, inherited debt, generational change, declining attendance, rival evangelists, and elite defections also weakened Voliva. Continuing blue laws may reflect stable resident preference rather than residual capture.",
        response_process="Internal dissent and congregational split; continued residence; coalition formation; petition; school-board and judicial elections; leader retaliation and reversal; municipal electoral defeat; church vote removing the overseer; later reuse of inherited ordinance power.",
        outcome="The Theocratic coalition lost municipal and church control without a new mass exodus, while several moral regulations and local sensibilities persisted beyond the leader.",
        transferability="High for separating membership from housing and livelihood, protecting dissenters' continued residence and association, preserving parallel institutions and neutral civic routes, and measuring policy persistence separately from leader replacement.",
        article_gap_status="B",
        likely_article_destination="Founderism / protected dissent / forks and continuity",
        confidence="high",
        external_verification_needed="yes",
        notes="The article reports a 1911 riot injuring more than fifty people; the positive mechanism is not the factional conflict but the later lawful counter-power. DOI: https://doi.org/10.9707/0739-1250.1358",
    ),
    finding(
        finding_id="F-104",
        track="Track A child custody, external standing, and admission rules",
        source_record_id="M-0749",
        source_file="010-review-of-the-great-divorce-a-nineteenth-century-mother-s-extraordinary-fight-against-her-husband-the-shakers.pdf",
        journal_volume_issue_year="Vol. 31, no. 1 (2011)",
        article_title="Review of The Great Divorce: A Nineteenth Century Mother's Extraordinary Fight Against Her Husband, the Shakers, and Her Times",
        author="Marlyn McGary Klee",
        community_group="United Society of Believers / Shakers; Chapman family",
        page_locator="PDF pp. 3-6; printed pp. 96-99",
        printed_page_number="96-99",
        source_access="full text",
        evidence_type="book review of a primary-source-based historical narrative",
        exact_factual_observation="After Eunice Chapman rejected Shakerism, her husband James took their three children to Watervliet with a Shaker team, wagon, and men. The Shakers protected James's patriarchal custody claim, hid the children, and moved them from New York to New Hampshire while Eunice had virtually no legal standing. Over five years she obtained a private divorce act restoring civil standing, lobbied legislators, published and sold her account, organized public support, recovered her eldest child with threatening townspeople present, and later received the two daughters when the Shakers relinquished them. The review says Mother Lucy Wright subsequently directed that no children be admitted unless both parents joined.",
        what_source_establishes="A community cannot treat one adult's claimed authority as sufficient child-admission or relocation authority while hiding the child from another lawful claimant. External standing, public scrutiny, and an admission rule attentive to both parents emerged only after a prolonged custody conflict; modern design requires verified lawful consent and independent child representation before crisis.",
        what_source_does_not_establish="It does not resolve every legal maneuver, establish a court custody order, record the children's independent wishes, prove why leaders returned them or changed the rule, show how consistently the rule was applied, or make threatening crowds and unilateral retrieval a safe model. Requiring both parents to join is not a modern rule for cases involving abuse, absence, or altered legal custody.",
        author_interpretation="The reviewer says the Shakers materially supported James despite later calling the matter private and suggests adverse publicity and political turmoil may have made retention institutionally untenable, while noting that no leadership decision record survives.",
        alternative_interpretation="Shaker leaders may have sincerely understood contemporary paternal custody law to favor James and may have changed course from legal, child-welfare, pragmatic, or reputational motives that the record cannot separate.",
        response_process="Parent-assisted child removal; community concealment and interstate relocation; lobbying and publication; private divorce legislation; public organizing; confrontation and retrieval of one child; voluntary return of two children; subsequent child-admission rule change.",
        outcome="All three children returned to Eunice; another mother in a similar conflict did not regain hers. The Shakers announced a stricter admission rule, though later accepted orphaned and abandoned children.",
        transferability="High in principle for verifying custody and consent, preserving contact and location records, appointing an independent child advocate, prohibiting concealment across jurisdictions, and preselecting external review; low for the era-specific legislation and crowd confrontation.",
        article_gap_status="C",
        likely_article_destination="Children / protected contact / external legal boundary",
        confidence="medium",
        external_verification_needed="yes",
        notes="Review-level evidence; retrieve the book and underlying legal and Shaker records before naming the case as a policy precedent. DOI: https://doi.org/10.9707/0739-1250.1348",
    ),
    finding(
        finding_id="F-105",
        track="Track A child negative result",
        source_file="Volume 31 discovery corpus",
        journal_volume_issue_year="Volume 31 (2011)",
        article_title="Cumulative targeted search and issue-by-issue discovery scan",
        author="Research checkpoint",
        community_group="Communal Societies volume 31",
        page_locator="31 PDFs; 16 relevant or contextual close reads; 10 child-danger proximity candidates",
        source_access="full extracted corpus",
        evidence_type="systematic bounded search result",
        exact_factual_observation="Across all 31 PDFs, complete title triage, six-family keyword scoring, five-family process screening, child-danger proximity inspection, and 16 relevant or contextual close reads found children as massacre victims, dependents in disrupted families, students, recipients of high-risk-youth services, objects of adult custody conflict, relatives near adult sexual-misconduct allegations, childhood subjects, or OCR and metaphor proximity. No source documented a persistently dangerous child as actor together with allegation, assessment, intervention, review, and later outcome.",
        what_source_establishes="The specified dangerous-child evidence pattern is absent from volume 31 under the recorded search, proximity, exclusion, and close-read procedure.",
        what_source_does_not_establish="It does not prove that no such case exists in volumes 32-45, standalone sources, different terminology, unpublished records, book-length sources, juvenile, educational, medical, or family records, or communities outside the journal.",
        author_interpretation="Not applicable.",
        alternative_interpretation="Privacy, euphemism, aggregate reporting, source destruction, and routing into other professional or family systems may hide relevant cases from a communal-history journal.",
        response_process="Not applicable.",
        outcome="Bounded null for volume 31.",
        transferability="High for this completed unit; none for the full literature until the remaining journal and standalone sources are processed.",
        article_gap_status="F",
        likely_article_destination="Research/school function / dangerous-child branch",
        confidence="high",
        external_verification_needed="no",
        notes="The cumulative bounded null now covers volumes 1-31. Children harmed or governed by adults and youth-service recipients were excluded from the child-as-dangerous-actor result.",
    ),
]


def update_ledger() -> None:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames == list(NEW_FINDINGS[0]), "ledger schema changed"
    expected_tail = [f"F-{number:03d}" for number in range(101, 106)]
    if len(rows) == 105 and [row["finding_id"] for row in rows[-5:]] == expected_tail:
        rows = rows[:100]
    assert len(rows) == 100 and rows[-1]["finding_id"] == "F-100", "unexpected ledger checkpoint"
    all_rows = rows + NEW_FINDINGS
    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)


CLOSE_IDS = {
    "M-0743", "M-0744", "M-0745", "M-0746", "M-0747", "M-0749",
    "M-0754", "M-0759", "M-0760", "M-0761", "M-0762", "M-0763",
    "M-0764", "M-0765", "M-0768", "M-0769",
}

PROMOTED_IDS = {"M-0749", "M-0759"}
METADATA_KINDS = {"front_matter", "contents", "editorial", "back_matter"}


def update_inventory() -> None:
    with INVENTORY.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames
        rows = list(reader)
    assert fieldnames is not None
    dispositions: Counter[str] = Counter()
    seen: set[str] = set()
    for row in rows:
        if row["record_id"] == "D-012":
            row["research_status"] = "container processed; 31 member PDFs triaged"
            row["local_path"] = "recovered/vol31.zip"
            row["notes"] = "Drive inventory row; archive downloaded, integrity-tested, and processed; 31 members follow"
        if row["record_type"] != "archive_pdf" or row["volume"] != "31":
            continue
        record_id = row["record_id"]
        seen.add(record_id)
        kind = row["notes"].removeprefix("kind=")
        if record_id in PROMOTED_IDS:
            status = "close read; finding promoted"
            disposition = "promoted"
        elif record_id in CLOSE_IDS:
            status = "contextual close read; no distinct finding"
            disposition = "contextual"
        elif kind in METADATA_KINDS:
            status = "metadata triaged"
            disposition = "metadata"
        else:
            status = "title and keyword triaged"
            disposition = "title"
        row["text_extraction_status"] = "extracted"
        row["research_status"] = status
        row["local_path"] = f"recovered/corpus-v31/{row['internal_filename']}"
        row["text_path"] = f"recovered/corpus-v31/{row['internal_filename'][:-4]}.txt"
        dispositions[disposition] += 1
    assert len(seen) == 31, f"expected 31 volume 31 records, got {len(seen)}"
    assert dispositions == Counter({"contextual": 14, "metadata": 8, "title": 7, "promoted": 2}), dispositions
    with INVENTORY.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


GAP_ADDITIONS = {
    "G-003": (
        "Protected dissent also needs an option to remain resident and organize through parallel institutions; a child-custody dispute needs outside standing before publicity or confrontation becomes the only route.",
        ["F-103", "F-104"],
    ),
    "G-004": (
        "A successful removal vote must reach titled assets and debt, while the capture audit must also cover candidate slates, municipal offices, schools, courts, and quasi-public districts.",
        ["F-101", "F-102", "F-103"],
    ),
    "G-005": (
        "Non-waivable rights must bind municipal or quasi-public enforcement captured by a community majority, not only private membership sanctions; child location and lawful family contact cannot be internal secrets.",
        ["F-102", "F-104"],
    ),
    "G-006": (
        "Measure policy persistence separately from leader replacement: the leader can lose office while inherited norms and enforcement tools remain and are repurposed.",
        ["F-103"],
    ),
    "G-007": (
        "A cohesive voting bloc and sincere shared belief do not establish free choice or safety when leader advice functions as command and expulsion remains available.",
        ["F-102"],
    ),
    "G-008": (
        "For minor children, the outward door begins with verified lawful custody and consent, preserved contact and location records, and an independent route when adults disagree.",
        ["F-104"],
    ),
    "G-009": (
        "Collective childrearing also requires lawful authority for admission and relocation plus independent child representation before the community becomes a party to a custody contest.",
        ["F-104"],
    ),
    "G-012": (
        "Founder removal is incomplete while common assets remain in personal title; plan automatic control transition and debt limits that do not require members to mortgage homes to recover their own institutions.",
        ["F-101"],
    ),
    "G-013": (
        "Map capture risk inside municipal boards, courts, schools, police, and special districts: public or quasi-public status is not independence. Child custody and interstate relocation require their own external review path.",
        ["F-102", "F-104"],
    ),
    "G-016": (
        "Let dissenters separate membership from residence, form parallel associations, and use shared civic channels; compulsory geographic exit destroys the counter-constituency that may later correct capture.",
        ["F-103"],
    ),
    "G-018": (
        "Volume 31 again found no evidence validating inner work or long exposure as a dangerous-person filter.",
        ["F-102", "F-105"],
    ),
}


NEW_VERIFICATION_BULLETS = """- **F status:** verify Zion City's 1907 referendum, asset title and receiverships, ordinances, injunction, selective enforcement, 1934-1935 elections, and church ouster in the underlying records before treating the article's synthesis as a legal or governance precedent; the Ave Maria coda is a 2011 snapshot and supplies no current-status claim.
- **F status:** retrieve *The Great Divorce* and inspect the private legislation, custody and indenture record, Shaker correspondence, and child-admission directive before using the Chapman sequence as a safeguarding precedent.
"""


NEW_NONPROMOTIONS = """- Amana's 1932 committee, large-majority vote, church-business separation, stock allocation, wages, outside manager, and later return migration materially corroborate F-080 and the success-dashboard gaps but do not create a distinct finding.
- *City Communes in Israel* supplies a 2009 map of small-group federation, mutual aid, service NGOs, and movement replication, but no dangerous-actor case or independent outcome audit; F-023 and G-016 already carry the continuity principle.
- *Thickened Light* is an insider document praising Charles Dederich while omitting Synanon's documented violence; it is not evidence that leader-centered trust positions or learning practices constrained the founder.
- The volume 31 Love Israel review does not establish rape or sexual-misconduct allegations and adds no process beyond the stronger existing Love Israel finding F-061.
- The Ave Maria coda remains a historical 2011 comparison, not evidence of present governance, policy, leadership, finances, or resident views.
- The Chapman finding is not a recommendation for threatening crowds, unilateral child retrieval, or a universal rule that both parents must join; its transferable elements are lawful custody verification, preserved contact, independent child representation, and external review.
- The comparative millennial-movement article concerns external political conflict and accommodation, not an internal dangerous-person protocol.
"""


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = text.replace(
        "Checkpoint: *Communal Societies* volumes 1-30",
        "Checkpoint: *Communal Societies* volumes 1-31",
    )
    text = text.replace(
        "After reconciling the volume 29-30 findings rather than inflating the list",
        "After reconciling the volume 31 findings rather than inflating the list",
    )
    lines = text.splitlines()
    seen: set[str] = set()
    for index, line in enumerate(lines):
        if not line.startswith("| G-"):
            continue
        parts = line.split("|")
        gap_id = parts[1].strip()
        if gap_id not in GAP_ADDITIONS:
            continue
        sentence, references = GAP_ADDITIONS[gap_id]
        if sentence not in parts[4]:
            parts[4] = parts[4].rstrip() + " " + sentence + " "
        evidence = parts[7].strip()
        for reference in references:
            if reference not in {item.strip() for item in evidence.split(",")}:
                evidence += ", " + reference
        parts[7] = " " + evidence + " "
        if gap_id == "G-018":
            parts[4] = parts[4].replace("through volume 30", "through volume 31")
        lines[index] = "|".join(parts)
        seen.add(gap_id)
    assert seen == set(GAP_ADDITIONS), f"missing gap rows: {set(GAP_ADDITIONS) - seen}"
    text = "\n".join(lines) + "\n"
    if "verify Zion City's 1907 referendum" not in text:
        text = text.replace("\n## Explicit non-promotions\n", "\n" + NEW_VERIFICATION_BULLETS + "\n## Explicit non-promotions\n")
    if "Amana's 1932 committee" not in text:
        marker = "- The volume 1-30 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100) are bounded negative results, not evidence that intentional communities never faced or managed such children."
        assert marker in text
        text = text.replace(marker, NEW_NONPROMOTIONS + marker)
    text = text.replace(
        "The volume 1-30 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100)",
        "The volume 1-31 dangerous-child searches (F-031, F-048, F-064, F-076, F-090, F-100, F-105)",
    )
    GAP_BANK.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    update_ledger()
    update_inventory()
    update_gap_bank()
    print("updated ledger, inventory, and gap bank for volume 31")
