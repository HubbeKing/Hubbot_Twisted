from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import random, string

class Instantiate(Function):
    Help = "rustle <rustlee> - There's no need to be upset."

    def GetResponse(self, HubbeBot, message):
        if message.Type != "PRIVMSG":
            return
        
        if message.Command == "rustle":
            if len(message.ParameterList) < 1:
                return IRCResponse(ResponseType.Say, "Rustle who?", message.ReplyTo)
            else:
                roll = random.randint(1,20)
                if roll == 1:
                    return IRCResponse(ResponseType.Say, message.User.Name + " has rustled their own jimmies in their critical failure!", message.ReplyTo)
                elif  (roll > 1) and (roll < 12):
                    return IRCResponse(ResponseType.Say, string.join(message.ParameterList) + "'s jimmies status: unrustled", message.ReplyTo)
                elif (roll > 11) and (roll < 20):
                    return IRCResponse(ResponseType.Say, string.join(message.ParameterList) + "'s jimmies status: rustled", message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, string.join(message.ParameterList) + "'s jimmies status: CRITICAL RUSTLE", message.ReplyTo)
