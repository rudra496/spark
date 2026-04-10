from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spark.core import SparkProject  # noqa: E402


def main() -> None:
    iterations = 2000
    project = SparkProject(Path(__file__).resolve().parents[1])
    start = time.perf_counter()
    for _ in range(iterations):
        project.validate()
    elapsed = time.perf_counter() - start
    per_op_ms = (elapsed / iterations) * 1000
    print(f"iterations={iterations}")
    print(f"elapsed_seconds={elapsed:.6f}")
    print(f"per_op_ms={per_op_ms:.6f}")


if __name__ == "__main__":
    main()
