import datetime
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Nope(ModuleInterface):
    help = "Nope."
    seconds = 300
    lastTriggered = datetime.datetime.min

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.MessageString.lower().startswith("nope"):
            if (datetime.datetime.now() - self.lastTriggered).seconds >= self.seconds:
                self.lastTriggered = datetime.datetime.now()
                return True
        else:
            return False

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return IRCResponse(ResponseType.Say, "I don't think so either.", message.ReplyTo)
