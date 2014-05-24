from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import GlobalVars


class Source(ModuleInterface):
    triggers = ["source"]

    def onLoad(self):
        self.help = "source - returns a link to {}'s source".format(self.bot.nickname)

    def onTrigger(self, message):
        return IRCResponse(ResponseType.Say, GlobalVars.source, message.ReplyTo)