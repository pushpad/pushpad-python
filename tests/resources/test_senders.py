# -*- coding: utf-8 -*-
from tests.helpers import BasePushpadTestCase, make_client, make_response


class SendersResourceTests(BasePushpadTestCase):
    def test_senders_create(self):
        response = make_response(payload={"id": 2})
        client, session = make_client(self.token, response=response)
        sender = client.senders.create(name="News")
        self.assertEqual(sender.id, 2)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/senders"))
        self.assertEqual(session.request.call_args[1]["json"], {"name": "News"})

    def test_senders_all(self):
        response = make_response(payload=[{"id": 1}])
        client, session = make_client(self.token, response=response)
        self.assertEqual(client.senders.all(), [{"id": 1}])
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/senders"))

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
