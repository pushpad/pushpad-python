"""High level Pushpad API client."""

from __future__ import annotations

import hmac
from datetime import date, datetime, timezone
from hashlib import sha256
from typing import Any, Dict, Iterable, MutableMapping, Optional

try:  # pragma: no cover - exercised when requests is available
    import requests  # type: ignore
    RequestException = requests.RequestException
except ModuleNotFoundError:  # pragma: no cover - fallback for limited envs/tests
    requests = None  # type: ignore

    class RequestException(Exception):
        """Fallback exception used when the requests package is not installed."""

        pass

from ._version import __version__
from .exceptions import PushpadAPIError, PushpadClientError

JSONDict = MutableMapping[str, Any]


class APIObject(dict):
    """Dictionary that also exposes keys as attributes."""

    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError as exc:  # pragma: no cover - defensive
            raise AttributeError(item) from exc


def _wrap_response(data: Any) -> Any:
    if isinstance(data, dict):
        return APIObject({key: _wrap_response(value) for key, value in data.items()})
    if isinstance(data, list):
        return [_wrap_response(item) for item in data]
    return data


def _isoformat(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _serialize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return _isoformat(value)
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _serialize_value(val) for key, val in value.items() if val is not None}
    if isinstance(value, (list, tuple, set)):
        return [_serialize_value(item) for item in value if item is not None]
    return value


def _prepare_payload(data: Optional[JSONDict]) -> Optional[JSONDict]:
    if not data:
        return None
    return _serialize_value(dict(data))  # type: ignore[arg-type]


def _prepare_params(params: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not params:
        return None
    serialized = _serialize_value(dict(params))
    assert isinstance(serialized, dict)
    return serialized  # type: ignore[return-value]


class Pushpad:
    """High level client used to interact with the Pushpad REST API."""

    DEFAULT_BASE_URL = "https://pushpad.xyz/api/v1"

    def __init__(
        self,
        auth_token: str,
        project_id: Optional[int] = None,
        *,
        base_url: Optional[str] = None,
        timeout: int = 10,
        session: Optional[Any] = None,
    ) -> None:
        if not auth_token:
            raise ValueError("auth_token is required")
        self.auth_token = auth_token
        self.project_id = project_id
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        if session is not None:
            self._session = session
        else:
            if requests is None:
                raise RuntimeError("The 'requests' package is required unless you provide a session instance.")
            self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.auth_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": f"pushpad-python/{__version__}",
            }
        )

        self.notifications = NotificationsResource(self)
        self.subscriptions = SubscriptionsResource(self)
        self.projects = ProjectsResource(self)
        self.senders = SendersResource(self)

    def __enter__(self) -> "Pushpad":
        return self

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        close = getattr(self._session, "close", None)
        if callable(close):
            close()

    def signature_for(self, data: str) -> str:
        """Return the HMAC signature for a user identifier."""
        return hmac.new(self.auth_token.encode(), data.encode(), sha256).hexdigest()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[JSONDict] = None,
        raw: bool = False,
    ):
        url = f"{self.base_url}{path}"
        try:
            response = self._session.request(
                method,
                url,
                params=_prepare_params(params),
                json=_prepare_payload(json),
                timeout=self.timeout,
            )
        except RequestException as exc:
            raise PushpadClientError(str(exc), original_exception=exc) from exc

        if response.status_code >= 400:
            message: Optional[str] = None
            payload: Optional[Any] = None
            try:
                payload = response.json()
                if isinstance(payload, dict):
                    message = payload.get("error") or payload.get("message")
            except ValueError:
                if response.text:
                    message = response.text
            raise PushpadAPIError(response.status_code, message, response_body=payload or response.text)

        if raw:
            return response

        if response.status_code in (202, 204) or not response.content:
            return None

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                return _wrap_response(response.json())
            except ValueError as exc:  # pragma: no cover - unexpected API behaviour
                raise PushpadAPIError(response.status_code, "Invalid JSON in response") from exc
        return response.content


class _ProjectBoundResource:
    def __init__(self, client: Pushpad) -> None:
        self._client = client

    def _project_id(self, project_id: Optional[int]) -> int:
        pid = project_id if project_id is not None else self._client.project_id
        if pid is None:
            raise ValueError("project_id is required for this operation")
        return pid


class NotificationsResource(_ProjectBoundResource):
    def all(self, *, project_id: Optional[int] = None, page: Optional[int] = None, **filters: Any):
        pid = self._project_id(project_id)
        params = {k: v for k, v in {"page": page, **filters}.items() if v is not None}
        return self._client._request("GET", f"/projects/{pid}/notifications", params=params)

    def create(self, *, project_id: Optional[int] = None, **notification: Any):
        pid = self._project_id(project_id)
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


class SubscriptionsResource(_ProjectBoundResource):
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
        pid = self._project_id(project_id)
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
        pid = self._project_id(project_id)
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
        pid = self._project_id(project_id)
        return self._client._request("POST", f"/projects/{pid}/subscriptions", json=subscription)

    def get(self, subscription_id: int, *, project_id: Optional[int] = None):
        if subscription_id is None:
            raise ValueError("subscription_id is required")
        pid = self._project_id(project_id)
        return self._client._request("GET", f"/projects/{pid}/subscriptions/{subscription_id}")

    def update(self, subscription_id: int, *, project_id: Optional[int] = None, **subscription: Any):
        if subscription_id is None:
            raise ValueError("subscription_id is required")
        pid = self._project_id(project_id)
        return self._client._request("PATCH", f"/projects/{pid}/subscriptions/{subscription_id}", json=subscription)

    def delete(self, subscription_id: int, *, project_id: Optional[int] = None) -> bool:
        if subscription_id is None:
            raise ValueError("subscription_id is required")
        pid = self._project_id(project_id)
        self._client._request("DELETE", f"/projects/{pid}/subscriptions/{subscription_id}")
        return True


class ProjectsResource:
    def __init__(self, client: Pushpad) -> None:
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


class SendersResource:
    def __init__(self, client: Pushpad) -> None:
        self._client = client

    def all(self):
        return self._client._request("GET", "/senders")

    def create(self, **sender: Any):
        return self._client._request("POST", "/senders", json=sender)

    def get(self, sender_id: int):
        if sender_id is None:
            raise ValueError("sender_id is required")
        return self._client._request("GET", f"/senders/{sender_id}")

    def update(self, sender_id: int, **sender: Any):
        if sender_id is None:
            raise ValueError("sender_id is required")
        return self._client._request("PATCH", f"/senders/{sender_id}", json=sender)

    def delete(self, sender_id: int) -> bool:
        if sender_id is None:
            raise ValueError("sender_id is required")
        self._client._request("DELETE", f"/senders/{sender_id}")
        return True
