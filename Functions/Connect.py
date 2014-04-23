from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars

class Instantiate(Function):
    Help = "connect <server:port> <channel> - connect to a new server"

    def GetResponse(self, Hubbot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command == "connect" and message.User.Name in GlobalVars.admins:
            if len(message.ParameterList)>=2:
                server_with_port = message.ParameterList[0]
                server = server_with_port.split(":")[0]
                port = int(server_with_port.split(":")[1])
                channels = message.ParameterList[1:]
                GlobalVars.bothandler.startBotFactory(server, port, channels)
                
