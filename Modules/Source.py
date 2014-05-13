from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import GlobalVars


class Module(ModuleInterface):
    triggers = ["source"]
    help = "source - returns a link to {}'s source".format(GlobalVars.CurrentNick)

    def trigger(self, Hubbot, message):
        return IRCResponse(ResponseType.Say, GlobalVars.source, message.ReplyTo)