"""
Performance showdown: pandas vs polars on realistic financial tasks.

Generates a synthetic dataset (~1M rows of daily stock returns) and
benchmarks five common operations: filter+aggregate, rolling window,
multi-key join, a complex analytical pipeline, and memory usage.

Usage:
    python benchmark.py
"""

import sys
import time
from datetime import date, timedelta

import numpy as np
import pandas as pd
import polars as pl


# ---------------------------------------------------------------------------
# Config — adjust these to change dataset size
# ---------------------------------------------------------------------------

N_TICKERS = 100
N_DAYS = 10_000  # ~1M rows
SEED = 42
N_RUNS = 3  # median of N_RUNS for each benchmark


# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------

def generate_data(n_tickers: int, n_days: int, seed: int = 42):
    """Generate synthetic stock data in both pandas and polars."""
    rng = np.random.default_rng(seed)

    tickers = [f"TICK{i:03d}" for i in range(n_tickers)]
    sectors = [
        "Technology", "Healthcare", "Finance", "Energy", "Consumer",
        "Industrial", "Materials", "Utilities", "RealEstate", "Telecom", "Other",
    ]
    exchanges = ["NYSE", "NASDAQ", "CBOE", "ARCA"]

    # Deterministic sector/exchange assignment per ticker
    ticker_sector = {t: sectors[i % len(sectors)] for i, t in enumerate(tickers)}
    ticker_exchange = {t: exchanges[i % len(exchanges)] for i, t in enumerate(tickers)}

    n_rows = n_tickers * n_days
    print(f"  Generating {n_rows:,} rows ({n_tickers} tickers × {n_days} days) ...")

    # Build dates as Python date objects in a list (polars handles these natively)
    base = date(2000, 1, 3)
    dates_list = [base + timedelta(days=i) for i in range(n_days)]
    ticker_arr = tickers * n_days
    date_arr = [d for d in dates_list for _ in range(n_tickers)]

    data = {
        "date": date_arr,
        "ticker": ticker_arr,
        "sector": [ticker_sector[t] for t in ticker_arr],
        "exchange": [ticker_exchange[t] for t in ticker_arr],
        "return_pct": rng.normal(0, 0.02, n_rows).tolist(),
        "volume": rng.lognormal(mean=14, sigma=1, size=n_rows).astype(int).tolist(),
        "market_cap": rng.lognormal(mean=23, sigma=2, size=n_rows).round(0).tolist(),
        "price": rng.uniform(10, 500, n_rows).round(2).tolist(),
    }

    pdf = pd.DataFrame(data)
    pdf["date"] = pd.to_datetime(pdf["date"])
    plf = pl.DataFrame(data)

    # Reference table for join benchmark
    ref_data = {
        "ticker": tickers,
        "sector": [ticker_sector[t] for t in tickers],
        "exchange": [ticker_exchange[t] for t in tickers],
        "full_name": [f"Company {t}" for t in tickers],
    }
    ref_pd = pd.DataFrame(ref_data)
    ref_pl = pl.DataFrame(ref_data)

    return pdf, plf, ref_pd, ref_pl


# ---------------------------------------------------------------------------
# Timing helper
# ---------------------------------------------------------------------------

def bench(func, n_runs: int = N_RUNS) -> float:
    """Run func n_runs times and return median elapsed time in seconds."""
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        func()
        times.append(time.perf_counter() - start)
    return sorted(times)[len(times) // 2]


# ---------------------------------------------------------------------------
# Benchmark tasks
# ---------------------------------------------------------------------------

def task_filter_aggregate(pdf, plf):
    """Filter to one sector, compute stats per ticker."""
    def pandas_version():
        return (
            pdf[pdf["sector"] == "Technology"]
            .groupby("ticker")
            .agg(
                avg_return=("return_pct", "mean"),
                total_volume=("volume", "sum"),
                count=("ticker", "count"),
            )
        )

    def polars_eager():
        return (
            plf
            .filter(pl.col("sector") == "Technology")
            .group_by("ticker")
            .agg(
                pl.col("return_pct").mean().alias("avg_return"),
                pl.col("volume").sum().alias("total_volume"),
                pl.len().alias("count"),
            )
        )

    def polars_lazy():
        return (
            plf.lazy()
            .filter(pl.col("sector") == "Technology")
            .group_by("ticker")
            .agg(
                pl.col("return_pct").mean().alias("avg_return"),
                pl.col("volume").sum().alias("total_volume"),
                pl.len().alias("count"),
            )
            .collect()
        )

    return bench(pandas_version), bench(polars_eager), bench(polars_lazy)


def task_rolling_window(pdf, plf):
    """20-day rolling mean of returns per ticker."""
    def pandas_version():
        return (
            pdf
            .sort_values(["ticker", "date"])
            .groupby("ticker")["return_pct"]
            .rolling(20)
            .mean()
        )

    def polars_eager():
        return plf.with_columns(
            pl.col("return_pct")
            .rolling_mean(window_size=20)
            .over("ticker")
            .alias("rolling_mean")
        )

    def polars_lazy():
        return (
            plf.lazy()
            .with_columns(
                pl.col("return_pct")
                .rolling_mean(window_size=20)
                .over("ticker")
                .alias("rolling_mean")
            )
            .collect()
        )

    return bench(pandas_version), bench(polars_eager), bench(polars_lazy)


def task_join(pdf, plf, ref_pd, ref_pl):
    """Join main table with reference table on ticker."""
    def pandas_version():
        return pdf.merge(ref_pd, on="ticker", suffixes=("", "_ref"))

    def polars_eager():
        return plf.join(ref_pl, on="ticker", suffix="_ref")

    def polars_lazy():
        return (
            plf.lazy()
            .join(ref_pl.lazy(), on="ticker", suffix="_ref")
            .collect()
        )

    return bench(pandas_version), bench(polars_eager), bench(polars_lazy)


def task_complex_pipeline(pdf, plf):
    """Full analytical pipeline: filter, transform, rolling, group, aggregate."""
    cutoff_date_pd = pd.Timestamp("2020-01-01")
    cutoff_date_pl = date(2020, 1, 1)

    def pandas_version():
        temp = pdf[pdf["date"] >= cutoff_date_pd].copy()
        temp["log_return"] = np.log(1 + temp["return_pct"])
        temp = temp.sort_values(["ticker", "date"])
        temp["rolling_vol"] = (
            temp.groupby("ticker")["log_return"]
            .rolling(20)
            .std()
            .reset_index(level=0, drop=True)
        )
        temp["year_month"] = temp["date"].dt.to_period("M")
        return (
            temp.groupby(["sector", "year_month"])
            .agg(
                avg_return=("log_return", "mean"),
                avg_vol=("rolling_vol", "mean"),
                total_volume=("volume", "sum"),
                count=("ticker", "count"),
            )
        )

    def polars_eager():
        return (
            plf
            .filter(pl.col("date") >= cutoff_date_pl)
            .with_columns(
                pl.col("return_pct").log1p().alias("log_return"),
            )
            .sort("ticker", "date")
            .with_columns(
                pl.col("log_return")
                .rolling_std(window_size=20)
                .over("ticker")
                .alias("rolling_vol"),
                pl.col("date").dt.strftime("%Y-%m").alias("year_month"),
            )
            .group_by("sector", "year_month")
            .agg(
                pl.col("log_return").mean().alias("avg_return"),
                pl.col("rolling_vol").mean().alias("avg_vol"),
                pl.col("volume").sum().alias("total_volume"),
                pl.len().alias("count"),
            )
        )

    def polars_lazy():
        return (
            plf.lazy()
            .filter(pl.col("date") >= cutoff_date_pl)
            .with_columns(
                pl.col("return_pct").log1p().alias("log_return"),
            )
            .sort("ticker", "date")
            .with_columns(
                pl.col("log_return")
                .rolling_std(window_size=20)
                .over("ticker")
                .alias("rolling_vol"),
                pl.col("date").dt.strftime("%Y-%m").alias("year_month"),
            )
            .group_by("sector", "year_month")
            .agg(
                pl.col("log_return").mean().alias("avg_return"),
                pl.col("rolling_vol").mean().alias("avg_vol"),
                pl.col("volume").sum().alias("total_volume"),
                pl.len().alias("count"),
            )
            .collect()
        )

    return bench(pandas_version), bench(polars_eager), bench(polars_lazy)


def task_memory(pdf, plf):
    """Compare memory footprint."""
    pd_mem = pdf.memory_usage(deep=True).sum() / 1e6
    pl_mem = plf.estimated_size("mb")
    return pd_mem, pl_mem


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 75)
    print("  PERFORMANCE SHOWDOWN: pandas vs polars")
    print("=" * 75)

    pdf, plf, ref_pd, ref_pl = generate_data(N_TICKERS, N_DAYS, SEED)
    print(f"  pandas shape: {pdf.shape}  |  polars shape: {plf.shape}")
    print(f"  Timing: median of {N_RUNS} runs per task\n")

    # -- Run benchmarks --------------------------------------------------------
    results = []

    print("  Running: Filter + aggregate ...")
    pd_t, pl_t, pl_lazy_t = task_filter_aggregate(pdf, plf)
    results.append(("Filter + aggregate", pd_t, pl_t, pl_lazy_t))

    print("  Running: Rolling window ...")
    pd_t, pl_t, pl_lazy_t = task_rolling_window(pdf, plf)
    results.append(("Rolling window", pd_t, pl_t, pl_lazy_t))

    print("  Running: Multi-key join ...")
    pd_t, pl_t, pl_lazy_t = task_join(pdf, plf, ref_pd, ref_pl)
    results.append(("Multi-key join", pd_t, pl_t, pl_lazy_t))

    print("  Running: Complex pipeline ...")
    pd_t, pl_t, pl_lazy_t = task_complex_pipeline(pdf, plf)
    results.append(("Complex pipeline", pd_t, pl_t, pl_lazy_t))

    pd_mem, pl_mem = task_memory(pdf, plf)

    # -- Print results ---------------------------------------------------------
    print()
    print("=" * 75)
    print(f"  {'Task':<25} {'pandas (s)':>12} {'polars (s)':>12} {'lazy (s)':>12} {'speedup':>10}")
    print("-" * 75)
    for name, pd_t, pl_t, pl_lazy_t in results:
        best_pl = min(pl_t, pl_lazy_t)
        speedup = pd_t / best_pl if best_pl > 0 else float("inf")
        print(f"  {name:<25} {pd_t:>12.4f} {pl_t:>12.4f} {pl_lazy_t:>12.4f} {speedup:>9.1f}x")
    print("-" * 75)
    print(f"  {'Memory (MB)':<25} {pd_mem:>12.1f} {pl_mem:>12.1f} {'---':>12} {pd_mem / pl_mem:>9.1f}x")
    print("=" * 75)
    print()
    print("  Note: Results vary by system. Adjust N_TICKERS and N_DAYS at the")
    print("  top of the script to change the dataset size.")
    print(f"\n  Python {sys.version.split()[0]}  |  pandas {pd.__version__}  |  polars {pl.__version__}")
