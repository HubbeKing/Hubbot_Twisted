from __future__ import unicode_literals
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType


class Unmask(ModuleInterface):
    triggers = ["unmask"]
    help = "unmask - sends a MODE -x command to unmask hostname on some ircds"
    access_level = ModuleAccessLevel.ADMINS
    
    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return IRCResponse(ResponseType.RAW, "MODE {} -x".format(self.bot.nickname), message.reply_to)
