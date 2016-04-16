import datetime
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class BotHandling(ModuleInterface):
    triggers = ["quit", "quitfrom", "restart", "shutdown"]
    accessLevel = ModuleAccessLevel.ADMINS

    def help(self, message):
        helpDict = {
            u"bothandling": u"quit, quitfrom <server>, restart, shutdown - Disconnect from servers, Restart, and Shutdown. Fairly self-explanatory.",
            u"quit": u"quit - Quits from the current server.",
            u"quitfrom": u"quitfrom <server> - Quits from the specified server.",
            u"restart": u"restart - Restarts the entire bot.",
            u"shutdown": u"shutdown - Shuts the entire bot down."
        }
        return helpDict[message.ParameterList[0].lower()]

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """

        if message.Command == "quit":
            if datetime.datetime.now() > self.bot.startTime + datetime.timedelta(seconds=10):
                self.bot.Quitting = True
                self.bot.restarting = False
                quitMessage = "ohok".encode("utf-8")
                self.bot.bothandler.stopBotFactory(self.bot.server, quitMessage)

        elif message.Command == "quitfrom":
            if len(message.ParameterList) >= 1:
                for server in message.ParameterList:
                    if server in self.bot.bothandler.botfactories and server != self.bot.server:
                        self.bot.bothandler.stopBotFactory(server)
                        return IRCResponse(ResponseType.Say, "Successfully quit from server '{}'".format(server), message.ReplyTo)
                    elif server == self.bot.server:
                        return IRCResponse(ResponseType.Say, "Please use quit to quit from current server.", message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "I don't think I am on that server.", message.ReplyTo)

        elif message.Command == "restart":
            if datetime.datetime.now() > self.bot.startTime + datetime.timedelta(seconds=10):
                self.bot.bothandler.restart()
                return

        elif message.Command == "shutdown":
            if datetime.datetime.now() > self.bot.startTime + datetime.timedelta(seconds=10):
                self.bot.bothandler.shutdown()
                return
