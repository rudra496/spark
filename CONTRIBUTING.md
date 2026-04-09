# Contributing to Spark

First off — **thank you for considering a contribution!** Every contribution, no matter how small, makes Spark better for everyone.

This document will help you get started quickly and confidently.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Style Guidelines](#style-guidelines)
- [Recognition](#recognition)

---

## Code of Conduct

By participating, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it — it helps us maintain a welcoming, productive community for everyone.

---

## How Can I Contribute?

There are many ways to contribute, even without writing code:

- 🐛 **Report bugs** using the [bug report template](https://github.com/rudra496/spark/issues/new?template=bug_report.yml)
- 💡 **Suggest features** using the [feature request template](https://github.com/rudra496/spark/issues/new?template=feature_request.yml)
- 📝 **Improve documentation** — fix typos, clarify explanations, add examples
- 🔍 **Review pull requests** — share feedback on open PRs
- 🌍 **Translate content** — help make Spark accessible globally
- ⭐ **Star and share** — help others discover the project

---

## Getting Started

### 1. Fork the Repository

Click **Fork** on the [GitHub repository page](https://github.com/rudra496/spark) to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/spark.git
cd spark
```

### 3. Set Up Upstream

```bash
git remote add upstream https://github.com/rudra496/spark.git
```

### 4. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:

- `feature/add-xyz`
- `fix/broken-link-in-readme`
- `docs/improve-architecture-doc`
- `chore/update-dependencies`

---

## Development Workflow

```bash
# Keep your fork up-to-date
git fetch upstream
git rebase upstream/main

# Make your changes, then stage and commit
git add .
git commit -m "feat: add XYZ feature"

# Push to your fork
git push origin feature/your-feature-name
```

---

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(optional scope): <short description>

[optional body]

[optional footer(s)]
```

### Types

| Type | When to use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, missing semicolons, etc. |
| `refactor` | Code restructuring without changing behavior |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks, dependency updates |
| `ci` | CI/CD pipeline changes |

### Examples

```bash
git commit -m "feat: add dark mode support"
git commit -m "fix: resolve crash on empty input"
git commit -m "docs: update architecture overview"
git commit -m "chore: bump dependency versions"
```

---

## Pull Request Process

1. **Ensure your changes are complete** — all tests pass, docs are updated
2. **Open a PR against `main`** using the [PR template](.github/pull_request_template.md)
3. **Fill in the PR template** — describe what changed and why
4. **Link related issues** — use `Closes #123` or `Fixes #456` in the PR body
5. **Wait for review** — a maintainer will review within a few days
6. **Address feedback** — push follow-up commits to your branch
7. **Merge** — once approved, a maintainer will merge your PR

### PR Checklist

Before submitting:

- [ ] Code compiles/runs without errors
- [ ] Relevant documentation is updated
- [ ] Commit messages follow the convention above
- [ ] No sensitive data or credentials are included

---

## Reporting Bugs

Use the [Bug Report template](https://github.com/rudra496/spark/issues/new?template=bug_report.yml).

A good bug report includes:

- Clear, descriptive title
- Steps to reproduce (minimal, reproducible example)
- Expected vs actual behavior
- Environment details (OS, versions, etc.)
- Screenshots or logs if applicable

---

## Suggesting Features

Use the [Feature Request template](https://github.com/rudra496/spark/issues/new?template=feature_request.yml).

A good feature request includes:

- The problem you're trying to solve
- Your proposed solution
- Alternatives you've considered
- Any relevant context or prior art

---

## Style Guidelines

- **Markdown**: Keep lines under ~120 characters, use ATX-style headings (`#`), and include a blank line before/after code blocks
- **Code**: Follow the conventions already present in the codebase
- **Documentation**: Be concise, use active voice, and write for a global audience (avoid idioms and jargon)

---

## Recognition

All contributors are listed in our [contributors graph](https://github.com/rudra496/spark/graphs/contributors).

We believe every contribution — large or small — deserves recognition. Thank you for helping make Spark better! 🙏

---

**Questions?** Open a [GitHub Discussion](https://github.com/rudra496/spark/discussions) or check [SUPPORT.md](SUPPORT.md).
