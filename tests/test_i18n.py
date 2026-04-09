from __future__ import annotations

import unittest

from spark.i18n import available_locales, translate


class I18NTests(unittest.TestCase):
    def test_available_locales_contains_en_and_es(self) -> None:
        locales = available_locales()
        self.assertIn("en", locales)
        self.assertIn("es", locales)

    def test_translate_falls_back_to_en_for_unknown_locale(self) -> None:
        text = translate("validation_ok", locale="fr")
        self.assertEqual(text, "Project is valid.")

    def test_translate_formats_placeholders(self) -> None:
        text = translate("plugin_registered", locale="es", name="demo")
        self.assertEqual(text, "Plugin 'demo' registrado.")


if __name__ == "__main__":
    unittest.main()
