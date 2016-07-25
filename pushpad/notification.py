# -*- coding: utf-8 -*-
from __future__ import absolute_import
import requests
import pushpad


class Notification(object):
    def __init__(self, project, body=None, title=None, target_url=None, icon_url=None, ttl=None):
        self._project = project
        self._body = body
        self._title = title
        self._target_url = target_url
        self._icon_url = icon_url
        self._ttl = ttl

    def _req_headers(self):
        return {
            'Authorization': 'Token token="%s"' % self._project.auth_token,
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json',
        }

    def _req_body(self, uids=None, tags=None):
        res = {
            'notification': {
                'body': self._body,
            }
        }
        if self._title:
            res['notification']['title'] = self._title
        if self._target_url:
            res['notification']['target_url'] = self._target_url
        if self._icon_url:
            res['notification']['icon_url'] = self._icon_url
        if self._ttl:
            res['notification']['ttl'] = self._ttl
        if uids:
            res['uids'] = uids
        if tags:
            res['tags'] = tags
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

    def broadcast(self, tags=None):
        return self._deliver(self._req_body(None, tags))

    def deliver_to(self, uids, tags=None):
        return self._deliver(
            req_body=self._req_body(uids, tags)
        )
