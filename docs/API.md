# API Reference

## `spark.core`

- `SparkProject(root)`
  - `validate(required_paths: tuple[str, ...] | None = None) -> ValidationReport`
  - `discover() -> dict[str, Any]`
  - `run_plugins(manager: PluginManager) -> dict[str, dict[str, Any]]`
- `scaffold_manifest(root, name, description, version="0.1.0") -> Path`
- `ValidationReport`
  - `root: Path`
  - `missing_paths: tuple[str, ...]`
  - `is_valid: bool`

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
