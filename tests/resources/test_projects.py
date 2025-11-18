# -*- coding: utf-8 -*-
from tests.helpers import BasePushpadTestCase, make_client, make_response


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
