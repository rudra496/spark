"""Spark toolkit public API."""

from .core import AssessmentReport, DEFAULT_REQUIRED_PATHS, SparkProject, scaffold_manifest
from .i18n import available_locales, translate
from .integrations import IntegrationRegistry
from .plugins import PluginManager, RequiredFilesPlugin
from .cli import run as run_cli

__all__ = [
    "DEFAULT_REQUIRED_PATHS",
    "AssessmentReport",
    "SparkProject",
    "PluginManager",
    "RequiredFilesPlugin",
    "IntegrationRegistry",
    "available_locales",
    "translate",
    "scaffold_manifest",
    "run_cli",
]
