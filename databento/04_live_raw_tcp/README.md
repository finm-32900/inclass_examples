# 04 Live Raw TCP

Stream live market data using a raw TCP socket — no SDK, no HTTP. This is the most dramatic SDK vs raw contrast in the series.

## Why TCP, not HTTP?

HTTP is request-response: you ask, the server answers, the connection closes. Live market data requires **continuous streaming** — the server pushes new trades as they happen. This needs a persistent TCP connection.

The SDK's `db.Live()` wraps this TCP protocol. Here we do it manually.

## Protocol Sequence

```
Client                              Server (gateway)
  |                                    |
  |  ── TCP connect ──────────────>    |
  |  <── greeting + challenge ─────    |   Server sends CRAM challenge
  |  ── auth (HMAC-SHA256) ───────>    |   Client proves it has the API key
  |  <── auth result ──────────────    |   Server confirms
  |  ── subscribe ────────────────>    |   Client requests data feed
  |  <── data records ─────────────    |   Server streams continuously
  |  <── data records ─────────────    |
  |  ...                               |
```

## CRAM Authentication

CRAM (Challenge-Response Authentication Mechanism):
1. Server sends a random challenge string
2. Client computes `HMAC-SHA256(challenge, api_key)`
3. Client sends the hex digest back
4. Server verifies — if correct, connection is authenticated

This avoids sending the API key over the wire.

## Setup

Export your API key:
```bash
export DATABENTO_API_KEY="db-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Run

```bash
bash live_raw_tcp.sh
```

The script connects, authenticates, subscribes, and prints raw messages for 20 seconds. Messages are prefixed with `[recv]` or `[send]` so you can see the protocol direction.

**Note:** Requires CME Globex to be open and bash with `/dev/tcp` support.

## Key points

- Live data uses TCP, not HTTP, because HTTP can't stream continuously
- CRAM auth means the API key never travels over the wire in plaintext
- The raw wire protocol uses pipe-delimited messages
- The SDK handles all of this automatically — connection, auth, decoding, reconnection

## Try it

- Read the `[recv]` and `[send]` prefixes to trace the protocol handshake
- Compare the raw output with `03_live_sdk/live_trades.py` — same data, very different developer experience
