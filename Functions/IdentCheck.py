from IRCResponse import IRCResponse, ResponseType
from Function import Function
import random

class Instantiate(Function):
    Help = "IdentCheck - Find out your TRUE identity... WHAT ARE YOU?"

    def GetResponse(self, HubbeBot, message):
        if message.Type != "PRIVMSG":
            return
        if message.MessageString.lower().startswith("meow"):
            roll = random.randint(1,20)
            if (message.User.Name == "BillTheCat"):
                return IRCResponse(ResponseType.Say, "Uhm... Hi?", message.ReplyTo)
            if message.User.Name.startswith("Caitiri") or message.User.Name == "Caity":
                return IRCResponse(ResponseType.Do, 'points at {}, "KITTEH!"'.format(message.User.Name), message.ReplyTo)
            elif (roll == 1):
                reroll = random.randint(1,20)
                if (reroll == 20):
                    return IRCResponse(ResponseType.Do, 'points at {}, "CRITICAL PUPPEH!"'.format(message.User.Name), message.ReplyTo), IRCResponse(ResponseType.Say, "Wait, what?", message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Do, 'points at {}, "NOT KITTEH."'.format(message.User.Name), message.ReplyTo)
            elif (roll > 1) and (roll < 8):
                return IRCResponse(ResponseType.Do, 'points at {}, "NOT KITTEH."'.format(message.User.Name), message.ReplyTo)
            elif (roll > 7) and (roll < 14):
                return IRCResponse(ResponseType.Do, 'points at {}, "MEHBEH KITTEH?"'.format(message.User.Name), message.ReplyTo)
            elif (roll > 13) and (roll < 20):
                return IRCResponse(ResponseType.Do, 'points at {}, "KITTEH!"'.format(message.User.Name), message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Do, 'points at {}, "CRITICAL KITTEH!"'.format(message.User.Name), message.ReplyTo)
        if message.MessageString.lower().startswith("rawr"):
            roll = random.randint(1,20)
            if (message.User.Name == "Itazu") or (message.User.Name == "Trahsi") or (message.User.Name == "reptile"):
                return IRCResponse(ResponseType.Say, "{} is a DRAGON!".format(message.User.Name) , message.ReplyTo)
            elif (roll == 1):
                reroll = random.randint(1,20)
                if (reroll == 20):
                    return IRCResponse(ResponseType.Say, " is SECRETLY A DRAGON!".format(message.User.Name), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, "{} is NOT a DINOSAUR.".format(message.User.Name), message.ReplyTo)
            elif (roll > 1) and (roll < 8):
                return IRCResponse(ResponseType.Say, "{} is NOT a DINOSAUR.".format(message.User.Name), message.ReplyTo)
            elif (roll > 7) and (roll < 14):
                return IRCResponse(ResponseType.Say, "{} MIGHT be a DINOSAUR.".format(message.User.Name), message.ReplyTo)
            elif (roll > 13) and (roll < 20):
                return IRCResponse(ResponseType.Say, "{} is a DINOSAUR.".format(message.User.Name), message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, "{} is a CRITICAL DINOSAUR!".format(message.User.Name), message.ReplyTo)
