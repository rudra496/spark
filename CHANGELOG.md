# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Spark v0.1 core toolkit (`spark.core`) with repository validation, discovery, and manifest scaffolding
- Plugin management and required-files plugin (`spark.plugins`)
- Integration registry and GitHub links integration (`spark.integrations`)
- i18n helpers with English and Spanish locales (`spark.i18n`)
- CLI module with validate/discover/scaffold/locales/integration-links commands (`spark.cli`)
- Repository assessment scoring with actionable recommendations (`spark assess`, `SparkProject.assess`)
- Unit and integration test suite under `tests/`
- CLI test suite for command behavior and edge cases (`tests/test_cli.py`)
- Core assessment tests (`tests/test_core.py`)
- API, i18n, benchmark, and release-readiness docs
- Innovation guide (`docs/INNOVATION.md`)
- Runnable examples under `examples/basic-usage`, `examples/advanced-config`, and `examples/integrations`
- Benchmark entrypoint at `benchmarks/benchmark_validation.py`
- Python packaging metadata and console-script entrypoint (`pyproject.toml`)

### Changed
- CI workflow now runs Python tests in addition to markdown lint and required-file validation
- CI required-file checks now include `pyproject.toml`
- Release workflow now has preflight checks (tests + changelog/tag consistency) before publishing
- README and API docs now include repository assessment capability

## [0.1.0] - 2024-04-08

### Added
- Repository foundation: README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT
- Community templates: issue forms, PR template, CODEOWNERS
- Documentation structure: ARCHITECTURE, FAQ, SHOWCASE
- CI/CD workflows: ci.yml, release.yml
- ROADMAP, CHANGELOG, SECURITY, SUPPORT files
