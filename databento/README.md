# Databento: SDK vs API

This directory teaches how to pull market data from [Databento](https://databento.com/) while illustrating the difference between using a **Python SDK** and making **raw API calls** (HTTP/curl or TCP).

Each of Databento's two client types — Historical and Live — is shown both ways so you can see what the SDK abstracts away.

## Cost Warning

Databento charges per query. Every script in this directory uses `limit=10` to keep costs negligible. The SDK examples call `metadata.get_cost` (free) before fetching data and skip the download if the cost is non-zero, so you never spend money by accident.

## Setup

1. Install the Python package:
   ```bash
   pip install databento python-dotenv pandas requests
   ```

2. Set your API key in the repo-root `.env` file:
   ```
   DATABENTO_API_KEY=db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   The `.env.example` at repo root already has this variable defined.

3. For bash scripts, export the key in your shell:
   ```bash
   export DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

## Dataset

All examples use **GLBX.MDP3** (CME Globex), which covers E-mini S&P 500 futures (ES) and other CME products. Students have subscriptions to this dataset.

## Examples

| Directory | Topic | Protocol |
|-----------|-------|----------|
| `01_historical_sdk` | Fetch historical trades via Python SDK | SDK |
| `02_historical_api` | Same query via curl and HTTP requests | HTTP REST |
| `03_live_sdk` | Stream live trades via Python SDK | SDK |
| `04_live_raw_tcp` | Same stream via raw TCP socket | TCP |
| `05_schemas_and_symbology` | Data schemas and symbol types | SDK |
| `06_treasury_futures_brief` | Treasury futures market brief (charts + table) | SDK |

Work through them in order. Each pair (01+02, 03+04) shows the SDK first, then the raw protocol underneath.

## SDK vs API — What's the Difference?

| | SDK (`databento` package) | Raw API (curl / TCP) |
|---|---|---|
| **Auth** | Pass key to constructor or set env var | HTTP Basic Auth or CRAM challenge |
| **Data format** | Auto-decoded to DataFrames | Raw JSON or binary DBN |
| **Streaming** | Iterator / callback | Persistent TCP socket |
| **Price scaling** | Automatic (human-readable floats) | Raw fixed-point integers (multiply by 1e-9) |
| **Error handling** | Python exceptions | HTTP status codes / socket errors |
