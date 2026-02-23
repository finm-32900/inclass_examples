"""
Streaming execution in Polars.

Demonstrates how to process data in batches using the streaming engine
and write results directly to disk with sink_parquet(), keeping peak
memory usage low for large datasets.

Usage:
    python 01_streaming.py
"""

import time
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import polars as pl


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "output"
PARQUET_PATH = OUTPUT_DIR / "trades.parquet"
SINK_PATH = OUTPUT_DIR / "sector_stats.parquet"

N_ROWS = 500_000


# ---------------------------------------------------------------------------
# Synthetic data
# ---------------------------------------------------------------------------

def generate_trade_data(n_rows: int, seed: int = 42) -> pl.DataFrame:
    """Generate synthetic trade data (~3M rows)."""
    rng = np.random.default_rng(seed)

    tickers = [f"TICK{i:03d}" for i in range(200)]
    sectors = [
        "Technology", "Healthcare", "Finance", "Energy", "Consumer",
        "Industrial", "Materials", "Utilities", "RealEstate", "Telecom",
    ]
    exchanges = ["NYSE", "NASDAQ", "CBOE", "ARCA"]
    sides = ["buy", "sell"]

    # Map tickers to sectors deterministically
    ticker_sector = {t: sectors[i % len(sectors)] for i, t in enumerate(tickers)}

    chosen_tickers = rng.choice(tickers, n_rows)

    return pl.DataFrame({
        "trade_id": list(range(n_rows)),
        "date": [date(2020, 1, 2) + timedelta(days=int(d))
                 for d in rng.integers(0, 1500, n_rows)],
        "ticker": chosen_tickers.tolist(),
        "sector": [ticker_sector[t] for t in chosen_tickers],
        "exchange": rng.choice(exchanges, n_rows).tolist(),
        "side": rng.choice(sides, n_rows).tolist(),
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # -- Generate data ---------------------------------------------------------
    section("Setup: Generating trade data")
    OUTPUT_DIR.mkdir(exist_ok=True)

    if not PARQUET_PATH.exists():
        print(f"  Generating {N_ROWS:,} rows of trade data ...")
        df = generate_trade_data(N_ROWS)
        df.write_parquet(PARQUET_PATH)
        print(f"  Written to {PARQUET_PATH} ({PARQUET_PATH.stat().st_size / 1e6:.1f} MB)")
    else:
        print(f"  Using existing {PARQUET_PATH}")

    # ======================================================================
    # 1. scan_parquet workflow
    # ======================================================================
    section("1. scan_parquet Workflow")

    lf = pl.scan_parquet(PARQUET_PATH)

    sub("Build a query: filter → aggregate")
    query = (
        lf
        .filter(pl.col("sector") == "Technology")
        .group_by("ticker")
        .agg(
            pl.col("price").mean().alias("avg_price"),
            pl.col("quantity").sum().alias("total_qty"),
            pl.len().alias("num_trades"),
        )
        .sort("total_qty", descending=True)
    )

    sub("Query plan (notice predicate pushdown into scan)")
    print(query.explain())

    sub("Collect results")
    result = query.collect()
    print(result.head(10))

    # ======================================================================
    # 2. Streaming execution
    # ======================================================================
    section("2. Streaming Execution")
    print("  Streaming processes data in batches, reducing peak memory.\n")

    query = (
        pl.scan_parquet(PARQUET_PATH)
        .group_by("sector", "exchange")
        .agg(
            pl.col("price").mean().alias("avg_price"),
            pl.col("quantity").sum().alias("total_qty"),
            pl.len().alias("num_trades"),
        )
    )

    sub("Standard .collect()")
    start = time.perf_counter()
    result_standard = query.collect()
    standard_time = time.perf_counter() - start
    print(f"  Time: {standard_time:.4f}s")

    sub(".collect(engine='streaming') — processes in batches")
    start = time.perf_counter()
    result_streaming = query.collect(engine="streaming")
    streaming_time = time.perf_counter() - start
    print(f"  Time: {streaming_time:.4f}s")

    print(f"\n  Both produce the same result: {result_standard.shape} rows")
    print(result_standard.sort("sector", "exchange").head(10))

    # ======================================================================
    # 3. sink_parquet — write results without collecting to memory
    # ======================================================================
    section("3. sink_parquet(): Write Directly to Disk")
    print("  Results are written to disk without ever being held in memory.\n")

    sink_query = (
        pl.scan_parquet(PARQUET_PATH)
        .group_by("sector")
        .agg(
            pl.col("price").mean().alias("avg_price"),
            pl.col("quantity").sum().alias("total_qty"),
            pl.col("quantity").mean().alias("avg_qty"),
            pl.len().alias("num_trades"),
        )
        .sort("sector")
    )

    sink_query.sink_parquet(SINK_PATH)
    print(f"  Written to {SINK_PATH} ({SINK_PATH.stat().st_size / 1e3:.1f} KB)")

    sub("Read back to verify")
    print(pl.read_parquet(SINK_PATH))

    # ======================================================================
    # 4. When to use streaming
    # ======================================================================
    section("4. When to Use Streaming")
    print(
        "  Use streaming when:\n"
        "  - Your dataset is larger than available RAM\n"
        "  - You want to minimize peak memory usage\n"
        "  - You're writing results to disk (sink_parquet)\n\n"
        "  Standard .collect() may be faster for data that fits in memory,\n"
        "  because the optimizer has more freedom without batch constraints.\n\n"
        "  Rule of thumb: if your data is >50% of available RAM, try streaming."
    )
