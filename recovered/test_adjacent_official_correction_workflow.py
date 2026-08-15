#!/usr/bin/env python3
"""Regression-test Unit D updater idempotency and verification."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
TRACKED = [
    "AGENTS.md",
    "README.md",
    "docs/INDEX.md",
    "docs/superpowers/plans/2026-08-15-adjacent-source-roadmap.md",
    "recovered/COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv",
    "recovered/COMMUNITIES-ARTICLE-GAP-BANK.md",
    "recovered/COMMUNITIES-EVIDENCE-LEDGER.csv",
    "recovered/COMMUNITIES-RESEARCH-STATE.md",
]


def digest(root: Path) -> str:
    value = hashlib.sha256()
    for relative in TRACKED:
        path = root / relative
        value.update(relative.encode("utf-8"))
        value.update(path.read_bytes())
    return value.hexdigest()


def run(script: Path, cwd: Path) -> None:
    subprocess.run([sys.executable, str(script)], cwd=cwd, check=True)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="communities-official-correction-") as temp:
        copy = Path(temp) / "repo"
        shutil.copytree(
            REPOSITORY,
            copy,
            ignore=shutil.ignore_patterns("corpus-*", "__pycache__", "*.pyc"),
        )
        recovered = copy / "recovered"
        updater = recovered / "update_adjacent_official_correction.py"
        verifier = recovered / "verify_adjacent_official_correction.py"

        run(updater, copy)
        first = digest(copy)
        run(updater, copy)
        second = digest(copy)
        assert first == second, "Unit D updater must be byte-idempotent"
        run(verifier, copy)

    print("adjacent official correction workflow regression: PASS")


if __name__ == "__main__":
    main()
