# Benchmarks

Spark includes a small benchmark for project validation to track baseline performance over time.

## Run

```bash
python3 benchmarks/benchmark_validation.py
```

## Output

- Total elapsed time for repeated validation runs
- Average milliseconds per operation

Use this as a regression signal while evolving validation and plugin logic.
