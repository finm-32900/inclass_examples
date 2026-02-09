"""
Survey the WRDS Datastream Futures library (tr_ds_fut).

Connects to WRDS and explores the library structure:
    1. Lists all tables in the library
    2. Describes column schemas for the key tables
    3. Shows row counts
    4. Samples first few rows from each table

This is the starting point for working with WRDS Datastream futures data.
The library is poorly documented, so hands-on exploration is essential.

Usage:
    python 01_explore_library.py
"""

import wrds
import pandas as pd

from decouple import Config, RepositoryEnv
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
config = Config(RepositoryEnv(repo_root / ".env"))
WRDS_USERNAME = config("WRDS_USERNAME")

LIBRARY = "tr_ds_fut"

# Key tables to inspect:
#   wrds_cseries_info  — catalog of pre-built continuous (rolled) futures series
#   wrds_contract_info — metadata for individual contracts (main lookup table)
#   wrds_fut_contract  — daily OHLCV (Open, High, Low, Close, and Volume) + settlement prices (main data table, ~168M rows)
#   dsfutcalcserval    — daily prices for the continuous series (~80M rows)
KEY_TABLES = [
    "wrds_cseries_info",
    "wrds_contract_info",
    "wrds_fut_contract",
    "dsfutcalcserval",
]

# ── Connect ──────────────────────────────────────────────────────
print("=" * 60)
print("Connecting to WRDS")
print("=" * 60)
db = wrds.Connection(wrds_username=WRDS_USERNAME)
print()

# ── Step 1: List all tables ──────────────────────────────────────
# The dsfut* tables are raw Refinitiv tables; the wrds_* tables are WRDS-curated and easier to use.
print("=" * 60)
print(f"Tables in '{LIBRARY}'")
print("=" * 60)
tables = db.list_tables(library=LIBRARY)
for t in tables:
    print(f"  {t}")
print(f"\n  Total: {len(tables)} tables")
print()

# ── Step 2: Describe key tables ──────────────────────────────────
for table in KEY_TABLES:
    print("=" * 60)
    print(f"Schema: {LIBRARY}.{table}")
    print("=" * 60)
    try:
        cols = db.describe_table(library=LIBRARY, table=table)
        print(cols.to_string())
    except Exception as e:
        print(f"  ERROR: {e}")
    print()

# ── Step 3: Row counts ──────────────────────────────────────────
print("=" * 60)
print("Row Counts")
print("=" * 60)
for table in KEY_TABLES:
    try:
        count = db.get_row_count(library=LIBRARY, table=table)
        print(f"  {table:30s} {count:>12,} rows")
    except Exception as e:
        print(f"  {table:30s} ERROR: {e}")
print()

# ── Step 4: Sample rows ─────────────────────────────────────────
# What to look for in the sample rows:
#   ldb values: FUT=US Financial, COM=US Commodity, LIF=Non-US Financial, CIE=Non-US Commodity
#   contrdate format: MMYY (e.g. "0624" = June 2024)
#   trdstatcode: A=Active, D=Discontinued
# In wrds_fut_contract, most columns (p, pb, pa, wa, ca, yd, hm, ha, mt, la, lm, oa, up) will
# be None for most contracts. The core columns are: settlement, open_, high, low, volume, openinterest.
for table in KEY_TABLES:
    print("=" * 60)
    print(f"Sample rows: {LIBRARY}.{table}")
    print("=" * 60)
    try:
        df = db.get_table(library=LIBRARY, table=table, obs=5)
        with pd.option_context("display.max_columns", None, "display.width", 120):
            print(df.to_string())
    except Exception as e:
        print(f"  ERROR: {e}")
    print()

# ── Cleanup ──────────────────────────────────────────────────────
db.close()
print("Done. Connection closed.")
