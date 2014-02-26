from twisted.internet import reactor
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
            try:
                delay = float(message.ParameterList[0])
            except:
                return IRCResponse(ResponseType.Say, "That doesn't look like a number to me...", message.ReplyTo)
            reactor.callLater(delay, self.notifyUser, HubbeBot, delay, message)
            return IRCResponse(ResponseType.Say, message.User.Name + ": A timer has been started!", message.ReplyTo)
            
            
    def notifyUser(self, HubbeBot, delay, message):
        HubbeBot.sendResponse(IRCResponse(ResponseType.Say, message.User.Name + ": Your " + str(int(delay)) + " second timer is up!" , message.ReplyTo))
