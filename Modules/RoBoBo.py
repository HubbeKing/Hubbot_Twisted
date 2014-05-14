from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import ModuleLoader


class Module(ModuleInterface):
    acceptedTypes = ["JOIN","QUIT"]
    help = "RoBoBo joins, IdentCheck unloads. RoBoBo leaves, IdentCheck loads."

    def onTrigger(self, Hubbot, message):
        if message.Type == 'JOIN':
            if message.User.Name.startswith("RoBoBo"):
                ModuleLoader.unload("IdentCheck")
                return IRCResponse(ResponseType.Say, "IdentCheck unloaded.", message.ReplyTo)
        if message.Type == 'QUIT' or message.Type == 'PART':
            if message.User.Name.startswith("RoBoBo"):
                ModuleLoader.load("IdentCheck")
                return IRCResponse(ResponseType.Say, "IdentCheck loaded.", message.ReplyTo)