"""
Stream live ES trades using the Databento Python SDK.

The SDK handles the TCP connection, CRAM authentication, and binary
decoding automatically. Compare with 04_live_raw_tcp/ to see what
happens under the hood.

Usage:
    python live_trades.py

Note: Requires CME Globex to be open (Sun 5 PM – Fri 4 PM CT).
"""

from dotenv import load_dotenv
from pathlib import Path
import signal
import databento as db

# Load API key from repo-root .env
repo_root = Path(__file__).resolve().parents[2]
load_dotenv(repo_root / ".env")

# Stop after 10 seconds so the script doesn't run forever
TIMEOUT_SECONDS = 10


def on_timeout(signum, frame):
    raise SystemExit(f"\nTimeout after {TIMEOUT_SECONDS}s — stopping.")


signal.signal(signal.SIGALRM, on_timeout)
signal.alarm(TIMEOUT_SECONDS)

# Create a live client (reads DATABENTO_API_KEY from environment)
client = db.Live()

# Subscribe to ES trades on CME Globex
client.subscribe(
    dataset="GLBX.MDP3",
    schema="trades",
    stype_in="parent",
    symbols="ES.FUT",
)

print(f"Streaming ES trades for {TIMEOUT_SECONDS} seconds...")
print("=" * 60)

count = 0
for record in client:
    # Each record is a TradeMsg with auto-scaled prices
    print(f"  {record}")
    count += 1

print(f"\nReceived {count} trade records.")
