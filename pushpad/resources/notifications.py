"""Notifications API resource."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Mapping, Optional, TYPE_CHECKING

from .._sentinel import _MISSING, _MissingType, remove_missing
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
    ) -> list[Notification]:
        pid = self._client._resolve_project_id(project_id)
        params = {"page": page} if page is not None else None
        response = self._client._request("GET", f"/projects/{pid}/notifications", params=params)
        payload = _ensure_api_list(response)
        return [Notification.from_api(item) for item in payload]

    def create(
        self,
        *,
        body: str,
        project_id: Optional[int] = None,
        title: str | _MissingType = _MISSING,
        target_url: str | _MissingType = _MISSING,
        icon_url: str | _MissingType = _MISSING,
        badge_url: str | _MissingType = _MISSING,
        image_url: str | _MissingType = _MISSING,
        ttl: int | _MissingType = _MISSING,
        require_interaction: bool | _MissingType = _MISSING,
        silent: bool | _MissingType = _MISSING,
        urgent: bool | _MissingType = _MISSING,
        custom_data: str | _MissingType = _MISSING,
        actions: Iterable[Mapping[str, str]] | _MissingType = _MISSING,
        starred: bool | _MissingType = _MISSING,
        send_at: datetime | str | _MissingType = _MISSING,
        custom_metrics: Iterable[str] | _MissingType = _MISSING,
        uids: Iterable[str] | _MissingType = _MISSING,
        tags: Iterable[str] | _MissingType = _MISSING,
    ) -> NotificationCreateResult:
        pid = self._client._resolve_project_id(project_id)
        payload = remove_missing(
            body=body,
            title=title,
            target_url=target_url,
            icon_url=icon_url,
            badge_url=badge_url,
            image_url=image_url,
            ttl=ttl,
            require_interaction=require_interaction,
            silent=silent,
            urgent=urgent,
            custom_data=custom_data,
            starred=starred,
            send_at=send_at,
            actions=actions,
            custom_metrics=custom_metrics,
            uids=uids,
            tags=tags,
        )
        response = self._client._request("POST", f"/projects/{pid}/notifications", json=payload)
        data = _ensure_api_object(response)
        return NotificationCreateResult.from_api(data)

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
