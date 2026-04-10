# API Reference

## `spark.core`

- `SparkProject(root)`
  - `validate(required_paths: tuple[str, ...] | None = None) -> ValidationReport`
  - `discover() -> dict[str, Any]`
  - `assess() -> AssessmentReport`
  - `run_plugins(manager: PluginManager) -> dict[str, dict[str, Any]]`
  - `badge_urls(owner: str, repo: str) -> dict[str, str]`
- `scaffold_manifest(root, name, description, version="0.1.0") -> Path`
- `SparkValidationError`
- `ValidationReport`
  - `root: Path`
  - `missing_paths: tuple[str, ...]`
  - `is_valid: bool`
  - `as_dict() -> dict[str, Any]`
- `AssessmentReport`
  - `root: Path`
  - `score: int`
  - `summary: str`
  - `strengths: tuple[str, ...]`
  - `recommendations: tuple[str, ...]`
  - `missing_required_paths: tuple[str, ...]`
  - `as_dict() -> dict[str, Any]`

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
  - `list_integrations() -> tuple[str, ...]`
- `github_links_integration(owner, repo) -> dict[str, str]`

## `spark.i18n`

- `available_locales() -> tuple[str, ...]`
- `translate(key, locale="en", **kwargs) -> str`

## `spark.cli`

- `run(argv: list[str] | None = None, *, stdout=None, stderr=None) -> int`
- `main() -> None`

### CLI Commands

- `spark validate --root <path> [--json] [--locale <en|es|fr>]`
- `spark discover --root <path>`
- `spark assess --root <path> [--json]`
- `spark scaffold --root <path> --name <name> --description <text> [--version <v>]`
- `spark locales`
- `spark integration-links --owner <org-or-user> --repo <repo>`
- `spark version`
- `spark health --root <path> [--json]`
