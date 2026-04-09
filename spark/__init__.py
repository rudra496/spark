"""Spark toolkit public API."""

from ._version import __version__
from .cli import run as run_cli
from .core import (
    DEFAULT_REQUIRED_PATHS,
    AssessmentReport,
    SparkProject,
    SparkValidationError,
    ValidationReport,
    scaffold_manifest,
)
from .i18n import available_locales, translate
from .integrations import IntegrationRegistry
from .plugins import PluginManager, RequiredFilesPlugin

__all__ = [
    "__version__",
    "DEFAULT_REQUIRED_PATHS",
    "AssessmentReport",
    "ValidationReport",
    "SparkProject",
    "SparkValidationError",
    "PluginManager",
    "RequiredFilesPlugin",
    "IntegrationRegistry",
    "available_locales",
    "translate",
    "scaffold_manifest",
    "run_cli",
]
