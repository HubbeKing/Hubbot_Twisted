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
                    if server in GlobalVars.bothandler.botfactories:
                        GlobalVars.bothandler.botfactories[server].protocol.Quitting = True
                        GlobalVars.bothandler.stopBotFactory(server)
                        return IRCResponse(ResponseType.Say, "Successfully quit from server '{}'".format(server), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "I don't think I am on that server.", message.ReplyTo)
