from __future__ import annotations

import unittest

from spark.integrations import IntegrationRegistry, github_links_integration


class IntegrationRegistryTests(unittest.TestCase):
    def test_register_and_run_integration(self) -> None:
        registry = IntegrationRegistry()
        registry.register("github", github_links_integration)
        payload = registry.run("github", owner="rudra496", repo="spark")
        self.assertEqual(payload["issues"], "https://github.com/rudra496/spark/issues")

    def test_duplicate_registration_raises(self) -> None:
        registry = IntegrationRegistry()
        registry.register("github", github_links_integration)
        with self.assertRaises(ValueError):
            registry.register("github", github_links_integration)

    def test_unregistered_integration_raises(self) -> None:
        registry = IntegrationRegistry()
        with self.assertRaises(KeyError):
            registry.run("missing")


if __name__ == "__main__":
    unittest.main()
