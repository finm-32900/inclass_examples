#!/usr/bin/env bash
#
# Stream live ES trades via raw TCP socket — no SDK, no HTTP.
#
# This demonstrates the wire protocol that db.Live() wraps:
#   1. TCP connect to Databento gateway
#   2. CRAM authentication (HMAC-SHA256)
#   3. Subscribe to a data feed
#   4. Read streaming binary/text data
#
# Usage:
#   export DATABENTO_API_KEY="db-..."
#   bash live_raw_tcp.sh
#
# Requires: bash with /dev/tcp support, openssl or shasum

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────
export $(grep DATABENTO_API_KEY ../../.env)
: "${DATABENTO_API_KEY:?Set DATABENTO_API_KEY in your environment}"

GATEWAY_HOST="lsg1.databento.com"
GATEWAY_PORT=13000
DATASET="GLBX.MDP3"
TIMEOUT=20

# ── Portable SHA-256 HMAC ────────────────────────────────────────
# macOS uses `shasum -a 256`, Linux uses `sha256sum`
hmac_sha256() {
    local key="$1"
    local data="$2"
    echo -n "$data" | openssl dgst -sha256 -hmac "$key" | awk '{print $NF}'
}

# ── Open TCP connection ─────────────────────────────────────────
echo "Connecting to ${GATEWAY_HOST}:${GATEWAY_PORT}..."
exec 3<>/dev/tcp/${GATEWAY_HOST}/${GATEWAY_PORT}

# Read the server greeting (contains the CRAM challenge)
read -r greeting <&3
echo "[recv] $greeting"

# ── CRAM Authentication ─────────────────────────────────────────
# The greeting contains a challenge string. We compute HMAC-SHA256
# of the challenge using our API key, then send it back.

# Extract the challenge bucket_id from the greeting
# Greeting format varies; we need to parse the challenge
challenge=$(echo "$greeting" | grep -oP 'cram=\K[^|]+' || echo "$greeting")

echo "Computing HMAC-SHA256 of challenge..."
auth_response=$(hmac_sha256 "$DATABENTO_API_KEY" "$challenge")

# Send authentication
auth_msg="auth=${auth_response}|dataset=${DATASET}|encoding=json"
echo "[send] $auth_msg"
echo "$auth_msg" >&3

# Read auth result
read -r auth_result <&3
echo "[recv] $auth_result"

# ── Subscribe ────────────────────────────────────────────────────
sub_msg="subscribe|schema=trades|stype_in=parent|symbols=ES.FUT"
echo "[send] $sub_msg"
echo "$sub_msg" >&3

# Signal that we're done sending control messages
echo "[send] start_session"
echo "start_session" >&3

# ── Read streaming data ─────────────────────────────────────────
echo
echo "Streaming raw data for ${TIMEOUT}s..."
echo "============================================"

# Read for TIMEOUT seconds, then stop
end_time=$((SECONDS + TIMEOUT))
count=0

while [ $SECONDS -lt $end_time ]; do
    if read -r -t 2 line <&3; then
        echo "[recv] $line"
        count=$((count + 1))
    fi
done

# ── Cleanup ──────────────────────────────────────────────────────
exec 3<&-
echo
echo "Connection closed. Received $count messages."
echo
echo "Compare this with 03_live_sdk/live_trades.py — same data,"
echo "but the SDK handles auth, decoding, and reconnection for you."
