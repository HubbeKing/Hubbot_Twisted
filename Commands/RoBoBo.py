from IRCResponse import IRCResponse, ResponseType
from CommandInterface import CommandInterface
import FuncLoader


class Command(CommandInterface):
    acceptedTypes = ["JOIN","QUIT"]
    help = "RoBoBo joins, IdentCheck unloads. RoBoBo leaves, IdentCheck loads."

    def execute(self, Hubbot, message):
        if message.Type == 'JOIN':
            if message.User.Name.startswith("RoBoBo"):
                FuncLoader.unload("IdentCheck")
                return IRCResponse(ResponseType.Say, "IdentCheck unloaded.", message.ReplyTo)
        if message.Type == 'QUIT' or message.Type == 'PART':
            if message.User.Name.startswith("RoBoBo"):
                FuncLoader.load("IdentCheck")
                return IRCResponse(ResponseType.Say, "IdentCheck loaded.", message.ReplyTo)