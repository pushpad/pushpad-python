"""High level Pushpad API client."""

from __future__ import annotations

import requests
from requests import RequestException

import hmac
from datetime import date, datetime, timezone
from hashlib import sha256
from typing import Any, Dict, MutableMapping, Optional

from ._version import __version__
from .exceptions import PushpadAPIError, PushpadClientError
from .resources import NotificationsResource, ProjectsResource, SendersResource, SubscriptionsResource

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
        return {key: _serialize_value(val) for key, val in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_serialize_value(item) for item in value]
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

    def _project_id(self, project_id: Optional[int]) -> int:
        pid = project_id if project_id is not None else self.project_id
        if pid is None:
            raise ValueError("project_id is required for this operation")
        return pid

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
