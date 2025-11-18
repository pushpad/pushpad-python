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

    def test_notifications_cancel(self):
        response = make_response(status=204)
        client, session = make_client(self.token, self.project_id, response)
        self.assertIsNone(client.notifications.cancel(10))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertIn("/notifications/10/cancel", url)
