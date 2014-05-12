from IRCResponse import IRCResponse, ResponseType
from CommandInterface import CommandInterface
from CommandHandler import LoadCommand, UnloadCommand


class Command(CommandInterface):
    acceptedTypes = ["JOIN","QUIT"]
    Help = "RoBoBo joins, IdentCheck unloads. RoBoBo leaves, IdentCheck loads."

    def execute(self, Hubbot, message):
        if message.Type == 'JOIN':
            if message.User.Name.startswith("RoBoBo"):
                UnloadCommand("identcheck")
                return IRCResponse(ResponseType.Say, "IdentCheck unloaded.", message.ReplyTo)
        if message.Type == 'QUIT' or message.Type == 'PART':
            if message.User.Name.startswith("RoBoBo"):
                LoadCommand("identcheck")
                return IRCResponse(ResponseType.Say, "IdentCheck loaded.", message.ReplyTo)