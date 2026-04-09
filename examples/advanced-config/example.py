from spark.core import SparkProject


def main() -> None:
    project = SparkProject(".")
    report = project.validate(required_paths=("README.md", "docs/API.md"))
    print("valid:", report.is_valid)
    print("missing:", report.missing_paths)
    print("discover:", project.discover())


if __name__ == "__main__":
    main()
