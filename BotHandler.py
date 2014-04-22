from twisted.internet import reactor
from hubbebot import HubbeBot, HubbeBotFactory
import GlobalVars

class BotHandler:
    botfactories = {}

    def __init__(self):
        for (server,channels) in GlobalVars.connections.items():
            self.startBotFactory(server, channels)

        reactor.run()

    def startBotFactory(self, server, channels):
        if server in self.botfactories:
            print "Already on server '{}'.".format(server)
            return False

        print "Joining server '{}'.".format(server)

        botfactory = HubbeBotFactory(server,channels)
        self.botfactories[server] = botfactory
        return True

    def stopBotFactory(self, server, quitmessage="ohok"):
        quitmessage = quitmessage.encode("utf-8")
        if server not in self.botfactories:
            print "ERROR: Bot for '{}' does not exist yet was asked to stop.".format(server)
        else:
            self.botfactories[server].protocol.quit(quitmessage)
            self.unregisterFactory(server)

    def unregisterFactory(self, server):
        if server in self.botfactories:
            del self.botfactories[server]

            if len(self.botfactories)==0:
                print "No more running bots, shutting down."
                reactor.callLater(2.0, reactor.stop)

if __name__=="__main__":
    bothandler = BotHandler()
