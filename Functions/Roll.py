from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import random

class Instantiate(Function):
    Help = "roll <dice> - Roll up some polyhedral dice! Ex: XdY+Zv - roll X Y-sided dice, with a +Z modifier and verbose output"

    def GetResponse(self, HubbeBot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "roll":
            verbose = False
            negIndex = posIndex = False
            if len(message.ParameterList) < 1:
                return IRCResponse(ResponseType.Say, "Roll what?", message.ReplyTo)
            if message.ParameterList[0].find("d")==-1:
                return IRCResponse(ResponseType.Say, "I don't understand that expression...", message.ReplyTo)
            else:
                dIndex = message.ParameterList[0].index("d")
            if message.ParameterList[0].find("v")==-1 or message.ParameterList[1].find("v"):
                continue
            else:
                verbose = True
            if message.ParameterList[0].find("+")==-1:
                if message.ParameterList[0].find("-")==-1:
                    if len(message.ParameterList) != 2:
                        modifier = 0
                    else:
                        # interpret ParameterList[1] as modifier
                        modifier = int(ParameterList[1])
                else:
                    # find - modifier in ParameterList[0]
                    negIndex = message.ParameterList[0].index("-")
                    try:
                        modifier = int(message.ParameterList[0][negIndex:])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)
            else:
                # find + modifier in ParameterList[0]
                posIndex = message.ParameterList[0].index("+")
                try:
                    modifier = int(message.ParameterList[0][posIndex:])
                except:
                    return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)


            # use dIndex to interpret dice expression
            # roll them dice
            # if verbose, output entire list and sum, otherwise just sum
