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
        print "-#- Started to connect to '{}'.".format(self.bot.server)

    def buildProtocol(self, addr):
        print "-#- Connected to '{}'.".format(self.bot.server)
        print "-#- Resetting reconnection delay."
        self.resetDelay()
        return self.bot

    def clientConnectionLost(self, connector, reason):
        if not self.bot.Quitting:
            print "-!- Connection lost. Reason:", reason
            protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print "-!- Connection failed. Reason:", reason
        protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

