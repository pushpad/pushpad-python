# -*- coding: utf-8 -*-
from ..helpers import BasePushpadTestCase, make_client, make_response


class ProjectsResourceTests(BasePushpadTestCase):
    def test_projects_create(self):
        response = make_response(payload={"id": 2})
        client, session = make_client(self.token, response=response)
        project = client.projects.create(
            sender_id=99,
            name="Demo",
            website="https://example.com",
        )
        self.assertEqual(project.id, 2)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/projects"))
        self.assertEqual(
            session.request.call_args[1]["json"],
            {"sender_id": 99, "name": "Demo", "website": "https://example.com"},
        )

    def test_projects_all(self):
        response = make_response(payload=[{"id": 1}])
        client, session = make_client(self.token, response=response)
        projects = client.projects.all()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].id, 1)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/projects"))

    def test_projects_get(self):
        response = make_response(payload={"id": 3})
        client, session = make_client(self.token, response=response)
        project = client.projects.get(3)
        self.assertEqual(project.id, 3)
        method, url = session.request.call_args[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/projects/3"))

    def test_projects_get_with_all_fields(self):
        payload = {
            "id": 10,
            "sender_id": 77,
            "name": "Marketing Site",
            "website": "https://example.com",
            "icon_url": "https://example.com/icon.png",
            "badge_url": "https://example.com/badge.png",
            "notifications_ttl": 3600,
            "notifications_require_interaction": True,
            "notifications_silent": False,
            "created_at": "2025-09-14T10:30:00.123Z",
        }
        response = make_response(payload=payload)
        client, _ = make_client(self.token, response=response)
        project = client.projects.get(payload["id"])
        self.assertEqual(project.id, payload["id"])
        self.assertEqual(project.sender_id, payload["sender_id"])
        self.assertEqual(project.name, payload["name"])
        self.assertEqual(project.website, payload["website"])
        self.assertEqual(project.icon_url, payload["icon_url"])
        self.assertEqual(project.badge_url, payload["badge_url"])
        self.assertEqual(project.notifications_ttl, payload["notifications_ttl"])
        self.assertEqual(
            project.notifications_require_interaction,
            payload["notifications_require_interaction"],
        )
        self.assertEqual(project.notifications_silent, payload["notifications_silent"])
        self.assertEqual(project.created_at, payload["created_at"])

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
        self.assertIsNone(client.projects.delete(99))
        method, url = session.request.call_args[0]
        self.assertEqual(method, "DELETE")
        self.assertTrue(url.endswith("/projects/99"))
