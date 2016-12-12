from enum import Enum


class ResponseType(Enum):
    SAY = 1
    DO = 2
    NOTICE = 3
    RAW = 4


class IRCResponse(object):
    def __init__(self, message_type, response, target):
        self.type = message_type
        try:
            self.response = unicode(response, "utf-8")
        except TypeError:
            self.response = response
        try:
            self.target = unicode(target, "utf-8")
        except TypeError:
            self.target = target
