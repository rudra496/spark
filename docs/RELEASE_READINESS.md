# Release Readiness

This checklist tracks readiness for the next stable release candidate.

## Required quality gates

- [x] Unit and integration tests pass (`pytest -q`)
- [x] Lint and type checks pass (`ruff check spark tests`, `mypy spark`)
- [x] Docs build passes with strict mode (`mkdocs build --strict`)
- [x] Dead-link checks run for `README.md` and `docs/**/*.md`
- [x] Docs deployment workflow performs strict build before deploy
- [x] Docs homepage reachability check is automated
- [x] Release workflow validates changelog/tag alignment
- [x] Release workflow builds package artifacts (`python -m build`)
- [x] Release workflow installs built wheel and verifies `import spark`

## Repository controls

- [ ] Branch protection enabled for `main`
  - Required status checks: CI, docs deploy/check workflows
  - Required pull request review before merge

## Release execution

- [ ] Update `CHANGELOG.md` for the release tag
- [ ] Create release tag (`vX.Y.Z`) after all checks are green
- [ ] Publish release artifacts and notes
