from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType


class CommandChar(ModuleInterface):
    triggers = ["commandchar"]
    help = "commandchar <char> -- changes the prefix for bot commands (admin-only)"
    accessLevel = ModuleAccessLevel.ADMINS

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "Change my command character to what?", message.ReplyTo)
        else:
            self.bot.CommandChar = message.ParameterList[0]
            return IRCResponse(ResponseType.Say, 'Command prefix char changed to \'{0}\'!'.format(self.bot.CommandChar), message.ReplyTo)
