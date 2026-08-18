#!/usr/bin/env python3
"""Route and verify volume 38 publisher PDFs by saved SHA-256 identity."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

if __package__:
    from recovered.recover_v37 import route_downloads, sha256, verify_corpus
else:
    from recover_v37 import route_downloads, sha256, verify_corpus


ROOT = Path(__file__).resolve().parent
DEFAULT_INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
DEFAULT_CORPUS = ROOT / "corpus-v38"


def load_volume_38_destinations(
    inventory: Path = DEFAULT_INVENTORY,
    corpus: Path = DEFAULT_CORPUS,
) -> dict[str, Path]:
    with inventory.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if row["volume"] == "38"]
    if len(rows) != 20:
        raise ValueError(f"expected 20 volume 38 inventory rows, found {len(rows)}")
    destinations = {row["sha256"]: corpus / row["internal_filename"] for row in rows}
    if len(destinations) != 20:
        raise ValueError("volume 38 inventory contains duplicate member hashes")
    return destinations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--downloads", nargs="*", type=Path, default=[])
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--allow-incomplete", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    destinations = load_volume_38_destinations()
    if args.downloads:
        routed = route_downloads(args.downloads, destinations)
        print(f"routed={len(routed)}")
    if args.verify or not args.downloads:
        verified, missing = verify_corpus(
            destinations,
            require_complete=not args.allow_incomplete,
        )
        print(f"verified={verified} missing={len(missing)}")


__all__ = [
    "load_volume_38_destinations",
    "main",
    "route_downloads",
    "sha256",
    "verify_corpus",
]


if __name__ == "__main__":
    main()
