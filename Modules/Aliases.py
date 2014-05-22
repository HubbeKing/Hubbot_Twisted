from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType


class Aliases(ModuleInterface):
    triggers = ["aliases"]
    help = "aliases [alias] -- show information about current aliases"

    def onTrigger(self, message):
        if len(message.ParameterList) == 0:
            returnString = "Current aliases: "
            for alias, command in self.bot.moduleHandler.commandAliases.iteritems():
                returnString += alias +", "
            returnString = returnString.rstrip().rstrip(",")
            return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)
        elif message.ParameterList[0] in self.bot.moduleHandler.commandAliases.keys():
            return IRCResponse(ResponseType.Say, " ".join(self.bot.moduleHandler.commandAliases[message.ParameterList[0]]), message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, "'{}' does not match any known alias!".format(message.ParameterList[0]), message.ReplyTo)