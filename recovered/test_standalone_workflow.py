#!/usr/bin/env python3
"""Regression tests for the eight-source standalone checkpoint."""

from __future__ import annotations

import ast
import csv
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
GAP_BANK = ROOT / "COMMUNITIES-ARTICLE-GAP-BANK.md"
STATE = ROOT / "COMMUNITIES-RESEARCH-STATE.md"
REPORT = ROOT / "COMMUNITIES-STANDALONE-RESEARCH-REPORT.md"
RANKING = ROOT / "STANDALONE-DISCOVERY-RANKING.csv"
KEYWORD_CONTEXTS = ROOT / "standalone-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "standalone-child-danger-contexts.txt"
DISCOVER = ROOT / "discover_standalone.py"
UPDATE = ROOT / "update_standalone.py"
VERIFY = ROOT / "verify_standalone.py"

EXPECTED_SOURCE_IDS = {
    "D-001", "D-002", "D-004", "D-005",
    "D-006", "D-007", "D-008", "D-018",
}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


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


def assignment_source(path: Path, name: str) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == name
        ):
            return ast.unparse(node.value)
    raise AssertionError(f"missing assignment {name} in {path}")


def digest_paths(paths: list[Path]) -> dict[str, str]:
    return {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }


class StandaloneDiscoveryTest(unittest.TestCase):
    def test_discovery_runs_from_repository_root(self) -> None:
        result = subprocess.run(
            [sys.executable, str(DISCOVER)],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(
            result.stdout.strip(),
            r"^ranked=8 substantive=8 child_candidate_files=8$",
        )

    def test_discovery_covers_exact_boundary(self) -> None:
        rows = load_csv(RANKING)
        self.assertEqual(len(rows), 8)
        self.assertEqual({row["record_id"] for row in rows}, EXPECTED_SOURCE_IDS)
        self.assertEqual(
            Counter(row["functional_class"] for row in rows),
            Counter({"substantive": 8}),
        )
        self.assertTrue(KEYWORD_CONTEXTS.is_file())
        self.assertTrue(CHILD_CONTEXTS.is_file())
        headers = re.findall(
            r"^===== (D-\d{3})\b",
            CHILD_CONTEXTS.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        self.assertEqual(len(headers), 8)
        self.assertEqual(set(headers), EXPECTED_SOURCE_IDS)

    def test_discovery_reuses_locked_families(self) -> None:
        self.assertEqual(
            assignment_source(DISCOVER, "FAMILIES"),
            "literal_assignment(ROOT / 'discover_v45.py', 'FAMILIES')",
        )
        self.assertEqual(
            assignment_source(DISCOVER, "PROCESS_FAMILIES"),
            "literal_assignment(ROOT / 'discover_v45.py', 'PROCESS_FAMILIES')",
        )
        self.assertTrue(literal_assignment(ROOT / "discover_v45.py", "FAMILIES"))
        self.assertTrue(
            literal_assignment(ROOT / "discover_v45.py", "PROCESS_FAMILIES")
        )

    def test_ranking_paths_resolve_to_nonempty_text(self) -> None:
        for row in load_csv(RANKING):
            path = REPOSITORY / row["file"]
            self.assertTrue(path.is_file(), row["record_id"])
            self.assertGreater(path.stat().st_size, 0, row["record_id"])


class StandaloneCheckpointTest(unittest.TestCase):
    def test_inventory_dispositions(self) -> None:
        rows = {
            row["record_id"]: row
            for row in load_csv(INVENTORY)
            if row["record_id"] in EXPECTED_SOURCE_IDS
        }
        self.assertEqual(set(rows), EXPECTED_SOURCE_IDS)
        self.assertEqual(
            Counter(row["research_status"] for row in rows.values()),
            Counter({
                "close read; findings promoted": 3,
                "contextual close read; no distinct finding": 5,
            }),
        )
        self.assertTrue(all(row["sha256"] for row in rows.values()))
        self.assertTrue(
            all(row["text_extraction_status"] == "extracted" for row in rows.values())
        )

    def test_ledger_boundary_and_classes(self) -> None:
        rows = load_csv(LEDGER)
        self.assertEqual(len(rows), 168)
        self.assertEqual(
            [row["finding_id"] for row in rows[-6:]],
            ["F-163", "F-164", "F-165", "F-166", "F-167", "F-168"],
        )
        self.assertEqual(
            [row["source_record_id"] for row in rows[-6:]],
            ["D-001", "D-001", "D-006", "D-006", "D-008", ""],
        )
        self.assertEqual(
            Counter(row["article_gap_status"] for row in rows[-6:]),
            Counter({"B": 2, "C": 3, "F": 1}),
        )
        for row in rows[-6:]:
            self.assertEqual(row["supporting_excerpt"], "")
            for field in (
                "source_access",
                "what_source_establishes",
                "what_source_does_not_establish",
                "alternative_interpretation",
                "response_process",
                "outcome",
                "transferability",
            ):
                self.assertTrue(row[field], (row["finding_id"], field))

    def test_gap_bank_remains_reconciled(self) -> None:
        text = GAP_BANK.read_text(encoding="utf-8")
        rows = [line for line in text.splitlines() if line.startswith("| G-")]
        self.assertEqual(len(rows), 18)
        self.assertEqual(
            Counter(line.split("|")[2].strip() for line in rows),
            Counter({"B": 8, "C": 7, "D": 3}),
        )
        for finding_id in ("F-163", "F-164", "F-165", "F-166", "F-167", "F-168"):
            self.assertIn(finding_id, text)

    def test_report_covers_every_source_and_rejects_coercive_transfer(self) -> None:
        text = REPORT.read_text(encoding="utf-8")
        self.assertEqual(
            set(re.findall(r"^\| (D-\d{3}) \|", text, re.MULTILINE)),
            EXPECTED_SOURCE_IDS,
        )
        self.assertIn("6 new findings, F-163 through F-168", text)
        self.assertIn("unethical, coercive, unsupported, and rejected", text)
        self.assertIn("Execution is not a recommendation", text)
        self.assertIn("No article prose was drafted or revised", text)

    def test_state_closes_assigned_primary_corpus(self) -> None:
        text = STATE.read_text(encoding="utf-8")
        self.assertIn("**168 findings** (`F-001` through `F-168`)", text)
        self.assertIn("**8 of 8 standalone substantive sources**", text)
        self.assertIn("No journal PDF or assigned standalone source remains", text)


class StandaloneWorkflowTest(unittest.TestCase):
    def test_update_is_idempotent_in_isolated_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            recovered = repo / "recovered"
            docs = repo / "docs"
            recovered.mkdir(parents=True)
            docs.mkdir(parents=True)
            for source in (
                UPDATE,
                LEDGER,
                INVENTORY,
                GAP_BANK,
                STATE,
                REPORT,
            ):
                shutil.copy2(source, recovered / source.name)
            shutil.copy2(REPOSITORY / "README.md", repo / "README.md")
            shutil.copy2(REPOSITORY / "AGENTS.md", repo / "AGENTS.md")
            shutil.copy2(REPOSITORY / "docs" / "INDEX.md", docs / "INDEX.md")
            command = [sys.executable, str(recovered / UPDATE.name)]
            first = subprocess.run(
                command, cwd=repo, capture_output=True, text=True, check=False
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            tracked = [
                recovered / LEDGER.name,
                recovered / INVENTORY.name,
                recovered / GAP_BANK.name,
                recovered / STATE.name,
                repo / "README.md",
                repo / "AGENTS.md",
                docs / "INDEX.md",
            ]
            after_first = digest_paths(tracked)
            second = subprocess.run(
                command, cwd=repo, capture_output=True, text=True, check=False
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(after_first, digest_paths(tracked))

    def test_full_source_verifier(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VERIFY)],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("verified standalone checkpoint", result.stdout)


if __name__ == "__main__":
    unittest.main()
