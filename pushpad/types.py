"""Typed resource objects returned by the client."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


def _to_str_list(values: Any) -> Optional[list[str]]:
    if values is None:
        return None
    if isinstance(values, list):
        return [str(item) for item in values]
    if isinstance(values, (tuple, set)):
        return [str(item) for item in values]
    return [str(values)]


@dataclass
class NotificationAction:
    title: Optional[str] = None
    target_url: Optional[str] = None
    icon: Optional[str] = None
    action: Optional[str] = None

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> "NotificationAction":
        return cls(
            title=data.get("title"),
            target_url=data.get("target_url"),
            icon=data.get("icon"),
            action=data.get("action"),
        )


def _to_actions(values: Any) -> list[NotificationAction]:
    if not values:
        return []
    actions: list[NotificationAction] = []
    for entry in values:
        if isinstance(entry, Mapping):
            actions.append(NotificationAction.from_api(entry))
    return actions


@dataclass
class NotificationCreateResult:
    id: Optional[int] = None
    scheduled: Optional[int] = None
    uids: Optional[list[str]] = None
    send_at: Optional[str] = None

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> "NotificationCreateResult":
        return cls(
            id=data.get("id"),
            scheduled=data.get("scheduled"),
            uids=_to_str_list(data.get("uids")),
            send_at=data.get("send_at"),
        )


@dataclass
class Notification:
    id: Optional[int] = None
    project_id: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    target_url: Optional[str] = None
    icon_url: Optional[str] = None
    badge_url: Optional[str] = None
    image_url: Optional[str] = None
    ttl: Optional[int] = None
    require_interaction: Optional[bool] = None
    silent: Optional[bool] = None
    urgent: Optional[bool] = None
    custom_data: Optional[str] = None
    actions: list[NotificationAction] = field(default_factory=list)
    starred: Optional[bool] = None
    send_at: Optional[str] = None
    custom_metrics: Optional[list[str]] = None
    uids: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    created_at: Optional[str] = None
    successfully_sent_count: Optional[int] = None
    opened_count: Optional[int] = None
    scheduled_count: Optional[int] = None
    scheduled: bool | int | None = None
    cancelled: Optional[bool] = None

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> "Notification":
        return cls(
            id=data.get("id"),
            project_id=data.get("project_id"),
            title=data.get("title"),
            body=data.get("body"),
            target_url=data.get("target_url"),
            icon_url=data.get("icon_url"),
            badge_url=data.get("badge_url"),
            image_url=data.get("image_url"),
            ttl=data.get("ttl"),
            require_interaction=data.get("require_interaction"),
            silent=data.get("silent"),
            urgent=data.get("urgent"),
            custom_data=data.get("custom_data"),
            actions=_to_actions(data.get("actions")),
            starred=data.get("starred"),
            send_at=data.get("send_at"),
            custom_metrics=_to_str_list(data.get("custom_metrics")),
            uids=_to_str_list(data.get("uids")),
            tags=_to_str_list(data.get("tags")),
            created_at=data.get("created_at"),
            successfully_sent_count=data.get("successfully_sent_count"),
            opened_count=data.get("opened_count"),
            scheduled_count=data.get("scheduled_count"),
            scheduled=data.get("scheduled"),
            cancelled=data.get("cancelled"),
        )


@dataclass
class Subscription:
    id: Optional[int] = None
    project_id: Optional[int] = None
    endpoint: Optional[str] = None
    p256dh: Optional[str] = None
    auth: Optional[str] = None
    uid: Optional[str] = None
    tags: Optional[list[str]] = None
    last_click_at: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> "Subscription":
        return cls(
            id=data.get("id"),
            project_id=data.get("project_id"),
            endpoint=data.get("endpoint"),
            p256dh=data.get("p256dh"),
            auth=data.get("auth"),
            uid=data.get("uid"),
            tags=_to_str_list(data.get("tags")),
            last_click_at=data.get("last_click_at"),
            created_at=data.get("created_at"),
        )


@dataclass
class Project:
    id: Optional[int] = None
    sender_id: Optional[int] = None
    name: Optional[str] = None
    website: Optional[str] = None
    icon_url: Optional[str] = None
    badge_url: Optional[str] = None
    notifications_ttl: Optional[int] = None
    notifications_require_interaction: Optional[bool] = None
    notifications_silent: Optional[bool] = None
    created_at: Optional[str] = None

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> "Project":
        return cls(
            id=data.get("id"),
            sender_id=data.get("sender_id"),
            name=data.get("name"),
            website=data.get("website"),
            icon_url=data.get("icon_url"),
            badge_url=data.get("badge_url"),
            notifications_ttl=data.get("notifications_ttl"),
            notifications_require_interaction=data.get("notifications_require_interaction"),
            notifications_silent=data.get("notifications_silent"),
            created_at=data.get("created_at"),
        )


@dataclass
class Sender:
    id: Optional[int] = None
    name: Optional[str] = None
    vapid_private_key: Optional[str] = None
    vapid_public_key: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> "Sender":
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            vapid_private_key=data.get("vapid_private_key"),
            vapid_public_key=data.get("vapid_public_key"),
            created_at=data.get("created_at"),
        )


__all__ = [
    "Notification",
    "NotificationAction",
    "NotificationCreateResult",
    "Subscription",
    "Project",
    "Sender",
]
