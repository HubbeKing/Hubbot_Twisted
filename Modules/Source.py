from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import GlobalVars


class Source(ModuleInterface):
    triggers = ["source"]
    help = "source - returns a link to {}'s source".format(GlobalVars.CurrentNick)

    def onTrigger(self, message):
        return IRCResponse(ResponseType.Say, GlobalVars.source, message.ReplyTo)