# Getting Started

This guide walks you through installing Spark, running your first commands, and integrating the Python API into your workflow.

---

## Prerequisites

- Python 3.10 or higher
- Git 2.x+

---

## Installation

### From source (development mode)

```bash
git clone https://github.com/rudra496/spark.git
cd spark
pip install -e .
```

### Verify installation

```bash
spark version
# spark 0.2.0
```

---

## First Steps

### 1. Validate your repository

Check that all required community and documentation files are present:

```bash
spark validate --root /path/to/your-repo
```

Example output:

```
Project has missing required files.
Missing:
- CONTRIBUTING.md
- docs/ARCHITECTURE.md
```

Use `--json` for structured output:

```bash
spark validate --root . --json
# {"valid": false, "missing": ["CONTRIBUTING.md"], "root": "/path/to/repo"}
```

Use `--locale` for localized messages:

```bash
spark validate --root . --locale es
# Al proyecto le faltan archivos requeridos.

spark validate --root . --locale fr
# Il manque des fichiers requis au projet.
```

---

### 2. Get a maturity score

Assess your repository and receive a 0–100 score plus actionable recommendations:

```bash
spark assess --root .
```

Example output:

```
Score: 80/100
Summary: Strong repository foundation with room to improve.
Strengths:
- All required foundation files are present.
- Automation workflows are configured.
- Documentation depth is solid.
Recommendations:
- Add a LICENSE file to clarify project licensing.
- Add automated tests to improve reliability.
```

---

### 3. Quick health check

Verify basic health in a single command:

```bash
spark health --root .
# ✅ Healthy    (exit 0)
# ⚠️  Unhealthy (exit 1)
```

Useful in CI pipelines:

```yaml
- name: Spark health check
  run: spark health --root .
```

---

### 4. Discover repository metadata

```bash
spark discover --root .
```

Returns JSON with:

```json
{
  "root": "/path/to/repo",
  "docs_count": 8,
  "example_count": 3,
  "workflow_count": 2,
  "has_license": true,
  "license_file": "LICENSE",
  "test_count": 5,
  "language": "python"
}
```

---

### 5. Scaffold a new manifest

```bash
spark scaffold --root ./my-new-project \
  --name "my-project" \
  --description "A focused, well-documented tool" \
  --version "0.1.0"
# Created /path/to/my-new-project/spark.json
```

---

## Python API Quick Reference

```python
from spark import SparkProject, scaffold_manifest, SparkValidationError

project = SparkProject(".")

# Validate
report = project.validate()
if not report.is_valid:
    print("Missing:", report.missing_paths)

# Assess
assessment = project.assess()
print(f"Score: {assessment.score}/100")

# Serialise to dict
data = assessment.as_dict()

# Discover
info = project.discover()
print(info["language"], info["test_count"])

# Badge URLs
badges = project.badge_urls("my-org", "my-repo")

# Scaffold (with validation)
try:
    path = scaffold_manifest("./new", name="demo", description="A demo")
except SparkValidationError as e:
    print(f"Invalid input: {e}")
```

---

## Using Plugins

```python
from spark import SparkProject, PluginManager, RequiredFilesPlugin

manager = PluginManager()
manager.register(RequiredFilesPlugin(required_files=("README.md", "LICENSE")))

project = SparkProject(".")
results = project.run_plugins(manager)
print(results["required-files"])
# {"ok": True, "missing": [], "checked": ["README.md", "LICENSE"]}
```

---

## Using Integrations

```python
from spark import IntegrationRegistry
from spark.integrations import github_links_integration

registry = IntegrationRegistry()
registry.register("github", github_links_integration)

links = registry.run("github", owner="rudra496", repo="spark")
print(links["issues"])
# https://github.com/rudra496/spark/issues
```

---

## Internationalization

```python
from spark import translate, available_locales

print(available_locales())  # ('en', 'es', 'fr')

print(translate("validation_ok", locale="fr"))
# Le projet est valide.
```

---

## Next Steps

- Read the [API Reference](API.md) for complete module documentation
- Explore [Architecture](ARCHITECTURE.md) to understand design decisions
- Check the [FAQ](FAQ.md) for common questions
- See [CONTRIBUTING](https://github.com/rudra496/spark/blob/main/CONTRIBUTING.md) to contribute
