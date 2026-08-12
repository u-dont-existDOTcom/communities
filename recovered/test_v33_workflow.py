#!/usr/bin/env python3
"""Regression tests for the volume 33 discovery boundary."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
RANKING = ROOT / "V33-DISCOVERY-RANKING.csv"
KEYWORD_CONTEXTS = ROOT / "v33-keyword-contexts.txt"
CHILD_CONTEXTS = ROOT / "v33-child-danger-contexts.txt"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class Volume33WorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        inventory_rows = load_csv(INVENTORY)
        cls.expected_rows = [row for row in inventory_rows if row["volume"] == "33"]
        cls.expected_ids = {row["record_id"] for row in cls.expected_rows}

    def test_inventory_boundary_is_36_pdfs_in_two_issues(self) -> None:
        self.assertEqual(len(self.expected_rows), 36)
        self.assertEqual(sum(row["issue"] == "1" for row in self.expected_rows), 14)
        self.assertEqual(sum(row["issue"] == "2" for row in self.expected_rows), 22)

    def test_volume_33_discovery_outputs_cover_every_inventory_row(self) -> None:
        rows = load_csv(RANKING)
        self.assertEqual(len(rows), 36)
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
