<meta name="description" content="Spark — Lightweight Python toolkit for validating OSS repository structure, assessing project maturity, scaffolding project foundations, and scoring codebase quality. CLI, plugin system, and i18n ready.">

# ⚡ Spark — Python Toolkit for OSS Project Validation & Maturity Scoring

> **Validate repository structure, score project maturity, and scaffold new foundations — all from your terminal.**

Spark is a lightweight, zero-dependency Python toolkit that helps open-source maintainers and contributors **validate repository structure**, **assess project maturity** with actionable 0–100 scores, **discover metadata**, and **scaffold project foundations**. Built with type safety, i18n, and a plugin system — ready for CI pipelines and developer workflows.

[![CI](https://github.com/rudra496/spark/actions/workflows/ci.yml/badge.svg)](https://github.com/rudra496/spark/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-live-blue?logo=readthedocs)](https://rudra496.github.io/spark/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Release v0.2.0](https://img.shields.io/github/v/release/rudra496/spark?color=orange)](https://github.com/rudra496/spark/releases/latest)

---

## 🚀 What is Spark?

**Spark** is a professional-grade Python toolkit for OSS project foundations. It helps you:

- ✅ **Validate** — Check that required files and structure are present
- 📊 **Assess** — Score project maturity (0–100) with actionable recommendations
- 🔍 **Discover** — Extract repository metadata as JSON
- 🏗️ **Scaffold** — Generate `spark.json` project manifests
- 🔌 **Extend** — Plugin system and integration registry
- 🌐 **Localize** — English, Spanish, and French built-in
- 🛡️ **Type Safe** — Full `mypy` strict-compatible annotations

---

## 📦 Installation

```bash
git clone https://github.com/rudra496/spark.git
cd spark
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .

# Verify
spark version
```

---

## ⌨️ CLI Commands

| Command                                                 | Description                             |
| ------------------------------------------------------- | --------------------------------------- |
| `spark validate --root <path>`                          | Check required files are present        |
| `spark assess --root <path>`                            | Score and summarize repository maturity |
| `spark discover --root <path>`                          | Output repository metadata as JSON      |
| `spark scaffold --root <path> --name X --description Y` | Create `spark.json` manifest            |
| `spark health --root <path>`                            | Quick healthy/unhealthy check           |
| `spark locales`                                         | List supported i18n locales             |
| `spark integration-links --owner X --repo Y`            | Generate GitHub community links         |
| `spark version`                                         | Print installed version                 |

All commands support `--json` for machine-readable output and `--locale` for i18n.

---

## 🐍 Python API

```python
from spark import SparkProject, scaffold_manifest

project = SparkProject("/path/to/repo")

# Validate
report = project.validate()
print(report.is_valid)        # True / False
print(report.missing_paths)  # tuple of missing paths

# Assess maturity
assessment = project.assess()
print(assessment.score)           # 0–100
print(assessment.summary)         # Human-readable summary
print(assessment.strengths)       # Things done right
print(assessment.recommendations) # What to improve

# Discover metadata
info = project.discover()
print(info["language"], info["has_license"], info["test_count"])

# Badge URLs
badges = project.badge_urls("my-org", "my-repo")

# Scaffold a manifest
scaffold_manifest("/new/project", name="my-project", description="A great project")
```

---

## ✨ Features

| Feature                     | Description                                                 |
| --------------------------- | ----------------------------------------------------------- |
| ⚡ **Zero Bloat**           | Pure Python standard library — no runtime dependencies      |
| 🔌 **Plugin System**        | Extend validation with custom `SparkPlugin` implementations |
| 🧩 **Integration Registry** | Register named handler functions for ecosystem extensions   |
| 🌐 **i18n Ready**           | English, Spanish, French built-in; easy to extend           |
| 📊 **Maturity Scoring**     | 0–100 score with actionable strengths and recommendations   |
| 🛡️ **Input Validation**     | `SparkValidationError` for clear, typed error handling      |
| 🏷️ **Badge Helpers**        | One-call badge URL generation for README shields            |
| 🎯 **Type Safe**            | Full `mypy` strict-compatible type annotations              |

---

## 📖 Documentation

- 🌐 [Live Docs](https://rudra496.github.io/spark/) — Full documentation site
- 🚀 [Getting Started](docs/getting-started.md) — Installation, first steps, common workflows
- 📚 [API Reference](docs/API.md) — Full module and class documentation
- 🏗️ [Architecture](docs/ARCHITECTURE.md) — Design principles and module map
- 🌐 [Internationalization](docs/I18N.md) — Adding and using locales
- ❓ [FAQ](docs/FAQ.md) — Common questions and answers

---

## 👨‍💻 Author

**Rudra Sarker** — 3rd-year IPE student at SUST, Bangladesh. Open-source advocate and assistive technology researcher.

[![Portfolio](https://img.shields.io/badge/Portfolio-rudra496-blue?logo=github)](https://rudra496.github.io/site)
[![GitHub](https://img.shields.io/badge/GitHub-rudra496-181717?logo=github)](https://github.com/rudra496)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Rudra_Sarker-0A66C2?logo=linkedin)](https://www.linkedin.com/in/rudrasarker)
[![Twitter/X](https://img.shields.io/badge/X-@Rudra496-000?logo=x)](https://x.com/Rudra496)

---

## 📬 Contact

| Platform   | Link                                                            |
| ---------- | --------------------------------------------------------------- |
| 📧 Email   | [rudrasarker130@gmail.com](mailto:rudrasarker130@gmail.com)     |
| 🌐 Web     | [rudra496.github.io/site](https://rudra496.github.io/site)     |
| 💻 GitHub  | [github.com/rudra496](https://github.com/rudra496)             |
| 💼 LinkedIn| [linkedin.com/in/rudrasarker](https://www.linkedin.com/in/rudrasarker) |
| 🐦 X/Twitter| [x.com/Rudra496](https://x.com/Rudra496)                     |
| 🎮 DevPost | [devpost.com/rudrasarker](https://devpost.com/rudrasarker)     |
| 🎥 YouTube| [youtube.com/@rudrasarker9732](https://www.youtube.com/@rudrasarker9732) |
| 📸 Instagram|[instagram.com/rudrasarker](https://www.instagram.com/rudrasarker/) |

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT — see [LICENSE](LICENSE).

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://github.com/rudra496">Rudra Sarker</a></strong><br>
  <sub>If you find Spark useful, consider giving it a ⭐ on GitHub!</sub>
</p>
