# Getting Started

This guide gets a contributor from clone to successful CLI usage in under 10 minutes.

## Prerequisites

- **Python 3.10+**
- **Git 2.x+**
- Optional but recommended: a virtual environment tool (`venv`, `uv`, or `virtualenv`)

## Installation

```bash
git clone https://github.com/rudra496/spark.git
cd spark
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## First-Run CLI Flow

Run these commands from the repository root:

```bash
python -m spark validate --root .
python -m spark discover --root .
python -m spark assess --root .
python -m spark health --root .
python -m spark version
```

Expected behavior:

- `validate` checks required repository files.
- `discover` prints repository metadata as JSON.
- `assess` returns a maturity score and recommendations.
- `health` exits with `0` only when the repo is valid and workflows exist.
- `version` prints the installed Spark version.

## JSON Automation Usage

Use `--json` for machine-readable output in CI scripts.

```bash
python -m spark validate --root . --json
python -m spark assess --root . --json
python -m spark health --root . --json
```

Example gate in shell:

```bash
python -m spark health --root . --json | python -c "import json,sys; sys.exit(0 if json.load(sys.stdin)['healthy'] else 1)"
```

## Troubleshooting

### `mkdocs: command not found`

Install docs tooling:

```bash
pip install mkdocs mkdocs-material
```

### `spark validate` reports missing files

Run discovery to understand current structure:

```bash
python -m spark discover --root .
```

Then add missing files listed by `validate`.

### Unexpected locale output

List supported locales and re-run with a valid locale code:

```bash
python -m spark locales
python -m spark validate --root . --locale en
```

### Command not found for `spark`

Use module mode if console scripts are unavailable:

```bash
python -m spark --help
```