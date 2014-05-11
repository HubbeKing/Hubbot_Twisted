import datetime
from IRCResponse import IRCResponse, ResponseType
from Function import Function

class Instantiate(Function):
    Help = "nope - nope"
    seconds = 300
    lastTriggered = datetime.datetime.min

    def GetResponse(self, HubbeBot, message):
        if message.MessageString.lower().startswith("nope"):
            if (datetime.datetime.now() - self.lastTriggered).seconds >= self.seconds:
                self.lastTriggered = datetime.datetime.now()
                return IRCResponse(ResponseType.Say, "I don't think so either.", message.ReplyTo)
