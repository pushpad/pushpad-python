"""Notifications API resource."""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - only used for typing
    from ..pushpad import Pushpad


class NotificationsResource:
    def __init__(self, client: "Pushpad") -> None:
        self._client = client

    def all(self, *, project_id: Optional[int] = None, page: Optional[int] = None, **filters: Any):
        pid = self._client._resolve_project_id(project_id)
        params = {k: v for k, v in {"page": page, **filters}.items() if v is not None}
        return self._client._request("GET", f"/projects/{pid}/notifications", params=params)

    def create(self, *, project_id: Optional[int] = None, **notification: Any):
        pid = self._client._resolve_project_id(project_id)
        return self._client._request("POST", f"/projects/{pid}/notifications", json=notification)

    def get(self, notification_id: int):
        if notification_id is None:
            raise ValueError("notification_id is required")
        return self._client._request("GET", f"/notifications/{notification_id}")

    def cancel(self, notification_id: int) -> bool:
        if notification_id is None:
            raise ValueError("notification_id is required")
        self._client._request("DELETE", f"/notifications/{notification_id}/cancel")
        return True
