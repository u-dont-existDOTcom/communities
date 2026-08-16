# Communities research → Creative Tail → article workflow architecture

Updated: 2026-08-16

Purpose: keep the end-to-end control flow visible in one source-controlled place. This map complements the prose state; it does not replace the evidence ledger, synthesis, gap bank, or branch-specific handoffs.

## 1. End-to-end overview

```mermaid
flowchart TD
    OWNER["Owner thesis, objections, and article"]
    EMP["New empirical research"]
    CORPUS["Communities authoritative corpus\nSynthesis + crosswalk + evidence ledger + lessons"]

    GEN["Retrieval-free Creative Tail generation"]
    CS{"Common-sense / user-familiarity veto"}
    COLL{"Active-project corpus collision"}
    NARROW["Narrow to additive residual"]
    PRACT["Practical lesson or discard"]

    EXA["Exa semantic collision attack\nMANDATORY"]
    PSEARCH["Parallel Search\noptional corroboration / disagreement"]
    PTASK["Parallel Task deep attack\nMANDATORY before strict promotion / 'real gap'"]
    DISP{"Final novelty disposition"}
    STRICT["Strict CTS finding / cross-domain connection"]

    SYNTH["Communities synthesis layer"]
    GAP["Article-gap bank"]
    EDIT{"Editorial phase authorized?"}
    HARM["Article harmonization"]
    HUMAN["Humanization / detector workflow"]
    PUB["Publication / public research link"]
    STATE["Research state + next gap"]

    OWNER --> GEN
    OWNER --> CS
    OWNER --> COLL
    EMP --> CORPUS
    CORPUS --> COLL

    GEN --> CS
    CS -- "obvious / familiar" --> PRACT
    CS -- "survives" --> COLL
    COLL -- "direct collision" --> PRACT
    COLL -- "root collision + residual" --> NARROW
    NARROW --> CS
    COLL -- "materially additive" --> EXA

    EXA -- "direct collision" --> PRACT
    EXA -- "root + residual" --> NARROW
    EXA -- "no convincing collision" --> PTASK
    PSEARCH -. "optional signal" .-> PTASK
    PTASK --> DISP
    DISP -- "reject" --> PRACT
    DISP -- "narrow" --> NARROW
    DISP -- "survive" --> STRICT

    CORPUS --> SYNTH
    STRICT --> SYNTH
    PRACT --> SYNTH
    SYNTH --> GAP
    OWNER --> GAP

    GAP --> EDIT
    EDIT -- "no" --> STATE
    EDIT -- "yes" --> HARM
    HARM --> HUMAN
    HUMAN --> PUB
    PUB --> STATE

    STATE --> GEN
```

### Reading rule

- Generation remains retrieval-free.
- A candidate may be discussed provisionally before external retrieval, but it must not be presented as a **real article gap**, **strict novelty survivor**, or **new finding** until it survives the internal corpus gate, mandatory Exa attack, and mandatory Parallel Task deep attack.
- Parallel Search is optional after Round 001 showed no incremental recall over Exa; use it for corroboration or provider disagreement, not as a required routine lane.
- Owner objections are first-class search evidence and update the rejection frontier immediately.

## 2. Novelty / promotion drill-down

```mermaid
flowchart TD
    C0["Plain candidate proposition"]
    C1{"Would the owner likely say 'obvious'?"}
    C2{"Already in the communities corpus / lessons?"}
    C3["Exa routine semantic attack"]
    C4{"Exa result"}
    C5["Parallel Task deep research"]
    C6{"Deep result"}
    USE["Useful but known\n→ community-development lessons"]
    RES["Narrow residual\n→ regenerate / retest"]
    PROM["Strict promotion candidate"]
    GAPQ{"Actually missing from the article?"}
    GAPYES["Verified article gap"]
    NOGAP["Research finding, but not an article gap"]

    C0 --> C1
    C1 -- "yes" --> USE
    C1 -- "no" --> C2
    C2 -- "direct collision" --> USE
    C2 -- "partial collision" --> RES
    RES --> C0
    C2 -- "additive" --> C3
    C3 --> C4
    C4 -- "direct collision" --> USE
    C4 -- "root + residual" --> RES
    C4 -- "no convincing collision" --> C5
    C5 --> C6
    C6 -- "reject" --> USE
    C6 -- "narrow" --> RES
    C6 -- "survive" --> PROM
    PROM --> GAPQ
    GAPQ -- "yes" --> GAPYES
    GAPQ -- "no" --> NOGAP
```

### Round 001 retrieval verdict encoded here

The production architecture follows the completed benchmark:

- Exa Search: 8/8 historical false-novelty catches.
- Parallel Search: materially weaker routine recall and no incremental catch over Exa in that round.
- Parallel Task `pro`: materially useful on all five escalated survivor/boundary cases and sharply narrowed several survivors.

Therefore:

1. Exa routine attack is mandatory.
2. Parallel Search is optional.
3. Parallel Task deep attack is mandatory before strict originality promotion or before telling the owner that a candidate is a verified real gap.

## 3. Evidence, article, and persistence dataflow

```mermaid
flowchart LR
    SRC["Primary / secondary / adjacent sources"]
    EMP["Empirical research units"]
    LEDGER["COMMUNITIES-EVIDENCE-LEDGER.csv"]
    CROSS["COMMUNITIES-SYNTHESIS-CROSSWALK.csv"]
    FINAL["COMMUNITIES-FINAL-SYNTHESIS-REPORT.md"]
    LESSONS["COMMUNITY-DEVELOPMENT-LESSONS*.md"]
    GAP["COMMUNITIES-ARTICLE-GAP-BANK.md"]
    ARTICLE["Owner article"]

    CTSRUN["creativeTailSampling/runs/"]
    CTSF["creativeTailSampling/FINDINGS.md"]
    CTSS["creativeTailSampling/STATE.md"]
    RET["Exa + Parallel retrieval artifacts"]

    MAP["This Mermaid architecture map"]
    UNIV["universal-dev-architecture\nliving Mermaid workflow pattern"]
    GIT["GitHub durable source of truth"]

    SRC --> EMP
    EMP --> LEDGER
    LEDGER --> CROSS
    CROSS --> FINAL
    FINAL --> GAP
    LESSONS --> GAP
    ARTICLE --> GAP

    CTSRUN --> CTSF
    RET --> CTSRUN
    CTSF --> FINAL
    CTSS --> CTSRUN

    MAP --> GIT
    LEDGER --> GIT
    FINAL --> GIT
    GAP --> GIT
    LESSONS --> GIT
    CTSRUN --> GIT
    CTSF --> GIT
    CTSS --> GIT
    RET --> GIT
    UNIV --> GIT
```

## 4. Canonical file roles

| Layer | Canonical artifact | Role |
|---|---|---|
| Recovery / authority | `docs/FRESH-CONVERSATION-HANDOFF.md`, `recovered/COMMUNITIES-RESEARCH-STATE.md` | Restore exact checkpoint and boundaries |
| Evidence | `recovered/COMMUNITIES-EVIDENCE-LEDGER.csv` | Source-level factual authority and limits |
| Synthesis | `recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md`, crosswalk | Horizontal interpretation of the evidence base |
| Practical design | `COMMUNITY-DEVELOPMENT-LESSONS.md` + tail batches | Useful lessons even when novelty fails |
| Creative Tail | `u-dont-existDOTcom/creativeTailSampling` | Novelty search, rejection frontier, retrieval attacks |
| Article changes | `recovered/COMMUNITIES-ARTICLE-GAP-BANK.md` | What the article is missing, partially contains, or gets wrong |
| Workflow visualization | `docs/COMMUNITIES-WORKFLOW-ARCHITECTURE.md` | Living visual control map |
| Universal pattern | `u-dont-existDOTcom/universal-dev-architecture/patterns/living-mermaid-workflow-maps.md` | Cross-project rule for maintaining visual architecture |

## 5. Update triggers

Update this map whenever any of these change materially:

- promotion/rejection gates;
- provider roles or retrieval architecture;
- authoritative repositories or files;
- research-to-article handoff;
- editorial authorization state;
- persistence/checkpoint topology;
- a new feedback loop becomes operationally important.

Do not add every small script or artifact to the overview. Put detail in a drill-down diagram and keep the top-level map readable.
