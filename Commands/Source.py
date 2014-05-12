from IRCResponse import IRCResponse, ResponseType
from CommandInterface import CommandInterface
import GlobalVars


class Command(CommandInterface):
    triggers = ["source"]
    Help = "source - returns a link to {}'s source".format(GlobalVars.CurrentNick)

    def execute(self, Hubbot, message):
        return IRCResponse(ResponseType.Say, GlobalVars.source, message.ReplyTo)