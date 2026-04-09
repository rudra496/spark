"""Command-line interface for Spark."""

from __future__ import annotations

import argparse
import json
import sys
from typing import TextIO

from .core import SparkProject, scaffold_manifest
from .i18n import available_locales, translate
from .integrations import github_links_integration


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spark", description="Spark project toolkit CLI")
    subparsers = parser.add_subparsers(dest="command")

    validate = subparsers.add_parser("validate", help="Validate repository structure")
    validate.add_argument("--root", default=".", help="Repository root path")
    validate.add_argument("--json", action="store_true", help="Emit JSON output")

    discover = subparsers.add_parser("discover", help="Discover repository metadata")
    discover.add_argument("--root", default=".", help="Repository root path")

    scaffold = subparsers.add_parser("scaffold", help="Create spark.json manifest")
    scaffold.add_argument("--root", default=".", help="Target root path")
    scaffold.add_argument("--name", required=True, help="Project name")
    scaffold.add_argument("--description", required=True, help="Project description")
    scaffold.add_argument("--version", default="0.1.0", help="Manifest version")

    subparsers.add_parser("locales", help="List available locales")

    links = subparsers.add_parser("integration-links", help="Generate GitHub links")
    links.add_argument("--owner", required=True, help="GitHub owner")
    links.add_argument("--repo", required=True, help="GitHub repository")

    return parser


def run(argv: list[str] | None = None, *, stdout: TextIO | None = None, stderr: TextIO | None = None) -> int:
    out = stdout or sys.stdout
    err = stderr or sys.stderr
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        project = SparkProject(args.root)
        report = project.validate()
        payload = {"valid": report.is_valid, "missing": list(report.missing_paths), "root": str(report.root)}
        if args.json:
            out.write(json.dumps(payload) + "\n")
        else:
            key = "validation_ok" if report.is_valid else "validation_failed"
            out.write(translate(key) + "\n")
            if report.missing_paths:
                out.write("Missing:\n")
                for path in report.missing_paths:
                    out.write(f"- {path}\n")
        return 0 if report.is_valid else 1

    if args.command == "discover":
        project = SparkProject(args.root)
        out.write(json.dumps(project.discover()) + "\n")
        return 0

    if args.command == "scaffold":
        manifest = scaffold_manifest(
            args.root,
            name=args.name,
            description=args.description,
            version=args.version,
        )
        out.write(f"Created {manifest}\n")
        return 0

    if args.command == "locales":
        out.write(json.dumps({"locales": list(available_locales())}) + "\n")
        return 0

    if args.command == "integration-links":
        out.write(json.dumps(github_links_integration(args.owner, args.repo)) + "\n")
        return 0

    parser.print_help(err)
    return 2


def main() -> None:
    raise SystemExit(run())
