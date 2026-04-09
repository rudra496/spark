"""Plugin support for Spark validation flows."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


class SparkPlugin(Protocol):
    """Protocol for Spark plugins."""

    name: str

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Run plugin logic and return serializable output."""


@dataclass
class PluginManager:
    """Register and execute Spark plugins."""

    _plugins: list[SparkPlugin] = field(default_factory=list)

    def register(self, plugin: SparkPlugin) -> None:
        if any(existing.name == plugin.name for existing in self._plugins):
            raise ValueError(f"Plugin '{plugin.name}' is already registered.")
        self._plugins.append(plugin)

    def run(self, context: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return {plugin.name: plugin.execute(context) for plugin in self._plugins}


@dataclass(frozen=True)
class RequiredFilesPlugin:
    """Checks if required files exist under a repository root."""

    required_files: tuple[str, ...]
    name: str = "required-files"

    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        root = Path(context["root"])
        missing = [path for path in self.required_files if not (root / path).exists()]
        return {
            "ok": len(missing) == 0,
            "missing": missing,
            "checked": list(self.required_files),
        }
