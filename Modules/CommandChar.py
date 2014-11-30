from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType


class CommandChar(ModuleInterface):
    triggers = ["commandchar"]
    help = "commandchar <char> -- changes the prefix for bot commands (admin-only)"
    accessLevel = 1

    def onTrigger(self, message):
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "Change my command character to what?", message.ReplyTo)
        else:
            self.bot.commandChar = message.ParameterList[0]
            return IRCResponse(ResponseType.Say, 'Command prefix char changed to \'{0}\'!'.format(self.bot.CommandChar), message.ReplyTo)