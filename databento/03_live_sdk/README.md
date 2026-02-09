# 03 Live SDK

Stream live market data using Databento's Python SDK. Unlike the historical examples (request-response), live data uses a **persistent connection** with a subscribe-iterate pattern.

## What you'll learn

- How to create a `db.Live` client
- The subscribe-iterate pattern for streaming data
- How to set a timeout so the script stops automatically
- Difference between historical (request-response) and live (streaming) workflows

## Setup

```bash
pip install -r requirements.txt
```

Make sure `DATABENTO_API_KEY` is set in the repo-root `.env` file.

## Run

```bash
python live_trades.py
```

The script subscribes to ES trades and prints them for 10 seconds, then stops.

**Note:** This requires the market to be open (CME Globex hours: Sunday 5 PM – Friday 4 PM CT, with a daily break 4–5 PM CT). Outside market hours you may see no trades.

## Key points

- `db.Live()` opens a persistent connection to Databento's gateway
- `.subscribe()` tells the server what data to send
- Iterating over the client (`for record in client`) blocks until data arrives
- The SDK handles the underlying TCP connection, authentication, and binary decoding

## Try it

- Change the schema from `trades` to `mbp-1` for top-of-book quotes
- Subscribe to multiple symbols: `symbols=["ES.FUT", "NQ.FUT"]`
- Remove the timeout and use Ctrl+C to stop manually
