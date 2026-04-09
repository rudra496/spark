from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

from spark.cli import run


class CLITests(unittest.TestCase):
    def test_validate_json_success(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for rel in (
                "README.md",
                "CONTRIBUTING.md",
                "CODE_OF_CONDUCT.md",
                "SECURITY.md",
                "SUPPORT.md",
                "CHANGELOG.md",
                "ROADMAP.md",
                "docs/ARCHITECTURE.md",
                "docs/FAQ.md",
                "docs/SHOWCASE.md",
                "examples/README.md",
            ):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("ok", encoding="utf-8")
            out = io.StringIO()
            code = run(["validate", "--root", str(root), "--json"], stdout=out, stderr=io.StringIO())
            payload = json.loads(out.getvalue())
            self.assertEqual(code, 0)
            self.assertTrue(payload["valid"])

    def test_validate_failure_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["validate", "--root", temp_dir], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 1)
            self.assertIn("missing required files", out.getvalue().lower())

    def test_discover_returns_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["discover", "--root", temp_dir], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 0)
            payload = json.loads(out.getvalue())
            self.assertEqual(Path(payload["root"]), Path(temp_dir).resolve())

    def test_scaffold_creates_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(
                [
                    "scaffold",
                    "--root",
                    temp_dir,
                    "--name",
                    "demo",
                    "--description",
                    "demo repo",
                    "--version",
                    "1.0.0",
                ],
                stdout=out,
                stderr=io.StringIO(),
            )
            self.assertEqual(code, 0)
            self.assertTrue((Path(temp_dir) / "spark.json").exists())

    def test_locales_lists_supported_locales(self) -> None:
        out = io.StringIO()
        code = run(["locales"], stdout=out, stderr=io.StringIO())
        payload = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertIn("en", payload["locales"])

    def test_integration_links(self) -> None:
        out = io.StringIO()
        code = run(
            ["integration-links", "--owner", "rudra496", "--repo", "spark"],
            stdout=out,
            stderr=io.StringIO(),
        )
        payload = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(payload["issues"], "https://github.com/rudra496/spark/issues")


if __name__ == "__main__":
    unittest.main()
