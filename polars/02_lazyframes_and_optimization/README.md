# 02 LazyFrames and Query Optimization

How Polars optimizes your queries before executing them — the key advantage for medium-to-large datasets.

## What You Learn

- Eager vs lazy execution and when to use each
- How to read query plans with `.explain()`
- Predicate pushdown: filtering happens at the data source, not after loading
- Projection pushdown: only needed columns are read from disk
- Measurable speedups with concrete timing comparisons

## Run

```bash
python lazy_and_pushdown.py
```

The script generates 100K rows (50 tickers x 2,000 days), writes a ~6 MB
parquet file to `output/` (gitignored), and demonstrates eager vs lazy
performance. Runs in under 10 seconds.

## Sample Results (M1 MacBook Pro)

| Operation | Eager | Lazy | Speedup |
|-----------|-------|------|---------|
| Predicate pushdown (filter 1 sector) | 0.020s | 0.003s | 7x |
| Projection pushdown (3 of 20 cols) | 0.019s | 0.002s | 10x |
| Combined (filter + select) | 0.020s | 0.002s | 10x |

## Key Concepts

- A **LazyFrame** is a recipe — it records what you want to do but executes nothing
- `.collect()` triggers execution of the entire optimized plan
- `.explain()` shows the plan as text; compare `optimized=True` vs `optimized=False`
- **Predicate pushdown**: a filter on rows is pushed into the parquet reader, so unneeded row groups are never decoded
- **Projection pushdown**: only the columns your query actually uses are read from disk

## Try It

- Add an unnecessary `.sort()` mid-pipeline and check if the optimizer removes it
- Try `.explain()` with a join between two LazyFrames
- Increase the dataset to 2M+ rows and re-run the timing comparison
