"""Integration registry for ecosystem extensions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

IntegrationHandler = Callable[..., dict[str, Any]]


@dataclass
class IntegrationRegistry:
    """Registers and executes named integration handlers."""

    _handlers: dict[str, IntegrationHandler] = field(default_factory=dict)

    def register(self, name: str, handler: IntegrationHandler) -> None:
        if name in self._handlers:
            raise ValueError(f"Integration '{name}' is already registered.")
        self._handlers[name] = handler

    def run(self, name: str, **kwargs: Any) -> dict[str, Any]:
        if name not in self._handlers:
            raise KeyError(f"Integration '{name}' is not registered.")
        return self._handlers[name](**kwargs)

    def list_integrations(self) -> tuple[str, ...]:
        return tuple(sorted(self._handlers.keys()))


def github_links_integration(owner: str, repo: str) -> dict[str, Any]:
    """Example integration for generating GitHub community links."""
    base = f"https://github.com/{owner}/{repo}"
    return {
        "issues": f"{base}/issues",
        "discussions": f"{base}/discussions",
        "pulls": f"{base}/pulls",
    }
