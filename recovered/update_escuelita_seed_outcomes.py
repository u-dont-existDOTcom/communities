#!/usr/bin/env python3
"""Apply the bounded Escuelita seed-outcomes research unit.

The pass adds eighteen public-source records, six findings, one synthesis
claim, and one article-gap row without editing article prose or reopening the
completed primary corpora.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
UNIT_LEDGER = ROOT / "COMMUNITIES-ESCUELITA-SEED-OUTCOMES-EVIDENCE-LEDGER.csv"
SOURCES = ROOT / "COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv"
UNIT_SOURCES = ROOT / "COMMUNITIES-ESCUELITA-SEED-OUTCOMES-SOURCE-INVENTORY.csv"
CROSSWALK = ROOT / "COMMUNITIES-SYNTHESIS-CROSSWALK.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
REPORT = ROOT / "COMMUNITIES-FINAL-SYNTHESIS-REPORT.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
README = REPOSITORY / "README.md"
INDEX = REPOSITORY / "docs" / "INDEX.md"
AGENTS = REPOSITORY / "AGENTS.md"
LESSONS = REPOSITORY / "COMMUNITY-DEVELOPMENT-LESSONS.md"


SOURCE_FIELDS = [
    "record_id", "lead_source_id", "lane", "title", "authors", "year",
    "publication", "doi", "canonical_url", "accessed_on", "access_status",
    "evidence_scope", "sequence_allegation", "sequence_assessment",
    "sequence_intervention", "sequence_review", "sequence_later_outcome",
    "disposition", "notes",
]


SOURCE_VALUES = [
    [
        "ES-001", "", "Escuelita primary design and outward intention",
        "Space full in communities for the Zapatista little school",
        "Ejercito Zapatista de Liberacion Nacional; Subcomandante Insurgente Moises",
        "2013", "Enlace Zapatista", "",
        "https://enlacezapatista.ezln.org.mx/2013/06/16/space-full-in-communities-for-the-zapatista-little-school/",
        "2026-08-15", "complete official English translation inspected",
        "First-session capacity, host-family and Votan teaching structure, materials, and stated possibility of sending teachers elsewhere",
        "not applicable", "community capacity was expanded from 500 to 1000 and then 1500 students",
        "families, guardians, teachers, videos, textbooks, later remote materials, and possible invited teaching teams",
        "the movement limited enrollment to housing and care capacity",
        "establishes exposure design and outward intent, not alumni adoption or outcomes",
        "F-198 search-frame context; no separate finding",
        "Primary movement statement. Intent is not evidence that later teaching teams or descendant institutions materialized.",
    ],
    [
        "ES-002", "ES-001", "Escuelita primary participant profile",
        "L@s condiscipul@s V. L@s estudiant@s",
        "Ejercito Zapatista de Liberacion Nacional; Subcomandante Insurgente Marcos",
        "2013", "Enlace Zapatista", "",
        "https://enlacezapatista.ezln.org.mx/2013/06/27/ls-condiscipuls-v-ls-estudiants/",
        "2026-08-15", "complete official Spanish statement inspected",
        "Invitation responses and first August 2013 community and CIDECI enrollment profile",
        "not applicable", "about 3000 invitations, about 2500 affirmative replies, 1500 community students, and about 200 CIDECI students",
        "large in-person and materials-based political education encounter",
        "no public alumni registry or longitudinal follow-up is supplied",
        "large exposure population; no adoption, project-formation, failure, or later-outcome denominator",
        "F-198 search-frame context; no separate finding",
        "Use the official approximate counts as design context, not as a count of later sprouts.",
    ],
    [
        "ES-003", "", "Escuelita alumni immediate solidarity",
        "Miembros de la UNAM apoyan a las bases de apoyo zapatistas agredidas",
        "UNAM members and Escuelita alumni", "2014", "Enlace Zapatista", "",
        "https://enlacezapatista.ezln.org.mx/2014/02/24/miembros-de-la-unam-apoyan-a-las-bases-de-apoyo-zapatistas-agredidas/",
        "2026-08-15", "complete officially reposted statement inspected",
        "Public solidarity action by university members including recent Escuelita alumni",
        "reported aggression against Zapatista support bases", "participants explicitly connect response to recent Escuelita coexistence",
        "public denunciation and solidarity statement", "no later organizational review described",
        "observable alumni action within months; no persistence or community outcome",
        "F-193 promoted",
        "Strong for an alumni identity and action; not a representative alumni outcome.",
    ],
    [
        "ES-004", "", "Escuelita alumni international solidarity",
        "Pronunciamiento de alumn@s de la Escuelita zapatista en agosto de 2013",
        "Ten August 2013 Escuelita alumni in Italy", "2014", "Enlace Zapatista", "",
        "https://enlacezapatista.ezln.org.mx/2014/05/06/pronunciamiento-de-alumns-de-la-escuelita-zapatista-en-agosto-de-2013/",
        "2026-08-15", "complete officially reposted statement inspected",
        "Named international alumni statement after the La Realidad attack",
        "killing, injuries, and destruction reported at La Realidad", "signers identify their shared August 2013 student experience",
        "joint denunciation, demands, and solidarity", "no organizational structure or follow-up review described",
        "observable international alumni mobilization; no descendant institution or human outcome",
        "F-193 promoted",
        "Named signers establish participation and joint action, not a stable organization.",
    ],
    [
        "ES-005", "", "Escuelita alumni material solidarity",
        "Vendimia solidaria desde Colima en apoyo a la transportacion del CNI",
        "Escuelita alumni and Sixth Declaration adherents in Colima", "2014", "Enlace Zapatista", "",
        "https://enlacezapatista.ezln.org.mx/2014/07/17/vendimia-solidaria-desde-colima-en-apoyo-a-la-transportacion-del-cni/",
        "2026-08-15", "complete officially reposted event notice inspected",
        "Fundraising event organized by alumni and allies for CNI travel",
        "travel-resource need for Indigenous delegates", "local organizers set a public fundraiser",
        "food sale, exhibits, media, and cultural activities", "no audited amount or later review reported",
        "observable material solidarity; no evidence of organizational durability or participant outcomes",
        "F-193 promoted",
        "One event demonstrates collective capacity but not institutional replication.",
    ],
    [
        "ES-006", "ES-003", "Escuelita alumni continuing political action",
        "La Sexta llama a marchar: 11 meses de impunidad. Nos faltan 43",
        "Sixth Declaration collectives, organizations, individuals, and Escuelita alumni in the Valley of Mexico",
        "2015", "Centro de Medios Libres Mexico", "",
        "https://www.centrodemedioslibres.org/2015/08/26/11-meses-de-impunidad-y-nos-faltan-43-la-exta-lama-a-marchar/",
        "2026-08-15", "complete public event notice inspected",
        "Escuelita alumni named among conveners of an Ayotzinapa march almost two years after the first session",
        "disappearance of 43 students and killings", "collectives and alumni issue a public call",
        "march and demands for truth, justice, and release of political prisoners", "no participation denominator or later review",
        "alumni category remained politically operative in 2015; no direct communal institution outcome",
        "F-193 promoted",
        "Supports continuity beyond the immediate aftermath, not continuous identity of any one group.",
    ],
    [
        "ES-007", "", "Escuelita-linked post-2013 coordination candidate",
        "Festival y Comparticion CompArte por la Humanidad sede alterna Grietas en el Muro",
        "Espacio de Coordinacion Grietas en el Muro and partner collectives", "2016", "Enlace Zapatista", "",
        "https://enlacezapatista.ezln.org.mx/2016/07/02/festival-y-comparticion-comparte-por-la-humanidad-sede-alterna-grietas-en-el-muro/",
        "2026-08-15", "complete officially reposted event statement inspected",
        "Creation of an alternate CompArte site by collectives and individuals including Sixth Declaration adherents and Escuelita students",
        "need for a local response to the EZLN CompArte call", "mixed group of existing collectives, adherents, and alumni organized a Mexico City site",
        "two-day festival, prior sharing session, workshops, arts, dialogue, and exchange",
        "named coordination space and partner list provide an observable organizational node",
        "post-Escuelita organization-level candidate with explicitly mixed lineage; later persistence requires separate records",
        "F-195 promoted",
        "Does not say the Escuelita alone founded the coordination space or describe its internal governance.",
    ],
    [
        "ES-008", "ES-007", "Escuelita-linked candidate persistence",
        "Viaje colectivo a la Asamblea convocada por el CNI El Istmo es Nuestro",
        "Espacio de Coordinacion Grietas en el Muro; Mujeres y la Sexta; Red Movimiento y Corazon Zapatista",
        "2019", "Enlace Zapatista", "",
        "https://enlacezapatista.ezln.org.mx/2019/08/29/viaje-colectivo-a-la-asamblea-convocada-por-el-cni-el-istmo-es-nuestro/",
        "2026-08-15", "complete officially reposted event notice inspected",
        "Named Grietas en el Muro coordination role three years after the 2016 CompArte record",
        "travel and coordination for a CNI assembly", "three organizations convened transportation",
        "collective travel and assembly support", "no internal governance or membership continuity audit",
        "public organizational activity in 2019",
        "F-195 persistence corroboration; no separate finding",
        "Activity persistence is not proof that the same people or practices persisted.",
    ],
    [
        "ES-009", "ES-007", "Escuelita-linked candidate persistence",
        "Diversos colectivos convocan al Mictlan Rebelde 2022",
        "Espacio de Coordinacion Grietas en el Muro and partner collectives", "2022", "Enlace Zapatista", "",
        "https://enlacezapatista.ezln.org.mx/2022/10/29/diversos-colectivos-convocan-al-mictlan-rebelde-2022-no-morira-la-flor-de-la-palabra/",
        "2026-08-15", "complete officially reposted event notice inspected",
        "Grietas en el Muro named as a convener of the eighteenth Mictlan Rebelde gathering",
        "militarization and violence against Indigenous peoples", "partner organizations issued a public call",
        "political-cultural gathering, workshops, music, art, and memory work", "no organization-level outcome evaluation",
        "public organizational activity in 2022",
        "F-195 persistence corroboration; no separate finding",
        "Supports durable public visibility of the coordination space, not residential or governance replication.",
    ],
    [
        "ES-010", "ES-007", "Escuelita-linked candidate persistence",
        "Pronunciamiento alto a la guerra contra los pueblos zapatistas",
        "Congreso Nacional Indigena and international and Mexican signatories", "2024", "Congreso Nacional Indigena", "",
        "https://www.congresonacionalindigena.org/2024/10/21/pronunciamiento-alto-a-la-guerra-contra-los-pueblos-zapatistas/",
        "2026-08-15", "complete primary movement statement and organization list inspected",
        "Espacio de Coordinacion Grietas en el Muro appears as a named Mexican signatory in October 2024",
        "violence and threats against Zapatista communities", "CNI assembled a broad solidarity statement and signatory list",
        "public denunciation and coordinated solidarity", "signatory presence only; no audit of activity or membership",
        "confirms public organizational identity through at least October 2024",
        "F-195 persistence corroboration; no separate finding",
        "A signature establishes current public identification, not continuous operations or outcomes.",
    ],
    [
        "ES-011", "", "participant follow-up and practice transfer",
        "On Community Building and the Zapatista Movement",
        "Charlotte Maria Saenz; Zara Zimbardo", "2023", "California Institute of Integral Studies podcast transcript", "",
        "https://www.ciis.edu/podcast/charlotte-saenz-and-zara-zimbardo-community-building-and-zapatista-movement",
        "2026-08-15", "complete public transcript inspected",
        "Organizer reflection on five or six CIIS delegations between 2012 and 2018 and later encounters with former students",
        "hierarchy, colonialism, and fragmented ways of living and learning", "first-person retrospective observation, not a structured alumni study",
        "Escuelita and other encounters; later care, organizing, political, and NGO work said to carry principles",
        "former students were encountered at a later Albuquerque Zapatista encuentro",
        "qualitative practice-transfer signal with bundled exposure and no named denominator or human outcomes",
        "F-194 promoted",
        "The trips included several kinds of Zapatista encounter, so the effect cannot be assigned solely to the Escuelita.",
    ],
    [
        "ES-012", "LP-005", "Zapatista seed-pedagogics qualitative study",
        "Zapatista Seed Pedagogics: Beyond Rights, Creating a Decolonizing Co-education",
        "Charlotte Maria Saenz", "2023", "International Journal of Human Rights Education 7(1)", "",
        "https://repository.usfca.edu/ijhre/vol7/iss1/4/",
        "2026-08-15", "public abstract, author metadata, and methods description inspected; PDF endpoint returned 403 in this pass",
        "Qualitative transgeographic interviews with pro-Zapatista interlocutors involved in local social-change processes",
        "oppressive power relations and colonial education", "qualitative interviews with movement-adjacent interlocutors",
        "learning to learn and listen differently and mutual political-ethical education",
        "reflexive and relational process rather than a fixed blueprint",
        "supports outward learning and local process involvement but not Escuelita-specific project lineage or comparative outcomes",
        "F-194 promoted",
        "Sympathetic interlocutors are not a representative alumni cohort.",
    ],
    [
        "ES-013", "ES-012", "Zapatista translocal seed-pedagogics follow-up",
        "Sowing Indigenous Autonomy: Building a Common Political-Ethical Territory of Struggle with Zapatista Seed Pedagogics",
        "Charlotte Maria Saenz", "2024", "Latin American Perspectives 51(5)", "10.1177/0094582X241288861",
        "https://doi.org/10.1177/0094582X241288861", "2026-08-15",
        "publisher abstract, methods summary, metadata, and references inspected",
        "Interviews with external activists in neo-Zapatista networks over three decades",
        "internalized hierarchies, vanguards, historical erasure, and nation-state political identity",
        "qualitative interviews and evolving conversations", "reflexive learning, ancestral memory, and organization of collectivities",
        "life-long learning and transgeographic political-ethical subjectivity",
        "reports collective organization beyond Chiapas without isolating the Escuelita or measuring durability and human outcomes",
        "F-194 promoted",
        "A broader Zapatista diffusion study; it cannot identify an Escuelita treatment effect.",
    ],
    [
        "ES-014", "", "named Escuelita participant micro-trace",
        "Locked Arms and Open Hearts for Ayotzinapa", "Levi Gahman", "2014", "Briarpatch Magazine", "",
        "https://briarpatchmagazine.com/articles/view/locked-arms-open-hearts-for-ayotzinapa",
        "2026-08-15", "complete public article and author note inspected",
        "Former Escuelita student's account of a small Okanagan Valley student solidarity mobilization",
        "disappearance and killing of Ayotzinapa students", "participants organized despite limited time, money, and institutional access",
        "banners, photos, gatherings, and transnational solidarity", "author note links participant identity to RAMA organizing",
        "named path from Escuelita participation to later organizing activity; no causal or outcome evaluation",
        "F-196 promoted",
        "The article does not say the Escuelita created RAMA or caused the action.",
    ],
    [
        "ES-015", "ES-014", "named participant knowledge transmission",
        "Food Sovereignty in Rebellion: Decolonization, Autonomy, Gender Equity and the Zapatista Solution",
        "Levi Gahman", "2016", "Solutions Journal 7(4)", "",
        "https://livrepository.liverpool.ac.uk/3031518/", "2026-08-15",
        "institutional repository metadata and indexed public reprint inspected",
        "Former student's later public analysis of Zapatista agroecology, education, autonomy, and gender equity",
        "neoliberal food systems and colonial domination", "participant observation and movement interpretation",
        "public knowledge transmission and continuing organizing and editorial roles",
        "author thanks the Zapatistas for accepting him into their school",
        "continuing individual pathway; no alumni cohort, organizational adoption test, or later human outcome",
        "F-196 promoted",
        "Useful as a traceable microcase, not proof of representative diffusion.",
    ],
    [
        "ES-016", "", "pre-Escuelita transnational diffusion control",
        "How Activists Take Zapatismo Home: South-to-North Dynamics in Transnational Social Movements",
        "Abigail Andrews", "2011", "Latin American Perspectives 38(1)", "10.1177/0094582X10384217",
        "https://doi.org/10.1177/0094582X10384217", "2026-08-15",
        "publisher abstract, metadata, and references inspected",
        "Ground-level implications of Northern activists adopting Zapatista tactics and reflexive politics before the Escuelita",
        "economic and political domination and Northern activist privilege", "qualitative movement research",
        "local reflexivity and changes in activist focus", "study also notes rifts with former allies and resource diversion from Chiapas",
        "demonstrates outward Zapatista adaptation before 2013 and supplies an attribution control",
        "F-197 promoted",
        "Post-2013 Zapatista resemblance cannot by itself establish Escuelita descent.",
    ],
    [
        "ES-017", "", "pre-Escuelita organizational diffusion control",
        "The Bridge Called Zapatismo: Transcultural and Transnational Activist Networks in Los Angeles and Beyond",
        "Kara Zugman Dellacioppa", "2011; book 2009", "Latin American Perspectives 38(1); Lexington Books", "10.1177/0094582X10384216",
        "https://doi.org/10.1177/0094582X10384216", "2026-08-15",
        "publisher abstract and book description inspected",
        "Ethnographic study of Casa del Pueblo and Zapatista-inspired community organizations in Mexico City and Los Angeles before 2013",
        "immigrant exclusion and one-way models of political diffusion", "ethnographic research on transnational activist networks",
        "community organizing of undocumented immigrants and local adaptation of Zapatista political culture",
        "book emphasizes complex and problematic linkages, not simple copying",
        "organizational Zapatista diffusion predates the Escuelita",
        "F-197 promoted",
        "A genuine broader-Zapatista sprout that must not be recoded as an Escuelita result.",
    ],
    [
        "ES-018", "", "pre-Escuelita pedagogical institution control",
        "In Defense of Conviviality and the Collective Subject", "Manuel Callahan", "2012", "Polis 11(33)", "10.4067/S0718-65682012000300004",
        "https://doi.org/10.4067/S0718-65682012000300004", "2026-08-15",
        "open abstract, metadata, and indexed article summary inspected",
        "Universidad de la Tierra Califas described before the Escuelita as a project between network and collective pedagogy and as Zapatismo beyond Chiapas",
        "democratic despotism and community fragmentation", "political-theoretical essay grounded in local project practice",
        "collective pedagogy, convivial tools, and community regeneration",
        "no Escuelita exposure was possible because the publication predates it",
        "preexisting Zapatista pedagogical ecosystem and direct attribution control",
        "F-197 promoted",
        "Later Escuelita participants may have joined or strengthened the project, but the project itself is not an Escuelita seedling.",
    ],
]


LEDGER_FIELDS = [
    "finding_id", "track", "source_record_id", "source_file",
    "journal_volume_issue_year", "article_title", "author", "community_group",
    "page_locator", "printed_page_number", "supporting_excerpt", "source_access",
    "evidence_type", "exact_factual_observation", "what_source_establishes",
    "what_source_does_not_establish", "author_interpretation",
    "alternative_interpretation", "response_process", "outcome",
    "transferability", "article_gap_status", "likely_article_destination",
    "confidence", "external_verification_needed", "notes",
]


FINDING_VALUES = [
    [
        "F-193", "Track G Escuelita alumni continuity and solidarity",
        "ES-003; ES-004; ES-005; ES-006",
        "public alumni statements and event notices linked in the unit source inventory",
        "2014-2015 public records with 2016 corroboration",
        "Escuelita alumni as continuing translocal collective actors",
        "UNAM members and regional alumni and allies", "Escuelita alumni across Mexico, Italy, and other locations",
        "complete public statements and notices", "", "", "complete public records inspected",
        "primary or participant-authored public movement records",
        "Within months of the first sessions, Escuelita alumni in several geographies publicly identified and acted together through denunciations, solidarity statements, fundraising, and coordination. Alumni remained a named constituency in Valley of Mexico action in 2015 and CompArte and CNI activity in 2016.",
        "The Escuelita produced or reinforced an alumni relation that reached lineage level 2 and supported repeated collective action across multiple places for at least three years.",
        "It does not give the number or proportion of alumni active, prove continuous membership of any group, isolate the Escuelita from prior Sixth Declaration ties, or establish a new communal institution or human outcome.",
        "The records frame shared learning and solidarity as an obligation to act with threatened Zapatista and Indigenous communities.",
        "Many participants were already activists; the Escuelita may have intensified an existing network rather than created it. Public archives disproportionately preserve visible solidarity actions.",
        "shared participant identity; local coordination; public statements; fundraising; marches; cultural and political events",
        "Documented alumni mobilization from 2014 through 2016; organizational persistence and human outcomes are unmeasured.",
        "High for distinguishing continued relation from inspiration. Medium for attributing network creation to the Escuelita. Low for communal replication.",
        "B", "Worldwide communal innovation / movement continuity / alumni infrastructure",
        "medium-high", "yes",
        "Lineage level 2. Do not count every Sixth Declaration action as an Escuelita outcome.",
    ],
    [
        "F-194", "Track G Escuelita practice transfer and seed pedagogics",
        "ES-011; ES-012; ES-013",
        "CIIS transcript and qualitative Zapatista seed-pedagogics studies",
        "2023-2024", "Participant follow-up and translocal Zapatista seed pedagogics",
        "Charlotte Maria Saenz; Zara Zimbardo", "CIIS delegations and pro-Zapatista interlocutors",
        "public transcript and publisher or repository abstracts", "", "", "public transcript and indexed scholarly records inspected",
        "first-person retrospective follow-up plus qualitative interview research",
        "A delegation organizer reported encountering former students later and seeing principles carried into care, organizing, political, and NGO work. Qualitative studies with pro-Zapatista interlocutors describe changes in listening, hierarchy, memory, and collective organization outside Chiapas.",
        "There is credible lineage-level-3 evidence that Zapatista encounters, including the Escuelita, informed later practice and collectivities.",
        "The exposure combines the Escuelita with other encounters and long accompaniment. The sources do not identify an Escuelita-only cohort, name a denominator, count failures, or measure institutional durability and human outcomes.",
        "Saenz theorizes a life-long mutual political-ethical education rather than export of a fixed institutional recipe.",
        "Sympathetic participants may overreport transformation, and the observed effects may come from prior activism, later encounters, or selection into the delegations.",
        "immersive learning; return to home contexts; reflection on hierarchy; practice adaptation; continuing encounter networks",
        "Reported practice transfer and collective political learning; no comparative or longitudinal outcome panel.",
        "Medium-high for recognizing practice transfer as a separate diffusion outcome. Low for causal effect size or successful community replication.",
        "B", "Worldwide communal innovation / internal school-research function / diffusion measurement",
        "medium", "yes",
        "Lineage level 3 with bundled exposure. Keep it separate from levels 4 through 6.",
    ],
    [
        "F-195", "Track G Escuelita-linked durable coordination candidate",
        "ES-007; ES-008; ES-009; ES-010",
        "officially reposted 2016-2022 records and 2024 CNI statement",
        "2016-2024", "Espacio de Coordinacion Grietas en el Muro as a mixed-lineage sprout candidate",
        "Grietas en el Muro and partner collectives", "Mexico City Zapatista-aligned coordination ecology",
        "complete public event and signatory records", "", "", "complete public records inspected",
        "organization event trail and movement-primary signatory records",
        "A 2016 CompArte notice says collectives and individuals including Sixth Declaration adherents and Escuelita students created an alternate festival site and names Espacio de Coordinacion Grietas en el Muro among organizers. The coordination space appears in 2019 and 2022 organizing records and as a named Mexican signatory in an October 2024 CNI statement.",
        "This is the strongest located lineage-level-4 candidate: a named post-Escuelita coordination space created with an explicit alumni role and publicly visible over at least eight years.",
        "The founding record is explicitly mixed-lineage and does not assign sole causation to the Escuelita. The trail does not prove continuous membership, internal governance, residential communal life, practice fidelity, or human outcomes.",
        "The organizers present art, exchange, memory, travel, and solidarity as tools for building resistance and autonomy in their own context.",
        "The name may have consolidated preexisting collectives around one event, while later appearances could reflect a small or changing core. Public visibility is not institutional health.",
        "local response to movement call; coordination space; repeated events; CNI solidarity; durable public identity",
        "Public activity from 2016 through at least October 2024; no level-5 shared-life institution or level-6 outcome evidence.",
        "High for a durable named coordination trail. Medium for Escuelita contribution to origin. Low for residential-governance replication.",
        "B", "Worldwide communal innovation / movement continuity / candidate descendant case",
        "medium-high", "yes",
        "Lineage level 4, mixed origin. This is a political-cultural coordination institution, not a replicated Zapatista municipality.",
    ],
    [
        "F-196", "Track G named Escuelita participant pathway",
        "ES-014; ES-015",
        "Briarpatch participant account and later institutional-repository publication record",
        "2014-2016 with later public scholarship", "Levi Gahman participant-to-organizing micro-trace",
        "Levi Gahman", "Okanagan Valley student organizers; RAMA; public and scholarly audiences",
        "complete 2014 article and indexed later records", "", "", "public records inspected",
        "named participant microhistory and public knowledge transmission",
        "A former Escuelita student documented a 2014 student solidarity mobilization, was identified as organizing with RAMA, later thanked the Zapatistas for accepting him into their school, and continued public and scholarly work on autonomy, mutual aid, food sovereignty, and social reproduction.",
        "A named individual trace connects participation to later organizing and knowledge transmission, avoiding a wholly anonymous influence claim.",
        "It does not establish that the Escuelita created RAMA, caused the action, produced organizational adoption, or generated later communal or human outcomes. One individual cannot represent the cohort.",
        "Gahman presents Zapatismo as a practical source for anti-capitalist, decolonial, gender-just collective life.",
        "The participant was already aligned with the Sixth and may have entered the Escuelita through prior organizing; later work may reflect broader Zapatista engagement.",
        "attendance; solidarity action; migrant-support organizing; writing and teaching",
        "Observable continuing pathway; causal contribution and outcome are unmeasured.",
        "Medium for a named lineage trace. Low for generalization or institutional replication.",
        "B", "Worldwide communal innovation / participant pathways / qualitative examples",
        "medium", "yes",
        "Lineage level 3 and possibly 4 only if a later project documents adoption; the current record does not.",
    ],
    [
        "F-197", "Track G Escuelita causal-attribution control",
        "ES-016; ES-017; ES-018",
        "pre-2013 scholarly records on transnational Zapatismo, Casa del Pueblo, and Universidad de la Tierra Califas",
        "2009-2012", "Transnational Zapatista diffusion predates the Escuelita",
        "Abigail Andrews; Kara Zugman Dellacioppa; Manuel Callahan",
        "Northern activist networks; Casa del Pueblo; Universidad de la Tierra Califas",
        "publisher abstracts, book description, and open indexed article summary", "", "", "public scholarly records inspected",
        "pre-event ethnography, movement research, and practice-grounded political theory",
        "Before the 2013 Escuelita, scholars documented activists taking Zapatismo home, Zapatista-inspired community organizations in Los Angeles and Mexico City, Casa del Pueblo organizing undocumented immigrants, and UT Califas as collective pedagogy and Zapatismo beyond Chiapas.",
        "The Escuelita entered an existing transnational Zapatista ecology. A post-2013 date or Zapatista resemblance cannot establish Escuelita descent; explicit participant or organizational lineage is required.",
        "The controls do not show that the Escuelita had no later effect on these networks or that every later project was preexisting. They do not evaluate post-2013 reinforcement or grafting.",
        "The authors describe adaptation, reflexivity, and complex South-to-North networks rather than simple institutional copying.",
        "Later Escuelita participation could materially strengthen, redirect, or connect an older organization without being its founding cause.",
        "date the organization; identify prior Zapatista exposure; require explicit lineage; classify reinforcement separately from creation",
        "Strong pre-2013 evidence of broader Zapatista diffusion; no Escuelita-specific outcome by definition.",
        "High for causal attribution control and for the grafting distinction.",
        "B", "Worldwide communal innovation / source-quality and lineage audit",
        "high", "no",
        "Preexisting soil is evidence of Zapatista success, but not an Escuelita seedling.",
    ],
    [
        "F-198", "Track G Escuelita descendant bounded null",
        "ES-001 through ES-018",
        "bounded public search across primary movement archives, alumni actions, scholarly studies, participant traces, candidate organizations, and pre-event controls",
        "records through October 2024 located in a search completed 2026-08-15",
        "No located Escuelita descendant reaches durable communal replication plus measured human outcomes",
        "research synthesis", "Escuelita alumni and candidate descendant projects",
        "source inventory and report search lanes", "", "", "bounded public search; no inaccessible or private alumni archive claimed",
        "bounded negative search result",
        "The search located no public participant registry, longitudinal or comparative alumni cohort, counted adoption or failure rate, new residential community or autonomous governing federation with an explicit Escuelita founding chain, or later safety, child-wellbeing, autonomy, retention, material-viability, and relational outcomes.",
        "The current evidence ceiling is lineage level 4 for one mixed-origin coordination space. Stronger claims of durable communal replication or success remain unverified.",
        "This does not establish historical absence. Quiet projects, failed attempts, renamed adaptations, nonpublic records, and nonindexed languages or geographies may be missing.",
        "not applicable; this is a bounded synthesis disposition",
        "The absence of systematic follow-up may reflect a movement ethic against standardized replication or surveillance as well as ordinary archival loss.",
        "define lineage ladder; search named alumni and projects; apply pre-event controls; record the evidence ceiling and missing denominator",
        "No level-5 direct descendant or level-6 outcome panel located; levels 2-4 have positive evidence.",
        "High for defining the missing evidence and preventing overclaiming. Medium for the bounded null because the search cannot cover private and unnamed adaptations.",
        "B", "Worldwide communal innovation / outcome dashboard / research agenda",
        "medium-high", "yes",
        "A bounded null is a result about this search, not proof that no Escuelita descendant exists.",
    ],
]


CROSSWALK_FIELDS = [
    "finding_id", "source_lane", "community_or_group", "primary_theme_id",
    "primary_theme", "synthesis_claim_ids", "evidence_role", "confidence",
    "external_verification_needed", "article_gap_refs",
]


CROSSWALK_VALUES = [
    ["F-193", "Escuelita alumni follow-up", "translocal Escuelita alumni", "T-11", "succession, fission, and movement continuity", "S-13;S-18", "positive continuity component with denominator limits", "medium-high", "yes", "G-020"],
    ["F-194", "Escuelita participant and seed-pedagogics follow-up", "CIIS delegations and pro-Zapatista interlocutors", "T-13", "autonomy, legal pluralism, and translocal federation", "S-16;S-18", "qualitative practice-transfer evidence with bundled exposure", "medium", "yes", "G-020"],
    ["F-195", "Escuelita-linked organization trace", "Espacio de Coordinacion Grietas en el Muro", "T-11", "succession, fission, and movement continuity", "S-13;S-18", "durable named candidate with mixed lineage", "medium-high", "yes", "G-020"],
    ["F-196", "named Escuelita participant trace", "Levi Gahman and later organizing and knowledge work", "T-13", "autonomy, legal pluralism, and translocal federation", "S-16;S-18", "individual pathway example with causal limits", "medium", "yes", "G-020"],
    ["F-197", "pre-Escuelita causal-attribution controls", "transnational Zapatismo; Casa del Pueblo; Universidad de la Tierra Califas", "T-10", "success, outcomes, source quality, and measurement", "S-09;S-11;S-18", "counterevidence and lineage control", "high", "no", "G-020"],
    ["F-198", "Escuelita descendant bounded search", "Escuelita alumni and candidate descendants", "T-10", "success, outcomes, source quality, and measurement", "S-11;S-18", "bounded null and evidence-ceiling finding", "medium-high", "yes", "G-020"],
]


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames is not None
        loaded = list(reader)
    assert all(None not in row for row in loaded), f"extra fields in {path.name}"
    assert all(None not in row.values() for row in loaded), f"missing fields in {path.name}"
    return list(reader.fieldnames), loaded


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def as_rows(fields: list[str], values: list[list[str]]) -> list[dict[str, str]]:
    assert all(len(row) == len(fields) for row in values)
    return [dict(zip(fields, row, strict=True)) for row in values]


def replace_once_or_confirm(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old in text:
        assert text.count(old) == 1, f"ambiguous replacement for {label}"
        return text.replace(old, new, 1)
    raise AssertionError(f"missing predecessor and successor for {label}")


def insert_before_once(text: str, marker: str, block: str, sentinel: str) -> str:
    if sentinel in text:
        return text
    assert text.count(marker) == 1, f"missing or ambiguous marker: {marker}"
    return text.replace(marker, block.rstrip() + "\n\n" + marker, 1)


def update_csvs() -> None:
    source_rows = as_rows(SOURCE_FIELDS, SOURCE_VALUES)
    finding_rows = as_rows(LEDGER_FIELDS, FINDING_VALUES)
    crosswalk_rows = as_rows(CROSSWALK_FIELDS, CROSSWALK_VALUES)
    write_rows(UNIT_SOURCES, SOURCE_FIELDS, source_rows)
    write_rows(UNIT_LEDGER, LEDGER_FIELDS, finding_rows)

    ledger_fields, ledger = read_rows(LEDGER)
    assert ledger_fields == LEDGER_FIELDS
    ledger = [row for row in ledger if row["finding_id"] not in {item["finding_id"] for item in finding_rows}]
    assert [row["finding_id"] for row in ledger] == [f"F-{number:03d}" for number in range(1, 193)]
    write_rows(LEDGER, ledger_fields, ledger + finding_rows)

    source_fields, sources = read_rows(SOURCES)
    assert source_fields == SOURCE_FIELDS
    sources = [row for row in sources if not row["record_id"].startswith("ES-")]
    assert sources[-1]["record_id"] == "LP-009"
    write_rows(SOURCES, source_fields, sources + source_rows)

    crosswalk_fields, crosswalk = read_rows(CROSSWALK)
    assert crosswalk_fields == CROSSWALK_FIELDS
    crosswalk = [row for row in crosswalk if row["finding_id"] not in {item["finding_id"] for item in crosswalk_rows}]
    assert [row["finding_id"] for row in crosswalk] == [f"F-{number:03d}" for number in range(1, 193)]
    write_rows(CROSSWALK, crosswalk_fields, crosswalk + crosswalk_rows)


def update_gap_bank() -> None:
    text = GAP_BANK.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response, assessment/review, durable treatment/transition, official-correction, fair-separation/pooled-risk/planned-fission, and autonomy/legal-pluralism units",
        "Checkpoint: *Communal Societies* volumes 1-45 plus eight standalone sources and adjacent child-response, assessment/review, durable treatment/transition, official-correction, fair-separation/pooled-risk/planned-fission, autonomy/legal-pluralism, and Escuelita seed-outcomes units",
        "gap checkpoint",
    )
    text = replace_once_or_confirm(
        text,
        "this corrected checkpoint retains 19 material items: **8 B, 7 C, and 4 D**.",
        "this updated checkpoint retains 20 material items: **9 B, 7 C, and 4 D**.",
        "gap item and class counts",
    )
    row = (
        "| G-020 | B | The article and prior synthesis recognize Zapatismo as unusually capable of teaching communal innovation outward, but they do not distinguish inspiration from a durable descendant institution. | Add an Escuelita lineage ladder: encounter; continued alumni relation; practice transfer; new organization; durable shared-life or governance institution; and later human outcomes. Alumni statements and actions establish continuing networks across several geographies (F-193). CIIS follow-up and seed-pedagogics interviews support practice transfer but bundle the Escuelita with longer Zapatista engagement (F-194). Espacio de Coordinacion Grietas en el Muro is the strongest organization-level candidate: a 2016 project organized with Escuelita alumni remained publicly visible through at least October 2024, but its origin was mixed and its internal governance and human outcomes are unmeasured (F-195). One former student supplies a named participant-to-organizing and knowledge-work trace without proving causation (F-196). Pre-2013 research on activists taking Zapatismo home, Casa del Pueblo, and Universidad de la Tierra Califas proves that broad transnational diffusion predates the Escuelita and must be treated as prior soil or grafting rather than a 2013 seedling (F-197). The bounded search found no alumni registry, longitudinal cohort, directly descended residential commune or autonomous federation, or later safety, child-wellbeing, autonomy, retention, and viability panel (F-198). | Some seeds clearly germinated as networks, political education, solidarity practice, and a durable coordination space. The evidence does not yet show that the Escuelita generated a population of durable new communities with verified human outcomes. | Worldwide communal innovation / movement school / outcome dashboard | F-193, F-194, F-195, F-196, F-197, F-198 |"
    )
    text = insert_before_once(text, "\n## Verification queue", row, "| G-020 |")
    GAP_BANK.write_text(text, encoding="utf-8")


def update_final_report() -> None:
    text = REPORT.read_text(encoding="utf-8")
    replacements = [
        ("Evidence base: 192 findings, F-001 through F-192", "Evidence base: 198 findings, F-001 through F-198", "report count header"),
        ("The corrected gap bank reaches 189 of 192 findings.", "The updated gap bank reaches 195 of 198 findings.", "gap coverage count"),
        ("accounts for all 192 findings", "accounts for all 198 findings", "crosswalk coverage"),
        ("29 bounded adjacent records", "47 bounded adjacent records", "adjacent source count"),
        ("192 promoted findings", "198 promoted findings", "finding count"),
        ("91 findings high confidence, 25 medium-high, 67 medium", "92 findings high confidence, 28 medium-high, 69 medium", "confidence counts"),
        ("128 for external verification and 64 as not needing it", "133 for external verification and 65 as not needing it", "verification counts"),
        ("all 192 are accounted for", "all 198 are accounted for", "theme-map count"),
        ("| T-10 success, outcomes, source quality, and measurement | 9 |", "| T-10 success, outcomes, source quality, and measurement | 11 |", "T10 count"),
        ("| T-11 succession, fission, and movement continuity | 11 |", "| T-11 succession, fission, and movement continuity | 13 |", "T11 count"),
        ("| T-13 autonomy, legal pluralism, and translocal federation | 6 |", "| T-13 autonomy, legal pluralism, and translocal federation | 8 |", "T13 count"),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)

    text = insert_before_once(
        text,
        "## 10. Success is a vector, not a score",
        """## 10. Outward diffusion needs a lineage ladder — T-10, T-11, T-13, S-18

The Escuelita seed-outcomes unit separates six endpoints that the language of inspiration can collapse: encounter, continued alumni relation, practice transfer, creation of a new organization, durable communal institution, and later human outcomes.

The evidence is strongest at the first three levels. Official records document a large, deliberately immersive school with an outward teaching intention. Alumni then appeared as collective actors in several regions through statements, fundraisers, marches, and cultural-political events from 2014 through 2016 (F-193). CIIS follow-up and qualitative seed-pedagogics research report participants carrying principles into care, organizing, political, and NGO work and describe collective political learning beyond Chiapas (F-194). These are real movement outcomes, but the exposure includes other Zapatista encounters and prior activism.

Espacio de Coordinacion Grietas en el Muro is the strongest organization-level candidate (F-195). A 2016 notice says collectives and individuals including Escuelita students created a local CompArte site and names the coordination space; it remains visible in 2019 and 2022 organizing records and a 2024 CNI signatory list. Its origin was explicitly mixed, and the record does not show continuous membership, internal governance, residential life, or human outcomes. A named former student, Levi Gahman, supplies a smaller trace from attendance to later solidarity organizing and knowledge work without proving that the Escuelita created the organization or caused the later activity (F-196).

Pre-2013 controls prevent false credit. Transnational activist reflexivity, Casa del Pueblo, and Universidad de la Tierra Califas were already documented as Zapatista-inspired practices or institutions before the Escuelita (F-197). Later similarity may reflect older roots, reinforcement, or grafting. It is not enough to establish descent.

The bounded search located no alumni registry, longitudinal cohort, counted adoption or failure rate, directly descended residential commune or autonomous federation, or later safety, child-wellbeing, autonomy, voluntary-retention, material-viability, and relational-outcome panel (F-198). This is not proof that no such project exists. It fixes the current evidence ceiling.

S-18 is therefore the diffusion rule: credit the highest demonstrated lineage level and do not promote a network, practice adaptation, or named organization into a successful communal replication without evidence of durability, shared-life or governance function, and later human outcomes. The detailed audit is in [the Escuelita seed-outcomes report](COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md).
""",
        "S-18 is therefore the diffusion rule",
    )
    # Repair the heading pair produced by the first development run, then
    # perform the same renumbering on an untouched predecessor.
    text = text.replace(
        "## 11. Success is a vector, not a score\n\n## 10. Success is a vector, not a score — T-10, S-11",
        "## 11. Success is a vector, not a score — T-10, S-11",
        1,
    )
    text = replace_once_or_confirm(
        text,
        "## 10. Success is a vector, not a score — T-10, S-11",
        "## 11. Success is a vector, not a score — T-10, S-11",
        "report S-11 heading",
    )
    text = text.replace("## 11. Continuity can outlive the institution", "## 12. Continuity can outlive the institution", 1)
    text = text.replace("## 12. The persistent-dangerous-child question remains unanswered", "## 13. The persistent-dangerous-child question remains unanswered", 1)
    text = replace_once_or_confirm(
        text,
        "- **Legal and medical systems are selected couplings.** The need for competence, rights, and non-self-review is not optional, but the institutional location is contingent. Zapatista and other Indigenous cases show autonomous justice, health, education, and regional correction; Cheran shows selective state recognition and referral; CRAC-PC shows protective translocal federation. The article should map which layer can legitimately perform each function under actual territorial and legal conditions (G-013 and G-019; S-10, S-16, and S-17).",
        "- **Legal and medical systems are selected couplings.** The need for competence, rights, and non-self-review is not optional, but the institutional location is contingent. Zapatista and other Indigenous cases show autonomous justice, health, education, and regional correction; Cheran shows selective state recognition and referral; CRAC-PC shows protective translocal federation. The article should map which layer can legitimately perform each function under actual territorial and legal conditions (G-013 and G-019; S-10, S-16, and S-17).\n- **Zapatismo produces worldwide communal innovation.** The Escuelita clearly produced continued alumni relations, reported practice transfer, and at least one durable mixed-lineage coordination candidate. The evidence does not yet establish a population of new residential or governing communities or later human outcomes. State the demonstrated lineage level and require a descendant and outcome audit before upgrading diffusion into successful communal replication (G-020; S-18).",
        "article implication S18",
    )
    text = replace_once_or_confirm(
        text,
        "11. The 2023 Zapatista reorganization has no independent later-outcome evaluation in this unit, and no common outcome panel compares autonomous, hybrid, and state-centered jurisdictional arrangements.",
        "11. The 2023 Zapatista reorganization has no independent later-outcome evaluation in this unit, and no common outcome panel compares autonomous, hybrid, and state-centered jurisdictional arrangements.\n12. No public Escuelita alumni registry or longitudinal cohort shows how many participants adopted practices, formed projects, abandoned attempts, or changed existing organizations.\n13. No located directly descended residential commune or autonomous federation has a complete durability and human-outcome panel.",
        "unknowns S18",
    )
    text = replace_once_or_confirm(
        text,
        "12. A community can preserve purpose through transformation, migration, teaching, alumni networks, parallel institutions, succession, or voluntary fission; preserving the original entity is not always the goal.",
        "12. A community can preserve purpose through transformation, migration, teaching, alumni networks, parallel institutions, succession, or voluntary fission; preserving the original entity is not always the goal. Outward diffusion must still be reported by lineage level so inspiration, network continuity, organization creation, durable communal replication, and human outcomes remain distinct.",
        "final conclusion S18",
    )
    text = replace_once_or_confirm(
        text,
        "- Read [COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md](COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md) for the state-monopoly correction, Zapatista synthesis, Indigenous comparators, and transfer boundaries.",
        "- Read [COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md](COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md) for the state-monopoly correction, Zapatista synthesis, Indigenous comparators, and transfer boundaries.\n- Read [COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md](COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md) for the alumni, practice-transfer, candidate-descendant, causal-attribution, and outcome audit.",
        "artifact guide S18",
    )
    REPORT.write_text(text, encoding="utf-8")


def update_state() -> None:
    text = STATE.read_text(encoding="utf-8")
    text = text.replace(
        "**198 findings** (`F-001` through `F-198`). The autonomy/legal-pluralism correction added six findings and the Escuelita seed-outcomes unit added six findings in an explicitly separate autonomous Indigenous governance lane; it does not alter the 984-journal-PDF or eight-standalone counts.",
        "**198 findings** (`F-001` through `F-198`). The autonomy/legal-pluralism correction added six findings in a separate autonomous Indigenous governance lane, and the Escuelita seed-outcomes unit added six findings in a separate diffusion lane; neither changes the 984-journal-PDF or eight-standalone counts.",
        1,
    )
    replacements = [
        ("**192 findings** (`F-001` through `F-192`). The autonomy/legal-pluralism correction added six findings in an explicitly separate autonomous Indigenous governance lane; it does not alter the 984-journal-PDF or eight-standalone counts.", "**198 findings** (`F-001` through `F-198`). The autonomy/legal-pluralism correction added six findings in a separate autonomous Indigenous governance lane, and the Escuelita seed-outcomes unit added six findings in a separate diffusion lane; neither changes the 984-journal-PDF or eight-standalone counts.", "state count"),
        ("horizontally synthesizes all 192 findings across thirteen themes", "horizontally synthesizes all 198 findings across thirteen themes", "state report count"),
        ("`COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md` records the state-monopoly correction and Indigenous comparators.", "`COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md` records the state-monopoly correction and Indigenous comparators. The synthesis now incorporates 47 bounded adjacent records, including the eighteen-record Escuelita descendant audit.", "state adjacent records"),
        ("Every finding through F-192 is mapped", "Every finding through F-198 is mapped", "state boundary mapping"),
        ("the new bounded lane adds six evidence rows and one article-gap challenge", "the latest bounded lane adds six evidence rows and one article-gap item", "state boundary lane"),
    ]
    for old, new, label in replacements:
        text = replace_once_or_confirm(text, old, new, label)
    text = replace_once_or_confirm(
        text,
        "retains 19 reconciled article-gap items: 8 partially present, 7 apparently missing, and 4 challenges",
        "retains 20 reconciled article-gap items: 9 partially present, 7 apparently missing, and 4 challenges",
        "state gap counts",
    )
    text = replace_once_or_confirm(
        text,
        "- The original five-unit adjacent-source roadmap remains complete. The owner-authorized autonomy/legal-pluralism correction is also complete; it was a bounded correction to a sampling-frame error, not an unbounded reopening of the corpus.",
        "- The original five-unit adjacent-source roadmap remains complete. The owner-authorized autonomy/legal-pluralism correction is also complete; it was a bounded correction to a sampling-frame error, not an unbounded reopening of the corpus.\n- The owner-authorized Escuelita seed-outcomes question is complete. It found alumni and practice-transfer sprouts, one durable mixed-lineage coordination candidate, strong pre-2013 attribution controls, and no located directly descended communal institution with a human-outcome panel.",
        "state completed unit",
    )
    text = replace_once_or_confirm(
        text,
        "- The autonomy/legal-pluralism correction rejects the equation independent correction equals state intervention.",
        "- The Escuelita seed-outcomes unit separates encounter, alumni continuity, practice transfer, new organization, durable communal institution, and human outcomes. Evidence reaches a durable mixed-lineage coordination space but not a directly descended commune or outcome panel.\n- The autonomy/legal-pluralism correction rejects the equation independent correction equals state intervention.",
        "state evidence picture",
    )
    text = replace_once_or_confirm(
        text,
        "2. The original adjacent-source roadmap and the owner-authorized legal-pluralism correction are complete. Do not invent another research unit; await explicit authority for article editing or a new bounded question.",
        "2. The original adjacent-source roadmap and the owner-authorized legal-pluralism and Escuelita seed-outcomes units are complete. Do not invent another research unit; await explicit authority for article editing or a new bounded question.",
        "state resume",
    )
    STATE.write_text(text, encoding="utf-8")


def update_navigation() -> None:
    readme = README.read_text(encoding="utf-8")
    replacements = [
        ("- **192** evidence findings (`F-001` through `F-192`)", "- **198** evidence findings (`F-001` through `F-198`)", "README finding count"),
        ("- **19** reconciled article gaps: 8 partially present, 7 apparently missing, and 4 challenges", "- **20** reconciled article gaps: 9 partially present, 7 apparently missing, and 4 challenges", "README gap count"),
        ("all 192 findings mapped across 13 themes", "all 198 findings mapped across 13 themes", "README synthesis count"),
        ("one-row-per-finding map from all 192 findings", "one-row-per-finding map from all 198 findings", "README crosswalk count"),
        ("python recovered/test_autonomy_legal_pluralism_workflow.py\npython recovered/verify_autonomy_legal_pluralism.py", "python recovered/test_escuelita_seed_outcomes_workflow.py\npython recovered/verify_escuelita_seed_outcomes.py", "README commands"),
        ("requires 192 sequential ledger and crosswalk rows, validates the nine-source and six-finding legal-pluralism unit, verifies the thirteen-theme and seventeen-claim report architecture", "requires 198 sequential ledger and crosswalk rows, validates the eighteen-source and six-finding Escuelita unit, preserves the legal-pluralism unit, and verifies the thirteen-theme and eighteen-claim report architecture", "README verifier description"),
    ]
    for old, new, label in replacements:
        readme = replace_once_or_confirm(readme, old, new, label)
    readme = replace_once_or_confirm(
        readme,
        "The load-bearing state-monopoly correction is [`recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`](recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md).",
        "The load-bearing state-monopoly correction is [`recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`](recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md). The Escuelita descendant audit is [`recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md`](recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md).",
        "README authority reports",
    )
    readme = replace_once_or_confirm(
        readme,
        "- `recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-EVIDENCE-LEDGER.csv` — six bounded correction findings, F-187 through F-192",
        "- `recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-EVIDENCE-LEDGER.csv` — six bounded correction findings, F-187 through F-192\n- `recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md` — lineage-ladder audit of alumni, practice transfer, candidate descendants, and outcomes\n- `recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-EVIDENCE-LEDGER.csv` — six bounded diffusion findings, F-193 through F-198\n- `recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-SOURCE-INVENTORY.csv` — eighteen public source and attribution-control records",
        "README unit files",
    )
    README.write_text(readme, encoding="utf-8")

    index = INDEX.read_text(encoding="utf-8")
    old_without_lessons = "4. `../recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`\n5. `../recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`\n6. the prior finite-roadmap endpoint, `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`\n7. `../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`\n8. `../recovered/COMMUNITIES-SOURCE-INVENTORY.csv`\n9. `../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`\n10. current discovery, update, test, and verification scripts"
    new_without_lessons = "4. `../recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`\n5. `../recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md`\n6. `../recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`\n7. the prior finite-roadmap endpoint, `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`\n8. `../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`\n9. `../recovered/COMMUNITIES-SOURCE-INVENTORY.csv`\n10. `../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`\n11. current discovery, update, test, and verification scripts"
    old_with_lessons = "4. `../COMMUNITY-DEVELOPMENT-LESSONS.md`\n5. `../recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`\n6. `../recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`\n7. the prior finite-roadmap endpoint, `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`\n8. `../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`\n9. `../recovered/COMMUNITIES-SOURCE-INVENTORY.csv`\n10. `../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`\n11. current discovery, update, test, and verification scripts"
    new_with_lessons = "4. `../COMMUNITY-DEVELOPMENT-LESSONS.md`\n5. `../recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md`\n6. `../recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md`\n7. `../recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv`\n8. the prior finite-roadmap endpoint, `../recovered/COMMUNITIES-ADJACENT-FAIR-SEPARATION-REPORT.md`\n9. `../recovered/COMMUNITIES-EVIDENCE-LEDGER.csv`\n10. `../recovered/COMMUNITIES-SOURCE-INVENTORY.csv`\n11. `../recovered/COMMUNITIES-ARTICLE-GAP-BANK.md`\n12. current discovery, update, test, and verification scripts"
    if new_with_lessons in index or new_without_lessons in index:
        pass
    elif old_with_lessons in index:
        index = index.replace(old_with_lessons, new_with_lessons, 1)
    elif old_without_lessons in index:
        index = index.replace(old_without_lessons, new_without_lessons, 1)
    else:
        raise AssertionError("missing predecessor and successor for index read order")
    index = replace_once_or_confirm(
        index,
        "The autonomy and legal-pluralism correction is recorded in `superpowers/plans/2026-08-15-autonomy-legal-pluralism-correction.md`; it was a bounded response to an owner-identified sampling-frame error and does not reopen the completed primary corpus.",
        "The autonomy and legal-pluralism correction is recorded in `superpowers/plans/2026-08-15-autonomy-legal-pluralism-correction.md`; it was a bounded response to an owner-identified sampling-frame error and does not reopen the completed primary corpus.\n\nThe Escuelita descendant audit is recorded in `superpowers/plans/2026-08-15-escuelita-seed-outcomes.md`; it is a bounded response to an owner-identified diffusion question and does not reopen the completed primary corpus.",
        "index unit note",
    )
    INDEX.write_text(index, encoding="utf-8")

    agents = AGENTS.read_text(encoding="utf-8")
    agents = replace_once_or_confirm(
        agents,
        "- Regression suite: `python recovered/test_autonomy_legal_pluralism_workflow.py` (current bounded-unit successor)\n- Current repository-contained verification: `python recovered/verify_autonomy_legal_pluralism.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "- Regression suite: `python recovered/test_escuelita_seed_outcomes_workflow.py` (current bounded-unit successor)\n- Current repository-contained verification: `python recovered/verify_escuelita_seed_outcomes.py`; run source-dependent predecessor checks only when their exact local corpora are restored",
        "AGENTS validation",
    )
    AGENTS.write_text(agents, encoding="utf-8")


def update_operational_lessons() -> None:
    """Integrate the lineage rule when the optional lessons layer is present."""
    if not LESSONS.exists():
        return
    text = LESSONS.read_text(encoding="utf-8")
    text = replace_once_or_confirm(
        text,
        "**Related:** F-189",
        "**Related:** F-189; F-193–F-198",
        "lessons Escuelita findings",
    )
    text = replace_once_or_confirm(
        text,
        "Separately measure spread of ideas, formation of new collectivities, durable adoption/adaptation, and verified human outcomes. A durable flagship is not automatically a reproducing/teaching movement.",
        "Separately measure encounter, continued alumni relation, practice transfer, formation of new collectivities, durable shared-life or governance adoption, and verified human outcomes. The Escuelita audit reaches practice transfer and one durable mixed-lineage coordination candidate, but not a directly descended commune or outcome panel. A durable flagship, alumni network, or visible coordination space is not automatically a successful communal-replication engine.",
        "lessons lineage ladder",
    )
    LESSONS.write_text(text, encoding="utf-8")


def main() -> None:
    update_csvs()
    update_gap_bank()
    update_final_report()
    update_state()
    update_navigation()
    update_operational_lessons()
    print("Escuelita seed-outcomes update: PASS")


if __name__ == "__main__":
    main()
