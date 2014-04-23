from IRCResponse import IRCResponse, ResponseType
from IRCMessage import IRCMessage
from Function import Function
import GlobalVars

class Instantiate(Function):
    Help = "restart - restart the bot on the current server"

    def GetResponse(self, Hubbot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "restart" and message.User.Name in GlobalVars.admins:
            GlobalVars.bothandler.stopBotFactory(Hubbot.server, "Restarting...")
