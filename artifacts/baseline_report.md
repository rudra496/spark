# Baseline Report

Date: 2026-04-09T23:07:39Z
Branch: production-hardening

## 1) Tests
......................................                                   [100%]
38 passed in 0.23s
EXIT_CODE=0

## 2) Lint (ruff)
E402 Module level import not at top of file
  --> benchmarks/benchmark_validation.py:11:1
   |
 9 |     sys.path.insert(0, str(ROOT))
10 |
11 | from spark.core import SparkProject
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

E402 Module level import not at top of file
  --> examples/advanced-config/example.py:10:1
   |
 8 |     sys.path.insert(0, str(ROOT))
 9 |
10 | from spark.core import SparkProject
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

E402 Module level import not at top of file
  --> examples/basic-usage/example.py:10:1
   |
 8 |     sys.path.insert(0, str(ROOT))
 9 |
10 | from spark.core import SparkProject
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

E402 Module level import not at top of file
  --> examples/integrations/example.py:10:1
   |
 8 |     sys.path.insert(0, str(ROOT))
 9 |
10 | from spark.integrations import IntegrationRegistry, github_links_integration
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |

Found 4 errors.
EXIT_CODE=1

## 3) Type check (mypy)
Success: no issues found in 8 source files
EXIT_CODE=0

## 4) Docs build
/bin/bash: line 17: mkdocs: command not found
EXIT_CODE=127

## 5) CLI smoke
usage: spark [-h]
             {validate,discover,assess,scaffold,locales,integration-links,version,health}
             ...

Spark project toolkit CLI

positional arguments:
  {validate,discover,assess,scaffold,locales,integration-links,version,health}
    validate            Validate repository structure
    discover            Discover repository metadata
    assess              Assess repository maturity and next actions
    scaffold            Create spark.json manifest
    locales             List available locales
    integration-links   Generate GitHub links
    version             Print the installed Spark version
    health              Quick health check (exit 0 = healthy)

options:
  -h, --help            show this help message and exit
EXIT_CODE=0
✅ Healthy
EXIT_CODE=0
spark 0.2.0
EXIT_CODE=0

## 6) Maturity assessment
{"root": "/workspace/spark", "score": 100, "summary": "Excellent repository foundation.", "strengths": ["All required foundation files are present.", "Automation workflows are configured.", "Documentation depth is solid.", "Example coverage helps adoption.", "Repository is properly licensed.", "Automated tests are present."], "recommendations": [], "missing_required_paths": []}
EXIT_CODE=0
