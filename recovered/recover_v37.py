#!/usr/bin/env python3
"""Route and verify volume 37 publisher PDFs by saved SHA-256 identity."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from collections.abc import Iterable, Mapping
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_INVENTORY = ROOT / "COMMUNITIES-SOURCE-INVENTORY.csv"
DEFAULT_CORPUS = ROOT / "corpus-v37"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_volume_37_destinations(
    inventory: Path = DEFAULT_INVENTORY,
    corpus: Path = DEFAULT_CORPUS,
) -> dict[str, Path]:
    with inventory.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if row["volume"] == "37"]
    if len(rows) != 26:
        raise ValueError(f"expected 26 volume 37 inventory rows, found {len(rows)}")
    destinations = {row["sha256"]: corpus / row["internal_filename"] for row in rows}
    if len(destinations) != 26:
        raise ValueError("volume 37 inventory contains duplicate member hashes")
    return destinations


def route_downloads(
    downloads: Iterable[Path],
    hash_to_destination: Mapping[str, Path],
) -> list[Path]:
    sources = [Path(path) for path in downloads]
    inspected: list[tuple[Path, str, Path]] = []
    seen_hashes: set[str] = set()
    for source in sources:
        if not source.is_file():
            raise ValueError(f"download is not a file: {source}")
        member_hash = sha256(source)
        if member_hash not in hash_to_destination:
            raise ValueError(f"unknown PDF hash {member_hash}: {source}")
        if member_hash in seen_hashes:
            raise ValueError(f"duplicate PDF hash {member_hash}: {source}")
        seen_hashes.add(member_hash)
        inspected.append((source, member_hash, Path(hash_to_destination[member_hash])))

    routed: list[Path] = []
    for source, member_hash, destination in inspected:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and sha256(destination) != member_hash:
            raise ValueError(f"destination hash conflict: {destination}")
        if source.resolve() != destination.resolve():
            shutil.move(str(source), str(destination))
        routed.append(destination)
    return routed


def verify_corpus(
    hash_to_destination: Mapping[str, Path],
    require_complete: bool = True,
) -> tuple[int, list[Path]]:
    missing: list[Path] = []
    verified = 0
    for expected_hash, destination in hash_to_destination.items():
        destination = Path(destination)
        if not destination.is_file():
            missing.append(destination)
            continue
        actual_hash = sha256(destination)
        if actual_hash != expected_hash:
            raise ValueError(
                f"corpus hash mismatch for {destination}: {actual_hash} != {expected_hash}"
            )
        verified += 1
    if require_complete and missing:
        raise ValueError(f"missing {len(missing)} volume 37 PDFs")
    return verified, missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--downloads", nargs="*", type=Path, default=[])
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--allow-incomplete", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    destinations = load_volume_37_destinations()
    if args.downloads:
        routed = route_downloads(args.downloads, destinations)
        print(f"routed={len(routed)}")
    if args.verify or not args.downloads:
        verified, missing = verify_corpus(
            destinations,
            require_complete=not args.allow_incomplete,
        )
        print(f"verified={verified} missing={len(missing)}")


if __name__ == "__main__":
    main()
