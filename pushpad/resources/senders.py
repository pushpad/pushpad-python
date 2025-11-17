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

    def get(self, sender_id: int):
        if sender_id is None:
            raise ValueError("sender_id is required")
        return self._client._request("GET", f"/senders/{sender_id}")

    def update(self, sender_id: int, **sender: Any):
        if sender_id is None:
            raise ValueError("sender_id is required")
        return self._client._request("PATCH", f"/senders/{sender_id}", json=sender)

    def delete(self, sender_id: int) -> bool:
        if sender_id is None:
            raise ValueError("sender_id is required")
        self._client._request("DELETE", f"/senders/{sender_id}")
        return True
