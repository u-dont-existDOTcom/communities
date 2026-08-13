#!/usr/bin/env python3
"""Regression tests for the volume 43 recovery boundary."""

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

from recovered.recover_v43 import load_volume_43_destinations, route_downloads


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
RANKING = ROOT / "V43-DISCOVERY-RANKING.csv"
KEYWORD_CONTEXTS = ROOT / "v43-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "v43-child-danger-contexts.txt"
LEDGER = ROOT / "COMMUNITIES-EVIDENCE-LEDGER.csv"
REPORT = ROOT / "COMMUNITIES-V43-RESEARCH-REPORT.md"
UPDATE = ROOT / "update_v43.py"
VERIFY = ROOT / "verify_v43.py"


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


class Volume43RecoveryTest(unittest.TestCase):
    def test_recovery_script_runs_from_repository_root(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "recover_v43.py"), "--allow-incomplete"],
            cwd=ROOT.parent,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = re.fullmatch(r"verified=(\d+) missing=(\d+)", result.stdout.strip())
        self.assertIsNotNone(receipt, result.stdout)
        self.assertEqual(sum(map(int, receipt.groups())), 37)

    def test_inventory_loader_maps_exact_volume_43_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory) / "corpus-v43"

            destinations = load_volume_43_destinations(INVENTORY, corpus)

            self.assertEqual(len(destinations), 37)
            self.assertEqual(
                sum("/iss1/" in path.as_posix() for path in destinations.values()),
                20,
            )
            self.assertEqual(
                sum("/iss2/" in path.as_posix() for path in destinations.values()),
                17,
            )
            self.assertTrue(
                all(path.is_relative_to(corpus / "vol43") for path in destinations.values())
            )

    def test_route_downloads_uses_saved_hash_instead_of_browser_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "arbitrary-browser-name.pdf"
            payload = b"%PDF-test-member"
            source.write_bytes(payload)
            expected_hash = hashlib.sha256(payload).hexdigest()
            destination = root / "corpus" / "vol43" / "iss2" / "001-from-the-editors.pdf"

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


class Volume43InventoryBoundaryTest(unittest.TestCase):
    def test_inventory_boundary_is_37_pdfs_split_across_two_issues(self) -> None:
        rows = [row for row in load_csv(INVENTORY) if row["volume"] == "43"]
        self.assertEqual(len(rows), 37)
        self.assertEqual(
            Counter(row["issue"] for row in rows),
            Counter({"1": 20, "2": 17}),
        )


class Volume43WorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        inventory_rows = load_csv(INVENTORY)
        cls.expected_rows = [row for row in inventory_rows if row["volume"] == "43"]
        cls.expected_ids = {row["record_id"] for row in cls.expected_rows}

    def test_volume_43_discovery_outputs_cover_every_inventory_row(self) -> None:
        rows = load_csv(RANKING)
        self.assertEqual(len(rows), 37)
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

        previous = ROOT / "discover_v42.py"
        current = ROOT / "discover_v43.py"
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
            "M-0046",
            "M-0047",
            "M-0048",
            "M-0065",
            "M-0066",
            "M-0067",
            "M-0081",
            "M-0082",
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
                "table_of_contents": 2,
                "editorial": 2,
                "back_matter": 2,
            }),
        )
        self.assertEqual(
            sum(row["functional_class"] == "substantive" for row in rows.values()),
            29,
        )

    def test_completed_checkpoint_contract(self) -> None:
        self.assertTrue(UPDATE.is_file())
        self.assertTrue(VERIFY.is_file())
        self.assertTrue(REPORT.is_file())

        ledger_rows = load_csv(LEDGER)
        self.assertEqual(len(ledger_rows), 154)
        self.assertEqual(
            [row["finding_id"] for row in ledger_rows[-3:]],
            ["F-152", "F-153", "F-154"],
        )
        self.assertEqual(
            [row["source_record_id"] for row in ledger_rows[-3:]],
            ["M-0070", "M-0075", ""],
        )
        self.assertEqual(
            Counter(row["article_gap_status"] for row in ledger_rows[-3:]),
            Counter({"C": 2, "F": 1}),
        )

        report = REPORT.read_text(encoding="utf-8")
        self.assertIn("All **37 PDFs** in volume 43 were processed", report)
        self.assertIn("**29** substantive close reads", report)
        self.assertIn("**3 new findings, F-152 through F-154**", report)
        self.assertEqual(
            set(re.findall(r"^\| (M-\d{4}) \|", report, re.MULTILINE)),
            self.expected_ids
            - {
                "M-0046",
                "M-0047",
                "M-0048",
                "M-0065",
                "M-0066",
                "M-0067",
                "M-0081",
                "M-0082",
            },
        )


if __name__ == "__main__":
    unittest.main()
