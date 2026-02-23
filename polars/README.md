# Polars: A Modern DataFrame Library

This directory teaches [Polars](https://pola.rs/) as a high-performance alternative to pandas, progressing from syntax comparison to handling medium and large datasets.

## Why Polars?

- **Consistent syntax**: No `.loc`/`.iloc` confusion, no `SettingWithCopyWarning`, one way to filter/select/mutate
- **Expression API**: Composable, reusable column expressions that run in Rust (not Python)
- **Lazy evaluation**: Query optimizer with predicate and projection pushdown
- **Built for scale**: Streaming execution and Hive-partitioned datasets for larger-than-memory data
- **Multi-threaded by default**: No GIL bottleneck — all cores used automatically

## Examples

| Directory | Topic | Key Concepts |
|-----------|-------|--------------|
| [01_syntax_comparison](01_syntax_comparison/) | Pandas vs Polars side-by-side | select, filter, group_by, with_columns, over(), chaining |
| [02_lazyframes_and_optimization](02_lazyframes_and_optimization/) | Lazy evaluation and query optimization | .lazy(), .collect(), .explain(), predicate/projection pushdown |
| [03_large_data](03_large_data/) | Working with medium-to-large data | scan_parquet, streaming, sink_parquet, Hive partitioning |
| [04_performance_showdown](04_performance_showdown/) | Head-to-head pandas vs polars benchmarks | Timing, memory, realistic financial tasks |

Work through them in order — each builds on concepts from the previous.

## Setup

```bash
pip install polars pandas numpy pyarrow
```

## Note on Data

All examples generate synthetic financial data internally. No external API keys or data files are required.
