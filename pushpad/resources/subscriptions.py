"""Subscriptions API resource."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, TYPE_CHECKING

from .._sentinel import _MISSING, _MissingType, remove_missing
from ..pushpad import _ensure_api_list, _ensure_api_object
from ..types import Subscription

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
    ) -> list[Subscription]:
        pid = self._client._resolve_project_id(project_id)
        params = self._build_filters(
            {"page": page, "per_page": per_page, "uids": uids, "tags": tags, **filters}
        )
        response = self._client._request("GET", f"/projects/{pid}/subscriptions", params=params)
        payload = _ensure_api_list(response)
        return [Subscription.from_api(item) for item in payload]

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
        response = self._client._raw_request(
            "GET",
            f"/projects/{pid}/subscriptions",
            params=params,
        )
        total = response.headers.get("X-Total-Count")
        if total is None:
            raise ValueError("response missing X-Total-Count header")
        return int(total)

    def create(
        self,
        *,
        project_id: Optional[int] = None,
        endpoint: str | None | _MissingType = _MISSING,
        p256dh: str | None | _MissingType = _MISSING,
        auth: str | None | _MissingType = _MISSING,
        uid: str | None | _MissingType = _MISSING,
        tags: Iterable[str] | str | None | _MissingType = _MISSING,
    ) -> Subscription:
        pid = self._client._resolve_project_id(project_id)
        payload = remove_missing(
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
            uid=uid,
            tags=tags,
        )
        response = self._client._request("POST", f"/projects/{pid}/subscriptions", json=payload)
        data = _ensure_api_object(response)
        return Subscription.from_api(data)

    def get(self, id: int, *, project_id: Optional[int] = None) -> Subscription:
        if id is None:
            raise ValueError("id is required")
        pid = self._client._resolve_project_id(project_id)
        response = self._client._request("GET", f"/projects/{pid}/subscriptions/{id}")
        payload = _ensure_api_object(response)
        return Subscription.from_api(payload)

    def update(
        self,
        id: int,
        *,
        project_id: Optional[int] = None,
        uid: str | None | _MissingType = _MISSING,
        tags: Iterable[str] | str | None | _MissingType = _MISSING,
    ) -> Subscription:
        if id is None:
            raise ValueError("id is required")
        pid = self._client._resolve_project_id(project_id)
        payload = remove_missing(
            uid=uid,
            tags=tags,
        )
        response = self._client._request("PATCH", f"/projects/{pid}/subscriptions/{id}", json=payload)
        data = _ensure_api_object(response)
        return Subscription.from_api(data)

    def delete(self, id: int, *, project_id: Optional[int] = None) -> None:
        if id is None:
            raise ValueError("id is required")
        pid = self._client._resolve_project_id(project_id)
        self._client._request("DELETE", f"/projects/{pid}/subscriptions/{id}")
        return None
