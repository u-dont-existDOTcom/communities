#!/usr/bin/env python3
"""Regression-test the public research report derivative workflow."""

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
    "docs/PUBLIC-RESEARCH-REPORT.md",
    "docs/ARTICLE-APPENDIX-RESEARCH-LINK.md",
    "recovered/COMMUNITIES-EVIDENCE-LEDGER.csv",
    "recovered/COMMUNITIES-SYNTHESIS-CROSSWALK.csv",
    "recovered/COMMUNITIES-ADJACENT-SOURCE-INVENTORY.csv",
    "recovered/COMMUNITIES-ARTICLE-GAP-BANK.md",
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
    with tempfile.TemporaryDirectory(prefix="communities-public-report-") as temp:
        copy = Path(temp) / "repo"
        shutil.copytree(
            REPOSITORY,
            copy,
            ignore=shutil.ignore_patterns(".git", "corpus-*", "__pycache__", "*.pyc"),
        )
        recovered = copy / "recovered"
        updater = recovered / "update_public_research_report.py"
        verifier = recovered / "verify_public_research_report.py"

        run(updater, copy)
        first = digest(copy)
        run(updater, copy)
        second = digest(copy)
        assert first == second, "public report updater must be byte-idempotent"
        run(verifier, copy)

    print("Public research report workflow regression: PASS")


if __name__ == "__main__":
    main()
