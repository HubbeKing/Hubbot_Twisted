import datetime
from IRCResponse import IRCResponse, ResponseType
from CommandInterface import CommandInterface


class Command(CommandInterface):
    Help = "nope - nope"
    seconds = 300
    lastTriggered = datetime.datetime.min

    def shouldExecute(self, message):
        if message.MessageString.lower().startswith("nope"):
            if (datetime.datetime.now() - self.lastTriggered).seconds >= self.seconds:
                self.lastTriggered = datetime.datetime.now()
                return True
        else:
            return False

    def execute(self, Hubbot, message):
        return IRCResponse(ResponseType.Say, "I don't think so either.", message.ReplyTo)
