# Innovation in Spark

Spark's core innovation is turning repository quality
practices into a small executable toolkit instead of only static guidelines.

## What is innovative here?

1. **Foundation-as-code**
   Required files and standards validated programmatically
   (`spark validate`).

2. **Maturity visibility**
   Repository health scored with actionable next steps
   (`spark assess`).

3. **Composable governance**
   Plugin and integration APIs let teams add org-specific
   checks and workflows.

4. **Release discipline by default**
   CI and release preflight checks enforce quality and
   changelog consistency before publishing.

## What can be done with Spark?

- Validate open-source repository foundations.
- Discover repository metadata for dashboards and automation.
- Generate project manifest (`spark.json`) for bootstrapping.
- Produce ecosystem links for collaboration surfaces.
- Assess maturity and prioritize improvements with concrete recommendations.

## How to do it quickly

From repository root:

```bash
python3 -m spark validate --root . --json
python3 -m spark discover --root .
python3 -m spark assess --root . --json
python3 -m spark scaffold --root . --name my-repo --description "My project"
python3 -m spark integration-links --owner my-org --repo my-repo
```

## Improvement plan (next)

- Add configurable scoring weights and policy profiles.
- Add machine-readable SARIF/JSON report formats for CI annotations.
- Add optional dependency/license audit integration.
- Add more locale packs and contributor-facing docs translation workflow.
- Add plugin marketplace-style registry metadata.
