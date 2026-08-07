"""Core primitives for Spark project validation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .plugins import PluginManager

RUNNABLE_EXAMPLE_SUFFIXES = {".py", ".sh", ".js", ".ts", ".go", ".rs"}

DEFAULT_REQUIRED_PATHS = (
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
)

# Files that indicate good CI practices
QUALITY_CI_FILES = (
    ".github/workflows/ci.yml",
    ".github/workflows/test.yml",
    ".github/workflows/lint.yml",
)

# Files that indicate good issue/PR workflow
COMMUNITY_FILES = (
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
)

# Files that indicate professional release process
RELEASE_FILES = (
    ".github/workflows/release.yml",
    "pyproject.toml",
    "setup.py",
    "package.json",
    "Cargo.toml",
)


class SparkValidationError(ValueError):
    """Raised when Spark detects an unrecoverable configuration problem."""


@dataclass(frozen=True)
class ValidationReport:
    """Validation output for a Spark project directory."""

    root: Path
    missing_paths: tuple[str, ...]
    extra_paths: tuple[str, ...] = ()

    @property
    def is_valid(self) -> bool:
        return len(self.missing_paths) == 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "root": str(self.root),
            "valid": self.is_valid,
            "missing": list(self.missing_paths),
            "total_required": len(DEFAULT_REQUIRED_PATHS),
            "present": len(DEFAULT_REQUIRED_PATHS) - len(self.missing_paths),
        }


@dataclass(frozen=True)
class AssessmentReport:
    """High-level maturity assessment for a Spark-style repository."""

    root: Path
    score: int
    grade: str
    summary: str
    strengths: tuple[str, ...]
    recommendations: tuple[str, ...]
    warnings: tuple[str, ...]
    missing_required_paths: tuple[str, ...]
    category_scores: dict[str, int] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "root": str(self.root),
            "score": self.score,
            "grade": self.grade,
            "summary": self.summary,
            "strengths": list(self.strengths),
            "recommendations": list(self.recommendations),
            "warnings": list(self.warnings),
            "missing_required_paths": list(self.missing_required_paths),
            "category_scores": self.category_scores,
        }


class SparkProject:
    """Represents a Spark-style repository on disk."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()

    def validate(self, required_paths: tuple[str, ...] | None = None) -> ValidationReport:
        required = required_paths or DEFAULT_REQUIRED_PATHS
        missing = tuple(path for path in required if not (self.root / path).exists())
        return ValidationReport(root=self.root, missing_paths=missing)

    def discover(self) -> dict[str, Any]:
        docs_dir = self.root / "docs"
        examples_dir = self.root / "examples"
        workflows_dir = self.root / ".github" / "workflows"
        tests_dir = self.root / "tests"

        license_file: str | None = None
        for candidate in ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE.rst"):
            if (self.root / candidate).exists():
                license_file = candidate
                break

        test_count = len(list(tests_dir.glob("test_*.py"))) if tests_dir.exists() else 0

        language: str | None = None
        if (self.root / "pyproject.toml").exists() or (self.root / "setup.py").exists():
            language = "python"
        elif (self.root / "package.json").exists():
            language = "javascript"
        elif (self.root / "go.mod").exists():
            language = "go"
        elif (self.root / "Cargo.toml").exists():
            language = "rust"

        runnable_examples = 0
        if examples_dir.exists():
            for path in examples_dir.rglob("*"):
                if not path.is_file():
                    continue
                if path.name.lower().startswith("readme"):
                    continue
                if path.suffix in RUNNABLE_EXAMPLE_SUFFIXES:
                    runnable_examples += 1

        workflow_count = 0
        if workflows_dir.exists():
            workflow_count = len(list(workflows_dir.glob("*.yml"))) + len(
                list(workflows_dir.glob("*.yaml"))
            )

        # Detect dependency management
        has_lock_file = False
        if language == "python":
            has_lock_file = (self.root / "poetry.lock").exists() or (
                self.root / "requirements-lock.txt"
            ).exists()
        elif language == "javascript":
            has_lock_file = (self.root / "package-lock.json").exists() or (
                self.root / "yarn.lock"
            ).exists()
        elif language == "go":
            has_lock_file = (self.root / "go.sum").exists()
        elif language == "rust":
            has_lock_file = (self.root / "Cargo.lock").exists()

        # Detect CI quality
        has_ci_quality = any((self.root / f).exists() for f in QUALITY_CI_FILES)

        # Detect community files
        community_count = sum(1 for f in COMMUNITY_FILES if (self.root / f).exists())

        # Detect release process
        has_release_workflow = (self.root / ".github/workflows/release.yml").exists()

        # Detect issue templates
        issue_dir = self.root / ".github" / "ISSUE_TEMPLATE"
        issue_templates = len(list(issue_dir.glob("*.md"))) if issue_dir.exists() else 0

        # Detect badges in README
        readme = self.root / "README.md"
        has_badges = False
        if readme.exists():
            content = readme.read_text(encoding="utf-8", errors="ignore")
            has_badges = (
                bool(re.search(r"https?://(?:[a-zA-Z0-9-]+\.)*shields\.io[/\s\"'\)]", content))
                or "![Build" in content
                or "![CI" in content
            )

        # Detect .gitignore
        has_gitignore = (self.root / ".gitignore").exists()

        # Detect FUNDING.yml
        has_funding = (self.root / ".github" / "FUNDING.yml").exists()

        # Detect dependabot
        has_dependabot = (self.root / ".github" / "dependabot.yml").exists()

        return {
            "root": str(self.root),
            "docs_count": len(list(docs_dir.glob("*.md"))) if docs_dir.exists() else 0,
            "example_count": runnable_examples,
            "workflow_count": workflow_count,
            "has_license": license_file is not None,
            "license_file": license_file,
            "test_count": test_count,
            "language": language,
            "has_lock_file": has_lock_file,
            "has_ci_quality": has_ci_quality,
            "community_files": community_count,
            "has_release_workflow": has_release_workflow,
            "issue_templates": issue_templates,
            "has_badges": has_badges,
            "has_gitignore": has_gitignore,
            "has_funding": has_funding,
            "has_dependabot": has_dependabot,
        }

    def run_plugins(self, manager: PluginManager) -> dict[str, dict[str, Any]]:
        context = {"root": self.root}
        return manager.run(context)

    def assess(self) -> AssessmentReport:
        validation = self.validate()
        discovery = self.discover()
        category_scores: dict[str, int] = {}
        strengths: list[str] = []
        recommendations: list[str] = []
        warnings: list[str] = []

        # Category 1: Foundation Files (max 25 points)
        foundation_score = 25
        if validation.is_valid:
            strengths.append("All required foundation files are present.")
        else:
            missing_count = len(validation.missing_paths)
            foundation_score -= min(25, missing_count * 3)
            recommendations.append(f"Add {missing_count} missing required foundation files.")
            if missing_count > 5:
                warnings.append(
                    f"{missing_count} missing files — repository lacks basic structure."
                )

        category_scores["foundation"] = foundation_score

        # Category 2: Automation (max 20 points)
        automation_score = 0
        if discovery["workflow_count"] > 0:
            automation_score += 8
            strengths.append("CI workflows are configured.")
        else:
            recommendations.append("Add CI workflows in .github/workflows/.")

        if discovery["has_ci_quality"]:
            automation_score += 5
            strengths.append("Quality-focused CI (lint/test) detected.")

        if discovery["has_release_workflow"]:
            automation_score += 4
            strengths.append("Release automation is configured.")

        if discovery["has_dependabot"]:
            automation_score += 3
            strengths.append("Automated dependency updates configured.")

        category_scores["automation"] = automation_score

        # Category 3: Documentation (max 20 points)
        docs_score = 0
        if discovery["docs_count"] >= 8:
            docs_score += 10
            strengths.append("Excellent documentation depth.")
        elif discovery["docs_count"] >= 5:
            docs_score += 8
            strengths.append("Solid documentation coverage.")
        elif discovery["docs_count"] >= 2:
            docs_score += 5
        else:
            recommendations.append("Expand documentation (architecture, API, FAQ, guides).")

        if discovery["has_badges"]:
            docs_score += 5
            strengths.append("README badges present for quick status overview.")
        else:
            recommendations.append("Add badges to README (CI, license, version).")

        if discovery["example_count"] >= 3:
            docs_score += 5
            strengths.append("Runnable examples help adoption.")
        elif discovery["example_count"] >= 1:
            docs_score += 3
            recommendations.append("Add more runnable examples for common use-cases.")
        else:
            docs_score += 0
            recommendations.append("Add runnable examples to demonstrate usage.")

        category_scores["documentation"] = docs_score

        # Category 4: Testing (max 15 points)
        test_score = 0
        if discovery["test_count"] >= 20:
            test_score += 10
            strengths.append(f"Comprehensive test suite ({discovery['test_count']} tests).")
        elif discovery["test_count"] >= 10:
            test_score += 8
            strengths.append(f"Good test coverage ({discovery['test_count']} tests).")
        elif discovery["test_count"] >= 3:
            test_score += 8
            strengths.append(f"Tests present ({discovery['test_count']} tests).")
        elif discovery["test_count"] > 0:
            test_score += 3
            recommendations.append("Add more tests to improve reliability.")
        else:
            recommendations.append("Add automated tests.")

        category_scores["testing"] = test_score

        # Category 5: Project Hygiene (max 20 points)
        hygiene_score = 0
        if discovery["has_license"]:
            hygiene_score += 5
            strengths.append("Repository is properly licensed.")
        else:
            recommendations.append("Add a LICENSE file.")

        if discovery["has_lock_file"]:
            hygiene_score += 5
            strengths.append("Dependency lock file ensures reproducible installs.")

        if discovery["has_gitignore"]:
            hygiene_score += 3
        else:
            recommendations.append("Add a .gitignore file.")

        if discovery["community_files"] >= 3:
            hygiene_score += 3
            strengths.append("Community templates (issues/PR) help contributors.")
        elif discovery["community_files"] >= 1:
            hygiene_score += 2
            recommendations.append("Add PR template and more issue templates.")

        if discovery["issue_templates"] >= 2:
            hygiene_score += 2
        elif discovery["issue_templates"] >= 1:
            hygiene_score += 1
            recommendations.append("Add more issue templates (bug report, feature request).")

        if discovery["has_funding"]:
            hygiene_score += 2
            strengths.append("Funding link available for supporters.")

        category_scores["hygiene"] = hygiene_score

        # Calculate total
        score = sum(category_scores.values())
        score = max(0, min(100, score))

        # Grade
        if score >= 90:
            grade = "A"
            summary = "Excellent repository foundation — well-structured and contributor-ready."
        elif score >= 80:
            grade = "B+"
            summary = "Strong foundation with a few improvements needed."
        elif score >= 70:
            grade = "B"
            summary = "Solid foundation. Focus on the flagged areas to improve."
        elif score >= 55:
            grade = "C"
            summary = "Moderate maturity. Several improvements recommended."
        elif score >= 40:
            grade = "D"
            summary = "Early-stage foundation. Significant improvements needed."
        else:
            grade = "F"
            summary = "Foundation needs major work before it's contributor-ready."
            warnings.append("Repository score is very low — prioritize the recommendations above.")

        return AssessmentReport(
            root=self.root,
            score=score,
            grade=grade,
            summary=summary,
            strengths=tuple(strengths),
            recommendations=tuple(recommendations),
            warnings=tuple(warnings),
            missing_required_paths=validation.missing_paths,
            category_scores=category_scores,
        )

    def badge_urls(self, owner: str, repo: str) -> dict[str, str]:
        return {
            "ci": f"https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg",
            "license": "https://img.shields.io/badge/License-MIT-yellow.svg",
            "python": "https://img.shields.io/pypi/pyversions/spark-toolkit",
            "prs": "https://img.shields.io/badge/PRs-welcome-brightgreen.svg",
            "docs": "https://img.shields.io/badge/docs-live-blue?logo=readthedocs",
        }

    def generate_report(self, format: str = "markdown") -> str:
        """Generate a human-readable assessment report."""
        assessment = self.assess()
        discovery = self.discover()

        if format == "markdown":
            lines = [
                f"# Spark Assessment: {self.root.name}",
                "",
                f"**Score:** {assessment.score}/100 ({assessment.grade})",
                f"**Summary:** {assessment.summary}",
                "",
                "## Category Scores",
                "",
            ]
            for cat, score in assessment.category_scores.items():
                bar = "#" * score + "-" * (25 - score)
                lines.append(f"| {cat.capitalize():20s} | {bar} {score}/25 |")

            if assessment.strengths:
                lines.append("")
                lines.append("## Strengths")
                for s in assessment.strengths:
                    lines.append(f"- {s}")

            if assessment.recommendations:
                lines.append("")
                lines.append("## Recommendations")
                for r in assessment.recommendations:
                    lines.append(f"- {r}")

            if assessment.warnings:
                lines.append("")
                lines.append("## Warnings")
                for w in assessment.warnings:
                    lines.append(f"> {w}")

            lines.append("")
            lines.append("## Discovery")
            lines.append("")
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            for key, value in discovery.items():
                if key == "root":
                    continue
                lines.append(f"| {key} | {value} |")

            return "\n".join(lines)

        return assessment.as_dict().__str__()


def scaffold_manifest(
    root: str | Path,
    *,
    name: str,
    description: str,
    version: str = "0.1.0",
) -> Path:
    if not name or not name.strip():
        raise SparkValidationError("Project name must not be empty.")
    if not description or not description.strip():
        raise SparkValidationError("Project description must not be empty.")

    root_path = Path(root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    manifest_path = root_path / "spark.json"
    payload = {"name": name.strip(), "description": description.strip(), "version": version}
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def scaffold_missing(root: str | Path, required_paths: tuple[str, ...] | None = None) -> list[str]:
    """Create missing required files with templates. Returns list of created files."""
    root_path = Path(root).resolve()
    required = required_paths or DEFAULT_REQUIRED_PATHS
    created = []

    for path in required:
        full_path = root_path / path
        if full_path.exists():
            continue
        full_path.parent.mkdir(parents=True, exist_ok=True)

        _name = root_path.name
        templates: dict[str, str] = {
            "README.md": f"# {_name}\n\nTODO: Add project description.\n",
            "CONTRIBUTING.md": (
                "# Contributing\n\n"
                "Thank you for your interest! Please see the guidelines below.\n\n"
                "## Setup\n\n"
                "```bash\ngit clone <repo-url>\n"
                f"cd {_name}\npip install -e .\n```\n\n"
                "## Development\n\n"
                "1. Create a branch\n2. Make your changes\n"
                "3. Add tests\n4. Open a PR\n"
            ),
            "CODE_OF_CONDUCT.md": (
                "# Code of Conduct\n\n"
                "Be respectful, constructive, and inclusive.\n"
            ),
            "SECURITY.md": (
                "# Security\n\n"
                "Report vulnerabilities via "
                "[GitHub Security Advisories](../../security/advisories/new).\n"
            ),
            "SUPPORT.md": (
                "# Support\n\n## Getting Help\n\n"
                "- Open a [GitHub Discussion](../../discussions)\n"
                "- Check the [FAQ](docs/FAQ.md)\n\n"
                "## Reporting Bugs\n\n"
                "- Open a [GitHub Issue](../../issues) with reproduction steps\n"
            ),
            "CHANGELOG.md": (
                "# Changelog\n\n"
                "All notable changes to this project will be documented in this file.\n\n"
                "## [Unreleased]\n\n- Initial project setup\n"
            ),
            "ROADMAP.md": (
                "# Roadmap\n\n## Current Focus\n\n"
                "- [ ] Core features\n- [ ] Documentation\n- [ ] Tests\n\n"
                "## Future\n\n- [ ] Plugin system\n- [ ] CI/CD improvements\n"
            ),
            "docs/ARCHITECTURE.md": "# Architecture\n\nTODO: Describe system architecture.\n",
            "docs/FAQ.md": (
                "# FAQ\n\n## General\n\n"
                "**Q: How do I install?**\nA: `pip install .`\n\n"
                "**Q: How do I contribute?**\n"
                "A: See [CONTRIBUTING.md](../CONTRIBUTING.md)\n"
            ),
            "docs/SHOWCASE.md": (
                "# Showcase\n\nProjects using this tool:\n\n"
                "- [Your project here]\n"
            ),
            "examples/README.md": (
                "# Examples\n\nBasic usage examples:\n\n"
                "```python\n# TODO: Add example\n```\n"
            ),
        }

        content = templates.get(path, f"# {path}\n\nTODO: Add content.\n")
        full_path.write_text(content, encoding="utf-8")
        created.append(path)

    return created
