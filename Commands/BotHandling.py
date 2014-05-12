from IRCResponse import IRCResponse, ResponseType
from CommandInterface import CommandInterface
import GlobalVars
import datetime


class Command(CommandInterface):
    triggers = ["connect", "quit", "quitfrom", "restart", "shutdown"]
    help = "connect <server> <channel>, quit, quitfrom <server>, restart, shutdown - Connect to / Disconnect from servers, Restart current bot, Shut down all bots"

    def execute(self, Hubbot, message):
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, "You are not allowed to use '{}'".format(message.Command), message.ReplyTo)

        if message.Command == "connect":
            if len(message.ParameterList) >= 2:
                server_with_port = message.ParameterList[0]
                if ":" in server_with_port:
                    server = server_with_port.split(":")[0]
                    port = int(server_with_port.split(":")[1])
                else:
                    server = server_with_port
                    port = 6667
                tmpChannels = message.ParameterList[1:]
                channels = []
                for chan in tmpChannels:
                    channels.append(chan.encode("ascii", "ignore"))
                GlobalVars.bothandler.startBotFactory(server, port, channels)
                if server not in GlobalVars.bothandler.botfactories:
                    return IRCResponse(ResponseType.Say, "Could not connect to server '{}'".format(server), message.ReplyTo)

        if message.Command == "quit":
            if datetime.datetime.now() > Hubbot.startTime + datetime.timedelta(seconds=10):
                Hubbot.Quitting = True
                Hubbot.restarting = False
                quitMessage = "ohok".encode("utf-8")
                GlobalVars.bothandler.stopBotFactory(Hubbot.server, quitMessage)

        if message.Command == "quitfrom":
            if len(message.ParameterList) >= 1:
                for server in message.ParameterList:
                    if server in GlobalVars.bothandler.botfactories and server != Hubbot.server:
                        GlobalVars.bothandler.stopBotFactory(server)
                        return IRCResponse(ResponseType.Say, "Successfully quit from server '{}'".format(server), message.ReplyTo)
                    elif server == Hubbot.server:
                        return IRCResponse(ResponseType.Say, "Please use quit to quit from current server.", message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "I don't think I am on that server.", message.ReplyTo)

        if message.Command == "restart":
            if datetime.datetime.now() > Hubbot.startTime + datetime.timedelta(seconds=10):
                server = Hubbot.server
                port = GlobalVars.bothandler.botfactories[server].port
                channels = Hubbot.channels
                GlobalVars.bothandler.stopBotFactory(Hubbot.server, "Restarting...")
                GlobalVars.bothandler.startBotFactory(server, port, channels)
                return

        if message.Command == "shutdown":
            if datetime.datetime.now() > Hubbot.startTime + datetime.timedelta(seconds=10):
                GlobalVars.bothandler.shutdown()
                return
