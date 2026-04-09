from spark.core import SparkProject


def main() -> None:
    project = SparkProject(".")
    report = project.validate()
    print("valid:", report.is_valid)
    print("missing:", report.missing_paths)


if __name__ == "__main__":
    main()
