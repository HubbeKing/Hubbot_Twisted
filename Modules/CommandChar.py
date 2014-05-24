from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import GlobalVars


class CommandChar(ModuleInterface):
    triggers = ["commandchar"]
    help = "commandchar <char> -- changes the prefix for bot commands (admin-only)"

    def onTrigger(self, message):
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, "Only my admins can change my command character!", message.ReplyTo)
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "Change my command character to what?", message.ReplyTo)
        else:
            self.bot.CommandChar = message.ParameterList[0]
            return IRCResponse(ResponseType.Say, 'Command prefix char changed to \'{0}\'!'.format(self.bot.CommandChar), message.ReplyTo)