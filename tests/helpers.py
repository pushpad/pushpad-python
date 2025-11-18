# -*- coding: utf-8 -*-
import json
import unittest
from unittest import mock

import pushpad


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


class BasePushpadTestCase(unittest.TestCase):
    def setUp(self):
        self.token = "5374d7dfeffa2eb49965624ba7596a09"
        self.project_id = 1
