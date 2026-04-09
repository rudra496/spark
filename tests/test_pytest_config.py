from __future__ import annotations

import importlib
import importlib.util
import unittest
from pathlib import Path


def _load_toml_module():
    module_name = "tomllib" if importlib.util.find_spec("tomllib") else "tomli"
    return importlib.import_module(module_name)


class PytestConfigTests(unittest.TestCase):
    def test_pyproject_sets_pythonpath_for_direct_pytest_invocation(self) -> None:
        pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
        toml_module = _load_toml_module()

        with pyproject.open("rb") as stream:
            config = toml_module.load(stream)

        pytest_config = config["tool"]["pytest"]["ini_options"]
        self.assertIn(".", pytest_config["pythonpath"])
        self.assertIn("tests", pytest_config["testpaths"])


if __name__ == "__main__":
    unittest.main()
