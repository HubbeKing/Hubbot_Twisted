from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

class Instantiate(Function):
    Help = "quitfrom <server> - disconnects from the given server"

    def GetResponse(self, Hubbot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "quitfrom" and message.User.Name in GlobalVars.admins:
            if len(message.ParameterList)>=1:
                for server in message.ParameterList:
                    GlobalVars.bothandler.botfactories[server].protocol.Quitting = True
                    GlobalVars.bothandler.stopBotFactory(server)
