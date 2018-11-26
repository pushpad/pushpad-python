# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
import pushpad
import requests
import datetime
try:
    import mock
except ImportError:
    from unittest import mock


class TestNotification(unittest.TestCase):
    _test_token = '5374d7dfeffa2eb49965624ba7596a09'
    _test_project_id = 123

    _project = pushpad.Pushpad(_test_token, _test_project_id)

    def test_instantiate(self):
        self.assertIsNotNone(
            pushpad.Notification(self._project, body="Hello world!")
        )
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com",
            icon_url="http://example.com/assets/icon.png",
            ttl=604800,
            require_interaction=True,
            urgent=True,
            image_url="http://example.com/assets/image.png",
            custom_data="123",
            custom_metrics=('examples', 'another_metric'),
            actions=(
                {
                    'title': "My Button 1",
                    'target_url': "http://example.com/button-link",
                    'icon': "http://example.com/assets/button-icon.png",
                    'action': "myActionName"
                },
            ),
            starred=True,
            send_at=datetime.datetime(2016, 7, 25, 10, 9, 0, 0)
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification._body, "Hello world!")
        self.assertEqual(notification._title, "Website Name")
        self.assertEqual(notification._target_url, "http://example.com")
        self.assertEqual(notification._icon_url, "http://example.com/assets/icon.png")
        self.assertEqual(notification._ttl, 604800)
        self.assertEqual(notification._require_interaction, True)
        self.assertEqual(notification._urgent, True)
        self.assertEqual(notification._image_url, "http://example.com/assets/image.png")
        self.assertEqual(notification._custom_data, "123")
        self.assertEqual(notification._custom_metrics, ('examples', 'another_metric'))
        self.assertEqual(notification._actions, (
            {
                'title': "My Button 1",
                'target_url': "http://example.com/button-link",
                'icon': "http://example.com/assets/button-icon.png",
                'action': "myActionName"
            },
        ))
        self.assertEqual(notification._starred, True)
        self.assertEqual(notification._send_at, datetime.datetime(2016, 7, 25, 10, 9, 0, 0))

    def test_req_headers(self):
        headers = {
            'Authorization': 'Token token="5374d7dfeffa2eb49965624ba7596a09"',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!"
        )
        self.assertDictEqual(
            notification._req_headers(),
            headers
        )

    def test_req_body_with_optional_fields(self):
        body = {
            'notification': {
                'body': 'Hello world!',
                'title': 'Website Name',
                'target_url': 'http://example.com',
                'icon_url': 'http://example.com/assets/icon.png',
                'ttl': 604800,
                'require_interaction': True,
                'urgent': True,
                'image_url': 'http://example.com/assets/image.png',
                'custom_data': '123',
                'custom_metrics': ('examples', 'another_metric'),
                'actions': (
                  {
                    'title': 'My Button 1',
                    'target_url': 'http://example.com/button-link',
                    'icon': 'http://example.com/assets/button-icon.png',
                    'action': 'myActionName'
                  },
                ),
                'starred': True,
                'send_at': '2016-07-25T10:09'
            }
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!",
            title="Website Name",
            target_url="http://example.com",
            icon_url="http://example.com/assets/icon.png",
            ttl=604800,
            require_interaction=True,
            urgent=True,
            image_url="http://example.com/assets/image.png",
            custom_data="123",
            custom_metrics=('examples', 'another_metric'),
            actions=(
                {
                    'title': "My Button 1",
                    'target_url': "http://example.com/button-link",
                    'icon': "http://example.com/assets/button-icon.png",
                    'action': "myActionName"
                },
            ),
            starred=True,
            send_at=datetime.datetime(2016, 7, 25, 10, 9, 0, 0)
        )
        self.assertDictEqual(
            notification._req_body(),
            body
        )

    def test_req_body_uids(self):
        body = {
            'notification': {
                'body': 'Hello world!'
            },
            'uids': ('user1', 'user2', 'user3')
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!"
        )
        self.assertDictEqual(
            notification._req_body(('user1', 'user2', 'user3')),
            body
        )

    def test_req_body_uid(self):
        body = {
            'notification': {
                'body': 'Hello world!'
            },
            'uids': 'user1'
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!"
        )
        self.assertDictEqual(
            notification._req_body('user1'),
            body
        )

    def test_req_body_tags(self):
        body = {
            'notification': {
                'body': 'Hello world!'
            },
            'tags': ('tag1', 'tag2')
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!"
        )
        self.assertDictEqual(
            notification._req_body(tags=('tag1', 'tag2')),
            body
        )

    def test_req_body_tag(self):
        body = {
            'notification': {
                'body': 'Hello world!'
            },
            'tags': 'tag1'
        }
        notification = pushpad.Notification(
            self._project,
            body="Hello world!"
        )
        self.assertDictEqual(
            notification._req_body(tags='tag1'),
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
    def test_broadcast_with_tags(self, deliver_mock):
        notification = pushpad.Notification(
            self._project,
            body="Hello world!"
        )
        notification.broadcast(tags=('tag1', 'tag2'))
        deliver_mock.assert_called_once_with(
            {
                'notification': {
                    'body': 'Hello world!'
                },
                'tags': ('tag1', 'tag2')
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

    @mock.patch('pushpad.Notification._deliver')
    def test_deliver_to_with_tags(self, deliver_mock):
        notification = pushpad.Notification(
            self._project,
            body="Hello world!"
        )
        notification.deliver_to(('user1', 'user2'), tags=('tag1', 'tag2'))
        deliver_mock.assert_called_once_with(
            req_body={
                'notification': {
                    'body': 'Hello world!'
                },
                'uids': ('user1', 'user2'),
                'tags': ('tag1', 'tag2')
            }
        )

    @mock.patch('requests.post')
    def test_deliver_to_never_broadcasts(self, req_post_mock):
        notification = pushpad.Notification(
            self._project,
            body="Hello world!"
        )

        mock_response = mock.Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {u'scheduled': 0}
        req_post_mock.return_value = mock_response

        notification.deliver_to(None)
        req_post_mock.assert_called_once_with(
            'https://pushpad.xyz/projects/123/notifications',
            headers={
                'Content-Type': 'application/json;charset=UTF-8',
                'Accept': 'application/json',
                'Authorization': 'Token token="5374d7dfeffa2eb49965624ba7596a09"'
            },
            json={
                'notification': {
                    'body': 'Hello world!'
                },
                'uids': []
            }
        )
