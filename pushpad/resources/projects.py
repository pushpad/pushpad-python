"""Projects API resource."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - only used for typing
    from ..pushpad import Pushpad


class ProjectsResource:
    def __init__(self, client: "Pushpad") -> None:
        self._client = client

    def all(self):
        return self._client._request("GET", "/projects")

    def create(self, **project: Any):
        return self._client._request("POST", "/projects", json=project)

    def get(self, project_id: int):
        if project_id is None:
            raise ValueError("project_id is required")
        return self._client._request("GET", f"/projects/{project_id}")

    def update(self, project_id: int, **project: Any):
        if project_id is None:
            raise ValueError("project_id is required")
        return self._client._request("PATCH", f"/projects/{project_id}", json=project)

    def delete(self, project_id: int) -> bool:
        if project_id is None:
            raise ValueError("project_id is required")
        self._client._request("DELETE", f"/projects/{project_id}")
        return True
