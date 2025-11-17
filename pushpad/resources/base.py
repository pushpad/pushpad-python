"""Shared helper classes for resource modules."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - only used for typing
    from ..pushpad import Pushpad


class _ProjectBoundResource:
    def __init__(self, client: "Pushpad") -> None:
        self._client = client

    def _project_id(self, project_id: Optional[int]) -> int:
        pid = project_id if project_id is not None else self._client.project_id
        if pid is None:
            raise ValueError("project_id is required for this operation")
        return pid
