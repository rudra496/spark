from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from spark.integrations import IntegrationRegistry, github_links_integration  # noqa: E402


def main() -> None:
    registry = IntegrationRegistry()
    registry.register("github", github_links_integration)
    links = registry.run("github", owner="rudra496", repo="spark")
    print(links)


if __name__ == "__main__":
    main()
