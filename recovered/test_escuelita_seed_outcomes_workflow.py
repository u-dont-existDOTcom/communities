#!/usr/bin/env python3
"""Regression-test the Escuelita descendant-audit workflow."""

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
    "COMMUNITY-DEVELOPMENT-LESSONS.md",
    "README.md",
    "docs/INDEX.md",
    "docs/superpowers/plans/2026-08-15-escuelita-seed-outcomes.md",
    "recovered/COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv",
    "recovered/COMMUNITIES-ARTICLE-GAP-BANK.md",
    "recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-EVIDENCE-LEDGER.csv",
    "recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-REPORT.md",
    "recovered/COMMUNITIES-ESCUELITA-SEED-OUTCOMES-SOURCE-INVENTORY.csv",
    "recovered/COMMUNITIES-EVIDENCE-LEDGER.csv",
    "recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md",
    "recovered/COMMUNITIES-RESEARCH-STATE.md",
    "recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv",
]


def digest(root: Path) -> str:
    value = hashlib.sha256()
    for relative in TRACKED:
        path = root / relative
        if not path.exists():
            continue
        value.update(relative.encode("utf-8"))
        value.update(path.read_bytes())
    return value.hexdigest()


def run(script: Path, cwd: Path) -> None:
    subprocess.run([sys.executable, str(script)], cwd=cwd, check=True)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="communities-escuelita-outcomes-") as temp:
        copy = Path(temp) / "repo"
        shutil.copytree(
            REPOSITORY,
            copy,
            ignore=shutil.ignore_patterns("corpus-*", "__pycache__", "*.pyc"),
        )
        recovered = copy / "recovered"
        updater = recovered / "update_escuelita_seed_outcomes.py"
        verifier = recovered / "verify_escuelita_seed_outcomes.py"

        run(updater, copy)
        first = digest(copy)
        run(updater, copy)
        second = digest(copy)
        assert first == second, "Escuelita updater must be byte-idempotent"
        run(verifier, copy)

    print("Escuelita seed-outcomes workflow regression: PASS")


if __name__ == "__main__":
    main()
