#!/usr/bin/env python3
"""Regression tests for the volume 38 recovery and discovery boundary."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from recovered.recover_v38 import load_volume_38_destinations, route_downloads


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
RANKING = ROOT / "V38-DISCOVERY-RANKING.csv"
KEYWORD_CONTEXTS = ROOT / "v38-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "v38-child-danger-contexts.txt"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class Volume38RecoveryTest(unittest.TestCase):
    def test_recovery_script_runs_from_repository_root(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "recover_v38.py"), "--allow-incomplete"],
            cwd=ROOT.parent,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = re.fullmatch(r"verified=(\d+) missing=(\d+)", result.stdout.strip())
        self.assertIsNotNone(receipt, result.stdout)
        self.assertEqual(sum(map(int, receipt.groups())), 20)

    def test_inventory_loader_maps_exact_volume_38_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory) / "corpus-v38"

            destinations = load_volume_38_destinations(INVENTORY, corpus)

            self.assertEqual(len(destinations), 20)
            self.assertEqual(
                sum("/iss1/" in path.as_posix() for path in destinations.values()),
                11,
            )
            self.assertEqual(
                sum("/iss2/" in path.as_posix() for path in destinations.values()),
                9,
            )
            self.assertTrue(
                all(path.is_relative_to(corpus / "vol38") for path in destinations.values())
            )

    def test_route_downloads_uses_saved_hash_instead_of_browser_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "arbitrary-browser-name.pdf"
            payload = b"%PDF-test-member"
            source.write_bytes(payload)
            expected_hash = hashlib.sha256(payload).hexdigest()
            destination = root / "corpus" / "vol38" / "iss1" / "001-front-matter.pdf"

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


class Volume38WorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        inventory_rows = load_csv(INVENTORY)
        cls.expected_rows = [row for row in inventory_rows if row["volume"] == "38"]
        cls.expected_ids = {row["record_id"] for row in cls.expected_rows}

    def test_inventory_boundary_is_20_pdfs_in_two_issues(self) -> None:
        self.assertEqual(len(self.expected_rows), 20)
        self.assertEqual(sum(row["issue"] == "1" for row in self.expected_rows), 11)
        self.assertEqual(sum(row["issue"] == "2" for row in self.expected_rows), 9)

    def test_volume_38_discovery_outputs_cover_every_inventory_row(self) -> None:
        rows = load_csv(RANKING)
        self.assertEqual(len(rows), 20)
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

    def test_discovery_uses_document_function_for_metadata_boundary(self) -> None:
        rows = {row["record_id"]: row for row in load_csv(RANKING)}

        self.assertEqual(rows["M-0949"]["kind"], "article")
        self.assertEqual(rows["M-0955"]["kind"], "article")
        self.assertEqual(rows["M-0949"]["functional_class"], "metadata")
        self.assertEqual(rows["M-0955"]["functional_class"], "metadata")
        self.assertEqual(rows["M-0950"]["functional_class"], "substantive")
        self.assertEqual(
            sum(row["functional_class"] == "substantive" for row in rows.values()),
            13,
        )


if __name__ == "__main__":
    unittest.main()
