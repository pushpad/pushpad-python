# -*- coding: utf-8 -*-
from hashlib import sha1
import hmac


class Pushpad(object):
    def __init__(self, auth_token, project_id):
        self.auth_token = auth_token
        self.project_id = project_id

    def signature_for(self, data):
        return hmac.new(bytes(self.auth_token.encode()), data.encode(), sha1).hexdigest()
