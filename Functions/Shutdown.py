from IRCResponse import IRCResponse, ResponseType
from IRCMessage import IRCMessage
from Function import Function
import GlobalVars

class Instantiate(Function):
    Help = "shutdown - shut down all the bots everywhere"

    def GetResponse(self, Hubbot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "shutdown" and message.User.Name in GlobalVars.admins:
            GlobalVars.bothandler.shutdown()
