"""Command-line interface for Spark."""

from __future__ import annotations

import argparse
import json
import sys
from typing import TextIO

from ._version import __version__
from .core import SparkProject, scaffold_manifest
from .i18n import available_locales, translate
from .integrations import github_links_integration


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spark", description="Spark project toolkit CLI")
    subparsers = parser.add_subparsers(dest="command")

    validate = subparsers.add_parser("validate", help="Validate repository structure")
    validate.add_argument("--root", default=".", help="Repository root path")
    validate.add_argument("--json", action="store_true", help="Emit JSON output")
    validate.add_argument("--locale", default="en", help="Output locale (e.g. en, es, fr)")

    discover = subparsers.add_parser("discover", help="Discover repository metadata")
    discover.add_argument("--root", default=".", help="Repository root path")

    assess = subparsers.add_parser("assess", help="Assess repository maturity and next actions")
    assess.add_argument("--root", default=".", help="Repository root path")
    assess.add_argument("--json", action="store_true", help="Emit JSON output")

    scaffold = subparsers.add_parser("scaffold", help="Create spark.json manifest")
    scaffold.add_argument("--root", default=".", help="Target root path")
    scaffold.add_argument("--name", required=True, help="Project name")
    scaffold.add_argument("--description", required=True, help="Project description")
    scaffold.add_argument("--version", default="0.1.0", help="Manifest version")

    subparsers.add_parser("locales", help="List available locales")

    links = subparsers.add_parser("integration-links", help="Generate GitHub links")
    links.add_argument("--owner", required=True, help="GitHub owner")
    links.add_argument("--repo", required=True, help="GitHub repository")

    subparsers.add_parser("version", help="Print the installed Spark version")

    health = subparsers.add_parser("health", help="Quick health check (exit 0 = healthy)")
    health.add_argument("--root", default=".", help="Repository root path")
    health.add_argument("--json", action="store_true", help="Emit JSON output")

    return parser


def run(
    argv: list[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = stdout or sys.stdout
    err = stderr or sys.stderr
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        project = SparkProject(args.root)
        report = project.validate()
        payload = {
            "valid": report.is_valid,
            "missing": list(report.missing_paths),
            "root": str(report.root),
        }
        if args.json:
            out.write(json.dumps(payload) + "\n")
        else:
            key = "validation_ok" if report.is_valid else "validation_failed"
            out.write(translate(key, locale=args.locale) + "\n")
            if report.missing_paths:
                out.write("Missing:\n")
                for path in report.missing_paths:
                    out.write(f"- {path}\n")
        return 0 if report.is_valid else 1

    if args.command == "discover":
        project = SparkProject(args.root)
        out.write(json.dumps(project.discover()) + "\n")
        return 0

    if args.command == "assess":
        project = SparkProject(args.root)
        assessment = project.assess()
        assess_payload = assessment.as_dict()
        if args.json:
            out.write(json.dumps(assess_payload) + "\n")
        else:
            out.write(f"Score: {assessment.score}/100\n")
            out.write(f"Summary: {assessment.summary}\n")
            if assessment.strengths:
                out.write("Strengths:\n")
                for item in assessment.strengths:
                    out.write(f"- {item}\n")
            if assessment.recommendations:
                out.write("Recommendations:\n")
                for item in assessment.recommendations:
                    out.write(f"- {item}\n")
        return 0

    if args.command == "scaffold":
        try:
            manifest = scaffold_manifest(
                args.root,
                name=args.name,
                description=args.description,
                version=args.version,
            )
        except ValueError as exc:
            err.write(f"Error: {exc}\n")
            return 1
        out.write(f"Created {manifest}\n")
        return 0

    if args.command == "locales":
        out.write(json.dumps({"locales": list(available_locales())}) + "\n")
        return 0

    if args.command == "integration-links":
        try:
            out.write(json.dumps(github_links_integration(args.owner, args.repo)) + "\n")
        except ValueError as exc:
            err.write(f"Error: {exc}\n")
            return 1
        return 0

    if args.command == "version":
        out.write(f"spark {__version__}\n")
        return 0

    if args.command == "health":
        project = SparkProject(args.root)
        validation = project.validate()
        discovery = project.discover()
        healthy = validation.is_valid and discovery["workflow_count"] > 0
        health_payload: dict[str, object] = {
            "healthy": healthy,
            "valid": validation.is_valid,
            "has_workflows": discovery["workflow_count"] > 0,
            "missing": list(validation.missing_paths),
        }
        if args.json:
            out.write(json.dumps(health_payload) + "\n")
        else:
            status = "✅ Healthy" if healthy else "⚠️  Unhealthy"
            out.write(f"{status}\n")
            if validation.missing_paths:
                out.write("Missing required files:\n")
                for path in validation.missing_paths:
                    out.write(f"- {path}\n")
            if not discovery["workflow_count"]:
                out.write("No CI workflows found.\n")
        return 0 if healthy else 1

    parser.print_help(err)
    return 2


def main() -> None:
    raise SystemExit(run())
