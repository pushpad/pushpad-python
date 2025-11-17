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

    def test_subscriptions_create(self):
        response = make_response(payload={"id": 11})
        client, session = make_client(self.token, self.project_id, response)
        subscription = client.subscriptions.create(uid="u1")
        self.assertEqual(subscription.id, 11)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "POST")
        self.assertIn("/projects/1/subscriptions", url)
        self.assertEqual(session.request.call_args[1]["json"], {"uid": "u1"})

    def test_subscriptions_get(self):
        response = make_response(payload={"id": 22})
        client, session = make_client(self.token, self.project_id, response)
        subscription = client.subscriptions.get(22)
        self.assertEqual(subscription.id, 22)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/projects/1/subscriptions/22"))

    def test_subscriptions_update(self):
        response = make_response(payload={"id": 33, "tags": ["a"]})
        client, session = make_client(self.token, self.project_id, response)
        subscription = client.subscriptions.update(33, tags=["a"])
        self.assertEqual(subscription.tags, ["a"])
        method, url = session.request.call_args[0]
        self.assertEqual(method, "PATCH")
        self.assertTrue(url.endswith("/projects/1/subscriptions/33"))
        self.assertEqual(session.request.call_args[1]["json"], {"tags": ["a"]})

    def test_subscriptions_delete(self):
        response = make_response(status=204)
        client, session = make_client(self.token, self.project_id, response)
        self.assertTrue(client.subscriptions.delete(44))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertTrue(url.endswith("/projects/1/subscriptions/44"))

    def test_projects_all(self):
        response = make_response(payload=[{"id": 1}])
        client, session = make_client(self.token, response=response)
        self.assertEqual(client.projects.all(), [{"id": 1}])
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/projects"))

    def test_projects_create(self):
        response = make_response(payload={"id": 2})
        client, session = make_client(self.token, response=response)
        project = client.projects.create(name="Demo")
        self.assertEqual(project.id, 2)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/projects"))
        self.assertEqual(session.request.call_args[1]["json"], {"name": "Demo"})

    def test_projects_get(self):
        response = make_response(payload={"id": 3})
        client, session = make_client(self.token, response=response)
        project = client.projects.get(3)
        self.assertEqual(project.id, 3)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/projects/3"))

    def test_projects_update(self):
        response = make_response(payload={"id": 4, "name": "Demo"})
        client, session = make_client(self.token, response=response)
        project = client.projects.update(4, name="Demo")
        self.assertEqual(project.name, "Demo")
        method, url = session.request.call_args[0]
        self.assertEqual(method, "PATCH")
        self.assertTrue(url.endswith("/projects/4"))
        self.assertEqual(session.request.call_args[1]["json"], {"name": "Demo"})

    def test_projects_delete(self):
        response = make_response(status=202)
        client, session = make_client(self.token, response=response)
        self.assertTrue(client.projects.delete(99))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertTrue(url.endswith("/projects/99"))

    def test_senders_all(self):
        response = make_response(payload=[{"id": 1}])
        client, session = make_client(self.token, response=response)
        self.assertEqual(client.senders.all(), [{"id": 1}])
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/senders"))

    def test_senders_create(self):
        response = make_response(payload={"id": 2})
        client, session = make_client(self.token, response=response)
        sender = client.senders.create(name="News")
        self.assertEqual(sender.id, 2)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/senders"))
        self.assertEqual(session.request.call_args[1]["json"], {"name": "News"})

    def test_senders_get(self):
        response = make_response(payload={"id": 3})
        client, session = make_client(self.token, response=response)
        sender = client.senders.get(3)
        self.assertEqual(sender.id, 3)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/senders/3"))

    def test_senders_update(self):
        response = make_response(payload={"id": 55})
        client, session = make_client(self.token, response=response)
        client.senders.update(55, name="Acme")
        method, url = session.request.call_args[0]
        self.assertEqual(method, "PATCH")
        self.assertTrue(url.endswith("/senders/55"))
        self.assertEqual(session.request.call_args[1]["json"], {"name": "Acme"})

    def test_senders_delete(self):
        response = make_response(status=204)
        client, session = make_client(self.token, response=response)
        self.assertTrue(client.senders.delete(66))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertTrue(url.endswith("/senders/66"))

    def test_error_response(self):
        response = make_response(status=403, payload={"error": "Forbidden"})
        client, _ = make_client(self.token, self.project_id, response)
        with self.assertRaises(PushpadAPIError):
            client.notifications.all()
