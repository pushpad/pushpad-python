"""Sentinel objects shared across the client implementation."""

from __future__ import annotations

from typing import TypeVar


class _Missing:
    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - trivial representation
        return "MISSING"


_MISSING = _Missing()

T = TypeVar("T")


def remove_missing(**values: object | _Missing) -> dict[str, object]:
    """Return a dict with all entries whose value is not the sentinel."""

    return {key: value for key, value in values.items() if value is not _MISSING}


__all__ = ["_MISSING", "_Missing", "remove_missing"]
