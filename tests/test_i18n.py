from __future__ import annotations

import unittest

from spark.i18n import available_locales, translate


class I18NTests(unittest.TestCase):
    def test_available_locales_contains_en_and_es(self) -> None:
        locales = available_locales()
        self.assertIn("en", locales)
        self.assertIn("es", locales)

    def test_translate_falls_back_to_en_for_unknown_locale(self) -> None:
        text = translate("validation_ok", locale="de")
        self.assertEqual(text, "Project is valid.")

    def test_translate_french_locale(self) -> None:
        text = translate("validation_ok", locale="fr")
        self.assertEqual(text, "Le projet est valide.")

    def test_translate_assessment_complete_all_locales(self) -> None:
        en = translate("assessment_complete", locale="en", score="95")
        es = translate("assessment_complete", locale="es", score="95")
        fr = translate("assessment_complete", locale="fr", score="95")
        self.assertIn("95", en)
        self.assertIn("95", es)
        self.assertIn("95", fr)
        self.assertIn("Score", en)
        self.assertIn("Puntuación", es)
        self.assertIn("Score", fr)

    def test_translate_formats_placeholders(self) -> None:
        text = translate("plugin_registered", locale="es", name="demo")
        self.assertEqual(text, "Plugin 'demo' registrado.")


if __name__ == "__main__":
    unittest.main()
