from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function

from FunctionHandler import LoadFunction, UnloadFunction

class Instantiate(Function):
    Help = "RoBoBo joins, IdentCheck unloads. RoBoBo leaves, IdentCheck loads."

    def GetResponse(self, HubbeBot, message):
        if message.Type == 'JOIN':
            if message.User.Name.startswith("RoBoBo"):
                UnloadFunction("Rustle")
                return IRCResponse(ResponseType.Say, "Rustle unloaded.", message.ReplyTo)
        if message.Type == 'QUIT' or message.Type == 'PART':
            if message.User.Name.startswith("RoBoBo"):
                LoadFunction("Rustle")
                return IRCResponse(ResponseType.Say, "Rustle loaded.", message.ReplyTo)
