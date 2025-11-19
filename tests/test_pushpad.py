# -*- coding: utf-8 -*-
from pushpad import PushpadAPIError

from tests.helpers import BasePushpadTestCase, make_client, make_response


class PushpadClientTests(BasePushpadTestCase):
    def test_signature_for(self):
        client, _ = make_client(self.token, self.project_id)
        self.assertEqual(
            client.signature_for("user12345"),
            "6627820dab00a1971f2a6d3ff16a5ad8ba4048a02b2d402820afc61aefd0b69f",
        )

    def test_error_response(self):
        response = make_response(status=403, payload={"error": "Forbidden"})
        client, _ = make_client(self.token, self.project_id, response)
        with self.assertRaises(PushpadAPIError) as ctx:
            client.notifications.all()
        self.assertIn("API error: 403", str(ctx.exception))
        self.assertIn("Forbidden", str(ctx.exception))
