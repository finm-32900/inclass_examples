"""
Create Market Data for Financial Tear Sheet
=============================================

Pulls market data from yfinance and FRED, then generates:
  - chart_sp500.pdf       : S&P 500 trailing 12-month performance
  - chart_yield_curve.pdf : US Treasury yield curve (current vs 1 year ago)
  - returns_table.tex     : Sector returns table (LaTeX fragment)

Run this script before compiling handout.tex.
"""

from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import seaborn as sns

OUTPUT_DIR = Path(__file__).absolute().parent

# UChicago color palette
MAROON = "#800000"
TERRACOTTA = "#DE7C00"
DARK_GREY = "#737373"
GREEN = "#319866"
RED = "#CC0000"

# Dates
TODAY = datetime.today()
ONE_YEAR_AGO = TODAY - timedelta(days=365)
START_1Y = ONE_YEAR_AGO.strftime("%Y-%m-%d")
END = TODAY.strftime("%Y-%m-%d")
YTD_START = f"{TODAY.year}-01-01"

# Sector ETF tickers and display names
SECTOR_MAP = {
    "XLK": "Technology",
    "XLF": "Financials",
    "XLV": "Healthcare",
    "XLE": "Energy",
    "XLY": "Cons.\ Discr.",
    "XLP": "Cons.\ Staples",
    "XLI": "Industrials",
    "XLB": "Materials",
    "XLC": "Comm.\ Svcs.",
    "XLRE": "Real Estate",
    "XLU": "Utilities",
}

# FRED series for Treasury yield curve
YIELD_SERIES = {
    "DGS1MO": "1M",
    "DGS3MO": "3M",
    "DGS6MO": "6M",
    "DGS1": "1Y",
    "DGS2": "2Y",
    "DGS3": "3Y",
    "DGS5": "5Y",
    "DGS7": "7Y",
    "DGS10": "10Y",
    "DGS20": "20Y",
    "DGS30": "30Y",
}


# ---------------------------------------------------------------------------
# Data pulling
# ---------------------------------------------------------------------------

def pull_equity_data():
    """Pull S&P 500 (SPY) and sector ETF data from yfinance."""
    tickers = ["SPY"] + list(SECTOR_MAP.keys())
    df = yf.download(tickers, start=START_1Y, end=END, auto_adjust=True, progress=False)
    prices = df["Close"]
    return prices


def pull_yield_data():
    """Pull Treasury yield curve data from FRED via pandas_datareader."""
    try:
        from pandas_datareader import data as pdr

        start = (TODAY - timedelta(days=400)).strftime("%Y-%m-%d")
        df = pdr.DataReader(list(YIELD_SERIES.keys()), "fred", start, END)
        return df
    except Exception as e:
        print(f"  Warning: FRED fetch failed ({e}). Using fallback data.")
        return _fallback_yield_data()


def _fallback_yield_data():
    """Hardcoded recent yield data in case FRED is unavailable."""
    current = [4.40, 4.35, 4.30, 4.22, 4.10, 4.05, 4.00, 4.05, 4.21, 4.45, 4.52]
    past = [5.30, 5.25, 5.10, 4.70, 4.35, 4.20, 4.05, 4.10, 4.15, 4.40, 4.50]
    idx = pd.DatetimeIndex([TODAY, ONE_YEAR_AGO])
    df = pd.DataFrame(
        [current, past],
        index=idx,
        columns=list(YIELD_SERIES.keys()),
    )
    return df


# ---------------------------------------------------------------------------
# Chart 1: S&P 500 trailing performance
# ---------------------------------------------------------------------------

def create_sp500_chart(prices):
    """Create a trailing 12-month S&P 500 line chart."""
    spy = prices["SPY"].dropna()

    sns.set_theme(style="whitegrid", font_scale=1.0)
    fig, ax = plt.subplots(figsize=(5.5, 3.0))

    ax.plot(spy.index, spy.values, color=MAROON, linewidth=1.5)
    ax.fill_between(spy.index, spy.values, spy.values.min() * 0.99,
                    color=MAROON, alpha=0.08)

    ax.set_title("S&P 500 — Trailing 12 Months", fontsize=11, fontweight="bold",
                 color="#333333", loc="left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.tick_params(labelsize=8, colors=DARK_GREY)
    ax.set_xlabel("")
    ax.set_ylabel("")

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()
    out = OUTPUT_DIR / "chart_sp500.pdf"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# Chart 2: Treasury yield curve
# ---------------------------------------------------------------------------

def create_yield_curve_chart(yields_df):
    """Create yield curve chart: current vs 1 year ago."""
    labels = list(YIELD_SERIES.values())

    # Get most recent row and the row closest to 1 year ago
    df = yields_df.dropna(how="all")
    current = df.iloc[-1].values
    past_target = TODAY - timedelta(days=365)
    past_idx = df.index.get_indexer([past_target], method="nearest")[0]
    past = df.iloc[past_idx].values

    sns.set_theme(style="whitegrid", font_scale=1.0)
    fig, ax = plt.subplots(figsize=(5.5, 3.0))

    ax.plot(labels, past, color=DARK_GREY, linewidth=1.2, linestyle="--",
            marker="o", markersize=4, label="1 Year Ago", alpha=0.7)
    ax.plot(labels, current, color=TERRACOTTA, linewidth=2.0,
            marker="o", markersize=5, label="Current")

    ax.set_title("US Treasury Yield Curve", fontsize=11, fontweight="bold",
                 color="#333333", loc="left")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
    ax.tick_params(labelsize=8, colors=DARK_GREY)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.legend(fontsize=8, frameon=True, fancybox=False, edgecolor="#cccccc")

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()
    out = OUTPUT_DIR / "chart_yield_curve.pdf"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# Table: Sector returns
# ---------------------------------------------------------------------------

def _compute_return(series, start_date):
    """Compute total return from start_date to the last available date."""
    s = series.dropna()
    subset = s[s.index >= pd.Timestamp(start_date)]
    if len(subset) < 2:
        return np.nan
    return (subset.iloc[-1] / subset.iloc[0] - 1) * 100


def _fmt_return(val):
    """Format a return value with LaTeX color markup."""
    if pd.isna(val):
        return "---"
    sign = "+" if val >= 0 else ""
    color = GREEN if val >= 0 else RED
    return f"\\textcolor[HTML]{{{color.lstrip('#')}}}{{{sign}{val:.1f}}}"


def create_returns_table(prices):
    """Generate a LaTeX table fragment of sector returns."""
    rows = []

    # S&P 500 first
    spy = prices["SPY"]
    one_m = TODAY - timedelta(days=30)
    three_m = TODAY - timedelta(days=91)
    rows.append({
        "Sector": "\\textbf{S\\&P 500}",
        "1M": _fmt_return(_compute_return(spy, one_m)),
        "3M": _fmt_return(_compute_return(spy, three_m)),
        "YTD": _fmt_return(_compute_return(spy, YTD_START)),
        "1Y": _fmt_return(_compute_return(spy, START_1Y)),
    })

    # Sector ETFs
    for ticker, name in SECTOR_MAP.items():
        s = prices[ticker]
        rows.append({
            "Sector": name,
            "1M": _fmt_return(_compute_return(s, one_m)),
            "3M": _fmt_return(_compute_return(s, three_m)),
            "YTD": _fmt_return(_compute_return(s, YTD_START)),
            "1Y": _fmt_return(_compute_return(s, START_1Y)),
        })

    df = pd.DataFrame(rows)

    # Build LaTeX tabular fragment
    lines = []
    lines.append("\\begin{tabular}{@{}lrrrr@{}}")
    lines.append("\\toprule")
    lines.append("\\textbf{Sector} & \\textbf{1M} & \\textbf{3M} & \\textbf{YTD} & \\textbf{1Y} \\\\")
    lines.append("\\midrule")
    for _, row in df.iterrows():
        lines.append(f"{row['Sector']} & {row['1M']} & {row['3M']} & {row['YTD']} & {row['1Y']} \\\\")
        if row["Sector"].startswith("\\textbf"):
            lines.append("\\midrule")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")

    tex = "\n".join(lines)
    out = OUTPUT_DIR / "returns_table.tex"
    out.write_text(tex)
    print(f"  Saved {out.name}")


# ---------------------------------------------------------------------------
# Key statistics (printed to stdout for reference)
# ---------------------------------------------------------------------------

def print_key_stats(prices, yields_df):
    """Print key statistics to stdout."""
    spy_last = prices["SPY"].dropna().iloc[-1]
    spy_ytd = _compute_return(prices["SPY"], YTD_START)
    ten_y = yields_df["DGS10"].dropna().iloc[-1]

    print("\n  Key Statistics (for handout reference):")
    print(f"    S&P 500:      {spy_last:,.0f}")
    print(f"    S&P 500 YTD:  {spy_ytd:+.1f}%")
    print(f"    10Y Yield:    {ten_y:.2f}%")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Pulling equity data from yfinance...")
    prices = pull_equity_data()

    print("Pulling yield data from FRED...")
    yields_df = pull_yield_data()

    print("Creating S&P 500 chart...")
    create_sp500_chart(prices)

    print("Creating yield curve chart...")
    create_yield_curve_chart(yields_df)

    print("Creating returns table...")
    create_returns_table(prices)

    print_key_stats(prices, yields_df)

    print("\nDone. Run pdflatex/biber to compile handout.tex.")
