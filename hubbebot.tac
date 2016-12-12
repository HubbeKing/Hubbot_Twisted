# run this with twistd -y hubbebot.tac

from twisted.application import internet, service
from hubbebot import HubbeBotFactory

application = service.Application("AllTheHubbeBots")
internet.TCPClient("irc.desertbus.org", 6667, HubbeBotFactory).setServiceParent(application)
# you can add more TCPClients here with different parameters
