from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from spark.core import SparkProject, scaffold_manifest


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
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci", encoding="utf-8")
            payload = SparkProject(root).discover()
            self.assertEqual(payload["docs_count"], 1)
            self.assertEqual(payload["workflow_count"], 1)

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
                "examples/README.md",
                "examples/basic.md",
                "examples/advanced.md",
                ".github/workflows/ci.yml",
            ):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("ok", encoding="utf-8")
            report = SparkProject(root).assess()
            self.assertEqual(report.score, 100)
            self.assertEqual(report.recommendations, ())


if __name__ == "__main__":
    unittest.main()
