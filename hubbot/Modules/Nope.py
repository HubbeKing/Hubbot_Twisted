from __future__ import unicode_literals
import datetime
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Nope(ModuleInterface):
    help = "Nope."
    seconds = 300
    last_triggered = datetime.datetime.min

    def should_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.message_string.lower().startswith("nope"):
            if (datetime.datetime.now() - self.last_triggered).seconds >= self.seconds:
                self.last_triggered = datetime.datetime.now()
                return True
        else:
            return False

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return IRCResponse(ResponseType.SAY, "I don't think so either.", message.reply_to)
