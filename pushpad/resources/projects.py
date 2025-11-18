"""Projects API resource."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .._sentinel import _MISSING, _MissingType, remove_missing
from ..pushpad import _ensure_api_list, _ensure_api_object
from ..types import Project

if TYPE_CHECKING:  # pragma: no cover - only used for typing
    from ..pushpad import Pushpad


class ProjectsResource:
    def __init__(self, client: "Pushpad") -> None:
        self._client = client

    def all(self) -> list[Project]:
        response = self._client._request("GET", "/projects")
        payload = _ensure_api_list(response)
        return [Project.from_api(item) for item in payload]

    def create(
        self,
        *,
        sender_id: int,
        name: str,
        website: str,
        icon_url: str | _MissingType = _MISSING,
        badge_url: str | _MissingType = _MISSING,
        notifications_ttl: int | _MissingType = _MISSING,
        notifications_require_interaction: bool | _MissingType = _MISSING,
        notifications_silent: bool | _MissingType = _MISSING,
    ) -> Project:
        payload = remove_missing(
            sender_id=sender_id,
            name=name,
            website=website,
            icon_url=icon_url,
            badge_url=badge_url,
            notifications_ttl=notifications_ttl,
            notifications_require_interaction=notifications_require_interaction,
            notifications_silent=notifications_silent,
        )
        response = self._client._request("POST", "/projects", json=payload)
        data = _ensure_api_object(response)
        return Project.from_api(data)

    def get(self, id: int) -> Project:
        if id is None:
            raise ValueError("id is required")
        response = self._client._request("GET", f"/projects/{id}")
        payload = _ensure_api_object(response)
        return Project.from_api(payload)

    def update(
        self,
        id: int,
        *,
        name: str | _MissingType = _MISSING,
        website: str | _MissingType = _MISSING,
        icon_url: str | _MissingType = _MISSING,
        badge_url: str | _MissingType = _MISSING,
        notifications_ttl: int | _MissingType = _MISSING,
        notifications_require_interaction: bool | _MissingType = _MISSING,
        notifications_silent: bool | _MissingType = _MISSING,
    ) -> Project:
        if id is None:
            raise ValueError("id is required")
        payload = remove_missing(
            name=name,
            website=website,
            icon_url=icon_url,
            badge_url=badge_url,
            notifications_ttl=notifications_ttl,
            notifications_require_interaction=notifications_require_interaction,
            notifications_silent=notifications_silent,
        )
        response = self._client._request("PATCH", f"/projects/{id}", json=payload)
        data = _ensure_api_object(response)
        return Project.from_api(data)

    def delete(self, id: int) -> None:
        if id is None:
            raise ValueError("id is required")
        self._client._request("DELETE", f"/projects/{id}")
        return None
