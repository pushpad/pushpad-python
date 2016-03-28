# -*- coding: utf-8 -*-
from hashlib import sha1
import hmac


class Pushpad(object):
    def __init__(self, auth_token, project_id):
        self.auth_token = auth_token
        self.project_id = project_id

    def signature_for(self, data):
        return hmac.new(bytes(self.auth_token.encode()), data.encode(), sha1).hexdigest()

    def path(self):
        return "https://pushpad.xyz/projects/{project_id}/subscription/edit".format(
            project_id=self.project_id
        )

    def path_for(self, uid):
        return "{project_path}?uid={uid}&uid_signature={uid_signature}".format(
            project_path=self.path(),
            uid=uid,
            uid_signature=self.signature_for(uid)
        )
