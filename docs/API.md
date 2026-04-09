# API Reference

## `spark.core`

- `SparkProject(root)`
  - `validate(required_paths: tuple[str, ...] | None = None) -> ValidationReport`
  - `discover() -> dict[str, Any]`
  - `assess() -> AssessmentReport`
  - `run_plugins(manager: PluginManager) -> dict[str, dict[str, Any]]`
- `scaffold_manifest(root, name, description, version="0.1.0") -> Path`
- `ValidationReport`
  - `root: Path`
  - `missing_paths: tuple[str, ...]`
  - `is_valid: bool`
- `AssessmentReport`
  - `root: Path`
  - `score: int`
  - `summary: str`
  - `strengths: tuple[str, ...]`
  - `recommendations: tuple[str, ...]`
  - `missing_required_paths: tuple[str, ...]`

## `spark.plugins`

- `PluginManager`
  - `register(plugin)`
  - `run(context)`
- `RequiredFilesPlugin(required_files)`
  - `execute(context)`

## `spark.integrations`

- `IntegrationRegistry`
  - `register(name, handler)`
  - `run(name, **kwargs)`
  - `list_integrations()`
- `github_links_integration(owner, repo)`

## `spark.i18n`

- `available_locales() -> tuple[str, ...]`
- `translate(key, locale="en", **kwargs) -> str`

## `spark.cli`

- `run(argv: list[str] | None = None, *, stdout=None, stderr=None) -> int`
- `main() -> None`

### CLI Commands

- `spark validate --root <path> [--json]`
- `spark discover --root <path>`
- `spark scaffold --root <path> --name <name> --description <text> [--version <v>]`
- `spark assess --root <path> [--json]`
- `spark locales`
- `spark integration-links --owner <org-or-user> --repo <repo>`
