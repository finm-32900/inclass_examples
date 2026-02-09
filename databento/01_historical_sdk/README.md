# 01 Historical SDK

Fetch historical trade data using Databento's Python SDK. This is the simplest way to get market data — a straightforward request-response pattern.

## What you'll learn

- How to create a `db.Historical` client
- How to check query cost **before** fetching data (free metadata call)
- How to guard against accidental charges with a cost check
- How to fetch trades with `timeseries.get_range`
- How to convert results to a pandas DataFrame

## Setup

```bash
pip install -r requirements.txt
```

Make sure `DATABENTO_API_KEY` is set in the repo-root `.env` file.

## Run

```bash
python 01_get_trades.py
```

The script checks the estimated cost first and only fetches data if the query is free. If the cost is non-zero it prints the estimate and exits, so you never spend money by accident.

## Key points

- `metadata.get_cost()` is free and tells you the estimated cost before you commit
- `timeseries.get_range()` returns a `DBNStore` object that converts to DataFrames
- The SDK automatically reads `DATABENTO_API_KEY` from the environment
- Prices are automatically scaled to human-readable floats (the raw wire format uses fixed-point integers)

## Try it

- Change the symbol from `ES.FUT` to `NQ.FUT` (Nasdaq futures)
- Try a different schema: replace `trades` with `ohlcv-1m` for 1-minute bars
- Increase the `limit` and re-run to see how cost scales
