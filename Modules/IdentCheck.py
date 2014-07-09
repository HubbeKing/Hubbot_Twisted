from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import random


class IdentCheck(ModuleInterface):
    help = "IdentCheck - Find out your TRUE identity... WHAT ARE YOU?"

    def shouldTrigger(self, message):
        return True

    def onTrigger(self, message):
        if message.ReplyTo in self.bot.channels.keys():
            if "RoBoBo" not in self.bot.channels[message.ReplyTo].Users.keys():
                if message.MessageString.lower().startswith("meow"):
                    roll = random.randint(1,20)
                    if message.User.Name == "BillTheCat":
                        return IRCResponse(ResponseType.Say, "Uhm... Hi?", message.ReplyTo)
                    if message.User.Name.startswith("Caitiri") or message.User.Name == "Caity":
                        return IRCResponse(ResponseType.Do, 'points at {}, "KITTEH!"'.format(message.User.Name), message.ReplyTo)
                    elif roll == 1:
                        reroll = random.randint(1,20)
                        if reroll == 20:
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
                    elif roll == 1:
                        reroll = random.randint(1,20)
                        if reroll == 20:
                            return IRCResponse(ResponseType.Say, "{} is SECRETLY A DRAGON!".format(message.User.Name), message.ReplyTo)
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
                if message.MessageString.lower().startswith("bleep bloop"):
                    roll = random.randint(1,20)
                    if roll == 1:
                        reroll = random.randint(1,20)
                        if reroll == 20:
                            return IRCResponse(ResponseType.Say, "{} is a CYBORG!".format(message.User.Name), message.ReplyTo)
                        else:
                            return IRCResponse(ResponseType.Say, "{} is NOT a ROBOT.".format(message.User.Name), message.ReplyTo)
                    elif (roll > 1) and (roll < 8):
                        return IRCResponse(ResponseType.Say, "{} is NOT a ROBOT.".format(message.User.Name), message.ReplyTo)
                    elif (roll > 7) and (roll < 14):
                        return IRCResponse(ResponseType.Say, "{} is PROBABLY a ROBOT.".format(message.User.Name), message.ReplyTo)
                    elif (roll > 13) and (roll < 20):
                        return IRCResponse(ResponseType.Say, "{} is TOTALLY a ROBOT.".format(message.User.Name), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "{} is a CRITICAL ROBOT!".format(message.User.Name), message.ReplyTo)
