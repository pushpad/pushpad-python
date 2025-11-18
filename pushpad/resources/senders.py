"""Senders API resource."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - only used for typing
    from ..pushpad import Pushpad


class SendersResource:
    def __init__(self, client: "Pushpad") -> None:
        self._client = client

    def all(self):
        return self._client._request("GET", "/senders")

    def create(self, **sender: Any):
        return self._client._request("POST", "/senders", json=sender)

    def get(self, id: int):
        if id is None:
            raise ValueError("id is required")
        return self._client._request("GET", f"/senders/{id}")

    def update(self, id: int, **sender: Any):
        if id is None:
            raise ValueError("id is required")
        return self._client._request("PATCH", f"/senders/{id}", json=sender)

    def delete(self, id: int) -> bool:
        if id is None:
            raise ValueError("id is required")
        self._client._request("DELETE", f"/senders/{id}")
        return True
