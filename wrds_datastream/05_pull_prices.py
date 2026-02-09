"""
Fetch settlement prices for specific futures contracts.

Demonstrates the complete two-step data retrieval workflow:
    1. Find recent contracts via wrds_contract_info
    2. Pull daily prices from wrds_fut_contract

Shows this for both a commodity (Gold) and a Treasury future
(10-Year US Treasury Note). Includes data quality checks.

Data is kept small via date filter (>= 2024-01-01) and LIMIT.

Usage:
    python 05_pull_prices.py
"""

import wrds
import pandas as pd

from decouple import Config, RepositoryEnv
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
config = Config(RepositoryEnv(repo_root / ".env"))
WRDS_USERNAME = config("WRDS_USERNAME")

LIBRARY = "tr_ds_fut"
DATE_CUTOFF = "2024-01-01"

# Products to fetch prices for
PRODUCTS = {
    "Gold (100 OZ)": 2020,
    "10 YEAR US TREASURY NOTE": 458,  # CBOT, active through 2025+
}

# ── Connect ──────────────────────────────────────────────────────
print("=" * 60)
print("Connecting to WRDS")
print("=" * 60)
db = wrds.Connection(wrds_username=WRDS_USERNAME)
print()

for product_name, contrcode in PRODUCTS.items():
    print("=" * 60)
    print(f"{product_name}  (contrcode={contrcode})")
    print("=" * 60)

    # ── Step 1: Find recent contracts ─────────────────────────────
    # Two-step workflow: first find contracts (metadata), then fetch prices (separate table).
    query = f"""
    SELECT futcode, contrcode, contrname, contrdate, startdate, lasttrddate
    FROM {LIBRARY}.wrds_contract_info
    WHERE contrcode = {contrcode}
      AND lasttrddate >= '{DATE_CUTOFF}'
    ORDER BY contrdate
    """
    contracts = db.raw_sql(query)

    if contracts.empty:
        print(f"  No contracts found after {DATE_CUTOFF}")
        print()
        continue

    print(f"\n  Contracts with last trade >= {DATE_CUTOFF}: {len(contracts)}")
    for _, row in contracts.iterrows():
        print(f"    futcode={int(row['futcode']):>8}  delivery={row['contrdate']}  "
              f"last_trade={str(row['lasttrddate'])[:10]}")
    print()

    # ── Step 2: Pull daily settlement prices ──────────────────────
    # settlement = exchange-published daily settlement price, used for marking positions.
    # open_ has a trailing underscore because "open" is a Python reserved word.
    futcodes = contracts["futcode"].tolist()
    futcode_list = ",".join(str(int(f)) for f in futcodes)

    query = f"""
    SELECT futcode, date_, settlement, open_, high, low, volume
    FROM {LIBRARY}.wrds_fut_contract
    WHERE futcode IN ({futcode_list})
      AND date_ >= '{DATE_CUTOFF}'
    ORDER BY futcode, date_
    """
    prices = db.raw_sql(query)

    if prices.empty:
        print("  No price data found.")
        print()
        continue

    prices["date_"] = pd.to_datetime(prices["date_"])

    print(f"  Price records fetched: {len(prices)}")
    print(f"  Date range: {prices['date_'].min().date()} to {prices['date_'].max().date()}")
    print(f"  Unique contracts with data: {prices['futcode'].nunique()}")
    print()

    # ── Step 3: Data quality checks ───────────────────────────────
    # Gold prices are in USD per troy ounce. T-Note prices are in points + 32nds
    # (e.g. 112.296875 = 112 + 9.5/32). The wide range across products is expected.
    print("  Data Quality:")
    print(f"    Settlement nulls: {prices['settlement'].isna().sum()} / {len(prices)}")
    print(f"    Volume nulls:     {prices['volume'].isna().sum()} / {len(prices)}")

    valid_prices = prices["settlement"].dropna()
    if not valid_prices.empty:
        print(f"    Settlement range:  {valid_prices.min():.4f} to {valid_prices.max():.4f}")
        print(f"    Settlement mean:   {valid_prices.mean():.4f}")
    print()

    # ── Step 4: Show sample data ──────────────────────────────────
    print("  First 10 rows:")
    with pd.option_context("display.max_columns", None, "display.width", 120):
        print(prices.head(10).to_string(index=False))
    print()

    print("  Last 10 rows:")
    with pd.option_context("display.max_columns", None, "display.width", 120):
        print(prices.tail(10).to_string(index=False))
    print()

# ── Cleanup ──────────────────────────────────────────────────────
db.close()
print("Done. Connection closed.")
