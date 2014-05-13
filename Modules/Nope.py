import datetime
from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface


class Module(ModuleInterface):
    help = "Nope."
    seconds = 300
    lastTriggered = datetime.datetime.min

    def shouldTrigger(self, message):
        if message.MessageString.lower().startswith("nope"):
            if (datetime.datetime.now() - self.lastTriggered).seconds >= self.seconds:
                self.lastTriggered = datetime.datetime.now()
                return True
        else:
            return False

    def trigger(self, Hubbot, message):
        return IRCResponse(ResponseType.Say, "I don't think so either.", message.ReplyTo)