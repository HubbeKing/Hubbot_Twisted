from twisted.internet import protocol, reactor
from hubbot.bot import Hubbot


class HubbotFactory(protocol.ReconnectingClientFactory):
    def __init__(self, server, port, channels, bothandler):
        """
        @type bothandler: hubbot.bothandler.BotHandler
        """
        self.port = port
        self.bot = Hubbot(server, channels, bothandler)
        self.protocol = self.bot
        reactor.connectTCP(server, port, self)

    def startedConnecting(self, connector):
        self.bot.logger.info("-#- Started to connect to '{}'.".format(self.bot.server))

    def buildProtocol(self, addr):
        self.bot.logger.info("-#- Connected to '{}'.".format(self.bot.server))
        self.bot.logger.info("-#- Resetting reconnection delay.")
        self.resetDelay()
        return self.bot

    def clientConnectionLost(self, connector, reason):
        if not self.bot.Quitting:
            self.bot.logger.info("-!- Connection lost. Reason:", reason)
            protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        self.bot.logger.info("-!- Connection failed. Reason:", reason)
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

