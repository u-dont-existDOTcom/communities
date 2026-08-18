#!/usr/bin/env python3
"""Regression tests for the volume 36 recovery and discovery boundary."""

from __future__ import annotations

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from recovered.recover_v36 import route_downloads


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
RANKING = ROOT / "V36-DISCOVERY-RANKING.csv"
KEYWORD_CONTEXTS = ROOT / "v36-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "v36-child-danger-contexts.txt"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class Volume36RecoveryTest(unittest.TestCase):
    def test_route_downloads_uses_saved_hash_instead_of_browser_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "arbitrary-browser-name.pdf"
            payload = b"%PDF-test-member"
            source.write_bytes(payload)
            expected_hash = hashlib.sha256(payload).hexdigest()
            destination = root / "corpus" / "vol36" / "iss1" / "001-contents.pdf"

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


class Volume36WorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        inventory_rows = load_csv(INVENTORY)
        cls.expected_rows = [row for row in inventory_rows if row["volume"] == "36"]
        cls.expected_ids = {row["record_id"] for row in cls.expected_rows}

    def test_inventory_boundary_is_21_pdfs_in_two_issues(self) -> None:
        self.assertEqual(len(self.expected_rows), 21)
        self.assertEqual(sum(row["issue"] == "1" for row in self.expected_rows), 10)
        self.assertEqual(sum(row["issue"] == "2" for row in self.expected_rows), 11)

    def test_volume_36_discovery_outputs_cover_every_inventory_row(self) -> None:
        rows = load_csv(RANKING)
        self.assertEqual(len(rows), 21)
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


if __name__ == "__main__":
    unittest.main()
