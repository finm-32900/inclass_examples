"""
Fetch historical ES trades via the Databento Python SDK.

Demonstrates the simplest SDK workflow:
    1. Create a Historical client
    2. Check estimated cost (free metadata call)
    3. Fetch trades only if the cost is zero
    4. Convert to a pandas DataFrame

Usage:
    python 01_get_trades.py
"""

from dotenv import load_dotenv
from pathlib import Path
import databento as db

# Load API key from repo-root .env
repo_root = Path(__file__).resolve().parents[2]
load_dotenv(repo_root / ".env")

# The SDK reads DATABENTO_API_KEY from the environment automatically
client = db.Historical()

# --- Query parameters (shared between cost check and data pull) ---
query = dict(
    dataset="GLBX.MDP3",
    symbols=["ES.FUT"],
    stype_in="parent",
    schema="trades",
    start="2024-08-01",
    end="2024-08-02",
    limit=10,
)

# --- Step 1: Check cost (free metadata call) ---
cost = client.metadata.get_cost(**query)

print(f"Estimated cost: ${cost:.4f}")
print()
print("Query parameters:")
print(f"  Dataset:  {query['dataset']} (CME Globex)")
print(f"  Symbol:   {query['symbols'][0]} (E-mini S&P 500, all expirations)")
print(f"  Schema:   {query['schema']}")
print(f"  Period:   {query['start']} to {query['end']}")
print(f"  Limit:    {query['limit']} records")
print()

# --- Step 2: Fetch data only if the query is free ---
if cost > 0:
    print(f"Skipping fetch — estimated cost is ${cost:.4f}. "
          "Adjust parameters or remove this guard if you want to proceed.")
    raise SystemExit(0)

data = client.timeseries.get_range(**query)

# Convert to pandas DataFrame — prices are automatically scaled
df = data.to_df()

print("ES Trades (via SDK)")
print("=" * 60)
print(df.to_string())
print()
print(f"Columns: {list(df.columns)}")
print(f"Records: {len(df)}")
