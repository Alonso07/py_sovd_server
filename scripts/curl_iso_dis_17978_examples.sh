#!/usr/bin/env bash
# Manual checks against a running SOVD server — mirrors ISO DIS 17978-3 / sovd-api.yaml paths.
# Usage:
#   ./scripts/curl_iso_dis_17978_examples.sh
#   BASE_URL=http://127.0.0.1:9000 ./scripts/curl_iso_dis_17978_examples.sh
#
# Start the server first, e.g.:
#   poetry run sovd-server
# or: PYTHONPATH=src poetry run python src/sovd_server/enhanced_server.py

set -euo pipefail
BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"
ENTITY_PATH="${ENTITY_PATH:-/engine/ecu}"

echo "=== GET data resource (DataResource shape: id + data) ==="
curl -sS "${BASE_URL}${ENTITY_PATH}/data/ECUVoltage" | python3 -m json.tool | head -40

echo ""
echo "=== PUT data resource (DataResourceWrite: { \"data\": { ... } }) ==="
curl -sS -X PUT "${BASE_URL}${ENTITY_PATH}/data/ECUVoltage" \
  -H "Content-Type: application/json" \
  -d '{"data":{"value":12.5}}' | python3 -m json.tool | head -30

echo ""
echo "=== POST start operation execution (expect HTTP 202 + Location) ==="
RESP=$(curl -sS -D /tmp/iso_hdr.txt -o /tmp/iso_body.json -w "%{http_code}" \
  -X POST "${BASE_URL}${ENTITY_PATH}/operations/ECU-RESET/executions" \
  -H "Content-Type: application/json" \
  -d '{}')
echo "status=$RESP"
grep -i '^[Ll]ocation:' /tmp/iso_hdr.txt || true
python3 -m json.tool < /tmp/iso_body.json

EXEC_ID=$(python3 -c "import json; print(json.load(open('/tmp/iso_body.json'))['id'])")
echo ""
echo "=== GET execution list ==="
curl -sS "${BASE_URL}${ENTITY_PATH}/operations/ECU-RESET/executions" | python3 -m json.tool

echo ""
echo "=== GET execution status ==="
curl -sS "${BASE_URL}${ENTITY_PATH}/operations/ECU-RESET/executions/${EXEC_ID}" | python3 -m json.tool

echo ""
echo "=== DELETE execution (terminate) — expect 204 empty body ==="
curl -sS -o /tmp/del_out -w "status=%{http_code}\n" \
  -X DELETE "${BASE_URL}${ENTITY_PATH}/operations/ECU-RESET/executions/${EXEC_ID}"
test ! -s /tmp/del_out && echo "(no body)"

echo ""
echo "=== GET execution after terminate (status terminated) ==="
curl -sS "${BASE_URL}${ENTITY_PATH}/operations/ECU-RESET/executions/${EXEC_ID}" | python3 -m json.tool

echo "Done."
