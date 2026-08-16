#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


def extract_native_markers(text: str) -> list[str]:
    """Return stable identifiers for Substack native objects in source order."""
    hits: list[tuple[int, str]] = []
    for m in re.finditer(r"public/images/[A-Za-z0-9._-]+", text):
        hits.append((m.start(), f"image:{m.group(0)}"))
    for m in re.finditer(r"&quot;nodeId&quot;:&quot;([^&]+)&quot;", text):
        hits.append((m.start(), f"digest:{m.group(1)}"))
    for m in re.finditer(r'id="youtube2-([^"]+)"', text):
        hits.append((m.start(), f"youtube:{m.group(1)}"))
    for m in re.finditer(r"instagram\.com/p/([^/?&<\"']+)", text):
        hits.append((m.start(), f"instagram:{m.group(1)}"))
    for m in re.finditer(r"%%(?:share_url|checkout_url)%%", text):
        hits.append((m.start(), f"button:{m.group(0)}"))
    hits.sort(key=lambda row: row[0])
    seen: set[str] = set()
    ordered: list[str] = []
    for _, marker in hits:
        if marker not in seen:
            seen.add(marker)
            ordered.append(marker)
    return ordered


def apply_operations(text: str, operations: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    out = text
    audit: list[dict[str, Any]] = []
    for op in operations:
        op_id = str(op["id"])
        kind = op["kind"]
        if kind == "replace":
            needle = op["old"]
            count = out.count(needle)
            if count != 1:
                raise ValueError(f"{op_id}: expected exactly one anchor match, found {count}")
            out = out.replace(needle, op["new"], 1)
        elif kind in {"insert_after", "insert_before"}:
            needle = op["anchor"]
            count = out.count(needle)
            if count != 1:
                raise ValueError(f"{op_id}: expected exactly one anchor match, found {count}")
            replacement = needle + op["html"] if kind == "insert_after" else op["html"] + needle
            out = out.replace(needle, replacement, 1)
        else:
            raise ValueError(f"{op_id}: unsupported operation kind {kind!r}")
        audit.append({"id": op_id, "kind": kind, "matches": 1})
    return out, audit


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply fail-closed repairs to raw Substack editor HTML.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--ops", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    raw = args.input.read_bytes()
    text = raw.decode("utf-8")
    if 'data-testid="editor"' not in text:
        raise SystemExit("input does not look like raw Substack editor HTML: data-testid=editor missing")
    spec = json.loads(args.ops.read_text(encoding="utf-8"))
    operations = spec["operations"] if isinstance(spec, dict) else spec

    native_before = extract_native_markers(text)
    repaired, op_audit = apply_operations(text, operations)
    native_after = extract_native_markers(repaired)
    if native_before != native_after:
        raise SystemExit("native Substack object marker sequence changed; refusing output")

    out_bytes = repaired.encode("utf-8")
    report = {
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "output_sha256": hashlib.sha256(out_bytes).hexdigest(),
        "source_bytes": len(raw),
        "output_bytes": len(out_bytes),
        "operations": op_audit,
        "native_markers": native_before,
        "native_marker_count": len(native_before),
        "native_markers_unchanged": True,
    }

    if args.audit:
        args.audit.parent.mkdir(parents=True, exist_ok=True)
        args.audit.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not args.check:
        if args.output is None:
            raise SystemExit("--output is required unless --check is used")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(out_bytes)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
