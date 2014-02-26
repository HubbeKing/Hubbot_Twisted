from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import random

class Instantiate(Function):
    Help = "Reveal the secret inside... WHAT ARE YOU REALLY?"

    def GetResponse(self, HubbeBot, message):
        if message.Type != "PRIVMSG":
            return
        if message.MessageString.lower().startswith("meow"):
            roll = random.randint(1,20)
            if (message.User.Name == "BillTheCat"):
                return IRCResponse(ResponseType.Say, "Uhm... Hi?", message.ReplyTo)
            elif (roll == 1):
                reroll = random.randint(1,20)
                if (reroll == 20):
                    return IRCResponse(ResponseType.Do, "points at " + message.User.Name + ', "CRITICAL PUPPEH!"', message.ReplyTo), IRCResponse(ResponseType.Say, "Wait, what?", message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Do, "points at " + message.User.Name + ', "NOT EVEN A LITTLE BIT KITTEH."', message.ReplyTo)
            elif (roll > 1) and (roll < 8):
                return IRCResponse(ResponseType.Do, "points at " + message.User.Name + ', "NOT KITTEH."', message.ReplyTo)
            elif (roll > 7) and (roll < 14):
                return IRCResponse(ResponseType.Do, "points at " + message.User.Name + ', "MAYBE KITTEH?"', message.ReplyTo)
            elif (roll > 13) and (roll < 20):
                return IRCResponse(ResponseType.Do, "points at " + message.User.Name + ', "KITTEH!"', message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Do, "points at " + message.User.Name + ', "CRITICAL KITTEH!"', message.ReplyTo)
        if message.MessageString.lower().startswith("rawr"):
            roll = random.randint(1,20)
            if (message.User.Name == "Itazu") or (message.User.Name == "Trahsi"):
                return IRCResponse(ResponseType.Say, message.User.Name + " is a DRAGON!" , message.ReplyTo)
            elif (roll == 1):
                reroll = random.randint(1,20)
                if (reroll == 20):
                    return IRCResponse(ResponseType.Say, message.User.Name + " is SECRETLY A DRAGON!", message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, message.User.Name + " is NOT a DINOSAUR.", message.ReplyTo)
            elif (roll > 1) and (roll < 8):
                return IRCResponse(ResponseType.Say, message.User.Name + " is NOT a DINOSAUR.", message.ReplyTo)
            elif (roll > 7) and (roll < 14):
                return IRCResponse(ResponseType.Say, message.User.Name + " MIGHT be a DINOSAUR.", message.ReplyTo)
            elif (roll > 13) and (roll < 20):
                return IRCResponse(ResponseType.Say, message.User.Name + " is a DINOSAUR.", message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, message.User.Name + " is a CRITICAL DINOSAUR!", message.ReplyTo)
