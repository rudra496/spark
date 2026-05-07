from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path

from spark import __version__
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
            err = io.StringIO()
            code = run(["validate", "--root", str(root), "--json"], stdout=out, stderr=err)
            payload = json.loads(out.getvalue())
            self.assertEqual(code, 0)
            self.assertTrue(payload["valid"])

    def test_validate_failure_exit_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["validate", "--root", temp_dir], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 1)
            self.assertIn("missing required files", out.getvalue().lower())

    def test_validate_locale_spanish(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            run(
                ["validate", "--root", temp_dir, "--locale", "es"],
                stdout=out,
                stderr=io.StringIO(),
            )
            self.assertIn("faltan", out.getvalue().lower())
    def test_discover_returns_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["discover", "--root", temp_dir], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 0)
            payload = json.loads(out.getvalue())
            self.assertEqual(Path(payload["root"]), Path(temp_dir).resolve())
            self.assertIn("has_license", payload)
            self.assertIn("test_count", payload)

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

    def test_scaffold_empty_name_returns_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            err = io.StringIO()
            code = run(
                ["scaffold", "--root", temp_dir, "--name", "", "--description", "valid"],
                stdout=io.StringIO(),
                stderr=err,
            )
            self.assertEqual(code, 1)
            self.assertIn("Error", err.getvalue())

    def test_assess_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["assess", "--root", temp_dir, "--json"], stdout=out, stderr=io.StringIO())
            payload = json.loads(out.getvalue())
            self.assertEqual(code, 0)
            self.assertIn("score", payload)
            self.assertIn("recommendations", payload)

    def test_locales_lists_supported_locales(self) -> None:
        out = io.StringIO()
        code = run(["locales"], stdout=out, stderr=io.StringIO())
        payload = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertIn("en", payload["locales"])
        self.assertIn("fr", payload["locales"])

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

    def test_integration_links_rejects_blank_inputs(self) -> None:
        err = io.StringIO()
        code = run(
            ["integration-links", "--owner", " ", "--repo", "spark"],
            stdout=io.StringIO(),
            stderr=err,
        )
        self.assertEqual(code, 1)
        self.assertIn("Error:", err.getvalue())

    def test_version_command(self) -> None:
        out = io.StringIO()
        code = run(["version"], stdout=out, stderr=io.StringIO())
        self.assertEqual(code, 0)
        self.assertIn(__version__, out.getvalue())
        self.assertIn("spark", out.getvalue())

    def test_health_healthy_repo(self) -> None:
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
                ".github/workflows/ci.yml",
            ):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("ok", encoding="utf-8")
            out = io.StringIO()
            code = run(["health", "--root", str(root), "--json"], stdout=out, stderr=io.StringIO())
            payload = json.loads(out.getvalue())
            self.assertEqual(code, 0)
            self.assertTrue(payload["healthy"])
            self.assertTrue(payload["has_workflows"])

    def test_health_healthy_repo_with_yaml_workflow(self) -> None:
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
                ".github/workflows/ci.yaml",
            ):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("ok", encoding="utf-8")
            out = io.StringIO()
            code = run(["health", "--root", str(root), "--json"], stdout=out, stderr=io.StringIO())
            payload = json.loads(out.getvalue())
            self.assertEqual(code, 0)
            self.assertTrue(payload["healthy"])

    def test_health_unhealthy_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["health", "--root", temp_dir], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 1)
            self.assertIn("Unhealthy", out.getvalue())

    def test_no_command_returns_help(self) -> None:
        err = io.StringIO()
        code = run([], stdout=io.StringIO(), stderr=err)
        self.assertEqual(code, 2)

    def test_init_creates_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            out = io.StringIO()
            code = run(["init", "--root", str(root)], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 0)
            self.assertIn("Created", out.getvalue())
            self.assertTrue((root / "README.md").exists())

    def test_init_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["init", "--root", temp_dir, "--json"], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 0)
            payload = json.loads(out.getvalue())
            self.assertIn("created", payload)
            self.assertGreater(payload["count"], 0)

    def test_init_no_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            # Create ALL required files
            from spark.core import DEFAULT_REQUIRED_PATHS
            for rel in DEFAULT_REQUIRED_PATHS:
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("ok", encoding="utf-8")
            out = io.StringIO()
            code = run(["init", "--root", str(root)], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 0)
            self.assertIn("already present", out.getvalue())

    def test_report_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["report", "--root", temp_dir], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 0)
            self.assertIn("# Spark Assessment", out.getvalue())

    def test_report_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(
                ["report", "--root", temp_dir, "--format", "json"],
                stdout=out, stderr=io.StringIO(),
            )
            self.assertEqual(code, 0)
            payload = json.loads(out.getvalue())
            self.assertIn("score", payload)
            self.assertIn("grade", payload)

    def test_assess_shows_grade(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["assess", "--root", temp_dir], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 0)
            output = out.getvalue()
            self.assertRegex(output, r"\d+/100 \([A-F][\+]?\)")

    def test_assess_json_includes_category_scores(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out = io.StringIO()
            code = run(["assess", "--root", temp_dir, "--json"], stdout=out, stderr=io.StringIO())
            self.assertEqual(code, 0)
            payload = json.loads(out.getvalue())
            self.assertIn("category_scores", payload)
            self.assertIn("grade", payload)


if __name__ == "__main__":
    unittest.main()
