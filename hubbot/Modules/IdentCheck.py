from __future__ import unicode_literals
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface
try:
    import re2 as re
except ImportError:
    import re
import time


class IdentCheck(ModuleInterface):
    accepted_types = ["PRIVMSG", "ACTION"]
    help = "IdentCheck - Find out your TRUE identity... WHAT ARE YOU?"

    def should_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.type in self.accepted_types:
            return True
        return False

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        pointing_pattern = "^points at {}.+(kitty|kitteh)".format(re.escape(self.bot.nickname))
        if message.reply_to in self.bot.channels.keys():
            if "RoBoBo" not in self.bot.channels[message.reply_to].users.keys():
                if message.message_string.lower().startswith("meow"):
                    roll = hash((message.user.name, int(time.time()) / 3600, "meow")) % 20 + 1
                    if message.user.name == "BillTheCat":
                        return IRCResponse(ResponseType.SAY, "Uhm... Hi?", message.reply_to)
                    if message.user.name.startswith(
                            "Caitiri") or message.user.name == "Caity" or message.user.name.startswith("Heuf"):
                        if roll == 20:
                            return IRCResponse(ResponseType.DO,
                                               'points at {}, "CRITICAL KITTEH!"'.format(message.user.name),
                                               message.reply_to)
                        else:
                            return IRCResponse(ResponseType.DO,
                                               'points at {}, "KITTEH!"'.format(message.user.name),
                                               message.reply_to)
                    elif roll == 1:
                        reroll = hash((message.user.name, int(time.time()) / 3600, "meow", 42)) % 20 + 1
                        if reroll == 20:
                            return [IRCResponse(ResponseType.DO,
                                                'points at {}, "CRITICAL PUPPEH!"'.format(message.user.name),
                                                message.reply_to),
                                    IRCResponse(ResponseType.SAY,
                                                "Wait, what?",
                                                message.reply_to)]
                        else:
                            return IRCResponse(ResponseType.DO,
                                               'points at {}, "NOT KITTEH."'.format(message.user.name),
                                               message.reply_to)
                    elif (roll > 1) and (roll < 8):
                        return IRCResponse(ResponseType.DO,
                                           'points at {}, "NOT KITTEH."'.format(message.user.name),
                                           message.reply_to)
                    elif (roll > 7) and (roll < 14):
                        return IRCResponse(ResponseType.DO,
                                           'points at {}, "MEHBEH KITTEH?"'.format(message.user.name),
                                           message.reply_to)
                    elif (roll > 13) and (roll < 20):
                        return IRCResponse(ResponseType.DO,
                                           'points at {}, "KITTEH!"'.format(message.user.name),
                                           message.reply_to)
                    else:
                        return IRCResponse(ResponseType.DO,
                                           'points at {}, "CRITICAL KITTEH!"'.format(message.user.name),
                                           message.reply_to)
                elif message.message_string.lower().startswith("rawr"):
                    roll = hash((message.user.name, int(time.time()) / 3600, "rawr")) % 20 + 1
                    dragons = ["Itazu", "Trahsi", "reptile"]
                    if message.user.name in dragons:
                        return IRCResponse(ResponseType.SAY,
                                           "{} is a DRAGON!".format(message.user.name),
                                           message.reply_to)
                    elif roll == 1:
                        reroll = hash((message.user.name, int(time.time()) / 3600, "rawr", 42)) % 20 + 1
                        if reroll == 20:
                            return IRCResponse(ResponseType.SAY,
                                               "{} is SECRETLY A DRAGON!".format(message.user.name),
                                               message.reply_to)
                        else:
                            return IRCResponse(ResponseType.SAY,
                                               "{} is NOT a DINOSAUR.".format(message.user.name),
                                               message.reply_to)
                    elif (roll > 1) and (roll < 8):
                        return IRCResponse(ResponseType.SAY,
                                           "{} is NOT a DINOSAUR.".format(message.user.name),
                                           message.reply_to)
                    elif (roll > 7) and (roll < 14):
                        return IRCResponse(ResponseType.SAY,
                                           "{} MIGHT be a DINOSAUR.".format(message.user.name),
                                           message.reply_to)
                    elif (roll > 13) and (roll < 20):
                        return IRCResponse(ResponseType.SAY,
                                           "{} is a DINOSAUR.".format(message.user.name),
                                           message.reply_to)
                    else:
                        return IRCResponse(ResponseType.SAY,
                                           "{} is a CRITICAL DINOSAUR!".format(message.user.name),
                                           message.reply_to)
                elif message.type == "ACTION" and re.match(pointing_pattern, message.message_string, re.IGNORECASE):
                    return IRCResponse(ResponseType.SAY,
                                       "Curses, you've tumbled my nefarious plan!",
                                       message.reply_to)
