"""Projects API resource."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

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

    def create(self, **project: Any) -> Project:
        response = self._client._request("POST", "/projects", json=project)
        payload = _ensure_api_object(response)
        return Project.from_api(payload)

    def get(self, id: int) -> Project:
        if id is None:
            raise ValueError("id is required")
        response = self._client._request("GET", f"/projects/{id}")
        payload = _ensure_api_object(response)
        return Project.from_api(payload)

    def update(self, id: int, **project: Any) -> Project:
        if id is None:
            raise ValueError("id is required")
        response = self._client._request("PATCH", f"/projects/{id}", json=project)
        payload = _ensure_api_object(response)
        return Project.from_api(payload)

    def delete(self, id: int) -> None:
        if id is None:
            raise ValueError("id is required")
        self._client._request("DELETE", f"/projects/{id}")
        return None
