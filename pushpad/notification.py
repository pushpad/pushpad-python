# -*- coding: utf-8 -*-
from __future__ import absolute_import
import requests
import pushpad


class Notification(object):
    def __init__(self, project, body=None, title=None, target_url=None, icon_url=None, ttl=None, require_interaction=None, silent=None, urgent=None, image_url=None, custom_data=None, custom_metrics=None, actions=None, starred=None, send_at=None):
        self._project = project
        self._body = body
        self._title = title
        self._target_url = target_url
        self._icon_url = icon_url
        self._ttl = ttl
        self._require_interaction = require_interaction
        self._silent = silent
        self._urgent = urgent
        self._image_url = image_url
        self._custom_data = custom_data
        self._custom_metrics = custom_metrics
        self._actions = actions
        self._starred = starred
        self._send_at = send_at

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
        if self._require_interaction is not None:
            res['notification']['require_interaction'] = self._require_interaction
        if self._silent is not None:
            res['notification']['silent'] = self._silent
        if self._urgent is not None:
            res['notification']['urgent'] = self._urgent
        if self._image_url:
            res['notification']['image_url'] = self._image_url
        if self._custom_data:
            res['notification']['custom_data'] = self._custom_data
        if self._custom_metrics:
            res['notification']['custom_metrics'] = self._custom_metrics
        if self._actions:
            res['notification']['actions'] = self._actions
        if self._starred is not None:
            res['notification']['starred'] = self._starred
        if self._send_at:
            res['notification']['send_at'] = self._send_at.strftime('%Y-%m-%dT%R')

        if uids != None:
            res['uids'] = uids
        if tags != None:
            res['tags'] = tags
        return res

    def _deliver(self, req_body):
        response = requests.post(
            'https://pushpad.xyz/api/v1/projects/%s/notifications' % self._project.project_id,
            headers=self._req_headers(),
            json=req_body,
        )
        if response.status_code != 201:
            raise pushpad.NotificationDeliveryError('Response %s: %s' %(response.status_code, response.text))
        return response.json()

    def broadcast(self, tags=None):
        return self._deliver(self._req_body(None, tags))

    def deliver_to(self, uids, tags=None):
        if not uids:
            uids = [] # prevent broadcasting
        return self._deliver(
            req_body=self._req_body(uids, tags)
        )
