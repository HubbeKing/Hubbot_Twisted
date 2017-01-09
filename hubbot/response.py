from __future__ import unicode_literals
from enum import Enum


class ResponseType(Enum):
    SAY = 1
    DO = 2
    NOTICE = 3
    RAW = 4


class IRCResponse(object):
    def __init__(self, message_type, message, target):
        self.type = message_type
        try:
            self.message = unicode(message, "utf-8")
        except TypeError:
            self.message = message
        try:
            self.target = unicode(target, "utf-8")
        except TypeError:
            self.target = target
