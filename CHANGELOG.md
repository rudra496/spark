# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Baseline hardening report at `artifacts/baseline_report.md` including tests, lint/type-check, docs build, CLI smoke, and `spark assess --json`
- New docs homepage reachability workflow: `.github/workflows/docs-link-check.yml`
- API docs consistency smoke test (`tests/test_docs_api.py`)
- Core tests for `.yaml` workflow discovery and runnable example counting semantics
- CLI regression test ensuring `health` succeeds for `.yaml` workflow repositories

### Changed

- Rewrote `docs/getting-started.md` for production onboarding (prerequisites, install, first-run flow, JSON automation, troubleshooting)
- Simplified README to a concise production-facing format with one canonical CLI section
- Expanded `docs/API.md` CLI command coverage (including `version`, `health`, and `validate --locale`)
- `SparkProject.discover()` now counts both `.yml` and `.yaml` workflows
- `SparkProject.discover()` example counting now targets runnable examples instead of all directory entries
- CI workflow now includes strict docs build and dead-link checks
- CI dead-link check now uses glob-aware input expansion for docs paths
- Docs deploy workflow now runs `mkdocs build --strict` before deployment and validates homepage reachability
- Release preflight now builds package artifacts and verifies wheel install/import
- README docs URL converted to a Markdown link for markdown-lint compatibility

## [0.2.0] - 2025-04-09

### Added

- `SparkValidationError` — typed exception for invalid configuration inputs
- `ValidationReport.as_dict()` — JSON-serialisable dict representation
- `AssessmentReport.as_dict()` — JSON-serialisable dict representation
- `SparkProject.badge_urls(owner, repo)` — one-call README badge URL generation
- `SparkProject.discover()` now returns `has_license`, `license_file`, `test_count`, and `language`
- `scaffold_manifest()` now validates that name and description are non-empty
- French locale (`fr`) added to i18n message bundles
- `assessment_complete` i18n message key in all supported locales
- CLI `version` command — prints installed Spark version
- CLI `health` command — quick `✅ Healthy` / `⚠️  Unhealthy` check for CI pipelines
- CLI `--locale` option on `validate` command for localized output
- `_version.py` module to hold `__version__` without circular imports
- MkDocs Material docs site (`mkdocs.yml`) — live at <https://rudra496.github.io/spark/>
- `docs/index.md` — professional landing page for the docs site
- `docs/getting-started.md` — comprehensive install, CLI, and API guide
- GitHub Actions `docs.yml` workflow — automatic Pages deployment on push to `main`
- CI `lint-python` job — `ruff` linting for `spark/` and `tests/`
- CI `typecheck` job — `mypy` type checking for `spark/`
- CI `test` matrix now covers Python 3.10, 3.11, and 3.12
- `.editorconfig` for consistent editor configuration
- Expanded `.gitignore` (`.venv`, `.mypy_cache`, `.ruff_cache`, `site/`, etc.)

### Changed

- `pyproject.toml`: version bumped to `0.2.0`; added `[project.urls]`, `[tool.ruff]`, `[tool.mypy]`, `Development Status` and topic classifiers
- `SparkProject.assess()` scoring now also rewards presence of a license file (+10) and automated tests (+10), with corresponding recommendations when absent
- CI jobs renamed from `lint`/`validate` to `lint-markdown`/`validate-files` for clarity
- README: added Docs, Python 3.10+ badges and link to live docs site; updated feature table and CLI section

### Fixed

- Removed accidental root-level `i` artifact file

## [0.1.0] - 2024-04-08

### Added

- Repository foundation: README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT
- Community templates: issue forms, PR template, CODEOWNERS
- Documentation structure: ARCHITECTURE, FAQ, SHOWCASE
- CI/CD workflows: ci.yml, release.yml
- ROADMAP, CHANGELOG, SECURITY, SUPPORT files
- Spark v0.1 core toolkit (`spark.core`) with repository validation, discovery, and manifest scaffolding
- Plugin management and required-files plugin (`spark.plugins`)
- Integration registry and GitHub links integration (`spark.integrations`)
- i18n helpers with English and Spanish locales (`spark.i18n`)
- CLI module with validate/discover/scaffold/locales/integration-links commands (`spark.cli`)
- Repository assessment scoring with actionable recommendations (`spark assess`, `SparkProject.assess`)
- Unit and integration test suite under `tests/`
