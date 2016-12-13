from __future__ import unicode_literals
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface
import random
import string


class Rustle(ModuleInterface):
    triggers = ["rustle"]
    help = "rustle <rustlee> - There's no need to be upset."

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) < 1:
            return IRCResponse(ResponseType.SAY, "Rustle who?", message.reply_to)
        else:
            roll = random.randint(1, 20)
            if roll == 1:
                return IRCResponse(ResponseType.SAY, "{} has rustled their own jimmies in their critical failure!".format(message.user.name), message.reply_to)
            elif (roll > 1) and (roll < 12):
                return IRCResponse(ResponseType.SAY, "{}'s jimmies status: unrustled".format(string.join(message.parameter_list)), message.reply_to)
            elif (roll > 11) and (roll < 20):
                return IRCResponse(ResponseType.SAY, "{}'s jimmies status: rustled".format(string.join(message.parameter_list)), message.reply_to)
            else:
                return IRCResponse(ResponseType.SAY, "{}'s jimmies status: CRITICAL RUSTLE".format(string.join(message.parameter_list)), message.reply_to)
