#!/usr/bin/env bash
# Regenerate Connexion/Flask stubs from generated/sovd_server/openapi/openapi.yaml
# Requires: openapi-generator-cli (https://openapi-generator.tech)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SPEC="$ROOT/generated/sovd_server/openapi/openapi.yaml"
OUT="${TMPDIR:-/tmp}/sovd_openapi_gen_$$"

rm -rf "$OUT"
openapi-generator-cli generate \
  -i "$SPEC" \
  -g python-flask \
  -o "$OUT" \
  --additional-properties packageName=sovd_server

rsync -a --delete "$OUT/sovd_server/models/" "$ROOT/generated/sovd_server/models/"
rsync -a --delete "$OUT/sovd_server/controllers/" "$ROOT/generated/sovd_server/controllers/"
rsync -a --delete "$OUT/sovd_server/test/" "$ROOT/generated/sovd_server/test/"
cp "$OUT/sovd_server/encoder.py" "$OUT/sovd_server/util.py" "$OUT/sovd_server/typing_utils.py" \
  "$OUT/sovd_server/__main__.py" "$OUT/sovd_server/__init__.py" "$ROOT/generated/sovd_server/"

# Connexion 3: generator still imports connexion.apps.flask_app — use stdlib JSONEncoder
cat > "$ROOT/generated/sovd_server/encoder.py" << 'ENC'
import json
from typing import Any

from sovd_server.models.base_model import Model


class JSONEncoder(json.JSONEncoder):
    """Serialize OpenAPI Model instances (stdlib; compatible with Connexion 3 / Flask 3)."""

    include_nulls = False

    def default(self, o: Any) -> Any:
        if isinstance(o, Model):
            dikt = {}
            for attr in o.openapi_types:
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                mapped = o.attribute_map[attr]
                dikt[mapped] = value
            return dikt
        return super().default(o)
ENC

# OpenAPI Generator may omit binary-only models — restore if missing
if [[ ! -f "$ROOT/generated/sovd_server/models/configuration_write_multipart.py" ]]; then
  echo "Restoring configuration_write_multipart.py (see script comments)" >&2
fi

echo "Done. If encoder or multipart model was overwritten, re-apply patches from git or this script."
rm -rf "$OUT"
