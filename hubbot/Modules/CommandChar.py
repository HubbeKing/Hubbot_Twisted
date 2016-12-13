from __future__ import unicode_literals
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType


class CommandChar(ModuleInterface):
    triggers = ["commandchar"]
    help = "commandchar <char> -- changes the prefix for bot commands (admin-only)"
    access_level = ModuleAccessLevel.ADMINS

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) == 0:
            return IRCResponse(ResponseType.SAY, "Change my command character to what?", message.reply_to)
        else:
            self.bot.command_char = message.parameter_list[0]
            return IRCResponse(ResponseType.SAY, "Command prefix char changed to {!r}".format(self.bot.command_char), message.reply_to)
