from __future__ import annotations

import unittest
from pathlib import Path


class PytestConfigTests(unittest.TestCase):
    def test_pyproject_sets_pythonpath_for_direct_pytest_invocation(self) -> None:
        pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
        content = pyproject.read_text(encoding="utf-8")

        self.assertIn("[tool.pytest.ini_options]", content)
        self.assertIn('pythonpath = ["."]', content)
        self.assertIn('testpaths = ["tests"]', content)


if __name__ == "__main__":
    unittest.main()
