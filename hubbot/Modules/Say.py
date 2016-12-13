from __future__ import unicode_literals
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType


class Say(ModuleInterface):
    help = "say [channel] <thing> -- say a thing."
    triggers = ["say"]

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) == 0:
            return IRCResponse(ResponseType.SAY, "Say what?", message.reply_to)
        else:
            channel = message.parameter_list[0]
            if channel not in self.bot.channels:
                return IRCResponse(ResponseType.SAY, "{}".format(" ".join(message.parameter_list)), message.reply_to)
            else:
                return IRCResponse(ResponseType.SAY, "{}".format(" ".join(message.parameter_list[1:])), channel)
