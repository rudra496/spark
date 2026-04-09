"""Minimal i18n helpers for Spark messages."""

from __future__ import annotations

MESSAGES = {
    "en": {
        "validation_ok": "Project is valid.",
        "validation_failed": "Project has missing required files.",
        "plugin_registered": "Plugin '{name}' registered.",
    },
    "es": {
        "validation_ok": "El proyecto es válido.",
        "validation_failed": "Al proyecto le faltan archivos requeridos.",
        "plugin_registered": "Plugin '{name}' registrado.",
    },
}


def available_locales() -> tuple[str, ...]:
    return tuple(sorted(MESSAGES.keys()))


def translate(key: str, locale: str = "en", **kwargs: str) -> str:
    bundle = MESSAGES.get(locale, MESSAGES["en"])
    template = bundle.get(key, MESSAGES["en"].get(key, key))
    return template.format(**kwargs)
