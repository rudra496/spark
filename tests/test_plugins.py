from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from spark.plugins import PluginManager, RequiredFilesPlugin


class PluginManagerTests(unittest.TestCase):
    def test_register_duplicate_plugin_raises(self) -> None:
        manager = PluginManager()
        plugin = RequiredFilesPlugin(required_files=("README.md",))
        manager.register(plugin)
        with self.assertRaises(ValueError):
            manager.register(plugin)

    def test_required_files_plugin_reports_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("ok", encoding="utf-8")
            plugin = RequiredFilesPlugin(required_files=("README.md", "ROADMAP.md"))
            result = plugin.execute({"root": root})
            self.assertFalse(result["ok"])
            self.assertEqual(result["missing"], ["ROADMAP.md"])


if __name__ == "__main__":
    unittest.main()
