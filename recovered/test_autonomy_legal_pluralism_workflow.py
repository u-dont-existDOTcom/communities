#!/usr/bin/env python3
"""Regression-test the autonomy/legal-pluralism correction workflow."""

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
    "docs/superpowers/plans/2026-08-15-autonomy-legal-pluralism-correction.md",
    "recovered/COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv",
    "recovered/COMMUNITIES-ARTICLE-GAP-BANK.md",
    "recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-EVIDENCE-LEDGER.csv",
    "recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-REPORT.md",
    "recovered/COMMUNITIES-AUTONOMY-LEGAL-PLURALISM-SOURCE-INVENTORY.csv",
    "recovered/COMMUNITIES-EVIDENCE-LEDGER.csv",
    "recovered/COMMUNITIES-FINAL-SYNTHESIS-REPORT.md",
    "recovered/COMMUNITIES-RESEARCH-STATE.md",
    "recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv",
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
    with tempfile.TemporaryDirectory(prefix="communities-autonomy-correction-") as temp:
        copy = Path(temp) / "repo"
        shutil.copytree(
            REPOSITORY,
            copy,
            ignore=shutil.ignore_patterns("corpus-*", "__pycache__", "*.pyc"),
        )
        recovered = copy / "recovered"
        updater = recovered / "update_autonomy_legal_pluralism.py"
        verifier = recovered / "verify_autonomy_legal_pluralism.py"

        run(updater, copy)
        first = digest(copy)
        run(updater, copy)
        second = digest(copy)
        assert first == second, "autonomy correction updater must be byte-idempotent"
        run(verifier, copy)

    print("autonomy/legal-pluralism workflow regression: PASS")


if __name__ == "__main__":
    main()
