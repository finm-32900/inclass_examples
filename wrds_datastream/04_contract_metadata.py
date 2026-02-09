"""
Inspect contract-level metadata for specific futures products.

Given contrcode values discovered in 02/03, pull all individual contracts
for two products — one commodity (Gold) and one Treasury future (10-Year
US Treasury Note) — and examine:
    1. Total contracts and delivery date range
    2. First and last 5 contracts
    3. Delivery month patterns
    4. Contract lifecycle duration (start → last trade)

Teaches the one-to-many relationship: contrcode → futcode.
Each contrcode (product) has many futcodes (individual contracts).

Usage:
    python 04_contract_metadata.py
"""

import wrds
import pandas as pd

from decouple import Config, RepositoryEnv
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
config = Config(RepositoryEnv(repo_root / ".env"))
WRDS_USERNAME = config("WRDS_USERNAME")

LIBRARY = "tr_ds_fut"

# Products to inspect (contrcode values from 02/03)
# Note: some products have multiple contrcodes (e.g. different exchanges
# or eras). Use 03_search_products.py to find the one with recent data.
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

    # ── Step 1: Pull all contracts ────────────────────────────────
    query = f"""
    SELECT futcode, contrcode, contrname, contrdate, startdate, lasttrddate
    FROM {LIBRARY}.wrds_contract_info
    WHERE contrcode = {contrcode}
    ORDER BY contrdate
    """
    info = db.raw_sql(query)

    if info.empty:
        print(f"  No contracts found for contrcode={contrcode}")
        print()
        continue

    info["startdate"] = pd.to_datetime(info["startdate"])
    info["lasttrddate"] = pd.to_datetime(info["lasttrddate"])

    print(f"\n  Contract name: {info['contrname'].iloc[0]}")
    print(f"  Total contracts: {len(info)}")
    print(f"  Delivery date range: {info['contrdate'].min()} to {info['contrdate'].max()}")
    print(f"  Data start range: {info['startdate'].min().date()} to {info['startdate'].max().date()}")
    print(f"  Last trade range: {info['lasttrddate'].min().date()} to {info['lasttrddate'].max().date()}")
    print()

    # ── Step 2: First and last 5 contracts ────────────────────────
    # contrdate format: MMYY where MM=delivery month, YY=year (e.g. "0624" = June 2024).
    # Sorted alphabetically, so "0100" (Jan 2000) comes before "0624" (Jun 2024).
    print("  First 5 contracts:")
    for _, row in info.head(5).iterrows():
        print(f"    futcode={int(row['futcode']):>8}  delivery={row['contrdate']}  "
              f"start={str(row['startdate'])[:10]}  last_trade={str(row['lasttrddate'])[:10]}")

    print("  ...")
    print("  Last 5 contracts:")
    for _, row in info.tail(5).iterrows():
        print(f"    futcode={int(row['futcode']):>8}  delivery={row['contrdate']}  "
              f"start={str(row['startdate'])[:10]}  last_trade={str(row['lasttrddate'])[:10]}")
    print()

    # ── Step 3: Delivery month patterns ───────────────────────────
    # Gold trades every month (12 deliveries/year), while T-Notes trade quarterly
    # (Mar/Jun/Sep/Dec = 4 deliveries/year). Look for this in the contrdate values.
    print("  Delivery month pattern (sample of contrdate values):")
    sample_dates = info["contrdate"].unique()
    for d in sample_dates[:12]:
        print(f"    {d}")
    if len(sample_dates) > 12:
        print(f"    ... ({len(sample_dates)} unique delivery dates total)")
    print()

    # ── Step 4: Contract lifecycle duration ───────────────────────
    # startdate = when WRDS begins recording prices (not necessarily first trade date).
    # lasttrddate = contract expiration.
    info["lifecycle_days"] = (info["lasttrddate"] - info["startdate"]).dt.days
    valid = info[info["lifecycle_days"] > 0]

    if not valid.empty:
        print("  Contract lifecycle (start → last trade date):")
        print(f"    Min:    {valid['lifecycle_days'].min()} days")
        print(f"    Median: {valid['lifecycle_days'].median():.0f} days")
        print(f"    Max:    {valid['lifecycle_days'].max()} days")
        print(f"    Mean:   {valid['lifecycle_days'].mean():.0f} days")
    print()

# ── Cleanup ──────────────────────────────────────────────────────
db.close()
print("Done. Connection closed.")
