import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_community_article_repair.py"
sys.path.insert(0, str(ROOT / "scripts"))

from apply_community_article_repair import apply_operations, extract_native_markers


class ApplyCommunityArticleRepairTests(unittest.TestCase):
    def test_applies_replace_and_insert_after_exactly_once(self):
        source = '<div data-testid="editor"><p>alpha</p><p>omega</p></div>'
        ops = [
            {"id": "R1", "kind": "replace", "old": "alpha", "new": "beta"},
            {"id": "R2", "kind": "insert_after", "anchor": "<p>omega</p>", "html": "<p>tail</p>"},
        ]
        repaired, audit = apply_operations(source, ops)
        self.assertEqual(repaired, '<div data-testid="editor"><p>beta</p><p>omega</p><p>tail</p></div>')
        self.assertEqual([row["id"] for row in audit], ["R1", "R2"])

    def test_rejects_missing_anchor(self):
        source = '<div data-testid="editor"><p>alpha</p></div>'
        with self.assertRaisesRegex(ValueError, "R1.*expected exactly one"):
            apply_operations(source, [{"id": "R1", "kind": "replace", "old": "missing", "new": "x"}])

    def test_rejects_duplicate_anchor(self):
        source = '<div data-testid="editor"><p>alpha</p><p>alpha</p></div>'
        with self.assertRaisesRegex(ValueError, "R1.*expected exactly one"):
            apply_operations(source, [{"id": "R1", "kind": "replace", "old": "alpha", "new": "x"}])

    def test_extracts_native_markers_in_stable_order(self):
        source = (
            'public/images/aaa.png public/images/aaa.png '
            '&quot;nodeId&quot;:&quot;node-1&quot; '
            'id="youtube2-abc123" '
            'https://instagram.com/p/xyz/ %%share_url%% %%checkout_url%%'
        )
        self.assertEqual(
            extract_native_markers(source),
            [
                "image:public/images/aaa.png",
                "digest:node-1",
                "youtube:abc123",
                "instagram:xyz",
                "button:%%share_url%%",
                "button:%%checkout_url%%",
            ],
        )

    def test_cli_writes_repaired_html_and_audit(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            source = td / "source.html"
            ops = td / "ops.json"
            output = td / "out.html"
            audit = td / "audit.json"
            source.write_text(
                '<div data-testid="editor">public/images/a.png<p>alpha</p>'
                '&quot;nodeId&quot;:&quot;n1&quot;</div>',
                encoding="utf-8",
            )
            ops.write_text(json.dumps({"operations": [
                {"id": "R1", "kind": "replace", "old": "alpha", "new": "beta"}
            ]}), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), "--ops", str(ops),
                 "--output", str(output), "--audit", str(audit)],
                text=True, capture_output=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("beta", output.read_text(encoding="utf-8"))
            report = json.loads(audit.read_text(encoding="utf-8"))
            self.assertTrue(report["native_markers_unchanged"])
            self.assertEqual(report["operations"][0]["id"], "R1")
            self.assertEqual(len(report["source_sha256"]), 64)
            self.assertEqual(len(report["output_sha256"]), 64)

    def test_cli_refuses_operation_that_changes_native_object_marker(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            source = td / "source.html"
            ops = td / "ops.json"
            output = td / "out.html"
            source.write_text(
                '<div data-testid="editor">&quot;nodeId&quot;:&quot;n1&quot;</div>',
                encoding="utf-8",
            )
            ops.write_text(json.dumps({"operations": [
                {"id": "R1", "kind": "replace", "old": "n1", "new": "n2"}
            ]}), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), "--ops", str(ops), "--output", str(output)],
                text=True, capture_output=True,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("native Substack object marker sequence changed", proc.stderr + proc.stdout)
            self.assertFalse(output.exists())

    def test_cli_check_mode_validates_without_writing_output(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            source = td / "source.html"
            ops = td / "ops.json"
            source.write_text('<div data-testid="editor"><p>alpha</p></div>', encoding="utf-8")
            ops.write_text(json.dumps({"operations": [
                {"id": "R1", "kind": "replace", "old": "alpha", "new": "beta"}
            ]}), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(source), "--ops", str(ops), "--check"],
                text=True, capture_output=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            self.assertEqual(report["operations"][0]["id"], "R1")


if __name__ == "__main__":
    unittest.main()
