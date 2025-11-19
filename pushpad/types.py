"""Typed resource objects returned by the client."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass
class NotificationAction:
    title: str | None
    target_url: str | None
    icon: str | None
    action: str | None

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
    id: int
    scheduled: int | None
    uids: list[str] | None
    send_at: str | None

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> "NotificationCreateResult":
        return cls(
            id=data.get("id"),
            scheduled=data.get("scheduled"),
            uids=data.get("uids"),
            send_at=data.get("send_at"),
        )


@dataclass
class Notification:
    id: int
    project_id: int
    title: str
    body: str
    target_url: str
    icon_url: str | None
    badge_url: str | None
    image_url: str | None
    ttl: int
    require_interaction: bool
    silent: bool
    urgent: bool
    custom_data: str | None
    actions: list[NotificationAction]
    starred: bool
    send_at: str | None
    custom_metrics: list[str]
    uids: list[str] | None
    tags: list[str] | None
    created_at: str
    successfully_sent_count: int | None
    opened_count: int | None
    scheduled_count: int | None
    scheduled: bool | None
    cancelled: bool | None

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
            custom_metrics=data.get("custom_metrics"),
            uids=data.get("uids"),
            tags=data.get("tags"),
            created_at=data.get("created_at"),
            successfully_sent_count=data.get("successfully_sent_count"),
            opened_count=data.get("opened_count"),
            scheduled_count=data.get("scheduled_count"),
            scheduled=data.get("scheduled"),
            cancelled=data.get("cancelled"),
        )


@dataclass
class Subscription:
    id: int
    project_id: int
    endpoint: str
    p256dh: str | None
    auth: str | None
    uid: str | None
    tags: list[str] | None
    last_click_at: str | None
    created_at: str

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> "Subscription":
        return cls(
            id=data.get("id"),
            project_id=data.get("project_id"),
            endpoint=data.get("endpoint"),
            p256dh=data.get("p256dh"),
            auth=data.get("auth"),
            uid=data.get("uid"),
            tags=data.get("tags"),
            last_click_at=data.get("last_click_at"),
            created_at=data.get("created_at"),
        )


@dataclass
class Project:
    id: int
    sender_id: int
    name: str
    website: str
    icon_url: str | None
    badge_url: str | None
    notifications_ttl: int
    notifications_require_interaction: bool
    notifications_silent: bool
    created_at: str

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
    id: int
    name: str
    vapid_private_key: str
    vapid_public_key: str
    created_at: str

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
