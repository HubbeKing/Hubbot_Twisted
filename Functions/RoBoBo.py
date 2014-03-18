from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function

from FunctionHandler import LoadFunction, UnloadFunction

class Instantiate(Function):
    Help = "RoBoBo joins, IdentCheck unloads. RoBoBo leaves, IdentCheck loads."

    def GetResponse(self, HubbeBot, message):
        if message.Type == 'JOIN':
            if message.User.Name.startswith("RoBoBo"):
                UnloadFunction("IdentCheck")
                return IRCResponse(ResponseType.Say, "IdentCheck unloaded.", message.ReplyTo)
        if message.Type == 'QUIT' or message.Type == 'PART':
            if message.User.Name.startswith("RoBoBo"):
                LoadFunction("IdentCheck")
                return IRCResponse(ResponseType.Say, "IdentCheck loaded.", message.ReplyTo)
