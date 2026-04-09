# FAQ

## 1) What is Spark?
Spark is a modern open-source repository foundation focused on discoverability, onboarding, and long-term growth.

## 2) Is Spark tied to a specific language/framework?
No. Spark is intentionally stack-agnostic.

## 3) How do I start using it?
Clone the repo and follow `README.md` and `examples/README.md`.

## 4) Where should I ask questions?
Use GitHub Discussions for questions and idea exchange.

## 5) Where do I report bugs?
Use the bug report issue template.

## 6) How do I request new features?
Use the feature request issue template.

## 7) How do I contribute?
Read `CONTRIBUTING.md` and submit a PR using the PR template.

## 8) What license is used?
MIT. See `LICENSE`.

## 9) How is security handled?
See `SECURITY.md` and report privately via advisory/email.

## 10) Where can I track planned work?
See `ROADMAP.md`.

## 11) How are releases documented?
In `CHANGELOG.md` using Keep a Changelog format.

## 12) Who reviews changes?
`@rudra496` is the code owner via `.github/CODEOWNERS`.

## 13) Is there an API reference for Spark modules?
Yes. See `docs/API.md`.

## 14) Are there runnable examples?
Yes. See `examples/basic-usage`, `examples/advanced-config`, and `examples/integrations`.

## 15) Does Spark support plugins and integrations?
Yes. Use `spark.plugins.PluginManager` and `spark.integrations.IntegrationRegistry`.

## 16) Does Spark support multiple languages for messages?
Yes. See `spark.i18n` and `docs/I18N.md`.

## 17) Is there a command-line interface?
Yes. Use `python3 -m spark` and see command examples in `README.md`.

## 18) How can I prepare a production release safely?
Use semantic tags (`v*.*.*`), ensure CHANGELOG includes the tag section, and rely on the release workflow preflight checks.

## 19) How do I get improvement suggestions for my repository?
Run `python3 -m spark assess --root .` (or add `--json` for automation-friendly output).
