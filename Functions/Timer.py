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
            delay = float(message.ParameterList[0])
            return IRCResponse(ResponseType.Say, message.User.Name + ": A timer has been started!", message.ReplyTo)
            HubbeBot.reactor.callLater(delay, self.notifyUser(message), "timer")
            
    def notifyUser(message):
        HubbeBot.sendResponse(IRCResponse(ResponseType.Say, message.User.Name + ": Time is up!", message.ReplyTo))
