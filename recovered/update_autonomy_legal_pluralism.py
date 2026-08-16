#!/usr/bin/env python3
"""Apply the bounded autonomy and legal-pluralism correction.

This pass adds six findings and nine public-source records. It corrects the
state-monopoly inference without altering article prose or reopening the
completed journal and standalone corpora.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
UNIT_LEDGER = ROOT / "COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-EVIDENCE-LEDGER.csv"
SOURCES = ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv"
UNIT_SOURCES = ROOT / "COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-SOURCE-INVENTORY.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
REPORT = ROOT / "COMMUNITIES-FINAL-SYNTHESIS-REPORT.md"
UNIT_REPORT = ROOT / "COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md"
CROSSWALK = ROOT / "COMMUNITIES-SYNTHESIS-CROSSWALK.csv"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"
INDEX = REPOSITORY / "docs" / "INDEX.md"
AGENTS = REPOSITORY / "AGENTS.md"


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        rows = list(reader)
    assert all(None not in row for row in rows), f"extra fields in {path.name}"
    assert all(None not in row.values() for row in rows), f"missing fields in {path.name}"
    return list(reader.fieldnames), rows


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old in text:
        assert text.count(old) == 1, f"ambiguous replacement for {label}"
        return text.replace(old, new, 1)
    raise AssertionError(f"missing predecessor and successor for {label}")


def replace_section(
    text: str,
    starts: tuple[str, ...],
    end: str,
    replacement: str,
    label: str,
) -> str:
    found = [(text.find(start), start) for start in starts if text.find(start) >= 0]
    assert found, f"missing section start for {label}"
    index, _ = min(found)
    end_index = text.find(end, index)
    assert end_index >= 0, f"missing section end for {label}"
    return text[:index] + replacement.rstrip() + "\n\n" + text[end_index:]


SOURCE_ROWS = [
    {
        "record_id": "LP-001",
        "lead_source_id": "",
        "lane": "autonomous Indigenous governance primary architecture",
        "title": "Chiapas: la treceava estela. Sexta parte: un buen gobierno",
        "authors": "Ejercito Zapatista de Liberacion Nacional; Subcomandante Insurgente Marcos",
        "year": "2003",
        "publication": "Enlace Zapatista",
        "doi": "",
        "canonical_url": "https://enlacezapatista.ezln.org.mx/2003/07/21/chiapas-la-treceava-estela-sexta-parte-un-buen-gobierno/",
        "accessed_on": "2026-08-15",
        "access_status": "complete official EZLN communique in Spanish inspected",
        "evidence_scope": "Declared division of functions among autonomous municipalities, regional Good Government Councils, communities, and the EZLN oversight structure",
        "sequence_allegation": "complaints against autonomous councils, human-rights violations, protests, conflicts, corruption, arbitrariness, or unequal municipal development",
        "sequence_assessment": "regional council receives complaints, investigates truth, mediates intermunicipal conflict, and monitors agreed laws and projects",
        "sequence_intervention": "Good Government Council may order an autonomous municipal council to correct an error and monitor compliance; municipalities retain justice and other ordinary governing functions",
        "sequence_review": "regional council plus a distinct EZLN committee oversight role intended to prevent corruption, intolerance, arbitrariness, and injustice",
        "sequence_later_outcome": "the communique establishes intended architecture and launch, not case-level implementation, appeal performance, or later human outcomes",
        "disposition": "F-187 promoted",
        "notes": "Primary movement statement. It directly distinguishes local government from a regional correction layer inside Zapatista autonomy; it does not prove that either layer always functioned as described.",
    },
    {
        "record_id": "LP-002",
        "lead_source_id": "LP-001",
        "lane": "autonomous Indigenous justice ethnography",
        "title": "The Politics of Justice: Zapatista Autonomy at the Margins of the Neoliberal Mexican State",
        "authors": "Mariana Mora",
        "year": "2015",
        "publication": "Latin American and Caribbean Ethnic Studies 10(1)",
        "doi": "10.1080/17442222.2015.1034439",
        "canonical_url": "https://doi.org/10.1080/17442222.2015.1034439",
        "accessed_on": "2026-08-15",
        "access_status": "publisher abstract, notes, and article metadata inspected; complete article not publicly accessible in this pass",
        "evidence_scope": "Ethnographic analysis of Zapatista conflict-resolution practices and their relationship to Mexican state regulation",
        "sequence_allegation": "local civil, interpersonal, and land conflicts in Zapatista autonomous territory",
        "sequence_assessment": "community and autonomous authorities use culturally grounded conflict-resolution practices",
        "sequence_intervention": "Zapatista justice operates as an alternative forum rather than merely referring ordinary conflict to official Peace Courts",
        "sequence_review": "article analyses the interplay between autonomous practice and shifting state regulation; complete case-level appeal records were not available in this pass",
        "sequence_later_outcome": "supports enactment of autonomous justice but does not provide a representative denominator or complete later-outcome panel",
        "disposition": "F-187 corroboration; no separate finding",
        "notes": "Kept distinct from the EZLN's own institutional statement. The article supports practice, not a claim that every decision was fair or independent.",
    },
    {
        "record_id": "LP-003",
        "lead_source_id": "LP-001",
        "lane": "autonomous Indigenous governance primary reorganization",
        "title": "Ninth Part: The new structure of Zapatista Autonomy",
        "authors": "Ejercito Zapatista de Liberacion Nacional; Subcomandante Insurgente Moises",
        "year": "2023",
        "publication": "Enlace Zapatista",
        "doi": "",
        "canonical_url": "https://enlacezapatista.ezln.org.mx/2023/11/13/ninth-part-the-new-structure-of-zapastista-autonomy/",
        "accessed_on": "2026-08-15",
        "access_status": "complete official English translation inspected",
        "evidence_scope": "Declared replacement of MAREZ/JBG structure with Local Autonomous Governments, Collectives, and zone assemblies after a decade of evaluation",
        "sequence_allegation": "mismanagement, corruption, errors, needs spanning communities, and external threats",
        "sequence_assessment": "local assemblies direct GALs; GALs report errors and convene CGAZ/ACGAZ layers according to need",
        "sequence_intervention": "health, education, agroecology, justice, commerce, training, security, and emergency functions move among local, regional, and zone levels according to scale",
        "sequence_review": "upper layers are declared accountable downward and without independent authority over the base; the movement describes criticism and self-criticism as the basis for redesign",
        "sequence_later_outcome": "the statement says the new structure is still being learned and supplies no evaluation of later performance",
        "disposition": "F-188 promoted",
        "notes": "High confidence for declared architecture; no inference that the 2023 design solved the weaknesses that motivated it.",
    },
    {
        "record_id": "LP-004",
        "lead_source_id": "LP-001",
        "lane": "current Zapatista authority field study and contested-control boundary",
        "title": "The difficult art of sustaining alternative governance: the case of the EZLN",
        "authors": "Luca Venga",
        "year": "2025",
        "publication": "Territory, Politics, Governance",
        "doi": "10.1080/21622671.2025.2583055",
        "canonical_url": "https://doi.org/10.1080/21622671.2025.2583055",
        "accessed_on": "2026-08-15",
        "access_status": "complete publisher HTML, methods, findings, limitations, ethics, and disclosure sections inspected through indexed full text",
        "evidence_scope": "Summer 2023 ethnography and more than 40 semi-structured interviews across several Chiapas sites concerning competing public authorities, justice, education, and recent pressure",
        "sequence_allegation": "fragmented public authority, cartel and paramilitary pressure, pandemic disruption, service gaps, and declining territorial reach",
        "sequence_assessment": "participant observation and purposive interviews with state officials, Zapatistas, sympathizers, businesses, journalists, clergy, and civil society actors",
        "sequence_intervention": "parallel Zapatista justice, education, public-goods provision, and recent decentralized reorganization",
        "sequence_review": "author compares multiple authority centers and reports both legitimacy and decline claims; interview data are anonymized and unavailable publicly for safety",
        "sequence_later_outcome": "reports long coexistence with state authority, some respected autonomous justice and educational diffusion, plus recent loss of reach under new pressures",
        "disposition": "F-187 and F-188 corroboration; no separate finding",
        "notes": "One current field study, not a definitive population estimate. Its decline interpretation may partly describe adaptation, sealed access, or regional variation and must not be universalized.",
    },
    {
        "record_id": "LP-005",
        "lead_source_id": "LP-003",
        "lane": "translocal Zapatista pedagogy and diffusion",
        "title": "Sowing Indigenous Autonomy: Building a Common Political-Ethical Territory of Struggle with Zapatista Seed Pedagogics",
        "authors": "Charlotte Maria Saenz",
        "year": "2024",
        "publication": "Latin American Perspectives 51(5)",
        "doi": "10.1177/0094582X241288861",
        "canonical_url": "https://doi.org/10.1177/0094582X241288861",
        "accessed_on": "2026-08-15",
        "access_status": "publisher abstract, methods summary, metadata, and references inspected; companion open 2023 article record inspected",
        "evidence_scope": "Interviews with external activists in neo-Zapatista networks about decades of learning, accompaniment, and organization outside autonomous territory",
        "sequence_allegation": "hierarchy and vanguard habits reproduced inside movements seeking social change",
        "sequence_assessment": "qualitative interviews and evolving conversations with external activists who encountered or accompanied Zapatismo",
        "sequence_intervention": "reflexive learning, listening, historical memory, collective organization, and transgeographic political-ethical practice",
        "sequence_review": "participants reflect on lifelong learning rather than receiving a fixed organizational blueprint",
        "sequence_later_outcome": "reports collectivities and political-ethical learning beyond Zapatista territory but not worldwide adoption rates or comparative community outcomes",
        "disposition": "F-189 promoted",
        "notes": "Useful for the owner's diffusion criterion. Interviewed movement-adjacent activists are not a representative sample of all visitors or attempted adaptations.",
    },
    {
        "record_id": "LP-006",
        "lead_source_id": "",
        "lane": "hybrid Indigenous municipal autonomy and communal security",
        "title": "Communal Responses to Structural Violence and Dispossession in Cheran, Mexico",
        "authors": "Giovanna Gasparello",
        "year": "2021",
        "publication": "Latin American Perspectives 48(1)",
        "doi": "10.1177/0094582X20975004",
        "canonical_url": "https://doi.org/10.1177/0094582X20975004",
        "accessed_on": "2026-08-15",
        "access_status": "complete indexed publisher article, methods, findings, limitations, and conclusion inspected",
        "evidence_scope": "Long-stay ethnography, 26 structured interviews, newspaper history, official demographic and crime data, and institutional analysis of Cheran after the 2011 uprising",
        "sequence_allegation": "kidnapping, extortion, illegal logging, homicide, disappearance, political corruption, and state failure",
        "sequence_assessment": "bonfire and neighborhood assemblies, communal councils, Community Watch, local mediation, field interviews, and public data",
        "sequence_intervention": "communal government and security replaced party government and municipal police; local council handles minor matters while serious crimes are referred to a state Public Ministry office",
        "sequence_review": "rotating and nested assemblies oversee councils; legal proceedings secured recognition of elections under Indigenous norms; state subsidies and serious-crime referral remained",
        "sequence_later_outcome": "reported drastic decline in high-impact crime after 2013, reforestation, renewed public life, and attempted replication nearby, with structural economic exclusion unresolved",
        "disposition": "F-190 promoted",
        "notes": "A hybrid autonomy case: community organization preceded legal recognition, while selective state interfaces and public subsidies remained. Observational design does not isolate causality.",
    },
    {
        "record_id": "LP-007",
        "lead_source_id": "LP-006",
        "lane": "official recognition of Indigenous self-government",
        "title": "SUP-JDC-9167/2011: Juicio para la proteccion de los derechos politico-electorales del ciudadano",
        "authors": "Tribunal Electoral del Poder Judicial de la Federacion, Sala Superior",
        "year": "2011",
        "publication": "Tribunal Electoral del Poder Judicial de la Federacion",
        "doi": "",
        "canonical_url": "https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-9167-2011",
        "accessed_on": "2026-08-15",
        "access_status": "complete official judgment HTML and dispositive orders inspected",
        "evidence_scope": "Official ruling on Cheran community members' right to elect their authorities through their own norms, procedures, and traditional practices",
        "sequence_allegation": "state electoral body claimed local law supplied neither a procedure nor authority for an usos-y-costumbres election",
        "sequence_assessment": "federal electoral judicial review grounded in constitutional Indigenous self-determination and effective access to justice",
        "sequence_intervention": "revoked the state electoral agreement, displaced the party-election preparations, and ordered implementation actions",
        "sequence_review": "federal electoral judgment and subsequent implementation duties",
        "sequence_later_outcome": "established legal recognition of the requested election route; it did not create Cheran's prior mobilization or prove later governance quality",
        "disposition": "F-190 official corroboration; no separate finding",
        "notes": "The case shows strategic use of a state court to protect an autonomous order, not dependence on the court for the origin of that order.",
    },
    {
        "record_id": "LP-008",
        "lead_source_id": "",
        "lane": "regional Indigenous policing and justice comparison",
        "title": "Indigenous Resistance to Criminal Governance: Why Regional Ethnic Autonomy Institutions Protect Communities from Narco Rule in Mexico",
        "authors": "Sandra Ley; Shannan Mattiace; Guillermo Trejo",
        "year": "2019",
        "publication": "Latin American Research Review 54(1)",
        "doi": "10.25222/larr.377",
        "canonical_url": "https://doi.org/10.25222/larr.377",
        "accessed_on": "2026-08-15",
        "access_status": "complete open article, methods, paired comparison, alternative explanations, and external-validity analysis inspected",
        "evidence_scope": "Paired process tracing in Guerrero and Chihuahua using more than 30 interviews plus statistical analysis of 881 Indigenous municipalities in 20 Mexican states",
        "sequence_allegation": "cartel attempts to capture local governments, police, territory, young recruits, and economic activity",
        "sequence_assessment": "community assemblies select and oversee local police and regional prosecutors; Casas de Justicia investigate; paired regional comparison and municipality-level analysis test mechanisms",
        "sequence_intervention": "CRAC-PC scales village accountability into regional policing, justice, information sharing, cross-village mobilization, and external territorial defense",
        "sequence_review": "assemblies oversee and sanction officers; multiple local and regional layers create internal accountability and translocal protection",
        "sequence_later_outcome": "study reports far stronger resistance to criminal governance in Guerrero than the isolated Tarahumara comparison and supportive municipality-level association",
        "disposition": "F-191 promoted",
        "notes": "Strong mechanism evidence but observational. It does not establish perfect due process, complete crime incidence, gender equality, or current performance after later CRAC-PC fractures.",
    },
    {
        "record_id": "LP-009",
        "lead_source_id": "",
        "lane": "international normative Indigenous juridical-systems boundary",
        "title": "United Nations Declaration on the Rights of Indigenous Peoples, Article 34",
        "authors": "United Nations General Assembly",
        "year": "2007",
        "publication": "United Nations General Assembly Resolution 61/295",
        "doi": "",
        "canonical_url": "https://www.un.org/esa/socdev/unpfii/documents/DRIPS_en.pdf",
        "accessed_on": "2026-08-15",
        "access_status": "official declaration text and Article 34 inspected through UN/OHCHR and government-hosted copies",
        "evidence_scope": "Normative recognition of Indigenous institutional structures, procedures, practices, and juridical systems",
        "sequence_allegation": "not applicable",
        "sequence_assessment": "not applicable",
        "sequence_intervention": "recognizes a right to promote, develop, and maintain Indigenous juridical systems and customs",
        "sequence_review": "expressly conditions the right on international human-rights standards",
        "sequence_later_outcome": "normative declaration; no implementation or comparative outcome supplied",
        "disposition": "F-192 promoted",
        "notes": "High authority for the normative boundary, zero causal or implementation evidence. It rejects a state-monopoly presumption while retaining a rights floor.",
    },
]


FINDING_ROWS = [
    {
        "finding_id": "F-187",
        "track": "Track F autonomous Indigenous governance and internal correction",
        "source_record_id": "LP-001; LP-002; LP-004",
        "source_file": "https://enlacezapatista.ezln.org.mx/2003/07/21/chiapas-la-treceava-estela-sexta-parte-un-buen-gobierno/; https://doi.org/10.1080/17442222.2015.1034439; https://doi.org/10.1080/21622671.2025.2583055",
        "journal_volume_issue_year": "EZLN communique 2003; scholarship 2015 and 2025",
        "article_title": "Good Government Council architecture and enacted Zapatista autonomous justice",
        "author": "EZLN; Mariana Mora; Luca Venga",
        "community_group": "Zapatista support-base communities, autonomous municipalities, and regional Good Government Councils",
        "page_locator": "2003 communique functions; Mora abstract and notes; Venga methods, justice, and public-authority sections",
        "printed_page_number": "",
        "supporting_excerpt": "",
        "source_access": "complete primary communique; scholarly publisher records and indexed full text as recorded in LP inventory",
        "evidence_type": "primary institutional architecture with ethnographic implementation corroboration",
        "exact_factual_observation": "The 2003 EZLN communique assigned justice, community health, education, housing, land, work, food, commerce, information, culture, and local transit to autonomous municipalities. It created a Good Government Council in each rebel zone to mediate conflicts among municipalities, receive and investigate complaints against autonomous councils, order correction, monitor compliance, and address unequal development. A distinct EZLN committee was assigned oversight against corruption, intolerance, arbitrariness, and injustice. Mora analyses enacted Zapatista conflict resolution, and Venga's 2023 fieldwork reports that some Zapatista justice forums were respected even by non-Zapatista or critical participants for small civil and interpersonal matters.",
        "what_source_establishes": "The Zapatista case falsifies the state monopoly equation independent correction equals nation-state correction. It supplies a declared and partly corroborated architecture in which ordinary justice and government are autonomous while complaint, mediation, monitoring, and correction can move to a regional layer inside the same movement but outside the implicated municipality.",
        "what_source_does_not_establish": "It does not establish that every council was independent in practice, that military oversight was itself democratically reviewable, that every accused person or victim had notice, representation, appeal, or a direct bypass, that serious crimes were handled safely, or that the architecture produced superior long-term outcomes across all communities.",
        "author_interpretation": "The movement presented the councils as a way to make authorities obey communities, correct errors, balance development, and connect autonomous territory with the world. The scholarship treats conflict resolution as a substantive form of autonomous public authority.",
        "alternative_interpretation": "Regional review may remain politically aligned with local authorities, armed-movement oversight may introduce another unreviewable layer, and perceived fairness may reflect case selection, legitimacy, or dissatisfaction with official courts rather than superior process in every matter.",
        "response_process": "local conflict or complaint; municipal handling; regional mediation or complaint intake; investigation; correction order and compliance monitoring; separate movement oversight. Published records do not reconstruct a representative sample of case files or appeals.",
        "outcome": "The structure operated for roughly two decades and autonomous justice acquired enough standing to be sought in at least some disputes. No complete denominator, rights audit, or long-term person-level outcome panel was located.",
        "transferability": "High for separating an implicated local authority from a regional correction layer without assuming state monopoly. Medium-low for direct institutional copying because the system rests on Indigenous territorial organization, a mass movement, an armed deterrent, and a contested sovereignty environment.",
        "article_gap_status": "D",
        "likely_article_destination": "Selecting your couplings / autonomous correction / federated governance",
        "confidence": "high",
        "external_verification_needed": "yes",
        "notes": "Use the four-level distinction: independent of the accused authority; outside the immediate community; outside the autonomous movement; and nation-state. These are not synonyms.",
    },
    {
        "finding_id": "F-188",
        "track": "Track F adaptive Zapatista decentralization and contested control",
        "source_record_id": "LP-003; LP-004",
        "source_file": "https://enlacezapatista.ezln.org.mx/2023/11/13/ninth-part-the-new-structure-of-zapastista-autonomy/; https://doi.org/10.1080/21622671.2025.2583055",
        "journal_volume_issue_year": "EZLN communique 2023; field study 2025",
        "article_title": "GAL/CGAZ/ACGAZ reorganization and the limits of de facto autonomy",
        "author": "EZLN; Luca Venga",
        "community_group": "Zapatista support-base communities and neighboring Chiapas authority systems",
        "page_locator": "official communique sections First through Sixth; Venga methods, reorganization, cartel, and conclusion sections",
        "printed_page_number": "",
        "supporting_excerpt": "",
        "source_access": "complete official English translation and indexed scholarly full text inspected",
        "evidence_type": "primary redesign statement plus current qualitative contested-authority study",
        "exact_factual_observation": "In 2023 the EZLN said that, after ten years of evaluation and three years of preparation, thousands of Local Autonomous Governments would become the base; several could convene Collectives for health, education, agroecology, justice, commerce, training, or common problems; and zone assemblies would convene only at the request of lower layers. Local governments were assigned resource control and detection of mismanagement, corruption, and error, while higher layers were declared non-authoritative and accountable downward. The same statement organized defense against aggression, company invasion, military occupation, epidemics, and disasters. Venga's 2023 ethnography and more than 40 interviews describe long coexistence with Mexican public authority but recent pressure from COVID, cartels, paramilitaries, and declining reach in some places.",
        "what_source_establishes": "Zapatista autonomy is an iterative, multilevel governance project rather than a static anti-institutional commune. The official redesign moves more initiative to the base while retaining scale-up channels. It also shows why full control is too strong: autonomy operates amid competing armed, state, criminal, market, and neighboring authorities.",
        "what_source_does_not_establish": "The official statement does not establish adoption, fidelity, case outcomes, independent appeal, or success after 2023. The field study does not prove uniform decline across sealed or inaccessible Zapatista territories, isolate COVID or cartel effects, or establish that reorganization is retreat rather than adaptation.",
        "author_interpretation": "The EZLN presents redesign as self-critical learning, survival, and an inversion of the organizational pyramid. Venga interprets the broader moment as a weakening alternative authority in an unstable field.",
        "alternative_interpretation": "Decentralization may increase resilience and reduce bureaucracy, or it may devolve responsibilities because regional capacity has weakened. Both can be true in different places and periods.",
        "response_process": "local assembly and GAL; need-based CGAZ; zone ACGAZ when requested; downward accountability; ongoing criticism and redesign; separate defense organization against external threats.",
        "outcome": "A new architecture was announced and described as still being learned. Later governance, safety, education, justice, migration, and child outcomes remain open.",
        "transferability": "High for treating governance form as revisable and for matching scale to the problem. Medium for network resilience. Low for claiming full sovereignty or importing a wartime defense structure into an ordinary voluntary community.",
        "article_gap_status": "D",
        "likely_article_destination": "Governance architecture / forks and evolution / selecting couplings",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "The user's visit to Oventik in 2005 belongs to the JBG era. The current structure is materially different and should not be described as unchanged continuity.",
    },
    {
        "finding_id": "F-189",
        "track": "Track F movement-scale pedagogy and communal innovation diffusion",
        "source_record_id": "LP-003; LP-004; LP-005",
        "source_file": "https://enlacezapatista.ezln.org.mx/2013/02/26/them-and-us-vii-the-smallest-of-them-all-1-learning-to-govern-and-govern-ourselves-that-is-to-respect-and-respect-ourselves/; https://doi.org/10.1177/0094582X241288861; https://doi.org/10.1080/21622671.2025.2583055",
        "journal_volume_issue_year": "EZLN Escuelita materials 2013; scholarship 2024 and 2025",
        "article_title": "Escuelita, seed pedagogy, and adaptation outside Zapatista territory",
        "author": "EZLN; Charlotte Maria Saenz; Luca Venga",
        "community_group": "Zapatista communities, external neo-Zapatista networks, and affiliated educational initiatives",
        "page_locator": "official course-material introduction; Saenz abstract and methods summary; Venga CIDECI and diffusion sections",
        "printed_page_number": "",
        "supporting_excerpt": "",
        "source_access": "official page, publisher records, companion open article record, and indexed current full text inspected",
        "evidence_type": "primary movement pedagogy plus qualitative interviews and field observation of external adaptation",
        "exact_factual_observation": "The EZLN described the Escuelita's Freedom According to the Zapatistas notebooks as the product of support-base meetings across five caracoles that exchanged experience, criticized, self-criticized, and evaluated what had and had not been done. Saenz's interviews with external activists describe learning and collective organization beyond autonomous territory across decades. Venga reports Zapatista-informed educational institutions and training intended to return practical capacity to home communities, with alumni participation and adaptation outside the formal caracol structure.",
        "what_source_establishes": "Zapatismo treats diffusion as pedagogy and adaptation rather than franchising a fixed commune. It offers stronger evidence for the owner's worldwide-innovation criterion than longevity alone: practices are deliberately made learnable by outsiders and are reported as informing collectivities beyond the territorial core.",
        "what_source_does_not_establish": "It does not measure the number, durability, safety, child wellbeing, or fidelity of adaptations; compare Zapatista influence with other movements; or prove that worldwide resonance produces successful communal institutions.",
        "author_interpretation": "Saenz describes a transgeographic political-ethical commons and ongoing dismantling of hierarchy. Venga emphasizes adaptable institutions and positive spillovers. The EZLN frames the materials as collective learning rather than a doctrine delivered by experts.",
        "alternative_interpretation": "Sympathetic networks may report inspiration more readily than failed or critical adaptations. Cultural resonance, political education, and durable community replication are distinct outcomes.",
        "response_process": "community self-evaluation; codified learning materials and hosted study; outsider accompaniment; local adaptation; return of skills and continuing exchange. No common adoption registry or outcome audit exists.",
        "outcome": "Documented educational encounters and reported external organizing influence; no representative diffusion denominator or long-term comparative outcome.",
        "transferability": "High for treating teachability, adaptation, and return of skills as movement-success dimensions. Medium for specific pedagogical forms. Low for claiming a universally exportable Zapatista model.",
        "article_gap_status": "B",
        "likely_article_destination": "Worldwide communal innovation / internal school-research function / movement continuity",
        "confidence": "medium-high",
        "external_verification_needed": "yes",
        "notes": "Separate spread of ideas, formation of collectivities, and verified improvement in how people live and love. The sources establish the first two better than the third.",
    },
    {
        "finding_id": "F-190",
        "track": "Track F hybrid Indigenous autonomy and strategic state interface",
        "source_record_id": "LP-006; LP-007",
        "source_file": "https://doi.org/10.1177/0094582X20975004; https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-9167-2011",
        "journal_volume_issue_year": "field research published 2021; official judgment 2011",
        "article_title": "Cheran communal government, security, justice, and selective legal recognition",
        "author": "Giovanna Gasparello; TEPJF Sala Superior",
        "community_group": "Purepecha community and municipality of Cheran, Michoacan",
        "page_locator": "Gasparello methods, communal participation, communal security, and conclusions; SUP-JDC-9167/2011 dispositive orders",
        "printed_page_number": "42-62",
        "supporting_excerpt": "",
        "source_access": "complete indexed article and complete official judgment HTML inspected",
        "evidence_type": "long-stay ethnography with 26 structured interviews and public data, paired with an official judicial recognition record",
        "exact_factual_observation": "After unanswered complaints and the 2011 uprising, Cheran organized bonfires, neighborhood assemblies, a communal council structure, and a Community Watch that replaced municipal police. Gasparello reports a drastic decline in high-impact crimes after communal government consolidated in 2013, renewed public use, and reforestation, while economic alternatives remained incomplete. A local Justice Procurement and Mediation Council handled minor criminal, family, civil, and protection matters; serious crimes were referred to a state Public Ministry office in Zamora. The federal electoral court separately recognized the community's right to elect authorities under its own norms and ordered state implementation. Some communal enterprises still depended on state subsidies.",
        "what_source_establishes": "Cheran is neither a state-dependence case nor a no-state case. Mobilization and communal institutions generated security and government before legal recognition; the community then used a state court strategically and retained selective state referral and funding interfaces. Jurisdictional coupling is function-specific and historically contingent.",
        "what_source_does_not_establish": "The observational record cannot isolate the causal effect of each institution, prove every rights or due-process outcome, establish economic self-sufficiency, or show that neighboring attempts to replicate the model succeeded.",
        "author_interpretation": "Gasparello treats communal participation, security, territory, and social reconstruction as a peace-formation process with important but incomplete results. The court treats Indigenous self-government as a right requiring effective state implementation.",
        "alternative_interpretation": "Crime trends may reflect wider regional changes, displacement, underreporting, or deterrence not captured by the study. State recognition and subsidies may have been more important to durability than the sequence alone establishes.",
        "response_process": "uprising and local defense; bonfires and assemblies; community watch and councils; local mediation and penalties; referral of serious crimes; judicial recognition of self-government; continuing public-program interfaces.",
        "outcome": "Reported lower high-impact crime, reforestation, renewed public activity, stable communal government, and imitation attempts, alongside unresolved exclusion and incomplete economic autonomy.",
        "transferability": "High for a hybrid interface map and for community-first institution building with selective legal recognition. Medium for nested assemblies and rotating service. Low for copying armed road control or assuming the same crime effect elsewhere.",
        "article_gap_status": "D",
        "likely_article_destination": "Selecting your couplings / public interface spectrum / outcome dashboard",
        "confidence": "high",
        "external_verification_needed": "yes",
        "notes": "This comparator demonstrates that the state can be a recognition forum and backstop without being the source or operator of ordinary communal governance.",
    },
    {
        "finding_id": "F-191",
        "track": "Track F regional Indigenous federation and anti-capture capacity",
        "source_record_id": "LP-008",
        "source_file": "https://doi.org/10.25222/larr.377",
        "journal_volume_issue_year": "Latin American Research Review 54(1), 2019",
        "article_title": "Indigenous Resistance to Criminal Governance",
        "author": "Sandra Ley; Shannan Mattiace; Guillermo Trejo",
        "community_group": "CRAC-PC communities in Guerrero and Tarahumara comparison communities in Chihuahua",
        "page_locator": "pp. 181-200; abstract, methods, CRAC-PC, alternative explanations, and external-validity sections",
        "printed_page_number": "181-200",
        "supporting_excerpt": "",
        "source_access": "complete open primary research article inspected",
        "evidence_type": "paired qualitative process tracing plus cross-sectional external-validity analysis",
        "exact_factual_observation": "The study reports that village-level customary accountability made cartel capture harder but was insufficient by itself. In Guerrero, decades of mobilization connected communities and scaled local practices into the CRAC-PC's regional policing and justice system. Assemblies selected, oversaw, and sanctioned police and prosecutors; regional institutions shared information and mobilized neighboring forces. More than 30 interviews supported the paired Guerrero-Chihuahua process trace, and an analysis of 881 Indigenous municipalities across 20 states supported the combination of mobilization and ethnic-autonomy institutions as protective against conditions enabling criminal governance.",
        "what_source_establishes": "The strongest comparator rejects both state monopoly and isolated-local sufficiency. A translocal Indigenous federation can provide the independent oversight, scale, information, solidarity, and defense that one village cannot sustain.",
        "what_source_does_not_establish": "It does not establish randomized causality, complete crime reporting, individual due process, victim outcomes, freedom from internal faction or gender bias, current performance after later organizational fractures, or safe transfer to an unarmed residential community.",
        "author_interpretation": "The authors identify scaled regional ethnic autonomy and translocal networks as the key mechanism distinguishing Guerrero resistance from Tarahumara vulnerability.",
        "alternative_interpretation": "Unmeasured geography, political alliances, state tolerance, economic routes, weapons, organizational history, or reporting may contribute. The federation's own internal cohesion changed later.",
        "response_process": "assembly selection and oversight; local policing; regional Houses of Justice and prosecutors; reeducation through community work; cross-village information and mobilization; territorial defense; community sanction for corruption.",
        "outcome": "Reported containment of criminal governance in the Guerrero comparison and supportive municipality-level association; no complete current outcome panel.",
        "transferability": "High for federation as anti-capture and capacity infrastructure. Medium for unpaid rotating service and restorative justice. Low for importing armed policing or territorial border control into ordinary communities.",
        "article_gap_status": "D",
        "likely_article_destination": "Federation / scale / selecting couplings / security architecture",
        "confidence": "medium-high",
        "external_verification_needed": "no",
        "notes": "The relevant meaning of external protection here is external to the village but internal to a regional Indigenous order. That distinction directly corrects the prior synthesis vocabulary.",
    },
    {
        "finding_id": "F-192",
        "track": "Track F international normative legal-pluralism boundary",
        "source_record_id": "LP-009",
        "source_file": "https://www.un.org/esa/socdev/unpfii/documents/DRIPS_en.pdf",
        "journal_volume_issue_year": "UN General Assembly Resolution 61/295, 2007",
        "article_title": "United Nations Declaration on the Rights of Indigenous Peoples, Article 34",
        "author": "United Nations General Assembly",
        "community_group": "Indigenous peoples generally",
        "page_locator": "Article 34",
        "printed_page_number": "",
        "supporting_excerpt": "",
        "source_access": "official declaration text inspected",
        "evidence_type": "international normative instrument",
        "exact_factual_observation": "Article 34 recognizes Indigenous peoples' right to promote, develop, and maintain their institutional structures, procedures, practices, and, where they exist, juridical systems or customs, in accordance with international human-rights standards.",
        "what_source_establishes": "A globally authoritative normative framework expressly rejects a blanket state-monopoly assumption for juridical systems while retaining a human-rights constraint.",
        "what_source_does_not_establish": "It is not a causal evaluation, directly enforceable outcome guarantee, implementation audit, allocation rule for overlapping jurisdictions, or proof that any particular Indigenous institution complies with human-rights standards.",
        "author_interpretation": "The declaration pairs self-determination and institutional continuity with universal human-rights limits.",
        "alternative_interpretation": "States differ on the declaration's domestic legal effect and may recognize, constrain, co-opt, or ignore Indigenous jurisdiction. The text alone does not resolve conflicts between collective and individual rights.",
        "response_process": "not applicable; normative recognition and rights boundary only",
        "outcome": "No implementation or human outcome reported.",
        "transferability": "High for the legal-pluralism boundary and for preserving direct rights. Zero for claiming an effective governance mechanism or outcome from declaration alone.",
        "article_gap_status": "D",
        "likely_article_destination": "Selecting your couplings / rights floor / Indigenous legal pluralism",
        "confidence": "high",
        "external_verification_needed": "no",
        "notes": "Do not use Indigenous rights instrumentally as a generic commune exemption. The source concerns Indigenous peoples and explicitly retains international human-rights standards.",
    },
]


UNIT_REPORT_TEXT = """# Autonomous governance and legal pluralism: correction report

Date: 2026-08-15 (Africa/Dakar)
Status: completed bounded correction; no article prose revised
Evidence added: F-187 through F-192

## Direct answer

Joel's objection is correct. The final synthesis made a scope error.

The earlier evidence base was dominated by intentional communities operating inside nation-state jurisdiction, followed by adjacent studies deliberately drawn from courts, regulators, licensed care, child-welfare systems, and official inquiries. Those sources support routes outside an implicated private authority. They do not support the universal inference that the route must be operated by the state.

The Zapatista evidence falsifies that inference. It does not falsify the need for law, adjudication, review, competence, or appeal. The Zapatistas built those functions inside an autonomous, multilevel political order. The correct distinction is not community versus state. It is implicated local authority versus a competent layer that can review it without sharing its conflict.

## The corrected rule

Independent correction is a relationship, not a geography.

For each function, use the lowest competent layer that:

1. is not reviewing its own conduct;
2. has enough scale, skill, information, and enforceability for the problem;
3. cannot disable the affected person's direct rights or bypass route; and
4. is itself accountable and reviewable.

That layer may be a neighboring community, autonomous municipality, regional Indigenous council, movement federation, professional body, public agency, court, state, or international forum. None is automatically correct because of its location.

The jurisdictional ladder is:

`person -> immediate community -> autonomous intercommunity review -> regional federation -> public/state/international backstop`

A function may skip levels. A child, survivor, accused person, patient, or dissenter cannot be forced to exhaust a captured local route before reaching a competent one.

## What the Zapatista case changes — F-187 and F-188

The 2003 Zapatista architecture was not a collection of sovereign villages with no institutions above them. Autonomous municipalities retained justice, health, education, housing, land, work, food, commerce, information, culture, and local-transit functions. Regional Good Government Councils were assigned mediation between municipalities, complaint intake against autonomous councils, investigation, correction orders, and compliance monitoring. A separate movement structure watched the regional councils for corruption, intolerance, arbitrariness, and injustice.

That is precisely the distinction the earlier report blurred:

- independent of the accused local authority;
- outside the immediate village or municipality;
- outside the autonomous movement; and
- operated by the nation-state.

Only the first is always required by the anti-self-review principle. The others depend on function, scale, rights, competence, and surrounding power.

The 2023 reorganization makes the point stronger. The EZLN replaced the MAREZ/JBG structure with thousands of Local Autonomous Governments, need-based regional Collectives, and zone assemblies that formally depend on the lower layers. It described the redesign as the product of a decade of evaluation, criticism, and self-criticism. Governance scale is therefore treated as revisable, not sacred.

But this is de facto and contested autonomy, not full sovereignty. The official statement itself plans for company invasion, military occupation, crime, epidemics, and external attack. A 2023 field study with more than 40 interviews describes long coexistence with Mexican authority and recent pressure from cartels, paramilitaries, and COVID. The author's decline interpretation is one current study, not a settled verdict; the official decentralization may also be adaptive resilience. Either way, “took back full control” overstates the evidence.

## Why Zapatismo fits the worldwide-innovation criterion — F-189

The user is also right to distinguish movement success from the survival of one residential institution.

The Zapatista Escuelita turned governance into something teachable. Its materials were produced through cross-caracol evaluation and self-criticism, not merely by a charismatic theorist. Later qualitative work with external activists describes Zapatista learning and collective organization outside autonomous territory. Current fieldwork also describes Zapatista-informed educational institutions designed to return practical capacity to people's home communities.

This makes Zapatismo unusually relevant to the user's mission: it is not merely a durable community but a movement-scale school for creating and adapting communal practices.

The evidence still has a hard boundary. It supports deliberate transmission, reported learning, and some organization beyond the territorial core. It does not count all adaptations, compare their durability or child wellbeing, or prove that worldwide resonance reliably produces communities where people live and love better. Spread of ideas, formation of collectivities, and verified human outcomes must remain three separate measures.

## Cheran: the hybrid case — F-190

Cheran rejects a simple autonomy/state binary.

After complaints to public authorities went unanswered, residents' 2011 uprising produced bonfires, assemblies, communal councils, and a Community Watch that replaced municipal police. Long-stay ethnography using 26 structured interviews and public data reports a sharp fall in high-impact crimes after the communal government consolidated, as well as reforestation and renewed public life. The local justice council handled minor matters and mediation.

Yet serious crimes were referred to a state Public Ministry office, some communal enterprises depended on state subsidies, and the community used a federal electoral court to force recognition of elections under its own norms. The legal ruling protected an order the community had already built; it did not create the movement that made the order possible.

Cheran therefore shows a strategic spectrum:

- communal authority for ordinary governance and local security;
- nested assemblies for accountability;
- state adjudication used to protect autonomous political form;
- selective serious-crime referral; and
- continuing public-resource dependence.

State coupling can be a tool, boundary, dependency, or recognition route. It is not the universal source of legitimate correction.

## CRAC-PC: why the village alone is not enough — F-191

The Guerrero comparison prevents the correction from swinging into the opposite mistake.

Ley, Mattiace, and Trejo found that village customary accountability made cartel capture harder but was insufficient by itself. The major difference was decades of mobilization that connected villages and scaled their practices into the CRAC-PC's regional policing and justice system. Assemblies selected and sanctioned officers and prosecutors; regional institutions shared information and could mobilize neighboring communities. The study used more than 30 interviews, paired process tracing against the Tarahumara region, and a supporting analysis of 881 Indigenous municipalities.

The transferable point is not armed policing. It is that translocal federation can provide:

- review outside one village;
- pooled skill and personnel;
- information beyond one local authority;
- resistance to bribery and capture;
- solidarity when one community is attacked; and
- a jurisdiction large enough to protect local accountability.

“External protection” in this case means external to the village but internal to a regional Indigenous order. That phrase must no longer be used as a synonym for state intervention.

## Rights boundary — F-192

UNDRIP Article 34 recognizes Indigenous peoples' right to maintain institutional structures and juridical systems while expressly retaining international human-rights standards.

That is the correct double boundary. Indigenous or communal jurisdiction cannot be dismissed because it is not state law. It also cannot be romanticized as inherently fair. Children, women, dissenters, accused people, survivors, patients, leavers, and minorities still need direct rights, accessible evidence, recusal, appeal, and a route around local capture.

The declaration is normative. It supplies no outcome evidence and should not be turned into a generic legal exemption for non-Indigenous voluntary communities.

## Corrected control map

| Question | Local layer | Autonomous/federated layer | State/professional/international layer |
|---|---|---|---|
| Who handles ordinary life? | usually primary | only when scale or conflict requires | only where law, rights, or dependency requires |
| Who reviews the local authority? | never the same implicated chain | neighboring, regional, federated, or Indigenous appellate body | backstop where autonomous review lacks independence, competence, reach, or enforceability |
| Who handles serious harm? | immediate safety and evidence preservation within legitimate scope | competent autonomous justice, safeguarding, or survivor-support layer where one exists | competent criminal, custody, clinical, regulatory, or rights forum where necessary |
| Who protects direct rights? | written local floor and accessible intake | bypass, appeal, archive, advocate, and intercommunity option | enforceable remedy and international or constitutional floor when lower layers fail |
| Who defends territory and institutions? | local vigilance and mutual aid | translocal coordination and pooled capacity | strategic alliance, recognition, or public protection when useful and legitimate |
| Who spreads innovation? | local practice and self-evaluation | movement schools, exchanges, federations, and adaptation | optional resources or recognition; not the source of the practice |

## Variables that determine the interface

The proper layer changes with:

1. territorial control and continuity;
2. population and geographic scale;
3. professional, investigative, clinical, and adjudicative competence;
4. whether the alleged wrong crosses communities or affects outsiders;
5. coercive capacity and the risk of violent capture;
6. legitimacy and corruption at each available layer;
7. enforceability of remedies and portability of records;
8. the person's direct right to bypass or appeal;
9. state recognition, hostility, absence, or dependence; and
10. whether the function is ordinary communal life, a specialized service, or a non-waivable rights question.

## What remains intact from the earlier synthesis

The counterexample does not rescue self-review.

- A founder, therapist, elder, council, police body, or assembly accused of abuse cannot select the evidence, reviewer, and remedy without recusal or bypass.
- Mediation cannot settle a contested crime, custody question, or nonconsenting person's rights merely because it is culturally grounded.
- Qualified care, due process, evidence preservation, and later outcomes still matter.
- A federation can be captured and needs its own audit and appeal.
- Local legitimacy and cohesion are not substitutes for child, survivor, leaver, or accused-person outcomes.

What changes is the institutional vocabulary. “Independent,” “outside the immediate community,” “federated,” “public,” “professional,” and “state” must never again be collapsed into one category.

## Bottom line

The Zapatistas are a genuine counterexample to the report's state-centric formulation. They do not show that institutions, law, or higher-level correction are unnecessary. They show that a community movement can create those capacities within a nested autonomous order and can teach its practices outward.

The broader comparative result is conditional:

`local autonomy + translocal federation + direct rights + adaptive scale + sufficient territorial and material capacity`

can substitute for much of what the earlier report assigned reflexively to the state. Where one of those capacities is missing, a state, professional, public, neighboring, or international interface may still be necessary. The design question is which layer is competent and independent for this function under these power conditions—not whether the state is always inside or outside.

## Source guide

- Primary Zapatista 2003 architecture: https://enlacezapatista.ezln.org.mx/2003/07/21/chiapas-la-treceava-estela-sexta-parte-un-buen-gobierno/
- Primary Zapatista 2023 reorganization: https://enlacezapatista.ezln.org.mx/2023/11/13/ninth-part-the-new-structure-of-zapastista-autonomy/
- Zapatista justice ethnography: https://doi.org/10.1080/17442222.2015.1034439
- Current competing-authority field study: https://doi.org/10.1080/21622671.2025.2583055
- Zapatista outward pedagogy: https://doi.org/10.1177/0094582X241288861
- Cheran field study: https://doi.org/10.1177/0094582X20975004
- Cheran official judgment: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-JDC-9167-2011
- CRAC-PC comparison: https://doi.org/10.25222/larr.377
- UNDRIP: https://www.un.org/esa/socdev/unpfii/documents/DRIPS_en.pdf
"""


SECTION_9 = """## 9. Independent correction is necessary; state externality is contingent — T-09, T-13, S-10, S-16, S-17

The earlier version of this section overgeneralized from its sampling frame. The corpus was dominated by intentional communities embedded in nation-state jurisdiction, and the adjacent units deliberately selected courts, regulators, clinicians, child-welfare systems, and official inquiries. Those records show why an implicated private authority needs a route it does not control. They do not establish that the route must always be a nation-state institution.

S-16 is the corrected rule: independent correction is a relationship, not a geography. Four locations must stay distinct:

1. independent of the person or local authority whose conduct is challenged;
2. outside the immediate household, village, or residential community;
3. outside the autonomous movement or federation; and
4. operated by the nation-state.

The first is the recurring anti-capture requirement. Which of the other three is necessary depends on jurisdiction, competence, scale, direct rights, territorial control, enforceability, and the surrounding threat environment.

The Zapatista case is the decisive counterexample (F-187). In 2003 autonomous municipalities retained justice, health, education, housing, land, work, food, commerce, information, culture, and local-transit functions. Regional Good Government Councils were assigned intermunicipal mediation, complaints against autonomous councils, investigation, correction orders, and compliance monitoring. This was an internal appellate and oversight layer: outside the implicated municipality, but inside Zapatista autonomy. Ethnographic work supports the enactment and local standing of at least some autonomous conflict-resolution forums, while leaving major case-level and rights questions open.

The 2023 GAL/CGAZ/ACGAZ reorganization further shows governance as iterative (F-188). Local assemblies and governments became the base; regional and zone structures were to convene according to need and remain accountable downward. The same primary statement acknowledges aggression, company invasion, crime, military occupation, epidemics, and disaster. Zapatista autonomy is therefore de facto and contested, not full sovereign control. One current field study reports long coexistence with Mexican authority and recent pressure from cartels, paramilitaries, and COVID; its decline interpretation is a bounded qualitative finding, not a final verdict on the new system.

Cheran supplies a hybrid rather than a no-state case (F-190). Communal organization, security, and government arose after official failure and before judicial recognition. Nested assemblies and a Community Watch handled ordinary governance and security; minor matters went through communal justice, serious crimes were referred to a state prosecutor, a federal court protected Indigenous election rules, and some programs remained subsidy-dependent. State interface was selective and strategic, not the source of the communal order.

The CRAC-PC comparison blocks the opposite overcorrection (F-191). Village custom alone was insufficient against cartel capture. Guerrero communities were more successful when decades of mobilization scaled local accountability into regional policing, justice, information sharing, and cross-village defense. “External protection” there meant external to one village but internal to a regional Indigenous order.

S-17 follows: place each function at the lowest competent layer that is not reviewing itself and cannot disable the person's direct rights. That layer may be a neighboring community, autonomous municipality, regional Indigenous council, movement federation, professional body, public agency, court, state, or international forum. A person may bypass layers when local capture, urgency, rights, or lack of competence requires it.

Courts, agencies, professional bodies, and autonomous forums remain narrow and fallible. Each answers the claim, evidence, jurisdiction, and remedy within its scope. A property judgment may not repair a relationship; a license revocation may not repair a family; a communal settlement may not establish a contested crime; a regional council may share the local authority's loyalties; and an official inquiry may recommend action without proving implementation (F-036, F-050, F-101, F-180 through F-182, F-187, F-190).

UNDRIP Article 34 supplies the normative double boundary (F-192): Indigenous peoples may maintain their institutions and juridical systems, and those systems remain subject to international human-rights standards. Indigenous or communal jurisdiction is not invalid because it is non-state. It is also not inherently rights-protecting.

The practical requirement is a named function, competent jurisdiction, accessible intake, evidence preservation, recusal, proportionality, stopping rule, appeal or bypass, and later outcome review. Community members and autonomous authorities can exercise the powers their legitimate order gives them. No one acquires unlimited police, court, clinical, custody, restraint, seclusion, licensing, or regulatory power merely by calling the institution communal.
"""


COMBINED_SECTION = """## The combined architecture — S-15

The corrected synthesis is function-specific subsidiarity with direct individual routes and jurisdictional pluralism. Each function belongs at the lowest level that can perform it competently without reviewing its own conduct or disabling a person's rights. “Lowest” is a relationship to the problem, not a presumption that the immediate community or the state is always preferred.

The available ladder is `person -> immediate community -> autonomous intercommunity review -> regional federation -> public/state/international backstop`. A function may skip levels when urgency, rights, conflict, competence, or enforceability requires it.

| Function | Immediate community may do | Next competent autonomous or federated layer may do | State, professional, public, or international backstop when needed | Direct individual route |
|---|---|---|---|---|
| Membership and roles | invite, stage access, define duties, evaluate observable role conduct | hear appeal, check conflicts, maintain intercommunity alternatives | enforce applicable employment, discrimination, contract, or safeguarding rights when lower remedies are unavailable or ineffective | obtain terms and records; refuse a role; appeal; change community or affiliation |
| Ordinary conflict | dialogue, voluntary peer support, cooling, reversible trial, ordinary boundaries | neutral intercommunity mediation, autonomous review, appeal of a separation decision | adjudicate legal claims or immediate danger when autonomous jurisdiction lacks scope, consent, independence, or enforceability | choose support; decline compelled disclosure; use a bypass route |
| Serious harm | protect immediate safety within legitimate scope, document observable conduct, preserve evidence | independent intake, survivor support, regional/autonomous investigation or justice where competent | investigate crime, assess specialized risk, order lawful restrictions, or determine custody where required | contact an autonomous, emergency, clinical, legal, advocacy, safeguarding, or rights forum directly |
| Care and medicine | mutual aid, meals, transport, companionship, implement a voluntary qualified plan | pooled financing, patient advocacy, regional training, quality and access audit | qualified diagnosis, treatment, medication, public-health action, or licensing oversight where the autonomous order cannot supply or lawfully govern it | independent care, confidentiality, second opinion, appeal, emergency access |
| Children and family | additional caring adults, schooling support, safe routines, age-appropriate participation | independent child advocate, family-contact support, autonomous safeguarding review where competent | custody, compulsory education, health, and protection backstop where rights, law, conflict, or capacity requires | child-accessible reporting and advocacy; protected family and outside contact |
| Evidence and reporting | log events, preserve originals, distinguish allegation from finding, protect correction | confidential intake, duplicate archives, independent review, accessible communication, regional appeal | subpoena, investigate, adjudicate, regulate, or publish official findings within legitimate scope when lower layers cannot | obtain, correct, and export records; report without local permission |
| Assets and exit | publish accounts, fund reserves, provide transition support, execute ordinary payments | neutral valuation, escrow, audit, pooled risk, leaver network, fork assistance | enforce fiduciary, trust, contract, property, insolvency, pension, and claims rights when needed | vested entitlement, advice, records, appeal, emergency withdrawal |
| Succession and fission | elect or replace leaders, amend rules, plan voluntary division | parity audit, successor support, shared records, intercommunity mobility | resolve contested title, debt, fiduciary, family, or legal claims beyond autonomous competence | refuse assignment, preserve household and family ties, choose affiliation |
| Territorial security and external threat | local vigilance, mutual aid, ordinary emergency action | translocal information, pooled capacity, coordinated defense within a legitimate order | strategic recognition, protection, rights forum, or public response when useful, requested, lawful, and trustworthy | report capture or abuse at any available competent layer |
| Outcomes and diffusion | collect local safety, wellbeing, participation, capacity, and learning data | compare communities, successors, leavers, and adaptations; audit missing data and adverse effects | maintain relevant official outcomes or independent evaluation where available | see results, contest the record, participate in evaluation, carry learning elsewhere |

The independent layer may belong to the community's own legal order. It can also be captured. Its authority should be task-specific, reviewable, and bypassable. Federations are most useful for functions a single community cannot neutrally or economically sustain: appeals, audits, pooled risk, records, specialist training, intercommunity mobility, territorial defense, alumni support, and planned-fission assistance (F-184, F-185, F-187, F-188, F-191).

Zapatista outward pedagogy adds a movement criterion to S-15 (F-189). A successful community architecture can teach and adapt practices beyond its territorial core without franchising a fixed blueprint. Diffusion, durable adoption, and better human outcomes remain separate measures.
"""


FINAL_CONCLUSIONS = """## Final conclusions

Everything learned can be compressed into thirteen decisive conclusions:

1. The recurring danger is not simply a bad leader. It is control that crosses functions and captures its own evidence and correction.
2. Formal democracy, equality, consensus, or consultation is inadequate unless practical veto, appointment, information, and appeal power can be used against the authority being challenged.
3. Communities need real, conduct-specific, reviewable separation authority; the absence of rules can be as unsafe as arbitrary rule.
4. Contribution, skill, charisma, cohesion, conformity, therapeutic fluency, long service, criminal history, poverty, and labels are not validated danger screens.
5. Community care is valuable when it remains support. It becomes governance when it controls medicine, custody, discipline, intimate life, evidence, or membership.
6. Children need direct rights and advocates because adult voluntariness and exit do not protect them.
7. Exit is not a sentence in an agreement. It is permission plus liquidity, records, housing and care continuity, family contact, advice, neutral review, and later usability.
8. Property title, accounts, appointments, records, debt, reserves, and succession are the practical constitution.
9. Independent correction is indispensable for some functions, but independence means separation from the implicated authority; it does not universally mean an institution outside the movement or operated by the state.
10. The competent layer depends on territorial control, scale, skill, rights, spillover, enforceability, and threat. Translocal federation can provide review and protection that an isolated community cannot.
11. Survival, cohesion, legal closure, conviction, leader removal, process completion, in-program gains, and worldwide resonance are not substitutes for disaggregated human outcomes.
12. A community can preserve purpose through transformation, migration, teaching, alumni networks, parallel institutions, succession, or voluntary fission; preserving the original entity is not always the goal.
13. The most defensible combined design is function-specific subsidiarity with legal pluralism, direct individual rights, and bypass routes. It is a synthesis of supported components, not a proven finished model.
"""


GAP_ROW = """| G-019 | D | The article treats legal and medical systems as selected couplings, while the earlier synthesis converted serious functions into a professional, judicial, or public layer that appeared universally state-external. | Separate four meanings that were collapsed: independent of the accused authority; outside the immediate community; outside the autonomous movement; and operated by the nation-state. Zapatista autonomous municipalities retained justice, health, education, land, and other governing functions while regional Good Government Councils mediated intermunicipal conflict, investigated complaints against autonomous councils, ordered correction, and monitored compliance (F-187). The 2023 GAL/CGAZ/ACGAZ redesign moved initiative downward while preserving need-based regional coordination and acknowledging contested territorial control (F-188). Zapatista pedagogy deliberately transmits and adapts communal practice beyond the territorial core, making diffusion a distinct success dimension (F-189). Cheran combined community-built government, security, and minor-case justice with strategic court recognition, serious-crime referral, and public subsidies (F-190). The CRAC-PC comparison found village custom insufficient by itself and regional Indigenous policing, justice, information, and solidarity protective against capture (F-191). UNDRIP Article 34 recognizes Indigenous juridical systems while retaining international human-rights standards (F-192). Replace the state-monopoly inference with the lowest competent non-self-reviewing layer plus a direct rights and bypass route. | This changes the theory of the institutional interface. The Zapatistas are not an exception to law or correction; they are a counterexample to treating state externality as the only form of law or correction. It also keeps the counterexample from becoming a romance of isolated village sufficiency. | “Selecting your couplings” / governance architecture / worldwide innovation | F-187, F-188, F-189, F-190, F-191, F-192 |"""


def build_unit_files() -> None:
    source_fields, _ = read_rows(SOURCES)
    assert set(SOURCE_ROWS[0]) == set(source_fields)
    write_rows(UNIT_SOURCES, source_fields, SOURCE_ROWS)

    ledger_fields, _ = read_rows(LEDGER)
    assert set(FINDING_ROWS[0]) == set(ledger_fields)
    write_rows(UNIT_LEDGER, ledger_fields, FINDING_ROWS)
    UNIT_REPORT.write_text(UNIT_REPORT_TEXT, encoding="utf-8")


def update_cumulative_csvs() -> None:
    source_fields, source_rows = read_rows(SOURCES)
    source_rows = [row for row in source_rows if not row["record_id"].startswith("LP-")]
    assert [row["record_id"] for row in source_rows[-4:]] == ["E-001", "E-002", "E-003", "E-004"]
    write_rows(SOURCES, source_fields, source_rows + SOURCE_ROWS)

    ledger_fields, ledger_rows = read_rows(LEDGER)
    ledger_rows = [row for row in ledger_rows if int(row["finding_id"][-3:]) <= 186]
    assert [row["finding_id"] for row in ledger_rows] == [f"F-{number:03d}" for number in range(1, 187)]
    write_rows(LEDGER, ledger_fields, ledger_rows + FINDING_ROWS)


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "adjacent child-response, assessment/review, durable treatment/transition, official-correction, and fair-separation/pooled-risk/planned-fission units",
        "adjacent child-response, assessment/review, durable treatment/transition, official-correction, fair-separation/pooled-risk/planned-fission, and autonomy/legal-pluralism units",
        "gap checkpoint",
    )
    text = replace_once_or_confirm(
        text,
        "this checkpoint retains 18 material items: **8 B, 7 C, and 3 D**.",
        "this corrected checkpoint retains 19 material items: **8 B, 7 C, and 4 D**.",
        "gap counts",
    )
    old = (
        "A court claims procedure, arbitration clause, or federation board answers a defined dispute; none supplies ordinary medical, family, housing, or safeguarding authority (F-183, F-184, F-186). | The state otherwise becomes the first real boundary only after internal failure or crisis; historical private punishment, medical refusal, or hidden construction cannot become a modern protocol."
    )
    new = (
        "A court claims procedure, arbitration clause, or federation board answers a defined dispute; none supplies ordinary medical, family, housing, or safeguarding authority (F-183, F-184, F-186). The autonomy/legal-pluralism unit corrects the state-monopoly inference: Zapatista regional councils, Cheran's hybrid order, and CRAC-PC show that independent review and protection can sit outside the implicated village while remaining inside an autonomous Indigenous or federated jurisdiction. Map when state, professional, public, or international backstops are actually needed, and preserve a direct rights route at every layer (F-187, F-188, F-190, F-191, F-192). | The surrounding state can become a late boundary after failure, a strategic recognition forum, a selective backstop, a dependency, or an aggressor. The design must name which role applies instead of assuming either state absence or state monopoly."
    )
    text = replace_once_or_confirm(text, old, new, "G-013 correction")
    if GAP_ROW not in text:
        anchor = "\n## Verification queue (not promoted to B/C/D)"
        assert anchor in text
        text = text.replace(anchor, "\n" + GAP_ROW + "\n" + anchor, 1)
    GAP_BANK.write_text(text, encoding="utf-8")


def gap_refs() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for line in GAP_BANK.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\| (G-\d{3}) \|", line)
        if not match:
            continue
        gap_id = match.group(1)
        for finding_id in sorted(set(re.findall(r"F-\d{3}", line))):
            result.setdefault(finding_id, []).append(gap_id)
    return result


def update_crosswalk() -> None:
    fields, rows = read_rows(CROSSWALK)
    rows = [row for row in rows if int(row["finding_id"][-3:]) <= 186]
    for row in rows:
        if row["primary_theme_id"] == "T-09":
            row["primary_theme"] = "independent correction, legal pluralism, and professional boundaries"
    ledger_fields, ledger_rows = read_rows(LEDGER)
    del ledger_fields
    ledger = {row["finding_id"]: row for row in ledger_rows}
    new_meta = {
        "F-187": ("S-01;S-09;S-10;S-15;S-16;S-17", "primary autonomous-governance architecture with implementation corroboration"),
        "F-188": ("S-01;S-11;S-12;S-15;S-16;S-17", "primary adaptive-governance architecture with contested-control boundary"),
        "F-189": ("S-11;S-13;S-17", "movement pedagogy and translocal-diffusion evidence with outcome boundary"),
        "F-190": ("S-09;S-10;S-11;S-12;S-15;S-16;S-17", "hybrid autonomous-state interface and observational outcome case"),
        "F-191": ("S-01;S-09;S-10;S-12;S-15;S-16;S-17", "comparative regional-federation and anti-capture mechanism evidence"),
        "F-192": ("S-06;S-10;S-15;S-16;S-17", "normative legal-pluralism and human-rights boundary"),
    }
    refs = gap_refs()
    for finding_id, (claims, role) in new_meta.items():
        source = ledger[finding_id]
        rows.append(
            {
                "finding_id": finding_id,
                "source_lane": "autonomous Indigenous governance and legal pluralism",
                "community_or_group": source["community_group"],
                "primary_theme_id": "T-13",
                "primary_theme": "autonomy, legal pluralism, and translocal federation",
                "synthesis_claim_ids": claims,
                "evidence_role": role,
                "confidence": source["confidence"],
                "external_verification_needed": source["external_verification_needed"],
                "article_gap_refs": ";".join(refs.get(finding_id, [])),
            }
        )
    for row in rows:
        row["article_gap_refs"] = ";".join(refs.get(row["finding_id"], []))
    assert [row["finding_id"] for row in rows] == [f"F-{number:03d}" for number in range(1, 193)]
    write_rows(CROSSWALK, fields, rows)


def update_final_report() -> None:
    text = REPORT.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Evidence base: 186 findings, F-001 through F-186",
        "Evidence base: 192 findings, F-001 through F-192",
        "report evidence base",
    )
    direct = """## Direct answer: the gap bank was not the final report

The research needed both the earlier horizontal synthesis and this correction pass.

The [article-gap bank](COMMUNITIES-ARTICLE-GAP-BANK.md) is an editorial control document. Its rows ask what the evidence implies for claims already present in the community article. It is not a neutral account of everything learned because the article's headings and propositions determine its questions and destinations.

The corrected gap bank reaches 189 of 192 findings. Three findings still do not appear in its article-facing rows: F-027 on Shaker communities as de facto child-care institutions, F-030 on an access-rich Rajneeshpuram account overtaken by later events, and F-032 on historical communal waves not establishing a present-day surge. The [finding crosswalk](COMMUNITIES-SYNTHESIS-CROSSWALK.csv) accounts for all 192 findings.

The first horizontal synthesis also inherited a sampling-frame error. Intentional communities inside nation-state jurisdiction and adjacent court, regulator, clinical, and inquiry records were allowed to imply that independent correction must be state-external. The autonomous-governance lane, summarized in [the legal-pluralism correction report](COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md), shows that the Zapatistas, Cheran, and CRAC-PC require a different rule: independence from the implicated authority and adequate scale are necessary; state operation is contingent.

The [evidence ledger](COMMUNITIES-EVIDENCE-LEDGER.csv) remains the authority for source facts, limits, alternative interpretations, outcomes, and verification needs.
"""
    text = replace_section(
        text,
        ("## Direct answer: the gap bank was not the final report",),
        "## Scope and evidentiary limits",
        direct,
        "direct answer",
    )
    text = replace_once_or_confirm(
        text,
        "20 bounded adjacent records covering child response, assessment and review, durable treatment and transition, official correction, and fair separation, pooled risk, and planned fission;",
        "29 bounded adjacent records covering child response, assessment and review, durable treatment and transition, official correction, fair separation, pooled risk, planned fission, autonomous Indigenous governance, legal pluralism, and translocal federation;",
        "scope adjacent records",
    )
    text = replace_once_or_confirm(text, "186 promoted findings.", "192 promoted findings.", "scope findings")
    text = replace_once_or_confirm(
        text,
        "The ledger assigns 88 findings high confidence, 22 medium-high, 67 medium, two medium-low, three low-medium, and four low. It marks 124 for external verification and 62 as not needing it at the present checkpoint.",
        "The ledger assigns 91 findings high confidence, 25 medium-high, 67 medium, two medium-low, three low-medium, and four low. It marks 128 for external verification and 64 as not needing it at the present checkpoint.",
        "confidence counts",
    )
    text = replace_once_or_confirm(text, "all 186 findings", "all 192 findings", "all findings first")
    text = replace_once_or_confirm(text, "all 186 are accounted for", "all 192 are accounted for", "all findings theme")
    text = replace_once_or_confirm(
        text,
        "The strongest counterdesign is not leaderlessness, bureaucracy, or state control of ordinary life. It is a modular arrangement in which authority is explicit, bounded by function, replaceable, separated from review of its own conduct, constrained by direct individual rights, and tested by later human outcomes.",
        "The strongest counterdesign is not leaderlessness, bureaucracy, state control of ordinary life, or isolated local sovereignty. It is a modular and potentially plural legal order in which authority is explicit, bounded by function, replaceable, separated from review of its own conduct, supported at the necessary translocal scale, constrained by direct individual rights, and tested by later human outcomes.",
        "executive correction",
    )
    old_theme = "| T-12 dangerous-child bounded null and adjacent response | 33 | What does and does not answer the hardest child-safety question? |"
    theme_13 = "| T-13 autonomy, legal pluralism, and translocal federation | 6 | Can independent correction and protection be autonomous, and when is a state interface contingent? |"
    new_theme = old_theme + "\n" + theme_13
    text = replace_once_or_confirm(text, old_theme, new_theme, "theme 13")
    while text.count(theme_13) > 1:
        text = text.replace("\n" + theme_13, "", 1)
    text = replace_section(
        text,
        (
            "## 9. Outside correction is necessary, function-specific, and fallible — T-09, S-10",
            "## 9. Independent correction is necessary; state externality is contingent — T-09, T-13, S-10, S-16, S-17",
        ),
        "## 10. Success is a vector, not a score — T-10, S-11",
        SECTION_9,
        "section 9",
    )
    text = replace_once_or_confirm(
        text,
        "Which institution performs each step depends on law and competence; the child cannot be made dependent on the home community's permission to reach it.",
        "Which institution performs each step depends on rights, jurisdiction, competence, independence, and available autonomous or public capacity; the child cannot be made dependent on the home community's permission to reach it.",
        "child interface",
    )
    text = replace_once_or_confirm(
        text,
        "| Local autonomy vs outside correction | culture, intimacy, self-government | some functions require independent, licensed, or statutory authority; outside systems can still be captured or wrong (F-102, F-123, F-145) |",
        "| Local autonomy vs independent correction | culture, intimacy, self-government | review must escape the implicated authority, but it may be autonomous, federated, Indigenous, professional, public, or state-based; every layer can be captured or wrong (F-102, F-123, F-145, F-187, F-190, F-191) |",
        "tension correction",
    )
    text = replace_section(
        text,
        ("## The combined architecture — S-15",),
        "## Minimum control set implied by the findings",
        COMBINED_SECTION,
        "combined architecture",
    )
    text = replace_once_or_confirm(
        text,
        "**A direct rights floor:** necessities, safety, privacy, care, outside and family contact, education, records, refusal, reply, appeal, advocacy, and lawful external access.",
        "**A direct rights floor:** necessities, safety, privacy, care, outside and family contact, education, records, refusal, reply, appeal, advocacy, and access to a competent autonomous, federated, public, or state route without local permission.",
        "rights floor",
    )
    text = replace_once_or_confirm(
        text,
        "**Independent truth channels:** accessible intake, confidentiality limits, anti-retaliation, preserved dissent, duplicate records, provenance, correction, and external escalation.",
        "**Independent truth channels:** accessible intake, confidentiality limits, anti-retaliation, preserved dissent, duplicate records, provenance, correction, and escalation outside the implicated authority at the necessary scale.",
        "truth channels",
    )
    text = replace_once_or_confirm(
        text,
        "**Named external interfaces:** purpose, jurisdiction, intake, evidence threshold, conflicts, proportionality, stopping rule, appeal, and after-action review for each outside function.",
        "**Named jurisdictional interfaces:** distinguish intercommunity, autonomous, federated, professional, public, state, and international layers; record purpose, trigger, jurisdiction, competence, conflicts, proportionality, stopping rule, bypass, appeal, and after-action review.",
        "interfaces control",
    )
    text = replace_once_or_confirm(
        text,
        "**The community can handle the hardest dangerous-child case internally.** The intentional-community evidence is a bounded null. The adjacent evidence supports an interface with trained and lawful systems, not a transfer of their powers (G-009 and G-018; S-06 and S-14).",
        "**The community can handle the hardest dangerous-child case internally.** The intentional-community evidence is a bounded null. The adjacent evidence supports an interface with trained, competent, independent, and rights-constrained systems. Those may be autonomous or public where genuinely capable; the evidence validates neither lay local monopoly nor automatic state monopoly (G-009 and G-018; S-06, S-14, S-16, and S-17).",
        "article child proposition",
    )
    text = replace_once_or_confirm(
        text,
        "**Legal and medical systems are selected couplings.** Communities can choose providers and institutional forms, but crime, custody, child protection, emergency care, public health, professional licensing, and other duties are not wholly optional (G-013; S-10).",
        "**Legal and medical systems are selected couplings.** The need for competence, rights, and non-self-review is not optional, but the institutional location is contingent. Zapatista and other Indigenous cases show autonomous justice, health, education, and regional correction; Cheran shows selective state recognition and referral; CRAC-PC shows protective translocal federation. The article should map which layer can legitimately perform each function under actual territorial and legal conditions (G-013 and G-019; S-10, S-16, and S-17).",
        "article coupling proposition",
    )
    unknown = "11. The 2023 Zapatista reorganization has no independent later-outcome evaluation in this unit, and no common outcome panel compares autonomous, hybrid, and state-centered jurisdictional arrangements."
    if unknown not in text:
        anchor = "10. It remains unknown which minimum set of safeguards produces the most protection with the least bureaucracy, cost, false-positive exclusion, or loss of local autonomy."
        assert anchor in text
        text = text.replace(anchor, anchor + "\n" + unknown, 1)
    text = replace_section(
        text,
        ("## Final conclusions",),
        "## Artifact guide",
        FINAL_CONCLUSIONS,
        "final conclusions",
    )
    guide = "- Read [COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md](COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md) for the state-monopoly correction, Zapatista synthesis, Indigenous comparators, and transfer boundaries.\n"
    if guide not in text:
        anchor = "- Read this report for the complete cross-corpus conclusions.\n"
        assert anchor in text
        text = text.replace(anchor, anchor + guide, 1)
    REPORT.write_text(text, encoding="utf-8")


def update_handoffs() -> None:
    text = STATE.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **186 findings** (`F-001` through `F-186`). The fair-separation unit added four findings in explicitly separate draft exit-instrument, pooled-risk, planned-fission/allocation, and court-supervised trust-closure lanes.",
        "`COMMUNITIES-EVIDENCE-LEDGER.csv` contains **192 findings** (`F-001` through `F-192`). The autonomy/legal-pluralism correction added six findings in an explicitly separate autonomous Indigenous governance lane; it does not alter the 984-journal-PDF or eight-standalone counts.",
        "state findings",
    )
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-ARTICLE-GAP-BANK.md` retains 18 reconciled article-gap items: 8 partially present, 7 apparently missing, and 3 challenges to the article.",
        "`COMMUNITIES-ARTICLE-GAP-BANK.md` retains 19 reconciled article-gap items: 8 partially present, 7 apparently missing, and 4 challenges to the article.",
        "state gaps",
    )
    text = replace_once_or_confirm(
        text,
        "`COMMUNITIES-FINAL-SYNTHESIS-REPORT.md` is the corpus-directed final report. It horizontally synthesizes all 186 findings across twelve themes, preserves counterevidence and transfer limits, and keeps the combined subsidiarity architecture explicitly model-assisted rather than source-validated.",
        "`COMMUNITIES-FINAL-SYNTHESIS-REPORT.md` is the corrected corpus-directed final report. It horizontally synthesizes all 192 findings across thirteen themes, preserves counterevidence and transfer limits, and keeps the combined subsidiarity/legal-pluralism architecture explicitly model-assisted rather than source-validated. `COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md` records the state-monopoly correction and Indigenous comparators.",
        "state final report",
    )
    text = replace_once_or_confirm(
        text,
        "The four-record fair-separation, pooled-risk, and planned-fission unit is complete. The assigned primary corpus and all five units in the finite adjacent-source roadmap are complete. There is no next research unit in the accepted roadmap.",
        "The original five-unit adjacent-source roadmap remains complete. The owner-authorized autonomy/legal-pluralism correction is also complete; it was a bounded correction to a sampling-frame error, not an unbounded reopening of the corpus.",
        "state boundary",
    )
    text = replace_once_or_confirm(
        text,
        "The post-corpus horizontal synthesis is complete. Every finding is mapped in `COMMUNITIES-SYNTHESIS-CROSSWALK.csv`; the synthesis adds no evidence rows and does not replace the article-directed gap bank.",
        "The corrected post-corpus horizontal synthesis is complete. Every finding through F-192 is mapped in `COMMUNITIES-SYNTHESIS-CROSSWALK.csv`; the new bounded lane adds six evidence rows and one article-gap challenge without replacing the article-directed gap bank.",
        "state synthesis boundary",
    )
    correction_bullet = "- The autonomy/legal-pluralism correction rejects the equation independent correction equals state intervention. Zapatista regional councils show internal autonomous correction; the 2023 redesign shows adaptive scale and contested control; Zapatista pedagogy adds a diffusion criterion; Cheran shows a hybrid strategic interface; CRAC-PC shows regional federation protecting isolated villages; and UNDRIP retains both Indigenous juridical systems and a human-rights floor.\n"
    if correction_bullet not in text:
        anchor = "## Current evidence picture\n\n"
        assert anchor in text
        text = text.replace(anchor, anchor + correction_bullet, 1)
    text = replace_once_or_confirm(
        text,
        "The strongest process contrast remains internal versus independent correction. Consultation, mediation, or settlement can be useful, but they do not substitute for independent evidence review, victim support, offender accountability, appeal, and outcome follow-up.",
        "The strongest process contrast is implicated authority versus independent correction, not community versus state. Consultation, mediation, or settlement can be useful, but they do not substitute for evidence review, victim support, offender accountability, appeal, and outcome follow-up at a competent autonomous, federated, professional, public, or state layer.",
        "state contrast",
    )
    text = replace_once_or_confirm(
        text,
        "Traditional-society evidence and intentional-community evidence must remain separate until a transfer argument is made. Execution, banishment, abandonment, policing, institutionalization, or state custody cannot be converted directly into a modern recommendation.",
        "Traditional-society, Indigenous autonomous-governance, intentional-community, professional, and state evidence must remain separate until a transfer argument is made. Indigenous rights and territorial jurisdiction are not generic voluntary-community exemptions; execution, banishment, abandonment, armed policing, institutionalization, or state custody cannot be converted directly into a modern recommendation.",
        "state evidence lanes",
    )
    text = replace_once_or_confirm(
        text,
        "2. The finite adjacent-source roadmap is complete. Do not invent another research unit; await explicit authority for article editing or a new bounded research question.",
        "2. The original adjacent-source roadmap and the owner-authorized legal-pluralism correction are complete. Do not invent another research unit; await explicit authority for article editing or a new bounded question.",
        "resume 2",
    )
    text = replace_once_or_confirm(
        text,
        "4. Keep traditional-society, clinical, legal, and intentional-community evidence separate until a transfer argument is made.",
        "4. Keep traditional-society, Indigenous autonomous-governance, clinical, state/legal, and intentional-community evidence separate until a transfer argument is made.",
        "resume 4",
    )
    STATE.write_text(text, encoding="utf-8")

    text = README.read_text(encoding="utf-8")
    text = replace_once_or_confirm(text, "**186** evidence findings (`F-001` through `F-186`)", "**192** evidence findings (`F-001` through `F-192`)", "README findings")
    text = replace_once_or_confirm(text, "**18** reconciled article gaps: 8 partially present, 7 apparently missing, and 3 challenges", "**19** reconciled article gaps: 8 partially present, 7 apparently missing, and 4 challenges", "README gaps")
    text = replace_once_or_confirm(text, "Final cross-corpus synthesis: **complete; all 186 findings mapped**", "Corrected cross-corpus synthesis: **complete; all 192 findings mapped across 13 themes**", "README synthesis")
    text = replace_once_or_confirm(
        text,
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The corpus-wide conclusion is [`recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`](recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md), with finding-level coverage in [`recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`](recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv). The latest bounded source report remains [`recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`](recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md).",
        "The authoritative handoff is [`recovered/COMMUNITIES-RESEARCH-STATE.md`](recovered/COMMUNITIES-RESEARCH-STATE.md). The corrected corpus-wide conclusion is [`recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`](recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md), with finding-level coverage in [`recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`](recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv). The load-bearing state-monopoly correction is [`recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`](recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md).",
        "README links",
    )
    layout = "- `recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md` — Zapatista, Cheran, CRAC-PC, and UNDRIP correction to the prior state-centric interface rule\n- `recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-EVIDENCE-LEDGER.csv` — six bounded correction findings, F-187 through F-192\n"
    if layout not in text:
        anchor = "- `recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md` — corpus-directed conclusions, tensions, boundaries, and remaining unknowns\n"
        assert anchor in text
        text = text.replace(anchor, anchor + layout, 1)
    text = replace_once_or_confirm(
        text,
        "- `recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv` — one-row-per-finding map from all 186 findings to synthesis themes, claims, evidence roles, and article gaps",
        "- `recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv` — one-row-per-finding map from all 192 findings to synthesis themes, claims, evidence roles, and article gaps",
        "README crosswalk count",
    )
    text = replace_once_or_confirm(
        text,
        "python recovered/test_final_synthesis_workflow.py\npython recovered/verify_final_synthesis.py",
        "python recovered/test_autonomy_legal_pluralism_workflow.py\npython recovered/verify_autonomy_legal_pluralism.py",
        "README commands",
    )
    text = replace_once_or_confirm(
        text,
        "The current verifier retains all Unit E checks, locks the evidence ledger and article-gap bank against synthesis-time mutation, requires one crosswalk row for every finding, verifies the twelve-theme and fifteen-claim architecture, confirms the three gap-unreferenced findings are nevertheless synthesized, and checks the final report's epistemic and transfer boundaries.",
        "The current verifier requires 192 sequential ledger and crosswalk rows, validates the nine-source and six-finding legal-pluralism unit, verifies the thirteen-theme and seventeen-claim report architecture, confirms the three gap-unreferenced findings are nevertheless synthesized, and checks the final report's epistemic and transfer boundaries.",
        "README corrected verifier",
    )
    README.write_text(text, encoding="utf-8")

    text = INDEX.read_text(encoding="utf-8")
    old_order = "3. `../recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`\n4. `../recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`\n5. the latest bounded report, currently `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`\n6. `../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`\n7. `../recovered/COMMUNITIES-SOURCE-INVENTORY.csv`\n8. `../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`\n9. current discovery, update, test, and verification scripts"
    new_order = "3. `../recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`\n4. `../recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`\n5. `../recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`\n6. the prior finite-roadmap endpoint, `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`\n7. `../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`\n8. `../recovered/COMMUNITIES-SOURCE-INVENTORY.csv`\n9. `../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`\n10. current discovery, update, test, and verification scripts"
    text = replace_once_or_confirm(text, old_order, new_order, "index read order")
    plan_line = "The autonomy and legal-pluralism correction is recorded in `superpowers/plans/2026-08-15-autonomy-legal-pluralism-correction.md`; it was a bounded response to an owner-identified sampling-frame error and does not reopen the completed primary corpus.\n\n"
    if plan_line not in text:
        anchor = "The corpus-directed synthesis method is recorded in `superpowers/plans/2026-08-15-final-synthesis-pass.md`. The gap bank remains the article-change specification; it is not the final research report.\n\n"
        assert anchor in text
        text = text.replace(anchor, anchor + plan_line, 1)
    INDEX.write_text(text, encoding="utf-8")

    text = AGENTS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Regression suite: `python recovered/test_final_synthesis_workflow.py` (or the current bounded-unit successor)",
        "Regression suite: `python recovered/test_autonomy_legal_pluralism_workflow.py` (current bounded-unit successor)",
        "AGENTS regression",
    )
    text = replace_once_or_confirm(
        text,
        "Full source verification: `python recovered/verify_final_synthesis.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "Current repository-contained verification: `python recovered/verify_autonomy_legal_pluralism.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "AGENTS verification",
    )
    AGENTS.write_text(text, encoding="utf-8")


def main() -> None:
    build_unit_files()
    update_cumulative_csvs()
    update_gap_bank()
    update_crosswalk()
    update_final_report()
    update_handoffs()
    print("autonomy/legal-pluralism correction applied")


if __name__ == "__main__":
    main()
