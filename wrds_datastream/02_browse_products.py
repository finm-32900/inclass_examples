"""
Browse all available futures products in the WRDS Datastream library.

Two approaches to discovering what's available:
    1. List all distinct products (contrcode + contrname) alphabetically
    2. Aggregate view: contract counts and date ranges per product
    3. Browse the continuous series catalog (wrds_cseries_info)

No prior knowledge of specific products is needed — this script
shows everything in the library so you can decide what to explore.

Usage:
    python 02_browse_products.py
"""
# %%
import wrds
import pandas as pd

from decouple import Config, RepositoryEnv
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
config = Config(RepositoryEnv(repo_root / ".env"))
WRDS_USERNAME = config("WRDS_USERNAME")

LIBRARY = "tr_ds_fut"

# %%
# ── Connect ──────────────────────────────────────────────────────
print("=" * 60)
print("Connecting to WRDS")
print("=" * 60)
db = wrds.Connection(wrds_username=WRDS_USERNAME)
print()

# %%
# ── Step 1: All distinct products (alphabetical) ─────────────────
# contrcode is the product-level ID (e.g. all Gold contracts share one contrcode),
# while futcode (not shown here) is the individual contract ID for each expiry.
print("=" * 60)
print("All Futures Products (alphabetical by name)")
print("=" * 60)

query = f"""
SELECT DISTINCT contrcode, contrname
FROM {LIBRARY}.wrds_contract_info
ORDER BY contrname
"""
products = db.raw_sql(query)

for _, row in products.iterrows():
    print(f"  contrcode={int(row['contrcode']):>6}  {row['contrname']}")
print(f"\n  Total distinct products: {len(products)}")
print()

# %%
# ── Step 2: Aggregate view (contract counts + date ranges) ───────
# "Contracts" count = total individual expiries (e.g. Gold with 598 contracts
# means 598 separate delivery months have traded historically).
print("=" * 60)
print("Products by Number of Contracts (most contracts first)")
print("=" * 60)

query = f"""
SELECT contrcode, contrname,
       COUNT(*) AS num_contracts,
       MIN(startdate) AS earliest_start,
       MAX(lasttrddate) AS latest_trade
FROM {LIBRARY}.wrds_contract_info
GROUP BY contrcode, contrname
ORDER BY num_contracts DESC
"""
summary = db.raw_sql(query)

print(f"\n  {'Product':<55s} {'Code':>6s} {'Contracts':>10s} {'From':>12s} {'To':>12s}")
print("  " + "-" * 100)
for _, row in summary.iterrows():
    earliest = str(row["earliest_start"])[:10]
    latest = str(row["latest_trade"])[:10]
    print(f"  {row['contrname']:<55s} {int(row['contrcode']):>6} "
          f"{int(row['num_contracts']):>10} {earliest:>12s} {latest:>12s}")
print(f"\n  Total products: {len(summary)}")
print()

# %%
# ── Step 3: Continuous series catalog ────────────────────────────
# Continuous series are pre-rolled price series — useful if you want a single
# time series per product without managing individual contract rolls yourself.
print("=" * 60)
print("Continuous Series Catalog (wrds_cseries_info)")
print("=" * 60)

cseries = db.get_table(library=LIBRARY, table="wrds_cseries_info")
print(f"  Rows: {len(cseries)}")
print(f"  Columns: {list(cseries.columns)}")
print()

with pd.option_context("display.max_columns", None, "display.width", 120):
    print(cseries.to_string())
print()

# %%
# ── Cleanup ──────────────────────────────────────────────────────
db.close()
print("Done. Connection closed.")
