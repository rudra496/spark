from spark.integrations import IntegrationRegistry, github_links_integration


def main() -> None:
    registry = IntegrationRegistry()
    registry.register("github", github_links_integration)
    links = registry.run("github", owner="rudra496", repo="spark")
    print(links)


if __name__ == "__main__":
    main()
