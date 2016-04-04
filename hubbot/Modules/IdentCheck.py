from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface
import re
import time


class IdentCheck(ModuleInterface):
    acceptedTypes = ["PRIVMSG", "ACTION"]
    help = "IdentCheck - Find out your TRUE identity... WHAT ARE YOU?"

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Type in self.acceptedTypes:
            return True
        return False

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        pointingPattern = "^points at {}.+(kitty|kitteh)".format(re.escape(self.bot.nickname))
        if message.ReplyTo in self.bot.channels.keys():
            if "RoBoBo" not in self.bot.channels[message.ReplyTo].Users.keys():
                if message.MessageString.lower().startswith("meow"):
                    roll = hash((message.User.Name, int(time.time()) / 3600, "meow")) % 20 + 1
                    if message.User.Name == "BillTheCat":
                        return IRCResponse(ResponseType.Say, "Uhm... Hi?", message.ReplyTo)
                    if message.User.Name.startswith(
                            "Caitiri") or message.User.Name == "Caity" or message.User.Name.startswith("Heuf"):
                        if roll == 20:
                            return IRCResponse(ResponseType.Do,
                                               'points at {}, "CRITICAL KITTEH!"'.format(message.User.Name),
                                               message.ReplyTo)
                        else:
                            return IRCResponse(ResponseType.Do,
                                               'points at {}, "KITTEH!"'.format(message.User.Name),
                                               message.ReplyTo)
                    elif roll == 1:
                        reroll = hash((message.User.Name, int(time.time()) / 3600, "meow", 42)) % 20 + 1
                        if reroll == 20:
                            return [IRCResponse(ResponseType.Do,
                                                'points at {}, "CRITICAL PUPPEH!"'.format(message.User.Name),
                                                message.ReplyTo),
                                    IRCResponse(ResponseType.Say,
                                                "Wait, what?",
                                                message.ReplyTo)]
                        else:
                            return IRCResponse(ResponseType.Do,
                                               'points at {}, "NOT KITTEH."'.format(message.User.Name),
                                               message.ReplyTo)
                    elif (roll > 1) and (roll < 8):
                        return IRCResponse(ResponseType.Do,
                                           'points at {}, "NOT KITTEH."'.format(message.User.Name),
                                           message.ReplyTo)
                    elif (roll > 7) and (roll < 14):
                        return IRCResponse(ResponseType.Do,
                                           'points at {}, "MEHBEH KITTEH?"'.format(message.User.Name),
                                           message.ReplyTo)
                    elif (roll > 13) and (roll < 20):
                        return IRCResponse(ResponseType.Do,
                                           'points at {}, "KITTEH!"'.format(message.User.Name),
                                           message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Do,
                                           'points at {}, "CRITICAL KITTEH!"'.format(message.User.Name),
                                           message.ReplyTo)
                elif message.MessageString.lower().startswith("rawr"):
                    roll = hash((message.User.Name, int(time.time()) / 3600, "rawr")) % 20 + 1
                    dragons = ["Itazu", "Trahsi", "reptile"]
                    if message.User.Name in dragons:
                        return IRCResponse(ResponseType.Say,
                                           "{} is a DRAGON!".format(message.User.Name),
                                           message.ReplyTo)
                    elif roll == 1:
                        reroll = hash((message.User.Name, int(time.time()) / 3600, "rawr", 42)) % 20 + 1
                        if reroll == 20:
                            return IRCResponse(ResponseType.Say,
                                               "{} is SECRETLY A DRAGON!".format(message.User.Name),
                                               message.ReplyTo)
                        else:
                            return IRCResponse(ResponseType.Say,
                                               "{} is NOT a DINOSAUR.".format(message.User.Name),
                                               message.ReplyTo)
                    elif (roll > 1) and (roll < 8):
                        return IRCResponse(ResponseType.Say,
                                           "{} is NOT a DINOSAUR.".format(message.User.Name),
                                           message.ReplyTo)
                    elif (roll > 7) and (roll < 14):
                        return IRCResponse(ResponseType.Say,
                                           "{} MIGHT be a DINOSAUR.".format(message.User.Name),
                                           message.ReplyTo)
                    elif (roll > 13) and (roll < 20):
                        return IRCResponse(ResponseType.Say,
                                           "{} is a DINOSAUR.".format(message.User.Name),
                                           message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say,
                                           "{} is a CRITICAL DINOSAUR!".format(message.User.Name),
                                           message.ReplyTo)
                elif message.Type == "ACTION" and re.match(pointingPattern, message.MessageString, re.IGNORECASE):
                    return IRCResponse(ResponseType.Say,
                                       "Curses, you've tumbled my nefarious plan!",
                                       message.ReplyTo)
