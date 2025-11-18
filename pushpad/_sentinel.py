"""Sentinel objects shared across the client implementation."""

from __future__ import annotations

from typing import TypeVar


class _MissingType:
    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - trivial representation
        return "MISSING"


_MISSING = _MissingType()

T = TypeVar("T")


def remove_missing(**values: object | _MissingType) -> dict[str, object]:
    """Return a dict with all entries whose value is not the sentinel."""

    return {key: value for key, value in values.items() if value is not _MISSING}


__all__ = ["_MISSING", "_MissingType", "remove_missing"]
