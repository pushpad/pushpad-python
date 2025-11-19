# -*- coding: utf-8 -*-
from tests.helpers import BasePushpadTestCase, make_client, make_response


class NotificationsResourceTests(BasePushpadTestCase):
    def test_notifications_create(self):
        response = make_response(payload={"id": 123, "scheduled": 10})
        client, session = make_client(self.token, self.project_id, response)
        result = client.notifications.create(body="Hello")
        self.assertEqual(result.id, 123)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "POST")
        self.assertIn("/projects/1/notifications", url)
        self.assertEqual(session.request.call_args[1]["json"], {"body": "Hello"})

    def test_notifications_requires_project(self):
        client, session = make_client(self.token)
        with self.assertRaises(ValueError):
            client.notifications.create(body="Hello")
        session.request.assert_not_called()

    def test_notifications_all(self):
        response = make_response(payload=[{"id": 1}])
        client, session = make_client(self.token, self.project_id, response)
        result = client.notifications.all(page=2)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, 1)
        kwargs = session.request.call_args[1]
        self.assertEqual(kwargs["params"], {"page": 2})

    def test_notifications_get(self):
        response = make_response(payload={"id": 77})
        client, session = make_client(self.token, self.project_id, response)
        result = client.notifications.get(77)
        self.assertEqual(result.id, 77)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/notifications/77"))

    def test_notifications_get_with_all_fields(self):
        payload = {
            "id": 101,
            "project_id": 7,
            "title": "New promotion",
            "body": "Buy now",
            "target_url": "https://example.com/promo",
            "icon_url": "https://example.com/icon.png",
            "badge_url": "https://example.com/badge.png",
            "image_url": "https://example.com/image.png",
            "ttl": 600,
            "require_interaction": True,
            "silent": False,
            "urgent": True,
            "custom_data": "metadata",
            "actions": [
                {
                    "title": "Open cart",
                    "target_url": "https://example.com/cart",
                    "icon": "https://example.com/cart.png",
                    "action": "open_cart",
                }
            ],
            "starred": True,
            "send_at": "2024-01-01T00:00:00.000Z",
            "custom_metrics": ["metric1", "metric2"],
            "uids": ["uid-a", "uid-b"],
            "tags": ["tag1", "tag2"],
            "created_at": "2023-12-31T12:00:00.000Z",
            "successfully_sent_count": 10,
            "opened_count": 3,
            "scheduled_count": 2,
            "scheduled": False,
            "cancelled": False,
        }
        response = make_response(payload=payload)
        client, _ = make_client(self.token, self.project_id, response)
        notification = client.notifications.get(payload["id"])
        self.assertEqual(notification.id, payload["id"])
        self.assertEqual(notification.project_id, payload["project_id"])
        self.assertEqual(notification.title, payload["title"])
        self.assertEqual(notification.body, payload["body"])
        self.assertEqual(notification.target_url, payload["target_url"])
        self.assertEqual(notification.icon_url, payload["icon_url"])
        self.assertEqual(notification.badge_url, payload["badge_url"])
        self.assertEqual(notification.image_url, payload["image_url"])
        self.assertEqual(notification.ttl, payload["ttl"])
        self.assertEqual(notification.require_interaction, payload["require_interaction"])
        self.assertEqual(notification.silent, payload["silent"])
        self.assertEqual(notification.urgent, payload["urgent"])
        self.assertEqual(notification.custom_data, payload["custom_data"])
        self.assertEqual(len(notification.actions), 1)
        self.assertEqual(notification.actions[0].title, payload["actions"][0]["title"])
        self.assertEqual(notification.actions[0].target_url, payload["actions"][0]["target_url"])
        self.assertEqual(notification.actions[0].icon, payload["actions"][0]["icon"])
        self.assertEqual(notification.actions[0].action, payload["actions"][0]["action"])
        self.assertEqual(notification.starred, payload["starred"])
        self.assertEqual(notification.send_at, payload["send_at"])
        self.assertEqual(notification.custom_metrics, payload["custom_metrics"])
        self.assertEqual(notification.uids, payload["uids"])
        self.assertEqual(notification.tags, payload["tags"])
        self.assertEqual(notification.created_at, payload["created_at"])
        self.assertEqual(notification.successfully_sent_count, payload["successfully_sent_count"])
        self.assertEqual(notification.opened_count, payload["opened_count"])
        self.assertEqual(notification.scheduled_count, payload["scheduled_count"])
        self.assertEqual(notification.scheduled, payload["scheduled"])
        self.assertEqual(notification.cancelled, payload["cancelled"])

    def test_notifications_cancel(self):
        response = make_response(status=204)
        client, session = make_client(self.token, self.project_id, response)
        self.assertIsNone(client.notifications.cancel(10))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertIn("/notifications/10/cancel", url)
