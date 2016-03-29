# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
import pushpad
import requests
try:
    import mock
except ImportError:
    from unittest import mock


class TestNotification(unittest.TestCase):
    _test_token = '5374d7dfeffa2eb49965624ba7596a09'
    _test_project_id = 123

    _project = pushpad.Pushpad(_test_token, _test_project_id)

    def test_instantiate(self):
        """ notification can be instantiated"""

        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )
        self.assertIsNotNone(notification)

    def test_set_body(self):
        """ can change body """
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )
        self.assertEqual(
            notification._body,
            "Hello world!"
        )

    def test_set_title(self):
        """ can change title """
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )
        self.assertEqual(
            notification._title,
            "Website Name"
        )

    def test_set_target_url(self):
        """ can change target_url """
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )
        self.assertEqual(
            notification._target_url,
            "http://example.com"
        )

    def test_req_headers(self):
        headers = {
            'Authorization': 'Token token="5374d7dfeffa2eb49965624ba7596a09"',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )
        self.assertDictEqual(
            notification._req_headers(),
            headers
        )

    def test_req_body_all(self):
        body = {
            'notification': {
                'body': 'Hello world!',
                'title': 'Website Name',
                'target_url': 'http://example.com',
            }
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )

        self.assertDictEqual(
            notification._req_body(),
            body
        )

    def test_req_body_list(self):
        body = {
            'notification': {
                'body': 'Hello world!',
                'title': 'Website Name',
                'target_url': 'http://example.com',
            },
            'uids': ('user1', 'user2', 'user3')
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )

        self.assertDictEqual(
            notification._req_body(('user1', 'user2', 'user3')),
            body
        )

    def test_req_body_single(self):
        body = {
            'notification': {
                'body': 'Hello world!',
                'title': 'Website Name',
                'target_url': 'http://example.com',
            },
            'uids': 'user1'
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )

        self.assertDictEqual(
            notification._req_body('user1'),
            body
        )

    @mock.patch('requests.post')
    def test_deliver(self, req_post_mock):
        body = {
            'notification': {
                'body': 'Hello world!',
                'title': 'Website Name',
                'target_url': 'http://example.com',
            },
            'uids': 'user1'
        }

        mock_response = mock.Mock()
        resp_json = {u'scheduled': 76}
        mock_response.status_code = 201
        mock_response.json.return_value = resp_json
        req_post_mock.return_value = mock_response

        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )

        notification._deliver(body)
        req_post_mock.assert_called_once_with(
            'https://pushpad.xyz/projects/123/notifications',
            headers={
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json',
                'Authorization': 'Token token="5374d7dfeffa2eb49965624ba7596a09"'
            },
            json={
                'notification': {
                    'body': 'Hello world!',
                    'target_url': 'http://example.com',
                    'title': 'Website Name'
                },
                'uids': 'user1'
            }
        )

    @mock.patch('pushpad.Notification._deliver')
    def test_broadcast(self, deliver_mock):
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )

        notification.broadcast()
        deliver_mock.assert_called_once_with(
            {
                'notification': {
                    'title': 'Website Name',
                    'target_url': 'http://example.com',
                    'body': 'Hello world!'
                }
            }
        )

    @mock.patch('pushpad.Notification._deliver')
    def test_deliver_to(self, deliver_mock):
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com"
        )

        notification.deliver_to('user1')
        deliver_mock.assert_called_once_with(
            req_body={
                'notification': {
                    'body': 'Hello world!',
                    'target_url':'http://example.com',
                    'title': 'Website Name'
                },
                'uids': 'user1'
            }
        )

