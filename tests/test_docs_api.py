from __future__ import annotations

import unittest
from pathlib import Path


class DocsAPITests(unittest.TestCase):
    def test_api_docs_list_all_cli_commands(self) -> None:
        api_doc = Path('docs/API.md').read_text(encoding='utf-8')
        for command in (
            'spark validate --root <path> [--json] [--locale <en|es|fr>]',
            'spark discover --root <path>',
            'spark assess --root <path> [--json]',
            'spark scaffold --root <path> --name <name> --description <text> [--version <v>]',
            'spark locales',
            'spark integration-links --owner <org-or-user> --repo <repo>',
            'spark version',
            'spark health --root <path> [--json]',
        ):
            self.assertIn(command, api_doc)


if __name__ == '__main__':
    unittest.main()
