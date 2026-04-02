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
