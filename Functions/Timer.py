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
            flag = False
            if len(message.ParameterList) != 1:
                return IRCResponse(ResponseType.Say, "Please use only 1 argument.", message.ReplyTo)
            try:
                delay = int(message.ParameterList[0])
                flag = True
            except:
                delay = timeparse(message.ParameterList[0])
            if delay <= 0 or delay == None:
                return IRCResponse(ResponseType.Say, "I don't think I understand that...", message.ReplyTo)
            elif delay > (60*60*24*365):
                return IRCResponse(ResponseType.Say, "Do you really need a timer that long?", message.ReplyTo)
            elif delay < 1:
                return IRCResponse(ResponseType.Say, "Less than a second? Really?", message.ReplyTo)

            else:
                reactor.callLater(delay, self.notifyUser, HubbeBot, flag, message)
                if flag:
                    return IRCResponse(ResponseType.Say, message.User.Name + ": A " + message.ParameterList[0] + " second timer has been started!", message.ReplyTo)
                else: 
                    return IRCResponse(ResponseType.Say, message.User.Name + ": A " + message.ParameterList[0] + " timer has been started!", message.ReplyTo)
                    
            
    def notifyUser(self, HubbeBot, flag, message):
        if flag:
            HubbeBot.sendResponse(IRCResponse(ResponseType.Say, message.User.Name + ": Your " + message.ParameterList[0] + " second timer is up!" , message.ReplyTo))
        else:
            HubbeBot.sendResponse(IRCResponse(ResponseType.Say, message.User.Name + ": Your " + message.ParameterList[0] + " timer is up!" , message.ReplyTo))
