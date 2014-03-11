from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import random

class Instantiate(Function):
    Help = "roll <dice> - Roll up some polyhedral dice! Ex. roll 1d20"

    def GetResponse(self, HubbeBot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "roll":
            if len(message.ParameterList) < 1:
                return IRCResponse(ResponseType.Say, "Roll what?", message.ReplyTo)
            if message.ParameterList[0].find("d")==-1:
                return IRCResponse(ResponseType.Say, "I don't understand that expression...", message.ReplyTo)
            else:
                dIndex = message.ParameterList[0].index("d")
        
