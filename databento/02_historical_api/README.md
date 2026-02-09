# 02 Historical API (Raw HTTP)

Fetch the same historical trade data from example 01, but using raw HTTP requests instead of the SDK. This reveals what the SDK does under the hood.

## What you'll learn

- How to call Databento's REST API directly with curl
- How HTTP Basic Auth works (API key as username, empty password)
- What the raw JSON response looks like before SDK processing
- Side-by-side comparison of SDK vs raw HTTP in one script

## Setup

```bash
pip install -r requirements.txt
```

For the curl script, export your API key:
```bash
export DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Run

```bash
# Pure curl — see the raw HTTP response
bash 01_curl_trades.sh

# Python side-by-side comparison
python 02_curl_vs_sdk.py
```

## Reading the output

Each JSON line is one trade record. Here's how to read the fields:

| Field | Example | Meaning |
|-------|---------|---------|
| `ts_recv` | `1722470400079196344` | Exchange receive timestamp (nanoseconds since Unix epoch) |
| `hd.ts_event` | `1722470400078950957` | Matching-engine event timestamp (ns). ~2024-08-01 00:00:00 UTC |
| `hd.rtype` | `0` | Record type: `0` = MBP-0 / trade |
| `hd.publisher_id` | `1` | Venue ID (`1` = CME) |
| `hd.instrument_id` | `118` | Numeric instrument ID for this contract |
| `action` | `"T"` | Message action: `T` = Trade |
| `side` | `"B"` / `"A"` | Aggressor side: `B` = buyer initiated, `A` = seller initiated |
| `depth` | `0` | Book depth level (always 0 for trades) |
| `price` | `5587750000000` | **Fixed-point integer** — multiply by 1e-9 → **$5,587.75** |
| `size` | `5` | Number of contracts traded |
| `flags` | `0` | Bit flags (e.g., last message in packet) |
| `ts_in_delta` | `14913` | Capture latency: `ts_recv - ts_event` in nanoseconds (~15 μs) |
| `sequence` | `45877799` | Exchange sequence number (detect gaps / ordering) |

**Price conversion:** Databento stores prices as fixed-point integers to avoid floating-point rounding. Divide by 1e9:
- `5587750000000 × 1e-9 = $5,587.75`
- `5587500000000 × 1e-9 = $5,587.50`

The Python SDK does this conversion automatically.

## curl flags explained

| Flag | Meaning |
|------|---------|
| `-s` | **Silent mode.** Suppresses the progress bar and error messages, so you only see the response body. |
| `-u "${DATABENTO_API_KEY}:"` | **HTTP Basic Auth.** Sets the `Authorization` header using `username:password`. The API key is the username; the trailing colon means the password is empty. curl base64-encodes `key:` and sends `Authorization: Basic <encoded>`. |
| `-X POST` | **HTTP method.** Specifies the request method (see below). |
| `-d "key=value"` | **Data / form field.** Sends a key-value pair in the request body as `application/x-www-form-urlencoded`. Each `-d` flag adds another field. When `-d` is present, curl implies `-X POST`, so the explicit `-X POST` is technically redundant but makes intent clear. |

### HTTP methods

Every HTTP request includes a **method** (also called a "verb") that tells the server what kind of operation you intend. The most common ones:

| Method | Purpose | Body? | Example |
|--------|---------|-------|---------|
| `GET` | **Read** a resource. This is what your browser sends when you visit a URL. Parameters go in the query string (`?key=value`). | No | `GET /v0/metadata.list_datasets` |
| `POST` | **Send data** to the server to create or query something. Parameters go in the request body. | Yes | `POST /v0/timeseries.get_range` (our curl example) |
| `PUT` | **Replace** a resource entirely with new data. | Yes | `PUT /users/42` (update full user record) |
| `PATCH` | **Partially update** a resource (only the fields you send). | Yes | `PATCH /users/42` (update just the email) |
| `DELETE` | **Remove** a resource. | Rarely | `DELETE /users/42` |

**Why POST here?** Databento's query has many parameters (dataset, symbols, date range, schema, etc.). Packing all of that into a URL query string would be unwieldy, so the API uses POST with form-encoded body fields instead. This is a common pattern for "read" endpoints that take complex inputs — even though the request is conceptually a read, POST is used because it supports a request body.

## Key points

- The REST API lives at `https://hist.databento.com/v0/timeseries.get_range`
- Authentication is HTTP Basic: your API key is the username, password is empty
- Raw JSON responses include prices as **fixed-point integers** (multiply by 1e-9)
- The SDK automatically handles auth, decoding, and price scaling

## Try it

- In `02_curl_vs_sdk.py`, compare the `price` field: raw integer vs SDK float
