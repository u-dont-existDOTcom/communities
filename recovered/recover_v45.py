#!/usr/bin/env python3
"""Route and verify volume 45 PDFs by saved SHA-256 identity."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
DEFAULT_CORPUS = ROOT / "corpus-v45"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def route_downloads(
    downloads: list[Path],
    destinations: dict[str, Path],
) -> list[Path]:
    """Move downloaded PDFs to inventory destinations using their content hashes."""
    routed: list[Path] = []
    for source in downloads:
        digest = sha256(source)
        if digest not in destinations:
            raise ValueError(f"unknown PDF hash: {source} {digest}")
        destination = destinations[digest]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if sha256(destination) != digest:
                raise ValueError(f"destination exists with wrong hash: {destination}")
            source.unlink()
        else:
            shutil.move(str(source), str(destination))
        routed.append(destination)
    return routed


def verify_corpus(
    destinations: dict[str, Path],
    *,
    require_complete: bool = True,
) -> tuple[int, list[Path]]:
    """Verify present corpus members and optionally require all destinations."""
    verified = 0
    missing: list[Path] = []
    for expected_hash, path in destinations.items():
        if not path.is_file():
            missing.append(path)
            continue
        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            raise ValueError(f"wrong PDF hash: {path} {actual_hash}")
        verified += 1
    if require_complete and missing:
        raise FileNotFoundError(f"missing {len(missing)} volume 45 PDFs")
    return verified, missing


def load_volume_45_destinations(
    inventory: Path = DEFAULT_INVENTORY,
    corpus: Path = DEFAULT_CORPUS,
) -> dict[str, Path]:
    with inventory.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if row["volume"] == "45"]
    if len(rows) != 15:
        raise ValueError(f"expected 15 volume 45 inventory rows, found {len(rows)}")
    if Counter(row["issue"] for row in rows) != Counter({"1": 15}):
        raise ValueError("expected all 15 volume 45 rows in issue 1")
    destinations = {
        row["sha256"]: corpus / Path(row["internal_filename"]).relative_to("archive")
        for row in rows
    }
    if len(destinations) != 15:
        raise ValueError("volume 45 inventory contains duplicate member hashes")
    return destinations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--downloads", nargs="*", type=Path, default=[])
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--allow-incomplete", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    destinations = load_volume_45_destinations()
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
    "load_volume_45_destinations",
    "main",
    "route_downloads",
    "sha256",
    "verify_corpus",
]


if __name__ == "__main__":
    main()
