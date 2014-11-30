from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface


class Source(ModuleInterface):
    triggers = ["source"]

    def onLoad(self):
        self.help = "source - returns a link to {}'s source".format(self.bot.nickname)

    def onTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        return IRCResponse(ResponseType.Say, self.bot.sourceURL, message.ReplyTo)
