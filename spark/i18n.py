"""Minimal i18n helpers for Spark messages."""

from __future__ import annotations

MESSAGES = {
    "en": {
        "validation_ok": "Project is valid.",
        "validation_failed": "Project has missing required files.",
        "plugin_registered": "Plugin '{name}' registered.",
        "assessment_complete": "Assessment complete. Score: {score}/100.",
    },
    "es": {
        "validation_ok": "El proyecto es válido.",
        "validation_failed": "Al proyecto le faltan archivos requeridos.",
        "plugin_registered": "Plugin '{name}' registrado.",
        "assessment_complete": "Evaluación completa. Puntuación: {score}/100.",
    },
    "fr": {
        "validation_ok": "Le projet est valide.",
        "validation_failed": "Il manque des fichiers requis au projet.",
        "plugin_registered": "Plugin '{name}' enregistré.",
        "assessment_complete": "Évaluation terminée. Score : {score}/100.",
    },
}


def available_locales() -> tuple[str, ...]:
    return tuple(sorted(MESSAGES.keys()))


def translate(key: str, locale: str = "en", **kwargs: str) -> str:
    bundle = MESSAGES.get(locale, MESSAGES["en"])
    template = bundle.get(key, MESSAGES["en"].get(key, key))
    return template.format(**kwargs)
