"""
Hive-style partitioned datasets in Polars.

Demonstrates how to write, read, and query Hive-partitioned parquet data.
Partition pruning lets Polars skip irrelevant subdirectories entirely,
making queries on specific slices dramatically faster.

Usage:
    python 02_hive_partitioning.py
"""

import shutil
import time
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import polars as pl


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "output"
HIVE_DIR = OUTPUT_DIR / "trades_hive"

N_ROWS = 500_000


# ---------------------------------------------------------------------------
# Synthetic data
# ---------------------------------------------------------------------------

def generate_trade_data(n_rows: int, seed: int = 42) -> pl.DataFrame:
    """Generate synthetic trade data for Hive partitioning demo."""
    rng = np.random.default_rng(seed)

    tickers = [f"TICK{i:03d}" for i in range(200)]
    sectors = [
        "Technology", "Healthcare", "Finance", "Energy", "Consumer",
        "Industrial", "Materials", "Utilities", "RealEstate", "Telecom",
    ]
    exchanges = ["NYSE", "NASDAQ", "CBOE", "ARCA"]

    ticker_sector = {t: sectors[i % len(sectors)] for i, t in enumerate(tickers)}
    chosen_tickers = rng.choice(tickers, n_rows)

    return pl.DataFrame({
        "trade_id": list(range(n_rows)),
        "date": [date(2020, 1, 2) + timedelta(days=int(d))
                 for d in rng.integers(0, 1500, n_rows)],
        "ticker": chosen_tickers.tolist(),
        "sector": [ticker_sector[t] for t in chosen_tickers],
        "exchange": rng.choice(exchanges, n_rows).tolist(),
        "price": rng.uniform(5, 500, n_rows).round(2).tolist(),
        "quantity": rng.lognormal(mean=6, sigma=1.5, size=n_rows).astype(int).tolist(),
    })


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def section(title: str):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def sub(label: str):
    print(f"\n--- {label} ---")


def show_directory_tree(path: Path, prefix: str = "", max_depth: int = 2, _depth: int = 0):
    """Print a simple directory tree."""
    if _depth > max_depth:
        return
    entries = sorted(path.iterdir())
    dirs = [e for e in entries if e.is_dir()]
    files = [e for e in entries if e.is_file()]
    for f in files:
        print(f"{prefix}{f.name} ({f.stat().st_size / 1e3:.0f} KB)")
    for d in dirs:
        print(f"{prefix}{d.name}/")
        show_directory_tree(d, prefix + "  ", max_depth, _depth + 1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    OUTPUT_DIR.mkdir(exist_ok=True)

    # ======================================================================
    # 1. Write Hive-partitioned data
    # ======================================================================
    section("1. Writing Hive-Partitioned Data")

    if HIVE_DIR.exists():
        shutil.rmtree(HIVE_DIR)

    print(f"  Generating {N_ROWS:,} rows of trade data ...")
    df = generate_trade_data(N_ROWS)

    # NOTE: Hive partitioning API may evolve; tested with polars >= 1.0
    print(f"  Writing to {HIVE_DIR}/ partitioned by 'sector' ...")
    df.write_parquet(
        HIVE_DIR,
        use_pyarrow=True,
        pyarrow_options={"partition_cols": ["sector"]},
    )

    sub("Resulting directory structure")
    show_directory_tree(HIVE_DIR)

    # ======================================================================
    # 2. Reading Hive-partitioned data
    # ======================================================================
    section("2. Reading Hive-Partitioned Data")

    sub("scan_parquet auto-detects Hive structure")
    lf = pl.scan_parquet(
        HIVE_DIR / "**/*.parquet",
        hive_partitioning=True,
    )
    print(f"  Schema: {lf.collect_schema()}")
    print(f"  Note: 'sector' column comes from the partition directories")

    sub("Collect all data")
    full = lf.collect()
    print(f"  Full dataset: {full.shape[0]:,} rows × {full.shape[1]} columns")

    # ======================================================================
    # 3. Partition pruning
    # ======================================================================
    section("3. Partition Pruning")
    print("  When filtering by a partition column, Polars only reads")
    print("  the relevant subdirectories — skipping the rest entirely.\n")

    sub("Query plan: filter by sector (partition column)")
    pruned_query = (
        pl.scan_parquet(HIVE_DIR / "**/*.parquet", hive_partitioning=True)
        .filter(pl.col("sector") == "Technology")
    )
    print(pruned_query.explain())

    sub("Timing: full scan vs partition-pruned scan")

    _, full_time = _time_full = (
        time.perf_counter(),
        None,
    )
    start = time.perf_counter()
    _ = (
        pl.scan_parquet(HIVE_DIR / "**/*.parquet", hive_partitioning=True)
        .collect()
    )
    full_time = time.perf_counter() - start
    print(f"  Full scan (all sectors):    {full_time:.4f}s")

    start = time.perf_counter()
    result = (
        pl.scan_parquet(HIVE_DIR / "**/*.parquet", hive_partitioning=True)
        .filter(pl.col("sector") == "Technology")
        .collect()
    )
    pruned_time = time.perf_counter() - start
    print(f"  Pruned scan (1 sector):     {pruned_time:.4f}s")
    print(f"  Speedup:                    {full_time / pruned_time:.1f}x")
    print(f"  Rows returned:              {result.height:,} / {full.height:,}")

    # ======================================================================
    # 4. Practical use case
    # ======================================================================
    section("4. Practical Use Case")
    print(
        "  In production, analysts store trade data partitioned by date\n"
        "  (e.g., year=2024/month=03/). Querying a specific date range\n"
        "  only reads the relevant subdirectories.\n\n"
        "  Hive partitioning is ideal when:\n"
        "  - You repeatedly query by the same categorical columns\n"
        "  - The data is too large to scan every time\n"
        "  - You want to add new data by writing new partition folders\n"
        "    without rewriting the entire dataset"
    )

    sub("Example: aggregate within a single sector")
    result = (
        pl.scan_parquet(HIVE_DIR / "**/*.parquet", hive_partitioning=True)
        .filter(pl.col("sector") == "Finance")
        .group_by("ticker")
        .agg(
            pl.col("price").mean().alias("avg_price"),
            pl.col("quantity").sum().alias("total_qty"),
            pl.len().alias("num_trades"),
        )
        .sort("total_qty", descending=True)
        .collect()
    )
    print(result.head(10))
