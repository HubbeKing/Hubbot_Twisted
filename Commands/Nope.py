import datetime
from IRCResponse import IRCResponse, ResponseType
from CommandInterface import CommandInterface


class Command(CommandInterface):
    Help = "nope - nope"
    seconds = 300
    lastTriggered = datetime.datetime.min

    def shouldExecute(self, message):
        if datetime.datetime.now() - self.lastTriggered.seconds >= self.seconds:
            self.lastTriggered = datetime.datetime.now()
            return True

    def execute(self, Hubbot, message):
        if message.MessageString.lower().startswith("nope"):
            return IRCResponse(ResponseType.Say, "I don't think so either.", message.ReplyTo)