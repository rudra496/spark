# ⚡ Spark

> **The lightweight toolkit that ignites your OSS projects.**

[![CI](https://github.com/rudra496/spark/actions/workflows/ci.yml/badge.svg)](https://github.com/rudra496/spark/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-live-blue?logo=readthedocs)](https://rudra496.github.io/spark/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/rudra496/spark/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/rudra496/spark/blob/main/CONTRIBUTING.md)

---

## What is Spark?

**Spark** is a professional-grade Python toolkit for OSS project foundations. It helps you:

- ✅ **Validate** repository structure and required files
- 📊 **Assess** project maturity with actionable scores
- 🔍 **Discover** metadata about any repository
- 🏗️ **Scaffold** new project manifests
- 🔌 **Extend** via plugins and integration registry
- 🌐 **Localize** messages in English, Spanish, and French

---

## Quick Start

```bash
# Install from source
git clone https://github.com/rudra496/spark.git
cd spark
pip install -e .

# Validate your repo
spark validate --root .

# Get a maturity score
spark assess --root .

# Quick health check
spark health --root .

# Show version
spark version
```

---

## CLI Commands

| Command | Description |
|---|---|
| `spark validate --root <path>` | Check required files are present |
| `spark assess --root <path>` | Score and summarize repository maturity |
| `spark discover --root <path>` | Output repository metadata as JSON |
| `spark scaffold --root <path> --name X --description Y` | Create `spark.json` manifest |
| `spark health --root <path>` | Quick healthy/unhealthy check |
| `spark locales` | List supported i18n locales |
| `spark integration-links --owner X --repo Y` | Generate GitHub community links |
| `spark version` | Print installed version |

All commands support `--json` for machine-readable output (where applicable).

---

## Python API

```python
from spark import SparkProject, scaffold_manifest

# Validate repository structure
project = SparkProject("/path/to/repo")
report = project.validate()
print(report.is_valid)        # True / False
print(report.missing_paths)  # tuple of missing paths

# Full maturity assessment
assessment = project.assess()
print(assessment.score)           # 0–100
print(assessment.summary)         # Human-readable summary
print(assessment.strengths)       # Things done right
print(assessment.recommendations) # What to improve

# Rich discovery
info = project.discover()
print(info["language"])     # "python", "javascript", etc.
print(info["has_license"])  # True / False
print(info["test_count"])   # Number of test files

# Badge URLs for README
badges = project.badge_urls("my-org", "my-repo")
print(badges["ci"])   # GitHub Actions badge URL
print(badges["docs"]) # Docs badge URL

# Create a manifest
manifest_path = scaffold_manifest(
    "/path/to/new-project",
    name="my-project",
    description="A great project",
    version="0.1.0",
)
```

---

## Features

| Feature | Description |
|---|---|
| ⚡ **Zero Bloat** | Pure Python standard library — no runtime dependencies |
| 🔌 **Plugin System** | Extend validation with custom `SparkPlugin` implementations |
| 🧩 **Integration Registry** | Register named handler functions for ecosystem extensions |
| 🌐 **i18n Ready** | English, Spanish, French built-in; easy to extend |
| 📊 **Maturity Scoring** | 0–100 score with actionable strengths and recommendations |
| 🛡️ **Input Validation** | `SparkValidationError` for clear, typed error handling |
| 🏷️ **Badge Helpers** | One-call badge URL generation for README shields |
| 🎯 **Type Safe** | Full `mypy` strict-compatible type annotations |

---

## Navigation

- 📖 [Getting Started](getting-started.md) — Installation, first steps, common workflows
- 📚 [API Reference](API.md) — Full module and class documentation
- 🏗️ [Architecture](ARCHITECTURE.md) — Design principles and module map
- 🌐 [Internationalization](I18N.md) — Adding and using locales
- 💡 [Innovation](INNOVATION.md) — Ecosystem design and extensibility
- ❓ [FAQ](FAQ.md) — Common questions and answers
- 🌟 [Showcase](SHOWCASE.md) — Projects using Spark
- ⚡ [Benchmarks](BENCHMARKS.md) — Performance baseline

---

*Made with ❤️ by [@rudra496](https://github.com/rudra496) and [contributors](https://github.com/rudra496/spark/graphs/contributors)*
