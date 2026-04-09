from __future__ import annotations

import unittest
from pathlib import Path

_PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


class PytestConfigTests(unittest.TestCase):
    def test_pytest_ini_options_present(self) -> None:
        content = _PYPROJECT.read_text(encoding="utf-8")

        self.assertIn("[tool.pytest.ini_options]", content)
        self.assertIn('pythonpath = ["."]', content)
        self.assertIn('testpaths = ["tests"]', content)


if __name__ == "__main__":
    unittest.main()
