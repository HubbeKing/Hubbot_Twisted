from twisted.internet import reactor
from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars
import re
from timeparse import timeparse

class Instantiate(Function):
    Help = "timer <time> - starts a countdown timer and notifies you when time's up."

    def GetResponse(self, HubbeBot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "timer":
            if len(message.ParameterList) != 1:
                return IRCResponse(ResponseType.Say, "Please use only 1 argument.", message.ReplyTo)
            try:
                delay = timeparse(message.ParameterList[0])
                if delay > (60*60*24*365):
                    return IRCResponse(ResponseType.Say, "Do you really need a timer that long?", message.ReplyTo)
            except:
                return IRCResponse(ResponseType.Say, "I don't understand that time...", message.ReplyTo)
            if delay < 1:
                return IRCResponse(ResponseType.Say, "Less than a second? Really?", message.ReplyTo)
            else:
                reactor.callLater(delay, self.notifyUser, HubbeBot, message)
                return IRCResponse(ResponseType.Say, message.User.Name + ": A " + message.ParameterList[0] + " timer has been started!", message.ReplyTo)
            
            
    def notifyUser(self, HubbeBot, message):
        HubbeBot.sendResponse(IRCResponse(ResponseType.Say, message.User.Name + ": Your " + message.ParameterList[0] + " timer is up!" , message.ReplyTo))
