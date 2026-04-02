from typing import Dict  # noqa: F401

from sovd_server.models.base_model import Model
from sovd_server import util


class ConfigurationWriteMultipart(Model):
    """Multipart configuration write (OpenAPI format: binary)."""

    def __init__(self, data=None, signature=None):  # noqa: E501
        self.openapi_types = {
            "data": str,
            "signature": str,
        }

        self.attribute_map = {
            "data": "data",
            "signature": "signature",
        }

        self._data = data
        self._signature = signature

    @classmethod
    def from_dict(cls, dikt) -> "ConfigurationWriteMultipart":
        return util.deserialize_model(dikt, cls)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, signature):
        self._signature = signature
