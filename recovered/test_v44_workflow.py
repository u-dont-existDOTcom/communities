#!/usr/bin/env python3
"""Regression tests for the volume 44 recovery boundary."""

from __future__ import annotations

import ast
import csv
import hashlib
import re
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from recovered.recover_v44 import load_volume_44_destinations, route_downloads


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
RANKING = ROOT / "V44-DISCOVERY-RANKING.csv"
KEYWORD_CONTEXTS = ROOT / "v44-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "v44-child-danger-contexts.txt"
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
REPORT = ROOT / "COMMUNITIES-V44-RESEARCH-REPORT.md"
UPDATE = ROOT / "update_v44.py"
VERIFY = ROOT / "verify_v44.py"


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


class Volume44RecoveryTest(unittest.TestCase):
    def test_recovery_script_runs_from_repository_root(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "recover_v44.py"), "--allow-incomplete"],
            cwd=ROOT.parent,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = re.fullmatch(r"verified=(\d+) missing=(\d+)", result.stdout.strip())
        self.assertIsNotNone(receipt, result.stdout)
        self.assertEqual(sum(map(int, receipt.groups())), 33)

    def test_inventory_loader_maps_exact_volume_44_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory) / "corpus-v44"

            destinations = load_volume_44_destinations(INVENTORY, corpus)

            self.assertEqual(len(destinations), 33)
            self.assertEqual(
                sum("/iss1/" in path.as_posix() for path in destinations.values()),
                20,
            )
            self.assertEqual(
                sum("/iss2/" in path.as_posix() for path in destinations.values()),
                13,
            )
            self.assertTrue(
                all(path.is_relative_to(corpus / "vol44") for path in destinations.values())
            )

    def test_route_downloads_uses_saved_hash_instead_of_browser_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "arbitrary-browser-name.pdf"
            payload = b"%PDF-test-member"
            source.write_bytes(payload)
            expected_hash = hashlib.sha256(payload).hexdigest()
            destination = root / "corpus" / "vol44" / "iss2" / "001-from-the-editors.pdf"

            routed = route_downloads([source], {expected_hash: destination})

            self.assertEqual(routed, [destination])
            self.assertEqual(destination.read_bytes(), payload)
            self.assertFalse(source.exists())

    def test_route_downloads_rejects_unknown_pdf_without_moving_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "unknown.pdf"
            source.write_bytes(b"%PDF-unknown")

            with self.assertRaisesRegex(ValueError, "unknown PDF hash"):
                route_downloads([source], {})

            self.assertTrue(source.is_file())


class Volume44InventoryBoundaryTest(unittest.TestCase):
    def test_inventory_boundary_is_33_pdfs_split_across_two_issues(self) -> None:
        rows = [row for row in load_csv(INVENTORY) if row["volume"] == "44"]
        self.assertEqual(len(rows), 33)
        self.assertEqual(
            Counter(row["issue"] for row in rows),
            Counter({"1": 20, "2": 13}),
        )


class Volume44WorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        inventory_rows = load_csv(INVENTORY)
        cls.expected_rows = [row for row in inventory_rows if row["volume"] == "44"]
        cls.expected_ids = {row["record_id"] for row in cls.expected_rows}

    def test_volume_44_discovery_outputs_cover_every_inventory_row(self) -> None:
        rows = load_csv(RANKING)
        self.assertEqual(len(rows), 33)
        self.assertEqual({row["record_id"] for row in rows}, self.expected_ids)
        self.assertTrue(KEYWORD_CONTEXTS.is_file())
        self.assertTrue(CHILD_CONTEXTS.is_file())

    def test_ranking_paths_resolve_to_nonempty_extracted_text(self) -> None:
        rows = load_csv(RANKING)
        for row in rows:
            path = ROOT / Path(row["file"]).relative_to("recovered")
            self.assertTrue(path.is_file(), row["record_id"])
            self.assertGreater(path.stat().st_size, 0, row["record_id"])

    def test_ranking_preserves_term_and_process_families(self) -> None:
        required = {
            "danger",
            "sanction",
            "governance",
            "child",
            "exit",
            "clinical",
            "process_allegation",
            "process_assessment",
            "process_intervention",
            "process_review",
            "process_outcome",
            "process_families_present",
        }
        rows = load_csv(RANKING)
        self.assertTrue(rows)
        self.assertTrue(required <= set(rows[0]))

        previous = ROOT / "discover_v43.py"
        current = ROOT / "discover_v44.py"
        self.assertEqual(
            literal_assignment(current, "FAMILIES"),
            literal_assignment(previous, "FAMILIES"),
        )
        self.assertEqual(
            literal_assignment(current, "PROCESS_FAMILIES"),
            literal_assignment(previous, "PROCESS_FAMILIES"),
        )

    def test_discovery_classifies_functional_metadata(self) -> None:
        rows = {row["record_id"]: row for row in load_csv(RANKING)}

        expected_metadata = {
            "M-0083",
            "M-0084",
            "M-0101",
            "M-0102",
            "M-0103",
            "M-0104",
            "M-0105",
            "M-0115",
        }
        self.assertEqual(
            {
                record_id
                for record_id, row in rows.items()
                if row["functional_class"] == "metadata"
            },
            expected_metadata,
        )
        self.assertEqual(
            Counter(rows[record_id]["kind"] for record_id in expected_metadata),
            Counter({
                "front_matter": 2,
                "contents": 1,
                "table_of_contents": 1,
                "editorial": 2,
                "back_matter": 2,
            }),
        )
        self.assertEqual(
            sum(row["functional_class"] == "substantive" for row in rows.values()),
            25,
        )

    def test_completed_checkpoint_contract(self) -> None:
        self.assertTrue(UPDATE.is_file())
        self.assertTrue(VERIFY.is_file())
        self.assertTrue(REPORT.is_file())

        ledger_rows = load_csv(LEDGER)
        self.assertEqual(len(ledger_rows), 158)
        self.assertEqual(
            [row["finding_id"] for row in ledger_rows[-4:]],
            ["F-155", "F-156", "F-157", "F-158"],
        )
        self.assertEqual(
            [row["source_record_id"] for row in ledger_rows[-4:]],
            ["M-0106", "M-0113", "M-0093", ""],
        )
        self.assertEqual(
            Counter(row["article_gap_status"] for row in ledger_rows[-4:]),
            Counter({"C": 3, "F": 1}),
        )

        report = REPORT.read_text(encoding="utf-8")
        self.assertIn("All **33 PDFs** in volume 44 were processed", report)
        self.assertIn("**25** substantive close reads", report)
        self.assertIn("**4 new findings, F-155 through F-158**", report)
        self.assertEqual(
            set(re.findall(r"^\| (M-\d{4}) \|", report, re.MULTILINE)),
            self.expected_ids
            - {
                "M-0083",
                "M-0084",
                "M-0101",
                "M-0102",
                "M-0103",
                "M-0104",
                "M-0105",
                "M-0115",
            },
        )


if __name__ == "__main__":
    unittest.main()
