from IRCResponse import IRCResponse, ResponseType
from IRCMessage import IRCMessage
from Function import Function
import GlobalVars
import datetime

class Instantiate(Function):
    Help = "shutdown - shut down all the bots everywhere"

    def GetResponse(self, Hubbot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "shutdown" and datetime.datetime.now() > Hubbot.startTime + datetime.timedelta(seconds=10) and message.User.Name in GlobalVars.admins:
            GlobalVars.bothandler.shutdown()
