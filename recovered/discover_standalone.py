#!/usr/bin/env python3
"""Rank and context-screen the eight standalone community-research sources."""

from __future__ import annotations

import ast
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus-standalone"
RANKING = ROOT / "STANDALONE-DISCOVERY-RANKING.csv"
CONTEXTS = ROOT / "standalone-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "standalone-child-danger-contexts.txt"


def literal_assignment(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == name
        ):
            return ast.literal_eval(node.value)
    raise AssertionError(f"missing literal assignment {name} in {path}")


FAMILIES = literal_assignment(ROOT / "discover_v45.py", "FAMILIES")
PROCESS_FAMILIES = literal_assignment(ROOT / "discover_v45.py", "PROCESS_FAMILIES")
assert isinstance(FAMILIES, dict)
assert isinstance(PROCESS_FAMILIES, dict)

SOURCES = [
    {
        "record_id": "D-001",
        "file_stem": "D-001-alienation-and-charisma",
        "kind": "book",
        "title": "Alienation and Charisma: A Study of Contemporary American Communes",
        "author": "Benjamin D. Zablocki",
        "year": "1980",
        "pages": "488",
    },
    {
        "record_id": "D-002",
        "file_stem": "D-002-commitment-and-community",
        "kind": "book",
        "title": "Commitment and Community: Communes and Utopias in Sociological Perspective",
        "author": "Rosabeth Moss Kanter",
        "year": "1972",
        "pages": "324",
    },
    {
        "record_id": "D-004",
        "file_stem": "D-004-evil-genes",
        "kind": "book",
        "title": "Evil Genes",
        "author": "Barbara Oakley",
        "year": "2008",
        "pages": "427",
    },
    {
        "record_id": "D-005",
        "file_stem": "D-005-wrangham-targeted-conspiratorial-killing",
        "kind": "research_article",
        "title": "Targeted Conspiratorial Killing, Human Self-Domestication and the Evolution of Groupishness",
        "author": "Richard W. Wrangham",
        "year": "2021",
        "pages": "21",
    },
    {
        "record_id": "D-006",
        "file_stem": "D-006-the-kung-san",
        "kind": "book",
        "title": "The !Kung San: Men, Women, and Work in a Foraging Society",
        "author": "Richard B. Lee",
        "year": "1979",
        "pages": "564",
    },
    {
        "record_id": "D-007",
        "file_stem": "D-007-the-mountain-people",
        "kind": "book",
        "title": "The Mountain People",
        "author": "Colin M. Turnbull",
        "year": "1972",
        "pages": "324",
    },
    {
        "record_id": "D-008",
        "file_stem": "D-008-the-riddle-of-amish-culture",
        "kind": "book_epub",
        "title": "The Riddle of Amish Culture, Revised Edition",
        "author": "Donald B. Kraybill",
        "year": "2001",
        "pages": "",
    },
    {
        "record_id": "D-018",
        "file_stem": "D-018-zarpentine-dissertation",
        "kind": "dissertation",
        "title": "The Fragmentation of Moral Psychology: Reason, Emotion, Motivation and Moral Judgment in Ethics and Science",
        "author": "Christopher Zarpentine",
        "year": "2011",
        "pages": "317",
    },
]


def compiled(parts: list[str]) -> re.Pattern[str]:
    return re.compile("(?:" + "|".join(parts) + ")", re.IGNORECASE)


REGEX = {name: compiled(parts) for name, parts in FAMILIES.items()}
PROCESS_REGEX = {name: compiled(parts) for name, parts in PROCESS_FAMILIES.items()}
ALL_REGEX = compiled([part for parts in FAMILIES.values() for part in parts])

ranking_rows: list[dict[str, object]] = []
full_text: dict[str, str] = {}
for source in SOURCES:
    path = CORPUS / f"{source['file_stem']}.txt"
    text = path.read_text(encoding="utf-8", errors="replace")
    full_text[str(source["record_id"])] = text
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
    ranking_rows.append({
        "record_id": source["record_id"],
        "file": str(path.relative_to(ROOT.parent)),
        "kind": source["kind"],
        "functional_class": "substantive",
        "title": source["title"],
        "author": source["author"],
        "year": source["year"],
        "source_pages": source["pages"],
        "score": score,
        "title_hits": len(ALL_REGEX.findall(str(source["title"]))),
        **counts,
        **{f"process_{name}": value for name, value in process.items()},
        "process_families_present": sum(value > 0 for value in process.values()),
    })

ranking_rows.sort(key=lambda item: (-int(item["score"]), str(item["record_id"])))
with RANKING.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(ranking_rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(ranking_rows)

context_lines: list[str] = []
for rank, item in enumerate(ranking_rows, 1):
    rid = str(item["record_id"])
    context_lines.append(
        f"===== RANK {rank} {rid} score={item['score']} danger={item['danger']} "
        f"sanction={item['sanction']} governance={item['governance']} "
        f"child={item['child']} exit={item['exit']} clinical={item['clinical']} ====="
    )
    context_lines.append(str(item["title"]))
    pages = full_text[rid].split("\f")
    emitted = 0
    for page_number, page in enumerate(pages, 1):
        lines = page.splitlines()
        for line_number, line in enumerate(lines, 1):
            if not ALL_REGEX.search(line):
                continue
            before = lines[line_number - 2].strip() if line_number > 1 else ""
            after = lines[line_number].strip() if line_number < len(lines) else ""
            if before:
                context_lines.append(f"p{page_number}:{line_number-1}: {before}")
            context_lines.append(f"p{page_number}:{line_number}: {line.strip()}")
            if after:
                context_lines.append(f"p{page_number}:{line_number+1}: {after}")
            context_lines.append("")
            emitted += 1
            if emitted >= 300:
                context_lines.append(
                    "[context display capped at 300 matching lines; counts remain complete]"
                )
                break
        if emitted >= 300:
            break
    context_lines.append("")
CONTEXTS.write_text("\n".join(context_lines), encoding="utf-8")

child_regex = REGEX["child"]
danger_regex = REGEX["danger"]
child_output: list[str] = []
for item in ranking_rows:
    rid = str(item["record_id"])
    pages = full_text[rid].split("\f")
    hits: list[tuple[int, int, str]] = []
    for page_number, page in enumerate(pages, 1):
        danger_spans = [match.span() for match in danger_regex.finditer(page)]
        if not danger_spans:
            continue
        seen_windows: set[tuple[int, int]] = set()
        for child_match in child_regex.finditer(page):
            nearest = min(
                danger_spans,
                key=lambda span: min(
                    abs(span[0] - child_match.end()),
                    abs(child_match.start() - span[1]),
                ),
            )
            distance = min(
                abs(nearest[0] - child_match.end()),
                abs(child_match.start() - nearest[1]),
            )
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
            f"===== {rid} hits={len(hits)} process_families={item['process_families_present']} ====="
        )
        child_output.append(str(item["title"]))
        for page_number, distance, snippet in hits[:300]:
            locator = f"PDF p.{page_number}" if item["kind"] != "book_epub" else "EPUB text"
            child_output.append(f"{locator} distance={distance}: {snippet}")
        if len(hits) > 300:
            child_output.append(
                f"[context display capped at 300 of {len(hits)} proximity windows]"
            )
        child_output.append("")
CHILD_CONTEXTS.write_text("\n".join(child_output), encoding="utf-8")

print(
    f"ranked={len(ranking_rows)} substantive={len(ranking_rows)} "
    f"child_candidate_files={sum(line.startswith('===== D-') for line in child_output)}"
)
