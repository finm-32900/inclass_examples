"""
Search for futures products by keyword in the WRDS Datastream library.

Provides a reusable search_products() function that queries
wrds_contract_info for products whose name matches a keyword.

Demonstrates searches for:
    - Commodities: crude oil, gold, corn
    - Treasuries: treasury, t-note, t-bond
    - Equity indices: s&p, nasdaq

Usage:
    python 03_search_products.py
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
def search_products(db, keyword):
    """
    Search for futures products by keyword.

    Parameters
    ----------
    db : wrds.Connection
        Active WRDS connection.
    keyword : str
        Search term (case-insensitive substring match on contrname).

    Returns
    -------
    pd.DataFrame
        Matching products with contrcode, contrname, num_contracts,
        earliest_start, and latest_trade.
    """
    # The %% in the SQL is Python string escaping for % in the LIKE pattern.
    kw = keyword.lower().replace("'", "''")
    query = f"""
    SELECT contrcode, contrname,
           COUNT(*) AS num_contracts,
           MIN(startdate) AS earliest_start,
           MAX(lasttrddate) AS latest_trade
    FROM {LIBRARY}.wrds_contract_info
    WHERE LOWER(contrname) LIKE '%%{kw}%%'
    GROUP BY contrcode, contrname
    ORDER BY num_contracts DESC
    """
    return db.raw_sql(query)

def print_results(keyword, df):
    """Print search results in a readable table."""
    print(f"\n  Search: '{keyword}'")
    if df.empty:
        print("    No matches found.")
        return
    print(f"  {'Product':<55s} {'Code':>6s} {'Contracts':>10s} {'From':>12s} {'To':>12s}")
    print("  " + "-" * 100)
    for _, row in df.iterrows():
        earliest = str(row["earliest_start"])[:10]
        latest = str(row["latest_trade"])[:10]
        print(f"  {row['contrname']:<55s} {int(row['contrcode']):>6} "
              f"{int(row['num_contracts']):>10} {earliest:>12s} {latest:>12s}")
    print(f"  ({len(df)} matches)")

# %%
# ── Connect ──────────────────────────────────────────────────────
print("=" * 60)
print("Connecting to WRDS")
print("=" * 60)
db = wrds.Connection(wrds_username=WRDS_USERNAME)
print()

# %%
# ── Step 1: Commodity searches ───────────────────────────────────
# Multiple contrcodes may match the same underlying (e.g. "crude oil" returns NYMEX WTI,
# ICE Brent, E-mini, etc.). The "Contracts" column helps identify the primary series —
# usually the one with the most contracts.
print("=" * 60)
print("Commodity Futures")
print("=" * 60)

for kw in ["crude oil", "gold", "corn", "natural gas", "wheat"]:
    results = search_products(db, kw)
    print_results(kw, results)
print()

# %%
# ── Step 2: Treasury / rates searches ────────────────────────────
# Treasury futures often have duplicate contrcodes from different eras (pre-2016 vs
# post-2016 electronic). Pick the one whose "To" date extends to the present.
print("=" * 60)
print("Treasury / Rates Futures")
print("=" * 60)

for kw in ["treasury", "t-note", "t-bond"]:
    results = search_products(db, kw)
    print_results(kw, results)
print()

# %%
# ── Step 3: Equity index searches ────────────────────────────────
print("=" * 60)
print("Equity Index Futures")
print("=" * 60)

for kw in ["s&p", "nasdaq", "dow", "russell"]:
    results = search_products(db, kw)
    print_results(kw, results)
print()

# %%
# ── Cleanup ──────────────────────────────────────────────────────
db.close()
print("Done. Connection closed.")

# %%
