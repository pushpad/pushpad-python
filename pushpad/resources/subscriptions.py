"""Subscriptions API resource."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - only used for typing
    from ..pushpad import Pushpad


class SubscriptionsResource:
    def __init__(self, client: "Pushpad") -> None:
        self._client = client

    def _build_filters(self, values: Dict[str, Any]) -> Dict[str, Any]:
        params = dict(values)
        uids = params.pop("uids", None)
        tags = params.pop("tags", None)

        def _normalize(value: Optional[Iterable[str]]):
            if value is None:
                return None
            if isinstance(value, (list, tuple, set)):
                return list(value)
            return [value]

        normalized_uids = _normalize(uids)
        normalized_tags = _normalize(tags)
        if normalized_uids is not None:
            params["uids[]"] = normalized_uids
        if normalized_tags is not None:
            params["tags[]"] = normalized_tags
        return {k: v for k, v in params.items() if v is not None}

    def all(
        self,
        *,
        project_id: Optional[int] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        uids: Optional[Iterable[str]] = None,
        tags: Optional[Iterable[str]] = None,
        **filters: Any,
    ):
        pid = self._client._resolve_project_id(project_id)
        params = self._build_filters(
            {"page": page, "per_page": per_page, "uids": uids, "tags": tags, **filters}
        )
        return self._client._request("GET", f"/projects/{pid}/subscriptions", params=params)

    def count(
        self,
        *,
        project_id: Optional[int] = None,
        uids: Optional[Iterable[str]] = None,
        tags: Optional[Iterable[str]] = None,
        **filters: Any,
    ) -> int:
        pid = self._client._resolve_project_id(project_id)
        params = self._build_filters({"uids": uids, "tags": tags, **filters})
        params.setdefault("per_page", 1)
        response = self._client._request(
            "GET",
            f"/projects/{pid}/subscriptions",
            params=params,
            raw=True,
        )
        total = response.headers.get("X-Total-Count")
        if total is not None:
            try:
                return int(total)
            except ValueError:
                pass
        try:
            data = response.json()
        except ValueError:
            data = []
        return len(data)

    def create(self, *, project_id: Optional[int] = None, **subscription: Any):
        pid = self._client._resolve_project_id(project_id)
        return self._client._request("POST", f"/projects/{pid}/subscriptions", json=subscription)

    def get(self, id: int, *, project_id: Optional[int] = None):
        if id is None:
            raise ValueError("id is required")
        pid = self._client._resolve_project_id(project_id)
        return self._client._request("GET", f"/projects/{pid}/subscriptions/{id}")

    def update(self, id: int, *, project_id: Optional[int] = None, **subscription: Any):
        if id is None:
            raise ValueError("id is required")
        pid = self._client._resolve_project_id(project_id)
        return self._client._request("PATCH", f"/projects/{pid}/subscriptions/{id}", json=subscription)

    def delete(self, id: int, *, project_id: Optional[int] = None) -> bool:
        if id is None:
            raise ValueError("id is required")
        pid = self._client._resolve_project_id(project_id)
        self._client._request("DELETE", f"/projects/{pid}/subscriptions/{id}")
        return True
