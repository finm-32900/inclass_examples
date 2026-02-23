# 03 Large Data: Streaming and Hive Partitioning

Working with datasets that challenge or exceed available memory using Polars'
streaming execution and Hive-style partitioned storage.

## What You Learn

- `scan_parquet()` / `scan_csv()` for lazy file reading
- Streaming execution with `.collect(engine="streaming")`
- `sink_parquet()` to write results without collecting to memory
- Hive-style partitioned datasets: writing, reading, and partition pruning

## Scripts

| Script | Topic |
|--------|-------|
| `01_streaming.py` | Streaming execution and sink_parquet |
| `02_hive_partitioning.py` | Hive-partitioned datasets and partition pruning |

## Run

```bash
python 01_streaming.py
python 02_hive_partitioning.py
```

Scripts generate synthetic data in `output/` (~100-200 MB, gitignored).
Run `01_streaming.py` first as `02_hive_partitioning.py` generates its own data independently.

## Key Concepts

- **Streaming** processes data in batches, keeping peak memory low even for large inputs
- **sink_parquet()** writes query results directly to disk — the data never needs to fit in memory
- **Hive partitioning** organizes data into directories by key columns (e.g., `sector=Technology/`)
- **Partition pruning** means Polars only reads the subdirectories matching your filter

## Try It

- Increase the row count to 10M and observe memory behavior
- Add more partition columns and check `.explain()` for pruning
- Write a streaming query that chains filter → group_by → sink_parquet
