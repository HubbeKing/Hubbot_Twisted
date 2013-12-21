from twisted.application import internet, service
from hubbebot import *

application = service.Application("AllTheHubbeBots")

internet.TCPClient("irc.desertbus.org", 6667, HubbeBotFactory()).setServiceParent(application)
