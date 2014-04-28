from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function
import GlobalVars
import datetime

class Instantiate(Function):
    Help = "quit, quitfrom <server>, restart, shutdown - Disconnect from servers, Restart current bot, Shut down all bots"

    def GetResponse(self, Hubbot, message):
        if message.Type != "PRIVMSG":
            return
        if message.Command not in ["quit", "quitfrom", "restart", "shutdown"]:
            return
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, "You are not allowed to use '{}'".format(message.Command), message.ReplyTo)
        if message.Command == "quit":
            if datetime.datetime.now() > Hubbot.startTime + datetime.timedelta(seconds = 10):
                Hubbot.Quitting = True
                Hubbot.restarting = False
                quitMessage = "ohok".encode("utf-8")
                GlobalVars.bothandler.stopBotFactory(Hubbot.server, quitMessage)

        if message.Command == "quitfrom":
            if len(message.ParameterList)>=1:
                for server in message.ParameterList:
                    if server in GlobalVars.bothandler.botfactories and server!=Hubbot.server:
                        GlobalVars.bothandler.stopBotFactory(server)
                        return IRCResponse(ResponseType.Say, "Successfully quit from server '{}'".format(server), message.ReplyTo)
                    elif server == Hubbot.server:
                        return IRCResponse(ResponseType.Say, "Please use quit to quit from current server.", message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "I don't think I am on that server.", message.ReplyTo)

        if message.Command == "restart":
            if datetime.datetime.now() > Hubbot.startTime + datetime.timedelta(seconds = 10):
                Hubbot.Quitting = False
                Hubbot.restarting = True
                Hubbot.quit(message = "Restarting...")
                return

        if message.Command == "shutdown":
            if datetime.datetime.now() > Hubbot.starttime + datetime.timedelta(seconds = 10):
                GlobalVars.bothandler.shutdown()
                return
