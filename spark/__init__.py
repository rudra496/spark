"""Spark toolkit public API."""

from .core import DEFAULT_REQUIRED_PATHS, SparkProject, scaffold_manifest
from .i18n import available_locales, translate
from .integrations import IntegrationRegistry
from .plugins import PluginManager, RequiredFilesPlugin

__all__ = [
    "DEFAULT_REQUIRED_PATHS",
    "SparkProject",
    "PluginManager",
    "RequiredFilesPlugin",
    "IntegrationRegistry",
    "available_locales",
    "translate",
    "scaffold_manifest",
]
