"""
Compare futures term structures: commodity vs. Treasury.

For a single recent reference date, pull all active contracts and
their settlement prices for two products:
    - Gold (commodity)
    - 10-Year US Treasury Note (rates)

Displays term structure tables (delivery month vs. settlement price)
and discusses backwardation/contango for commodities vs. yield curve
shape for rates.

Very small data pull — one date only.

Usage:
    python 06_term_structure.py
"""

import wrds
import pandas as pd

from decouple import Config, RepositoryEnv
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
config = Config(RepositoryEnv(repo_root / ".env"))
WRDS_USERNAME = config("WRDS_USERNAME")

LIBRARY = "tr_ds_fut"

# Products to compare
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

# ── Step 1: Find a recent date with good data ────────────────────
# Use the most recent available date across both products
print("=" * 60)
print("Finding most recent trading date with data")
print("=" * 60)

query = f"""
SELECT MAX(date_) AS max_date
FROM {LIBRARY}.wrds_fut_contract
"""
result = db.raw_sql(query)
ref_date = str(result["max_date"].iloc[0])[:10]
print(f"  Most recent date in database: {ref_date}")
print()

for product_name, contrcode in PRODUCTS.items():
    print("=" * 60)
    print(f"Term Structure: {product_name}  (contrcode={contrcode})")
    print(f"Reference date: {ref_date}")
    print("=" * 60)

    # ── Step 2: Find all contracts active on the reference date ───
    # JOIN links wrds_contract_info (which contract) with wrds_fut_contract (what price)
    # on futcode, filtering to a single date to get a snapshot across all active maturities.
    query = f"""
    SELECT ci.futcode, ci.contrdate, ci.lasttrddate,
           fc.settlement, fc.volume
    FROM {LIBRARY}.wrds_contract_info ci
    JOIN {LIBRARY}.wrds_fut_contract fc
      ON ci.futcode = fc.futcode
    WHERE ci.contrcode = {contrcode}
      AND fc.date_ = '{ref_date}'
      AND fc.settlement IS NOT NULL
    ORDER BY ci.contrdate
    """
    term = db.raw_sql(query)

    if term.empty:
        # Try one day earlier if no data on the exact date
        query_fallback = f"""
        SELECT MAX(fc.date_) AS max_date
        FROM {LIBRARY}.wrds_contract_info ci
        JOIN {LIBRARY}.wrds_fut_contract fc
          ON ci.futcode = fc.futcode
        WHERE ci.contrcode = {contrcode}
          AND fc.settlement IS NOT NULL
        """
        fallback = db.raw_sql(query_fallback)
        alt_date = str(fallback["max_date"].iloc[0])[:10]
        print(f"  No data on {ref_date}. Using latest available: {alt_date}")

        query = f"""
        SELECT ci.futcode, ci.contrdate, ci.lasttrddate,
               fc.settlement, fc.volume
        FROM {LIBRARY}.wrds_contract_info ci
        JOIN {LIBRARY}.wrds_fut_contract fc
          ON ci.futcode = fc.futcode
        WHERE ci.contrcode = {contrcode}
          AND fc.date_ = '{alt_date}'
          AND fc.settlement IS NOT NULL
        ORDER BY ci.contrdate
        """
        term = db.raw_sql(query)

    if term.empty:
        print("  No term structure data available.")
        print()
        continue

    # ── Step 3: Display term structure ────────────────────────────
    print(f"\n  Active contracts: {len(term)}")
    print()
    print(f"  {'Delivery':<12s} {'Futcode':>8s} {'Settlement':>12s} {'Volume':>10s} {'Last Trade':>12s}")
    print("  " + "-" * 60)
    for _, row in term.iterrows():
        vol = f"{int(row['volume']):>10}" if pd.notna(row["volume"]) else "       N/A"
        print(f"  {str(row['contrdate']):<12s} {int(row['futcode']):>8} "
              f"{row['settlement']:>12.4f} {vol} {str(row['lasttrddate'])[:10]:>12s}")
    print()

    # ── Step 4: Term structure analysis ───────────────────────────
    # Contango (futures > spot) is normal for storable commodities due to storage costs;
    # backwardation signals supply tightness. For Treasuries, the "term structure" here is
    # across delivery months of the same underlying (the 10Y note), not across different
    # maturities — it reflects carry and financing costs, not the yield curve.
    prices = term["settlement"].values
    if len(prices) >= 2:
        front = prices[0]
        back = prices[-1]
        spread = back - front
        pct_spread = (back / front - 1) * 100

        print("  Term Structure Shape:")
        print(f"    Front month:  {front:.4f}")
        print(f"    Back month:   {back:.4f}")
        print(f"    Spread:       {spread:+.4f} ({pct_spread:+.2f}%)")

        if contrcode == 2020:
            shape = "contango" if spread > 0 else "backwardation"
            print(f"    Structure:    {shape}")
            print(f"    (Commodities: contango = futures > spot, "
                  f"backwardation = futures < spot)")
        else:
            shape = "upward sloping" if spread > 0 else "downward sloping (inverted)"
            print(f"    Structure:    {shape}")
            print(f"    (Treasuries: price reflects yield expectations — "
                  f"lower price = higher yield)")
    print()

# ── Cleanup ──────────────────────────────────────────────────────
db.close()
print("Done. Connection closed.")
