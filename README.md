# ⚡ Spark

Spark is a lightweight toolkit for validating repository structure, discovering metadata, and assessing project maturity.

[![CI](https://github.com/rudra496/spark/actions/workflows/ci.yml/badge.svg)](https://github.com/rudra496/spark/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-live-blue?logo=readthedocs)](https://rudra496.github.io/spark/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Getting Started

```bash
git clone https://github.com/rudra496/spark.git
cd spark
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
python -m spark validate --root .
python -m spark assess --root . --json
```

For full onboarding and troubleshooting, see [docs/getting-started.md](docs/getting-started.md).

## CLI

```bash
python -m spark validate --root . --locale en
python -m spark validate --root . --json
python -m spark discover --root .
python -m spark assess --root .
python -m spark assess --root . --json
python -m spark health --root .
python -m spark health --root . --json
python -m spark locales
python -m spark integration-links --owner rudra496 --repo spark
python -m spark scaffold --root . --name spark --description "Toolkit repo"
python -m spark version
```

## Documentation

- Live docs: https://rudra496.github.io/spark/
- API reference: [docs/API.md](docs/API.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- FAQ: [docs/FAQ.md](docs/FAQ.md)
- Release checklist: [docs/RELEASE_READINESS.md](docs/RELEASE_READINESS.md)

## Development

```bash
ruff check spark tests
mypy spark
pytest -q
mkdocs build --strict
```

## License

MIT. See [LICENSE](LICENSE).
