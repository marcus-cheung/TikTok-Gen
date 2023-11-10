"""Wrapper for tiktok api response."""
# pylint: disable=super-init-not-called, arguments-differ

from typing import Any
import requests


class DummyResponse(requests.Response):
    """Mock response from http request."""

    def __init__(self, status_code: int = 200, data: Any = None, message: str = ""):
        self.status_code = status_code
        self._json = {"data": data, "error": {"message": message}}

    def json(self) -> dict:
        """Returns mock json."""
        return self._json


class Status:
    """Wrapper for api response."""

    def __init__(self, response: requests.Response):
        self.code = response.status_code
        self.data = response.json()["data"]
        self.message = response.json()["error"]["message"]

    def __eq__(self, other: int) -> bool:
        return self.code == other

    def __str__(self) -> str:
        return self.message

    def __getitem__(self, __key: str) -> Any:
        return self.data[__key]
