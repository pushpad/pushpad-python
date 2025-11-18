# -*- coding: utf-8 -*-
from tests.helpers import BasePushpadTestCase, make_client, make_response


class SubscriptionsResourceTests(BasePushpadTestCase):
    def test_subscriptions_create(self):
        response = make_response(payload={"id": 11})
        client, session = make_client(self.token, self.project_id, response)
        subscription = client.subscriptions.create(uid="u1")
        self.assertEqual(subscription.id, 11)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "POST")
        self.assertIn("/projects/1/subscriptions", url)
        self.assertEqual(session.request.call_args[1]["json"], {"uid": "u1"})

    def test_subscriptions_all_accepts_boolean_expression(self):
        response = make_response(payload=[])
        client, session = make_client(self.token, self.project_id, response)
        client.subscriptions.all(tags="tag1 && tag2")
        params = session.request.call_args[1]["params"]
        self.assertEqual(params["tags[]"], ["tag1 && tag2"])

    def test_subscriptions_count_uses_header(self):
        headers = {"Content-Type": "application/json", "X-Total-Count": "42"}
        response = make_response(payload=[], headers=headers)
        client, session = make_client(self.token, self.project_id, response)
        count = client.subscriptions.count(tags=["paid"])
        self.assertEqual(count, 42)
        kwargs = session.request.call_args[1]
        self.assertEqual(kwargs["params"], {"tags[]": ["paid"], "per_page": 1})

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

    def test_subscriptions_update_can_set_fields_to_null(self):
        response = make_response(payload={"id": 33, "uid": None})
        client, session = make_client(self.token, self.project_id, response)
        subscription = client.subscriptions.update(33, uid=None)
        self.assertEqual(subscription.uid, None)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "PATCH")
        self.assertTrue(url.endswith("/projects/1/subscriptions/33"))
        self.assertEqual(session.request.call_args[1]["json"], {"uid": None})

    def test_subscriptions_delete(self):
        response = make_response(status=204)
        client, session = make_client(self.token, self.project_id, response)
        self.assertIsNone(client.subscriptions.delete(44))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertTrue(url.endswith("/projects/1/subscriptions/44"))
