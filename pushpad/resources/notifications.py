"""Notifications API resource."""

from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from ..pushpad import _ensure_api_list, _ensure_api_object
from ..types import Notification, NotificationCreateResult

if TYPE_CHECKING:  # pragma: no cover - only used for typing
    from ..pushpad import Pushpad


class NotificationsResource:
    def __init__(self, client: "Pushpad") -> None:
        self._client = client

    def all(
        self,
        *,
        project_id: Optional[int] = None,
        page: Optional[int] = None,
        **filters: Any,
    ) -> list[Notification]:
        pid = self._client._resolve_project_id(project_id)
        params = {k: v for k, v in {"page": page, **filters}.items() if v is not None}
        response = self._client._request("GET", f"/projects/{pid}/notifications", params=params)
        payload = _ensure_api_list(response)
        return [Notification.from_api(item) for item in payload]

    def create(self, *, project_id: Optional[int] = None, **notification: Any) -> NotificationCreateResult:
        pid = self._client._resolve_project_id(project_id)
        response = self._client._request("POST", f"/projects/{pid}/notifications", json=notification)
        payload = _ensure_api_object(response)
        return NotificationCreateResult.from_api(payload)

    def get(self, id: int) -> Notification:
        if id is None:
            raise ValueError("id is required")
        response = self._client._request("GET", f"/notifications/{id}")
        payload = _ensure_api_object(response)
        return Notification.from_api(payload)

    def cancel(self, id: int) -> None:
        if id is None:
            raise ValueError("id is required")
        self._client._request("DELETE", f"/notifications/{id}/cancel")
        return None
