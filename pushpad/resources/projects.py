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

    def get(self, id: int):
        if id is None:
            raise ValueError("id is required")
        return self._client._request("GET", f"/projects/{id}")

    def update(self, id: int, **project: Any):
        if id is None:
            raise ValueError("id is required")
        return self._client._request("PATCH", f"/projects/{id}", json=project)

    def delete(self, id: int) -> bool:
        if id is None:
            raise ValueError("id is required")
        self._client._request("DELETE", f"/projects/{id}")
        return True
