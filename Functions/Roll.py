from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import random

class Instantiate(Function):
    Help = "roll <dice> - Roll up some polyhedral dice! Limited to 32d200 +/-100 Ex: XdYv +Z - roll X Y-sided dice, with a +Z modifier and verbose output"

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
                verbose = False
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
                        modifier = int(message.ParameterList[0][negIndex+1:])
                        modifier = -modifier
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)
            else:
                # find + modifier in ParameterList[0]
                posIndex = message.ParameterList[0].index("+")
                try:
                    modifier = int(message.ParameterList[0][posIndex+1:])
                except:
                    return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)

            if negIndex == False and posIndex == False:
                # no modifier in ParameterList[0]
                try:
                    sides = int(message.ParameterList[0][dIndex+1:])
                else:
                    return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)
                try:
                    numberOfDice = int(message.ParameterList[0][0:dIndex])
                except:
                    return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)
            else:
                if negIndex = False:
                    # negative sign in ParameterList[0]
                    try:
                        sides = int(message.ParameterList[0][dIndex+1:negIndex])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)
                    try:
                        numberOfDice = int(message.ParameterList[0][0:dIndex])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)
                else:
                    # positive sign in ParameterList[0]
                    try:
                        sides = int(message.ParameterList[0][dIndex+1:posIndex])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)
                    try:
                        numberOfDice = int(message.ParameterList[0][0:dIndex])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.", message.ReplyTo)
                    
            if numberOfDice < 33 and sides < 201:
                results = []
                for i in range(numberOfDice):
                    results.append(random.randint(1,sides))
            else:
                return IRCResponse(ResponseType.Say, "I can't roll that many dice, silly!", message.ReplyTo)

            if modifier > 100:
                return IRCResponse(ResponseType.Say, "That modifier is too big, silly!", message.ReplyTo)
            if modifier < 100:
                return IRCResponse(ResponseType.Say, "That modifier is too big, silly!", message.ReplyTo)

            if modifier < 0:
                modString = " -" + str(abs(modifier))
            else:
                modString = " +" + str(abs(modifier))
            
            if verbose:
                # output entire list and sum
                return IRCResponse(ResponseType.Say, message.User.Name + " rolled: " + str(results) + modString + " | " + str(sum(results)+modifier), message.ReplyTo)
            else:
                # output sum
                return IRCResponse(ResponseType.Say, message.User.Name + " rolled: " + str(sum(results)+modifier), message.ReplyTo)
