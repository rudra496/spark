# ⚡ Spark — OSS Project Foundation Toolkit

> **Validate, score, and scaffold open-source repositories. Zero dependencies.**

[![CI](https://github.com/rudra496/spark/actions/workflows/ci.yml/badge.svg)](https://github.com/rudra496/spark/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-live-blue?logo=readthedocs)](https://rudra496.github.io/spark/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/rudra496/spark/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/rudra496/spark/blob/main/CONTRIBUTING.md)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

**Spark** is a professional-grade Python toolkit for OSS project foundations. It helps you:

- ✅ **Validate** repository structure and required files
- 📊 **Assess** project maturity with actionable scores (0–100)
- 🔍 **Discover** metadata about any repository
- 🏗️ **Scaffold** new project manifests (`spark.json`)
- 🔌 **Extend** via plugins and integration registry
- 🌐 **Localize** messages in English, Spanish, and French

**Why Spark?** Most projects start with good intentions but drift into missing docs, no CI, stale configs. Spark gives you a clear score and actionable recommendations to fix it.

---

## Quick Start

```bash
git clone https://github.com/rudra496/spark.git
cd spark
pip install -e .

# Validate your repo
spark validate --root .

# Get a maturity score
spark assess --root .

# Quick health check
spark health --root .
```

---

## CLI Commands

| Command | Description |
|---|---|
| `spark validate --root <path>` | Check required files are present |
| `spark assess --root <path>` | Score and summarize repository maturity |
| `spark discover --root <path>` | Output repository metadata as JSON |
| `spark scaffold --root <path> --name X --desc Y` | Create `spark.json` manifest |
| `spark health --root <path>` | Quick healthy/unhealthy check |
| `spark locales` | List supported i18n locales |
| `spark integration-links --owner X --repo Y` | Generate GitHub community links |
| `spark version` | Print installed version |

All commands support `--json` for machine-readable output.

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
print(assessment.score)           # 0-100
print(assessment.summary)         # Human-readable summary
print(assessment.strengths)       # Things done right
print(assessment.recommendations) # What to improve

# Rich discovery
info = project.discover()
print(info["language"])     # "python", "javascript", etc.
print(info["has_license"])  # True / False
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
| 🎯 **Type Safe** | Full `mypy` strict-compatible type annotations |

---

## Use Cases

- **Repo hygiene audits** — quickly score any repository's health
- **Hacktoberfest validation** — ensure repos meet contribution-readiness standards
- **CI integration** — gate PRs on minimum maturity scores
- **Org-wide scans** — assess multiple repositories at scale
- **Onboarding checklists** — verify new projects have all required files

---

## Navigation

- 📖 [Getting Started](https://rudra496.github.io/spark/getting-started/) — Installation, first steps
- 📚 [API Reference](https://rudra496.github.io/spark/API/) — Full module documentation
- 🏗️ [Architecture](https://rudra496.github.io/spark/ARCHITECTURE/) — Design principles
- 🌐 [i18n Guide](https://rudra496.github.io/spark/I18N/) — Adding locales
- ❓ [FAQ](https://rudra496.github.io/spark/FAQ/) — Common questions

---

## Author

**Rudra Sarker** — AI & Open Source Developer | SUST Bangladesh

---

## License

MIT
