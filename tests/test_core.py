from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from spark.core import SparkProject, SparkValidationError, scaffold_manifest, scaffold_missing


class SparkProjectTests(unittest.TestCase):
    def test_validate_returns_missing_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("ok", encoding="utf-8")
            project = SparkProject(root)
            report = project.validate(required_paths=("README.md", "docs/ARCHITECTURE.md"))
            self.assertFalse(report.is_valid)
            self.assertEqual(report.missing_paths, ("docs/ARCHITECTURE.md",))

    def test_discover_counts_existing_areas(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir(parents=True)
            (root / "examples").mkdir(parents=True)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "docs" / "ARCHITECTURE.md").write_text("doc", encoding="utf-8")
            (root / "examples" / "README.md").write_text("example", encoding="utf-8")
            (root / "examples" / "demo.py").write_text("print('ok')", encoding="utf-8")
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci", encoding="utf-8")
            payload = SparkProject(root).discover()
            self.assertEqual(payload["docs_count"], 1)
            self.assertEqual(payload["example_count"], 1)
            self.assertEqual(payload["workflow_count"], 1)

    def test_discover_counts_yaml_workflows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yaml").write_text("name: ci", encoding="utf-8")
            payload = SparkProject(root).discover()
            self.assertEqual(payload["workflow_count"], 1)

    def test_discover_counts_only_runnable_examples(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "examples" / "basic").mkdir(parents=True)
            (root / "examples" / "README.md").write_text("guide", encoding="utf-8")
            (root / "examples" / "basic" / "example.py").write_text("print('ok')", encoding="utf-8")
            (root / "examples" / "basic" / "notes.md").write_text("not runnable", encoding="utf-8")
            payload = SparkProject(root).discover()
            self.assertEqual(payload["example_count"], 1)

    def test_discover_detects_license_and_tests(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "LICENSE").write_text("MIT", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_main.py").write_text("# test", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]", encoding="utf-8")
            payload = SparkProject(root).discover()
            self.assertTrue(payload["has_license"])
            self.assertEqual(payload["license_file"], "LICENSE")
            self.assertEqual(payload["test_count"], 1)
            self.assertEqual(payload["language"], "python")

    def test_discover_no_license(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = SparkProject(temp_dir).discover()
            self.assertFalse(payload["has_license"])
            self.assertIsNone(payload["license_file"])
            self.assertEqual(payload["test_count"], 0)

    def test_scaffold_manifest_writes_expected_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = scaffold_manifest(
                temp_dir,
                name="demo",
                description="demo project",
                version="0.2.0",
            )
            self.assertTrue(manifest.exists())
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["name"], "demo")
            self.assertEqual(payload["version"], "0.2.0")

    def test_scaffold_manifest_rejects_empty_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(SparkValidationError):
                scaffold_manifest(temp_dir, name="", description="valid desc")

    def test_scaffold_manifest_rejects_empty_description(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(SparkValidationError):
                scaffold_manifest(temp_dir, name="valid", description="   ")

    def test_scaffold_manifest_strips_whitespace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = scaffold_manifest(
                temp_dir,
                name="  trimmed  ",
                description="  cleaned  ",
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["name"], "trimmed")
            self.assertEqual(payload["description"], "cleaned")

    def test_validation_report_as_dict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("ok", encoding="utf-8")
            report = SparkProject(root).validate(required_paths=("README.md", "MISSING.md"))
            d = report.as_dict()
            self.assertFalse(d["valid"])
            self.assertIn("MISSING.md", d["missing"])
            self.assertEqual(d["root"], str(root))

    def test_assessment_report_as_dict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = SparkProject(temp_dir).assess()
            d = report.as_dict()
            self.assertIn("score", d)
            self.assertIn("summary", d)
            self.assertIn("strengths", d)
            self.assertIn("recommendations", d)
            self.assertIn("missing_required_paths", d)
            self.assertIsInstance(d["strengths"], list)

    def test_badge_urls_returns_expected_keys(self) -> None:
        project = SparkProject(".")
        badges = project.badge_urls("rudra496", "spark")
        self.assertIn("ci", badges)
        self.assertIn("license", badges)
        self.assertIn("docs", badges)
        self.assertIn("rudra496/spark", badges["ci"])

    def test_assess_reports_recommendations_for_sparse_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("ok", encoding="utf-8")
            report = SparkProject(root).assess()
            self.assertLess(report.score, 100)
            self.assertGreater(len(report.recommendations), 0)
            self.assertIn("CONTRIBUTING.md", report.missing_required_paths)

    def test_assess_reports_excellent_for_complete_repo(self) -> None:
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
                "docs/API.md",
                "docs/I18N.md",
                "docs/INNOVATION.md",
                "docs/BENCHMARKS.md",
                "docs/GETTING-STARTED.md",
                "examples/README.md",
                "examples/basic.py",
                "examples/advanced.py",
                "examples/integrations.py",
                ".github/workflows/ci.yml",
                ".github/workflows/test.yml",
                ".github/workflows/release.yml",
                ".github/dependabot.yml",
                ".github/ISSUE_TEMPLATE/bug_report.md",
                ".github/ISSUE_TEMPLATE/feature_request.md",
                ".github/PULL_REQUEST_TEMPLATE.md",
                ".github/FUNDING.yml",
                "LICENSE",
                "poetry.lock",
                "tests/test_core.py",
                "tests/test_cli.py",
                "tests/test_plugins.py",
                ".gitignore",
                "pyproject.toml",
            ):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                content = "ok"
                if rel == "README.md":
                    content = "# Test\n\n![CI](https://img.shields.io/badge/test-passing-brightgreen)\n"
                target.write_text(content, encoding="utf-8")
            report = SparkProject(root).assess()
            self.assertGreaterEqual(report.score, 90)
            self.assertEqual(report.grade, "A")

    def test_assess_includes_category_scores(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = SparkProject(temp_dir).assess()
            d = report.as_dict()
            self.assertIn("category_scores", d)
            self.assertIn("foundation", d["category_scores"])
            self.assertIn("automation", d["category_scores"])
            self.assertIn("documentation", d["category_scores"])
            self.assertIn("testing", d["category_scores"])
            self.assertIn("hygiene", d["category_scores"])

    def test_assess_includes_grade(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = SparkProject(temp_dir).assess()
            self.assertIn(report.grade, ("A", "B+", "B", "C", "D", "F"))

    def test_assess_includes_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = SparkProject(temp_dir).assess()
            self.assertIsInstance(report.warnings, tuple)

    def test_scaffold_missing_creates_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            created = scaffold_missing(root, required_paths=("README.md", "SECURITY.md"))
            self.assertEqual(len(created), 2)
            self.assertTrue((root / "README.md").exists())
            self.assertTrue((root / "SECURITY.md").exists())

    def test_scaffold_missing_skips_existing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("exists", encoding="utf-8")
            created = scaffold_missing(root, required_paths=("README.md", "SECURITY.md"))
            self.assertEqual(len(created), 1)
            self.assertFalse("README.md" in created)
            self.assertTrue((root / "README.md").read_text() == "exists")

    def test_scaffold_missing_creates_nested_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            created = scaffold_missing(root, required_paths=("docs/ARCHITECTURE.md",))
            self.assertEqual(len(created), 1)
            self.assertTrue((root / "docs" / "ARCHITECTURE.md").exists())

    def test_generate_report_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report = SparkProject(temp_dir).generate_report(format="markdown")
            self.assertIn("# Spark Assessment", report)
            self.assertIn("Score:", report)
            self.assertIn("Category Scores", report)

    def test_discover_detects_badges(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            badge = "![CI](https://img.shields.io/badge/test-badge)"
            (root / "README.md").write_text(badge, encoding="utf-8")
            payload = SparkProject(root).discover()
            self.assertTrue(payload["has_badges"])

    def test_discover_detects_no_badges(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = SparkProject(temp_dir).discover()
            self.assertFalse(payload["has_badges"])

    def test_discover_detects_lock_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "pyproject.toml").write_text("[project]", encoding="utf-8")
            (root / "poetry.lock").write_text("{}", encoding="utf-8")
            payload = SparkProject(root).discover()
            self.assertTrue(payload["has_lock_file"])

    def test_discover_detects_dependabot(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            github_dir = root / ".github"
            github_dir.mkdir(exist_ok=True)
            (github_dir / "dependabot.yml").write_text("{}", encoding="utf-8")
            payload = SparkProject(root).discover()
            self.assertTrue(payload["has_dependabot"])


if __name__ == "__main__":
    unittest.main()
