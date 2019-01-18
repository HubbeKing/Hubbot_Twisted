from enum import Enum


class ResponseType(Enum):
    SAY = 1
    DO = 2
    NOTICE = 3
    RAW = 4


class IRCResponse(object):
    def __init__(self, message_type, message, target):
        self.type = message_type
        if isinstance(message, bytes):
            self.message = message.decode("utf-8", "ignore")
        else:
            self.message = message
        if isinstance(target, bytes):
            self.target = target.decode("utf-8", "ignore")
        else:
            self.target = target
