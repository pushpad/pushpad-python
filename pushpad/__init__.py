# -*- coding: utf-8 -*-
from .pushpad import Pushpad
from .notification import Notification

class PushpadBaseException(BaseException):
    """
    Generic pushpad exception
    """
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class NotificationDeliveryError(PushpadBaseException):
    pass