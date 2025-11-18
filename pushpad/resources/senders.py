"""Senders API resource."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .._sentinel import _MISSING, _MissingType, remove_missing
from ..pushpad import _ensure_api_list, _ensure_api_object
from ..types import Sender

if TYPE_CHECKING:  # pragma: no cover - only used for typing
    from ..pushpad import Pushpad


class SendersResource:
    def __init__(self, client: "Pushpad") -> None:
        self._client = client

    def all(self) -> list[Sender]:
        response = self._client._request("GET", "/senders")
        payload = _ensure_api_list(response)
        return [Sender.from_api(item) for item in payload]

    def create(
        self,
        *,
        name: str,
        vapid_private_key: str | None | _MissingType = _MISSING,
        vapid_public_key: str | None | _MissingType = _MISSING,
    ) -> Sender:
        payload = remove_missing(
            name=name,
            vapid_private_key=vapid_private_key,
            vapid_public_key=vapid_public_key,
        )
        response = self._client._request("POST", "/senders", json=payload)
        data = _ensure_api_object(response)
        return Sender.from_api(data)

    def get(self, id: int) -> Sender:
        if id is None:
            raise ValueError("id is required")
        response = self._client._request("GET", f"/senders/{id}")
        payload = _ensure_api_object(response)
        return Sender.from_api(payload)

    def update(
        self,
        id: int,
        *,
        name: str | None | _MissingType = _MISSING,
    ) -> Sender:
        if id is None:
            raise ValueError("id is required")
        payload = remove_missing(name=name)
        response = self._client._request("PATCH", f"/senders/{id}", json=payload)
        data = _ensure_api_object(response)
        return Sender.from_api(data)

    def delete(self, id: int) -> None:
        if id is None:
            raise ValueError("id is required")
        self._client._request("DELETE", f"/senders/{id}")
        return None
