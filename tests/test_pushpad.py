# -*- coding: utf-8 -*-
import json
import unittest
from unittest import mock

import pushpad
from pushpad import PushpadAPIError


def make_response(status=200, payload=None, headers=None):
    response = mock.Mock()
    response.status_code = status
    response.headers = headers or {"Content-Type": "application/json"}
    if payload is None:
        response.content = b""
        response.text = ""
        response.json.side_effect = ValueError("No JSON")
    else:
        body = json.dumps(payload).encode()
        response.content = body
        response.text = body.decode()
        response.json.return_value = payload
    return response


class DummySession:
    def __init__(self):
        self.headers = {}
        self.request = mock.Mock()

    def close(self):
        pass


def make_client(token, project_id=None, response=None):
    session = DummySession()
    if response is not None:
        session.request.return_value = response
    client = pushpad.Pushpad(token, project_id, session=session)
    return client, session


class PushpadClientTests(unittest.TestCase):
    def setUp(self):
        self.token = "5374d7dfeffa2eb49965624ba7596a09"
        self.project_id = 1

    def test_signature_for(self):
        client, _ = make_client(self.token, self.project_id)
        self.assertEqual(
            client.signature_for("user12345"),
            "6627820dab00a1971f2a6d3ff16a5ad8ba4048a02b2d402820afc61aefd0b69f",
        )

    def test_notifications_create(self):
        response = make_response(payload={"id": 123, "scheduled": 10})
        client, session = make_client(self.token, self.project_id, response)
        result = client.notifications.create(body="Hello")
        self.assertEqual(result["id"], 123)
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
        self.assertEqual(result, [{"id": 1}])
        kwargs = session.request.call_args[1]
        self.assertEqual(kwargs["params"], {"page": 2})

    def test_notifications_cancel(self):
        response = make_response(status=204)
        client, session = make_client(self.token, self.project_id, response)
        self.assertTrue(client.notifications.cancel(10))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertIn("/notifications/10/cancel", url)

    def test_subscriptions_count_uses_header(self):
        headers = {"Content-Type": "application/json", "X-Total-Count": "42"}
        response = make_response(payload=[], headers=headers)
        client, session = make_client(self.token, self.project_id, response)
        count = client.subscriptions.count(tags=["paid"])
        self.assertEqual(count, 42)
        kwargs = session.request.call_args[1]
        self.assertEqual(kwargs["params"], {"tags[]": ["paid"], "per_page": 1})

    def test_subscriptions_all_accepts_boolean_expression(self):
        response = make_response(payload=[])
        client, session = make_client(self.token, self.project_id, response)
        client.subscriptions.all(tags="tag1 && tag2")
        params = session.request.call_args[1]["params"]
        self.assertEqual(params["tags[]"], ["tag1 && tag2"])

    def test_projects_delete(self):
        response = make_response(status=202)
        client, session = make_client(self.token, response=response)
        self.assertTrue(client.projects.delete(99))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertTrue(url.endswith("/projects/99"))

    def test_senders_update(self):
        response = make_response(payload={"id": 55})
        client, session = make_client(self.token, response=response)
        client.senders.update(55, name="Acme")
        method, url = session.request.call_args[0]
        self.assertEqual(method, "PATCH")
        self.assertTrue(url.endswith("/senders/55"))
        self.assertEqual(session.request.call_args[1]["json"], {"name": "Acme"})

    def test_error_response(self):
        response = make_response(status=403, payload={"error": "Forbidden"})
        client, _ = make_client(self.token, self.project_id, response)
        with self.assertRaises(PushpadAPIError):
            client.notifications.all()
