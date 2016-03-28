# -*- coding: utf-8 -*-
from __future__ import absolute_import
import requests
import pushpad


class Notification(object):
    def __init__(self, project, body=None, title=None, target_url=None):
        self._project = project
        self._body = body
        self._title = title
        self._target_url = target_url

    def _req_headers(self):
        return {
            'Authorization': 'Token token="%s"' % self._project.auth_token,
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
        }

    def _req_body(self, uids=[]):
        res = {
            'notification': {
                'body': self._body,
                'title': self._title,
                'target_url': self._target_url,
            }
        }
        if uids:
            res.update({'uids': uids})
        return res

    def _deliver(self, req_body):
        response = requests.post(
            'https://pushpad.xyz/projects/%s/notifications' % self._project.project_id,
            headers=self._req_headers(),
            json=req_body,
        )
        if response.status_code != 201:
            raise pushpad.NotificationDeliveryError('Response %s: %s' %(response.status_code, response.text))
        return response.json()

    def broadcast(self):
        return self._deliver(self._req_body())

    def deliver_to(self, uids):
        return self._deliver(
            req_body=self._req_body(uids)
        )