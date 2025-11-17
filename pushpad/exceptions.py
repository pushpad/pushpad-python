"""Custom exceptions raised by the Pushpad client library."""

from __future__ import annotations

from typing import Any, Optional


class PushpadError(Exception):
    """Base class for all library errors."""


class PushpadClientError(PushpadError):
    """Raised for local/network errors before a response is received."""

    def __init__(self, message: str, *, original_exception: Optional[BaseException] = None) -> None:
        super().__init__(message)
        self.original_exception = original_exception


class PushpadAPIError(PushpadError):
    """Raised for HTTP errors returned by the Pushpad API."""

    def __init__(
        self,
        status_code: int,
        message: Optional[str] = None,
        *,
        response_body: Optional[Any] = None,
    ) -> None:
        msg = message or f"Pushpad API error (status_code={status_code})"
        super().__init__(msg)
        self.status_code = status_code
        self.response_body = response_body
