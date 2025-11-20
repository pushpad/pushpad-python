"""High level Pushpad API client."""

from __future__ import annotations

import requests
from requests import RequestException, Response

import hmac
from hashlib import sha256
from typing import Any, Dict, MutableMapping, Optional, Union

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


APIResponse = Union[APIObject, list[APIObject], None]


def _wrap_response(data: Any) -> Any:
    if isinstance(data, dict):
        return APIObject({key: _wrap_response(value) for key, value in data.items()})
    if isinstance(data, list):
        return [_wrap_response(item) for item in data]
    return data


def _ensure_api_object(data: APIResponse) -> APIObject:
    if isinstance(data, APIObject):
        return data
    raise PushpadClientError(f"API response is not an object: {type(data).__name__}")


def _ensure_api_list(data: APIResponse) -> list[APIObject]:
    if data is None:
        return []
    if isinstance(data, list):
        if all(isinstance(item, APIObject) for item in data):
            return data
        raise PushpadClientError("API response list contains invalid entries")
    raise PushpadClientError(f"API response is not a list: {type(data).__name__}")


from .resources import NotificationsResource, ProjectsResource, SendersResource, SubscriptionsResource


class Pushpad:
    """High level client used to interact with the Pushpad REST API."""

    DEFAULT_BASE_URL = "https://pushpad.xyz/api/v1"

    def __init__(
        self,
        auth_token: str,
        project_id: Optional[int] = None,
        *,
        base_url: Optional[str] = None,
        timeout: int = 30,
        session: Optional[Any] = None,
    ) -> None:
        if not auth_token:
            raise ValueError("auth_token is required")
        self._auth_token = auth_token
        self._project_id = project_id
        self._base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout
        if session is not None:
            self._session = session
        else:
            self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._auth_token}",
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
        return hmac.new(self._auth_token.encode(), data.encode(), sha256).hexdigest()

    def _resolve_project_id(self, project_id: Optional[int]) -> int:
        pid = project_id if project_id is not None else self._project_id
        if pid is None:
            raise ValueError("project_id is required for this operation")
        return pid

    def _raw_request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[JSONDict] = None,
    ) -> Response:
        url = f"{self._base_url}{path}"
        try:
            response = self._session.request(
                method,
                url,
                params=params,
                json=json,
                timeout=self._timeout,
            )
        except RequestException as exc:
            raise PushpadClientError(str(exc), original_exception=exc) from exc

        if response.status_code >= 400:
            raise PushpadAPIError(response.status_code, reason=response.reason, response_body=response.text)

        return response

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[JSONDict] = None,
    ) -> APIResponse:
        response = self._raw_request(method, path, params=params, json=json)
        if response.status_code in (202, 204) or not response.content:
            return None

        try:
            data = response.json()
        except ValueError as exc:  # pragma: no cover - unexpected API behaviour
            raise PushpadClientError("Invalid JSON in response", original_exception=exc) from exc
        return _wrap_response(data)
