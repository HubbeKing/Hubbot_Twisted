from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

class Instantiate(Function):
    Help = "timer <time> - starts a countdown timer and notifies you when time's up."

    def GetResponse(self, HubbeBot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "timer":
            if len(message.ParameterList) != 1:
                return IRCResponse(ResponseType.Say, "Please use only 1 argument.", message.ReplyTo)
            delay = float(ParameterList[0])
            HubbeBot.reactor.callLater(self.notifyUser(message))

    def notifyUser(message):
        HubbeBot.sendResponse(IRCResponse(ResponseType.Say, message.User.Name + ": Time is up!", message.ReplyTo))
