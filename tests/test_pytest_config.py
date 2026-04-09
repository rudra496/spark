from __future__ import annotations

import unittest
from pathlib import Path

import tomli


class PytestConfigTests(unittest.TestCase):
    def test_pyproject_sets_pythonpath_for_direct_pytest_invocation(self) -> None:
        pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
        with pyproject.open("rb") as stream:
            config = tomli.load(stream)

        pytest_config = config["tool"]["pytest"]["ini_options"]
        self.assertIn(".", pytest_config["pythonpath"])
        self.assertIn("tests", pytest_config["testpaths"])


if __name__ == "__main__":
    unittest.main()
