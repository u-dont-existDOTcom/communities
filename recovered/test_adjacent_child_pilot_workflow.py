#!/usr/bin/env python3
"""Regression-test idempotency and verification for the adjacent pilot."""

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
    with tempfile.TemporaryDirectory(prefix="communities-adjacent-pilot-") as temp:
        copy = Path(temp) / "repo"
        shutil.copytree(
            REPOSITORY,
            copy,
            ignore=shutil.ignore_patterns("corpus-*", "__pycache__", "*.pyc"),
        )
        recovered = copy / "recovered"
        updater = recovered / "update_adjacent_child_pilot.py"
        verifier = recovered / "verify_adjacent_child_pilot.py"

        run(updater, copy)
        first = digest(copy)
        run(updater, copy)
        second = digest(copy)
        assert first == second, "updater must be idempotent"
        run(verifier, copy)

    print("adjacent child-response pilot workflow regression: PASS")


if __name__ == "__main__":
    main()
