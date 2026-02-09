"""
Reference: Pull all 21 commodity futures + US Treasury futures.

Capstone script that pulls settlement prices for:
    - 21 commodity futures from Szymanowska et al. (2014)
    - 4 US Treasury futures (2Y, 5Y, 10Y, 30Y)

Uses a short time window (2024 only) to keep pulls fast.
Saves results to DataFrames and prints summary statistics.
Adapt the date range and product codes for your own projects.

Usage:
    python 07_pull_commodities_and_treasuries.py
"""

import wrds
import pandas as pd

from decouple import Config, RepositoryEnv
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
config = Config(RepositoryEnv(repo_root / ".env"))
WRDS_USERNAME = config("WRDS_USERNAME")

LIBRARY = "tr_ds_fut"
DATE_START = "2024-01-01"
DATE_END = "2024-12-31"

# ── Commodity product codes ──────────────────────────────────────
# From Szymanowska et al. (2014) / commodities research project.
# NOTE: Some contrcodes were discontinued before 2024 (e.g. Platinum=2087
# ended 2016, Soybeans=396 ended 2018). These will show "NO DATA" for
# recent date ranges. Use 03_search_products.py to find active alternatives,
# or change DATE_START/DATE_END to an earlier period.
COMMODITY_CODES = {
    # Energy
    "Crude Oil": 1986,
    "Heating Oil": 2091,
    "Natural Gas": 2029,
    # Meats
    "Live Cattle": 2675,
    "Feeder Cattle": 2676,
    "Lean Hogs": 3126,
    # Metals
    "Gold": 2020,
    "Silver": 2026,
    "Platinum": 2087,
    # Grains
    "Corn": 3247,
    "Wheat": 3250,
    "Oats": 3256,
    "Rough Rice": 3847,
    # Oilseeds
    "Soybeans": 396,
    "Soybean Meal": 430,
    "Soybean Oil": 379,
    # Softs
    "Coffee": 2038,
    "Orange Juice": 2060,
    "Cocoa": 2032,
    # Industrial Materials
    "Cotton": 1992,
    "Lumber": 2036,
}

# ── US Treasury futures product codes ────────────────────────────
# Discovered via 03_search_products.py
# Note: some products have multiple contrcodes for different eras/exchanges.
# These are the CBOT codes with data through 2025+.
TREASURY_CODES = {
    "2Y T-Note": 463,
    "5Y T-Note": 452,
    "10Y T-Note": 458,
    "30Y T-Bond": 448,
}


# General pattern: query wrds_contract_info to get futcode list, then query
# wrds_fut_contract with those futcodes. This two-table JOIN is the fundamental
# workflow for all WRDS Datastream futures data.
def pull_product_prices(db, contrcode, date_start, date_end):
    """
    Pull settlement prices for all contracts of a product within a date range.

    Parameters
    ----------
    db : wrds.Connection
        Active WRDS connection.
    contrcode : int
        Product contract code.
    date_start, date_end : str
        Date range filter (YYYY-MM-DD).

    Returns
    -------
    pd.DataFrame
        Columns: futcode, contrdate, date_, settlement.
    """
    # Step 1: find contracts active in the date range
    query = f"""
    SELECT futcode, contrdate
    FROM {LIBRARY}.wrds_contract_info
    WHERE contrcode = {contrcode}
      AND lasttrddate >= '{date_start}'
      AND startdate <= '{date_end}'
    ORDER BY contrdate
    """
    contracts = db.raw_sql(query)

    if contracts.empty:
        return pd.DataFrame()

    futcodes = contracts["futcode"].tolist()
    futcode_list = ",".join(str(int(f)) for f in futcodes)

    # Step 2: pull prices
    query = f"""
    SELECT futcode, date_, settlement
    FROM {LIBRARY}.wrds_fut_contract
    WHERE futcode IN ({futcode_list})
      AND date_ BETWEEN '{date_start}' AND '{date_end}'
    ORDER BY futcode, date_
    """
    prices = db.raw_sql(query)

    if prices.empty:
        return pd.DataFrame()

    # Merge in contrdate
    prices = prices.merge(contracts[["futcode", "contrdate"]], on="futcode", how="left")
    prices["date_"] = pd.to_datetime(prices["date_"])
    return prices


# ── Connect ──────────────────────────────────────────────────────
print("=" * 60)
print("Connecting to WRDS")
print("=" * 60)
db = wrds.Connection(wrds_username=WRDS_USERNAME)
print()

# ── Pull Commodity Futures ───────────────────────────────────────
print("=" * 60)
print(f"Pulling {len(COMMODITY_CODES)} Commodity Futures ({DATE_START} to {DATE_END})")
print("=" * 60)

commodity_frames = []
for name, code in COMMODITY_CODES.items():
    df = pull_product_prices(db, code, DATE_START, DATE_END)
    if not df.empty:
        df["product"] = name
        df["contrcode"] = code
        commodity_frames.append(df)
        n_contracts = df["futcode"].nunique()
        n_records = len(df)
        print(f"  {name:<20s} (code={code:>4})  contracts={n_contracts:>3}  records={n_records:>6}")
    else:
        print(f"  {name:<20s} (code={code:>4})  NO DATA")

if commodity_frames:
    commodities_df = pd.concat(commodity_frames, ignore_index=True)
    print(f"\n  Total commodity records: {len(commodities_df):,}")
    print(f"  Unique products with data: {commodities_df['product'].nunique()}")
else:
    commodities_df = pd.DataFrame()
    print("\n  WARNING: No commodity data retrieved.")
print()

# ── Pull Treasury Futures ────────────────────────────────────────
print("=" * 60)
print(f"Pulling {len(TREASURY_CODES)} Treasury Futures ({DATE_START} to {DATE_END})")
print("=" * 60)

treasury_frames = []
for name, code in TREASURY_CODES.items():
    df = pull_product_prices(db, code, DATE_START, DATE_END)
    if not df.empty:
        df["product"] = name
        df["contrcode"] = code
        treasury_frames.append(df)
        n_contracts = df["futcode"].nunique()
        n_records = len(df)
        print(f"  {name:<20s} (code={code:>4})  contracts={n_contracts:>3}  records={n_records:>6}")
    else:
        print(f"  {name:<20s} (code={code:>4})  NO DATA")

if treasury_frames:
    treasuries_df = pd.concat(treasury_frames, ignore_index=True)
    print(f"\n  Total treasury records: {len(treasuries_df):,}")
    print(f"  Unique products with data: {treasuries_df['product'].nunique()}")
else:
    treasuries_df = pd.DataFrame()
    print("\n  WARNING: No treasury data retrieved.")
print()

# ── Summary Statistics ───────────────────────────────────────────
# Price units vary by product (Gold=USD/oz, Crude=USD/barrel, T-Notes=points, etc.),
# so the wide settlement range across products is expected.
print("=" * 60)
print("Summary Statistics")
print("=" * 60)

for label, df in [("Commodities", commodities_df), ("Treasuries", treasuries_df)]:
    if df.empty:
        print(f"\n  {label}: No data")
        continue

    print(f"\n  {label}:")
    print(f"    Records:     {len(df):,}")
    print(f"    Date range:  {df['date_'].min().date()} to {df['date_'].max().date()}")
    print(f"    Products:    {df['product'].nunique()}")
    print(f"    Contracts:   {df['futcode'].nunique()}")

    valid = df["settlement"].dropna()
    print(f"    Settlement nulls:  {df['settlement'].isna().sum()} / {len(df)}")
    if not valid.empty:
        print(f"    Settlement range:  {valid.min():.4f} to {valid.max():.4f}")

    # Per-product summary
    print(f"\n    Per-product breakdown:")
    print(f"    {'Product':<20s} {'Records':>8s} {'Contracts':>10s} {'Min Price':>12s} {'Max Price':>12s}")
    print("    " + "-" * 66)
    for product in sorted(df["product"].unique()):
        sub = df[df["product"] == product]
        s = sub["settlement"].dropna()
        min_p = f"{s.min():.2f}" if not s.empty else "N/A"
        max_p = f"{s.max():.2f}" if not s.empty else "N/A"
        print(f"    {product:<20s} {len(sub):>8} {sub['futcode'].nunique():>10} {min_p:>12s} {max_p:>12s}")
print()

# ── Cleanup ──────────────────────────────────────────────────────
db.close()
print("Done. Connection closed.")
print(f"\nDataFrames available: commodities_df ({len(commodities_df)} rows), "
      f"treasuries_df ({len(treasuries_df)} rows)")
