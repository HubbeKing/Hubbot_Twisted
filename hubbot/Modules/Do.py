from __future__ import unicode_literals
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType


class Do(ModuleInterface):
    help = "do [channel] <thing> -- do a thing."
    triggers = ["do"]

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) == 0:
            return IRCResponse(ResponseType.SAY, "Do what?", message.reply_to)
        else:
            channel = message.parameter_list[0]
            if channel not in self.bot.channels:
                return IRCResponse(ResponseType.DO, "{}".format(" ".join(message.parameter_list)), message.reply_to)
            else:
                return IRCResponse(ResponseType.DO, "{}".format(" ".join(message.parameter_list[1:])), channel)
