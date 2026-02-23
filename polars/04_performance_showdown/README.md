# 04 Performance Showdown: Pandas vs Polars

Head-to-head benchmarks on realistic financial data tasks, comparing pandas,
polars eager, and polars lazy execution.

## What You Learn

- Concrete speedup numbers for common financial data operations
- Where polars excels most (aggregation, joins, parallelism)
- Memory usage comparison
- When pandas might still be acceptable

## Run

```bash
python benchmark.py
```

The script generates ~1M rows of synthetic data (100 tickers x 10K days) and
runs five benchmark tasks. Takes about 30 seconds. Adjust `N_TICKERS` and
`N_DAYS` at the top of the script to change the dataset size.

## Sample Results (1M rows, M1 MacBook Pro)

```
Task                        pandas (s)   polars (s)     lazy (s)    speedup
---------------------------------------------------------------------------
Filter + aggregate              0.0369       0.0032       0.0027      13.7x
Rolling window                  0.2647       0.0110       0.0106      24.9x
Multi-key join                  0.0853       0.0061       0.0062      14.0x
Complex pipeline                0.1206       0.0338       0.0335       3.6x
---------------------------------------------------------------------------
Memory (MB)                      230.8         53.2          ---       4.3x
```

## Key Concepts

- Polars is not just faster — it **scales better** with data size
- The speedup comes from: Rust backend, columnar memory layout, SIMD instructions, automatic multi-threading, and query optimization
- For very small datasets (<1,000 rows), pandas overhead is comparable
- For medium-to-large datasets (>100K rows), polars' advantage becomes dramatic

## Try It

- Change `N_TICKERS` and `N_DAYS` to scale the dataset up or down
- Add your own benchmark task (e.g., pivot, melt, string operations)
- Try running with `POLARS_MAX_THREADS=1` to see the effect of parallelism
