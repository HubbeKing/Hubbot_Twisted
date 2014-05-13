from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import random


class Module(ModuleInterface):
    triggers = ["roll"]
    help = "roll <dice> - Roll up some polyhedral dice! Ex: 4d20v +8 - roll 4 20-sided dice, with a +8 modifier and verbose output"

    def execute(self, Hubbot, message):
        if len(message.ParameterList) > 1:
            if message.ParameterList[0].find("v") == -1 and message.ParameterList[1].find("v") == -1:
                verbose = False
                paramList = message.ParameterList
            else:
                verbose = True
                paramList = []
                for item in message.ParameterList:
                    paramList.append(item.replace("v", ""))
        elif message.ParameterList[0].find("v") == -1 and len(message.ParameterList) == 1:
            verbose = False
            paramList = message.ParameterList
        else:
            verbose = True
            paramList = []
            for item in message.ParameterList:
                paramList.append(item.replace("v", ""))
        negIndex = posIndex = False

        if len(paramList) < 1:
            return IRCResponse(ResponseType.Say, "Roll what?", message.ReplyTo)
        if paramList[0].find("d") == -1:
            return IRCResponse(ResponseType.Say, "I don't understand that expression...", message.ReplyTo)
        else:
            dIndex = paramList[0].index("d")

        if paramList[0].find("+") == -1:
            if paramList[0].find("-") == -1:
                if len(paramList) != 2:
                    modifier = 0
                else:
                    # interpret ParameterList[1] as modifier
                    try:
                        modifier = int(paramList[1])
                    except:
                        return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)
            else:
                # find - modifier in ParameterList[0]
                negIndex = paramList[0].index("-")
                try:
                    modifier = int(paramList[0][negIndex + 1:])
                    modifier = -modifier
                except:
                    return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)
        else:
            # find + modifier in ParameterList[0]
            posIndex = paramList[0].index("+")
            try:
                modifier = int(paramList[0][posIndex + 1:])
            except:
                return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)

        if not negIndex and not posIndex:
            # no modifier in ParameterList[0]
            try:
                sides = int(paramList[0][dIndex + 1:])
            except:
                return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)
            try:
                numberOfDice = int(paramList[0][0:dIndex])
            except:
                return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)
        else:
            if negIndex:
                # negative sign in ParameterList[0]
                try:
                    sides = int(paramList[0][dIndex + 1:negIndex])
                except:
                    return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)
                try:
                    numberOfDice = int(paramList[0][0:dIndex])
                except:
                    return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)
            else:
                # positive sign in ParameterList[0]
                try:
                    sides = int(paramList[0][dIndex + 1:posIndex])
                except:
                    return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)
                try:
                    numberOfDice = int(paramList[0][0:dIndex])
                except:
                    return IRCResponse(ResponseType.Say, "I don't think that's a number.", message.ReplyTo)

        if numberOfDice > (2 ** 16):
            return IRCResponse(ResponseType.Say, "I can't roll that many dice, silly!", message.ReplyTo)
        elif sides > (2 ** 16):
            return IRCResponse(ResponseType.Say, "I can't roll dice that big, silly!", message.ReplyTo)
        elif sides == 0:
            return IRCResponse(ResponseType.Say, "You found 0-sided dice?! WHERE?!?", message.ReplyTo)
        elif verbose and numberOfDice <= 20:
            results = (random.randint(1, sides) for x in xrange(numberOfDice))
        else:
            results = sum(random.randint(1, sides) for x in xrange(numberOfDice))

        if modifier == 0:
            modString = ""
        elif modifier < 0:
            modString = " -" + str(abs(modifier))
        else:
            modString = " +" + str(abs(modifier))

        if verbose and numberOfDice <= 20:
            # output entire list and sum
            resultList = list(results)
            return IRCResponse(ResponseType.Say,
                               "{} rolled: {}{} | {:,}".format(message.User.Name, resultList, modString,
                                                               sum(resultList) + modifier), message.ReplyTo)
        elif verbose and numberOfDice > 20:
            return IRCResponse(ResponseType.Say,
                               "{} rolled: [LOTS]{} | {:,}".format(message.User.Name, modString, results + modifier),
                               message.ReplyTo)
        else:
            # output sum
            return IRCResponse(ResponseType.Say, "{} rolled: {:,}".format(message.User.Name, results + modifier),
                               message.ReplyTo)