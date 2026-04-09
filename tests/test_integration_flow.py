from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from spark.core import SparkProject
from spark.plugins import PluginManager, RequiredFilesPlugin


class EndToEndFlowTests(unittest.TestCase):
    def test_project_plugin_flow(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("ok", encoding="utf-8")
            project = SparkProject(root)
            manager = PluginManager()
            manager.register(RequiredFilesPlugin(required_files=("README.md", "ROADMAP.md")))
            output = project.run_plugins(manager)
            self.assertIn("required-files", output)
            self.assertFalse(output["required-files"]["ok"])


if __name__ == "__main__":
    unittest.main()
