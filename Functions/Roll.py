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
            if len(message.ParameterList) > 1:
                if message.ParameterList[0].find("v")==-1 and message.ParameterList[1].find("v")==-1:
                    verbose = False
                    paramList = message.ParameterList
                else:
                    verbose = True
                    paramList = []
                    for item in message.ParameterList:
                        paramList.append(item.replace("v",""))
            elif message.ParameterList[0].find("v")==-1 and len(message.ParameterList) == 1:
                verbose = False
                paramList = message.ParameterList
            else:
                verbose = True
                paramList = []
                for item in message.ParameterList:
                    paramList.append(item.replace("v",""))
            negIndex = posIndex = False
            
            if len(paramList) < 1:
                return IRCResponse(ResponseType.Say, "Roll what?", message.ReplyTo)
            if paramList[0].find("d")==-1:
                return IRCResponse(ResponseType.Say, "I don't understand that expression...", message.ReplyTo)
            else:
                dIndex = paramList[0].index("d")
            
            if paramList[0].find("+")==-1:
                if paramList[0].find("-")==-1:
                    if len(paramList) != 2:
                        modifier = 0
                    else:
                        # interpret ParameterList[1] as modifier
                        try:
                            modifier = int(paramList[1])
                        except:
                            return IRCResponse(ResponseType.Say, "I don't understand that.41", message.ReplyTo)
                else:
                    # find - modifier in ParameterList[0]
                    negIndex = paramList[0].index("-")
                    try:
                        modifier = int(paramList[0][negIndex+1:])
                        modifier = -modifier
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.49", message.ReplyTo)
            else:
                # find + modifier in ParameterList[0]
                posIndex = paramList[0].index("+")
                try:
                    modifier = int(paramList[0][posIndex+1:])
                except:
                    return IRCResponse(ResponseType.Say, "I don't understand that.56", message.ReplyTo)

            if negIndex == False and posIndex == False:
                # no modifier in ParameterList[0]
                try:
                    sides = int(paramList[0][dIndex+1:])
                except:
                    return IRCResponse(ResponseType.Say, "I don't understand that.63", message.ReplyTo)
                try:
                    numberOfDice = int(paramList[0][0:dIndex])
                except:
                    return IRCResponse(ResponseType.Say, "I don't understand that.67", message.ReplyTo)
            else:
                if negIndex != False:
                    # negative sign in ParameterList[0]
                    try:
                        sides = int(paramList[0][dIndex+1:negIndex])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.74", message.ReplyTo)
                    try:
                        numberOfDice = int(paramList[0][0:dIndex])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.78", message.ReplyTo)
                else:
                    # positive sign in ParameterList[0]
                    try:
                        sides = int(paramList[0][dIndex+1:posIndex])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.84", message.ReplyTo)
                    try:
                        numberOfDice = int(paramList[0][0:dIndex])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't understand that.88", message.ReplyTo)
                    
            if numberOfDice < 33 and sides < 201:
                results = []
                for i in range(numberOfDice):
                    results.append(random.randint(1,sides))
            else:
                return IRCResponse(ResponseType.Say, "I can't roll that many dice, silly!", message.ReplyTo)

            if modifier > 100:
                return IRCResponse(ResponseType.Say, "That modifier is too big, silly!", message.ReplyTo)
            if modifier < -100:
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
