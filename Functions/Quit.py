from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

class Instantiate(Function):
    Help = "quit <message> - Disconnect."

    def GetResponse(self, Hubbot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "quit":
            if message.User.Name in GlobalVars.admins:
                if len(message.ParameterList)>0:
                    quitMessage = message.ParameterList[0].encode("utf-8")
                else:
                    quitMessage = "ohok".encode("utf-8")

                GlobalVars.bothandler.stopBotFactory(Hubbot.server, quitMessage)
