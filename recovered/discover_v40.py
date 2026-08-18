from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
CORPUS = ROOT / "corpus-v40"
RANKING = ROOT / "V40-DISCOVERY-RANKING.csv"
CONTEXTS = ROOT / "v40-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "v40-child-danger-contexts.txt"


FAMILIES = {
    "danger": [
        r"\bviol(?:ence|ent|ently)\b", r"\bassault\w*\b", r"\battack\w*\b",
        r"\bkill(?:ed|ing|s)?\b", r"\bmurder\w*\b", r"\bhomicid\w*\b",
        r"\bthreat\w*\b", r"\bdanger\w*\b", r"\bharm\w*\b", r"\binjur\w*\b",
        r"\babuse\w*\b", r"\bmolest\w*\b", r"\brap(?:e|ed|es|ing|ist)\b",
        r"\bsexual(?:ly)?\s+(?:abuse|assault|exploit)\w*\b", r"\bpredat\w*\b",
        r"\bcoerc\w*\b", r"\bintimidat\w*\b", r"\bterror\w*\b",
        r"\bbeat(?:en|ing|s)?\b", r"\bwhipp\w*\b", r"\bweapon\w*\b",
        r"\bgun\w*\b", r"\bknife\b", r"\barson\w*\b", r"\bfirebomb\w*\b",
        r"\btheft\b", r"\bsteal(?:ing|s)?\b", r"\bstole\w*\b", r"\bfraud\w*\b",
        r"\bcrime\w*\b", r"\bcriminal\w*\b", r"\boutlaw\w*\b",
        r"\bsuicid\w*\b", r"\bmassacre\w*\b", r"\bdelinquen\w*\b",
        r"\baggress\w*\b", r"\bpsychopath\w*\b", r"\bsociopath\w*\b",
        r"\bantisocial\b",
    ],
    "sanction": [
        r"\bexpel\w*\b", r"\bexcommunicat\w*\b", r"\bostraci[sz]\w*\b",
        r"\bbanish\w*\b", r"\bshun\w*\b", r"\bexclude\w*\b", r"\bremov\w*\b",
        r"\bdismiss\w*\b", r"\bdisciplin\w*\b", r"\bpunish\w*\b",
        r"\bsanction\w*\b", r"\bwarn(?:ed|ing|s)?\b", r"\bprobation\w*\b",
        r"\baccus\w*\b", r"\balleg\w*\b", r"\bcomplain\w*\b", r"\bgrievance\w*\b",
        r"\bhearing\w*\b", r"\btrial\w*\b", r"\bappeal\w*\b", r"\binvestigat\w*\b",
        r"\bconfine\w*\b", r"\barrest\w*\b", r"\bpolice\b", r"\bsheriff\w*\b",
        r"\bcourt\w*\b", r"\blawsuit\w*\b", r"\blitigat\w*\b", r"\bjail\w*\b",
        r"\bprison\w*\b", r"\breintegrat\w*\b", r"\breconcil\w*\b",
        r"\bforgiv\w*\b", r"\bdisfellow\w*\b",
    ],
    "governance": [
        r"\bfounder\w*\b", r"\bleader\w*\b", r"\bauthorit\w*\b", r"\bpower\w*\b",
        r"\bgovern\w*\b", r"\bdecision\w*\b", r"\bconsensus\b", r"\bvote\w*\b",
        r"\bcouncil\w*\b", r"\bcommittee\w*\b", r"\bboard\w*\b", r"\brule\w*\b",
        r"\bconstitution\w*\b", r"\bbylaws?\b", r"\bcontrol\w*\b", r"\bdissent\w*\b",
        r"\bcritic\w*\b", r"\baccountab\w*\b", r"\btransparent\w*\b",
        r"\bsecret\w*\b", r"\bsuccession\w*\b", r"\bproperty\b", r"\bassets?\b",
        r"\btrust\w*\b", r"\bfinanc\w*\b", r"\bmoney\b", r"\bmembership\b",
        r"\badmission\w*\b", r"\brecruit\w*\b", r"\bmonitor\w*\b",
        r"\bevidence\b", r"\breport\w*\b", r"\bassembly\b", r"\bpolicy\b",
    ],
    "child": [
        r"\bchild(?:ren|hood)?\b", r"\bboys?\b", r"\bgirls?\b", r"\byouth\b",
        r"\bjuvenile\w*\b", r"\bminors?\b", r"\badolescen\w*\b", r"\bteen\w*\b",
        r"\bschool\w*\b", r"\bparents?\b", r"\bfamil(?:y|ies)\b", r"\bsons?\b",
        r"\bdaughters?\b",
    ],
    "exit": [
        r"\bexit\w*\b", r"\bleav(?:e|es|ing)\b", r"\bleft\b", r"\bdepart\w*\b",
        r"\bexpel\w*\b", r"\bexclude\w*\b", r"\bostraci[sz]\w*\b", r"\bbanish\w*\b",
        r"\bshun\w*\b", r"\bdefect\w*\b", r"\bapostat\w*\b", r"\bdissent\w*\b",
        r"\bschism\w*\b", r"\bsplit\w*\b", r"\bseparat\w*\b", r"\bwithdraw\w*\b",
        r"\bresign\w*\b", r"\brefuge\w*\b", r"\boutside\b", r"\bcourt\w*\b",
        r"\bpolice\b",
    ],
    "clinical": [
        r"\bpsych\w*\b", r"\bmental\w*\b", r"\bdisorder\w*\b", r"\btherap\w*\b",
        r"\btreat\w*\b", r"\bdiagnos\w*\b", r"\btrauma\w*\b", r"\baddict\w*\b",
        r"\balcohol\w*\b", r"\bdrug\w*\b", r"\brehab\w*\b", r"\bhospital\w*\b",
        r"\binstitutionali[sz]\w*\b", r"\bmedic\w*\b", r"\bcounsel\w*\b",
        r"\bbehavio[u]?r\w*\b", r"\baggress\w*\b", r"\bdelinquen\w*\b",
        r"\bpsychopath\w*\b", r"\bsociopath\w*\b", r"\bantisocial\b",
    ],
}

PROCESS_FAMILIES = {
    "allegation": [r"\baccus\w*\b", r"\balleg\w*\b", r"\breport\w*\b", r"\bcomplain\w*\b"],
    "assessment": [r"\bassess\w*\b", r"\bdiagnos\w*\b", r"\bevaluat\w*\b", r"\binvestigat\w*\b", r"\bexamin\w*\b"],
    "intervention": [r"\binterven\w*\b", r"\btreat\w*\b", r"\bdisciplin\w*\b", r"\bpunish\w*\b", r"\bconfine\w*\b", r"\bremove\w*\b", r"\bexpel\w*\b"],
    "review": [r"\breview\w*\b", r"\bappeal\w*\b", r"\bhearing\w*\b", r"\breconsider\w*\b", r"\bfollow[- ]?up\b"],
    "outcome": [r"\boutcome\w*\b", r"\bresult\w*\b", r"\blater\b", r"\bsubsequen\w*\b", r"\byears? later\b"],
}


def compiled(parts: list[str]) -> re.Pattern[str]:
    return re.compile("(?:" + "|".join(parts) + ")", re.IGNORECASE)


REGEX = {name: compiled(parts) for name, parts in FAMILIES.items()}
PROCESS_REGEX = {name: compiled(parts) for name, parts in PROCESS_FAMILIES.items()}
ALL_REGEX = compiled([part for parts in FAMILIES.values() for part in parts])
METADATA_KINDS = {"front_matter", "contents", "table_of_contents", "editorial", "back_matter"}
METADATA_RECORD_IDS = {
    "M-0979", "M-0980", "M-0981", "M-0987",
}


with INVENTORY.open(newline="", encoding="utf-8-sig") as handle:
    source_rows = [row for row in csv.DictReader(handle) if row.get("volume", "") == "40"]
assert len(source_rows) == 9

ranking_rows: list[dict[str, object]] = []
full_text: dict[str, str] = {}
for row in source_rows:
    path = CORPUS / Path(row["internal_filename"]).with_suffix(".txt")
    text = path.read_text(encoding="utf-8", errors="replace")
    full_text[row["record_id"]] = text
    counts = {name: len(regex.findall(text)) for name, regex in REGEX.items()}
    process = {name: len(regex.findall(text)) for name, regex in PROCESS_REGEX.items()}
    score = (
        counts["danger"] * 3
        + counts["sanction"] * 2
        + counts["governance"]
        + counts["child"]
        + counts["exit"]
        + counts["clinical"] * 3
    )
    kind = row["notes"].removeprefix("kind=")
    functional_class = (
        "metadata"
        if kind in METADATA_KINDS or row["record_id"] in METADATA_RECORD_IDS
        else "substantive"
    )
    title_hits = len(ALL_REGEX.findall(row["article_title"]))
    ranking_rows.append({
        "record_id": row["record_id"],
        "file": str(path.relative_to(ROOT.parent)),
        "volume": row["volume"],
        "issue": row["issue"],
        "kind": kind,
        "functional_class": functional_class,
        "article_title": row["article_title"],
        "author": row["author"],
        "pdf_pages": row["pdf_pages"],
        "score": score,
        "title_hits": title_hits,
        **counts,
        **{f"process_{name}": value for name, value in process.items()},
        "process_families_present": sum(value > 0 for value in process.values()),
    })

ranking_rows.sort(
    key=lambda item: (
        item["functional_class"] == "metadata",
        -int(item["score"]),
        item["record_id"],
    )
)
fields = list(ranking_rows[0])
with RANKING.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(ranking_rows)

context_lines: list[str] = []
for rank, item in enumerate(ranking_rows, 1):
    if item["functional_class"] == "metadata":
        continue
    rid = str(item["record_id"])
    context_lines.append(
        f"===== RANK {rank} {rid} V{item['volume']}.{item['issue']} score={item['score']} "
        f"danger={item['danger']} sanction={item['sanction']} governance={item['governance']} "
        f"child={item['child']} exit={item['exit']} clinical={item['clinical']} ====="
    )
    context_lines.append(str(item["article_title"]))
    text = full_text[rid]
    pages = text.split("\f")
    emitted = 0
    for page_number, page in enumerate(pages, 1):
        lines = page.splitlines()
        for line_number, line in enumerate(lines, 1):
            if ALL_REGEX.search(line):
                before = lines[line_number - 2].strip() if line_number > 1 else ""
                after = lines[line_number].strip() if line_number < len(lines) else ""
                if before:
                    context_lines.append(f"p{page_number}:{line_number-1}: {before}")
                context_lines.append(f"p{page_number}:{line_number}: {line.strip()}")
                if after:
                    context_lines.append(f"p{page_number}:{line_number+1}: {after}")
                context_lines.append("")
                emitted += 1
                if emitted >= 240:
                    context_lines.append("[context display capped at 240 matching lines; counts remain complete]")
                    break
        if emitted >= 240:
            break
    context_lines.append("")
CONTEXTS.write_text("\n".join(context_lines), encoding="utf-8")

child_regex = REGEX["child"]
danger_regex = REGEX["danger"]
child_output: list[str] = []
for item in ranking_rows:
    if item["functional_class"] == "metadata":
        continue
    rid = str(item["record_id"])
    text = full_text[rid]
    pages = text.split("\f")
    hits: list[tuple[int, int, str]] = []
    for page_number, page in enumerate(pages, 1):
        danger_spans = [match.span() for match in danger_regex.finditer(page)]
        if not danger_spans:
            continue
        seen_windows: set[tuple[int, int]] = set()
        for child_match in child_regex.finditer(page):
            nearest = min(
                danger_spans,
                key=lambda span: min(abs(span[0] - child_match.end()), abs(child_match.start() - span[1])),
            )
            distance = min(abs(nearest[0] - child_match.end()), abs(child_match.start() - nearest[1]))
            if distance > 450:
                continue
            start = max(0, min(child_match.start(), nearest[0]) - 180)
            end = min(len(page), max(child_match.end(), nearest[1]) + 220)
            key = (start // 120, end // 120)
            if key in seen_windows:
                continue
            seen_windows.add(key)
            snippet = re.sub(r"\s+", " ", page[start:end]).strip()
            hits.append((page_number, distance, snippet))

    if hits:
        child_output.append(
            f"===== {rid} V{item['volume']}.{item['issue']} hits={len(hits)} "
            f"process_families={item['process_families_present']} ====="
        )
        child_output.append(str(item["article_title"]))
        for page_number, distance, snippet in hits:
            child_output.append(f"PDF p.{page_number} distance={distance}: {snippet}")
        child_output.append("")
CHILD_CONTEXTS.write_text("\n".join(child_output), encoding="utf-8")

print(
    f"ranked={len(ranking_rows)} "
    f"nonmetadata={sum(row['functional_class'] == 'substantive' for row in ranking_rows)} "
    f"child_candidate_files={sum(1 for line in child_output if line.startswith('===== M-'))}"
)
