import datetime
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class BotHandling(ModuleInterface):
    triggers = ["connect", "quit", "quitfrom", "restart", "shutdown"]
    accessLevel = ModuleAccessLevel.ADMINS

    def help(self, message):
        helpDict = {
            u"bothandling": u"connect <server> <channel>, quit, quitfrom <server>, restart, shutdown - Connect to / Disconnect from servers, Restart current bot, Shut down all bots",
            u"connect": u"connect <server>[:port] <channel> - Connects to the specified server and channel.",
            u"quit": u"quit - Quits from the current server.",
            u"quitfrom": u"quitfrom <server> - Quits from the specified server.",
            u"restart": u"restart - Restarts the entire bot, reconnecting using currently loaded config.",
            u"shutdown": u"shutdown - Shuts the entire bot down."
        }
        return helpDict[message.ParameterList[0].lower()]

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
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
                self.bot.bothandler.startBotFactory(server, port, channels)
                if server not in self.bot.bothandler.botfactories:
                    return IRCResponse(ResponseType.Say, "Could not connect to server '{}'".format(server), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, "Connected to server '{}'".format(server), message.ReplyTo)

        if message.Command == "quit":
            if datetime.datetime.now() > self.bot.startTime + datetime.timedelta(seconds=10):
                self.bot.Quitting = True
                self.bot.restarting = False
                quitMessage = "ohok".encode("utf-8")
                self.bot.bothandler.stopBotFactory(self.bot.server, quitMessage)

        if message.Command == "quitfrom":
            if len(message.ParameterList) >= 1:
                for server in message.ParameterList:
                    if server in self.bot.bothandler.botfactories and server != self.bot.server:
                        self.bot.bothandler.stopBotFactory(server)
                        return IRCResponse(ResponseType.Say, "Successfully quit from server '{}'".format(server), message.ReplyTo)
                    elif server == self.bot.server:
                        return IRCResponse(ResponseType.Say, "Please use quit to quit from current server.", message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "I don't think I am on that server.", message.ReplyTo)

        if message.Command == "restart":
            if datetime.datetime.now() > self.bot.startTime + datetime.timedelta(seconds=10):
                self.bot.bothandler.restart()
                return

        if message.Command == "shutdown":
            if datetime.datetime.now() > self.bot.startTime + datetime.timedelta(seconds=10):
                self.bot.bothandler.shutdown()
                return
