from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spark.core import SparkProject  # noqa: E402


def main() -> None:
    project = SparkProject(".")
    report = project.validate()
    print("valid:", report.is_valid)
    print("missing:", report.missing_paths)


if __name__ == "__main__":
    main()
