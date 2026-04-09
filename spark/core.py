"""Core primitives for Spark project validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .plugins import PluginManager

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


@dataclass(frozen=True)
class ValidationReport:
    """Validation output for a Spark project directory."""

    root: Path
    missing_paths: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return len(self.missing_paths) == 0


@dataclass(frozen=True)
class AssessmentReport:
    """High-level maturity assessment for a Spark-style repository."""

    root: Path
    score: int
    summary: str
    strengths: tuple[str, ...]
    recommendations: tuple[str, ...]
    missing_required_paths: tuple[str, ...]


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
        return {
            "root": str(self.root),
            "docs_count": len(list(docs_dir.glob("*.md"))) if docs_dir.exists() else 0,
            "example_count": len(list(examples_dir.iterdir())) if examples_dir.exists() else 0,
            "workflow_count": len(list(workflows_dir.glob("*.yml"))) if workflows_dir.exists() else 0,
        }

    def run_plugins(self, manager: PluginManager) -> dict[str, dict[str, Any]]:
        context = {"root": self.root}
        return manager.run(context)

    def assess(self) -> AssessmentReport:
        validation = self.validate()
        discovery = self.discover()
        score = 100
        strengths: list[str] = []
        recommendations: list[str] = []

        if validation.is_valid:
            strengths.append("All required foundation files are present.")
        else:
            score -= min(40, len(validation.missing_paths) * 4)
            recommendations.append("Add missing required foundation files.")

        if discovery["workflow_count"] > 0:
            strengths.append("Automation workflows are configured.")
        else:
            score -= 20
            recommendations.append("Add CI workflow automation in .github/workflows.")

        if discovery["docs_count"] >= 5:
            strengths.append("Documentation depth is solid.")
        else:
            score -= 20
            recommendations.append("Expand docs coverage (architecture, API, FAQ, guides).")

        if discovery["example_count"] >= 3:
            strengths.append("Example coverage helps adoption.")
        else:
            score -= 20
            recommendations.append("Add more runnable examples for common use-cases.")

        score = max(0, min(100, score))
        if score >= 90:
            summary = "Excellent repository foundation."
        elif score >= 75:
            summary = "Strong repository foundation with room to improve."
        elif score >= 50:
            summary = "Moderate repository maturity; prioritize improvements."
        else:
            summary = "Early-stage repository foundation; major improvements needed."

        return AssessmentReport(
            root=self.root,
            score=score,
            summary=summary,
            strengths=tuple(strengths),
            recommendations=tuple(recommendations),
            missing_required_paths=validation.missing_paths,
        )


def scaffold_manifest(
    root: str | Path,
    *,
    name: str,
    description: str,
    version: str = "0.1.0",
) -> Path:
    """Create or replace a Spark manifest file and return its path."""
    root_path = Path(root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    manifest_path = root_path / "spark.json"
    payload = {"name": name, "description": description, "version": version}
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return manifest_path
