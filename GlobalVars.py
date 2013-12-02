import os

functions = {}

CurrentNick = "Hubbot"
server = "irc.desertbus.org"
port = 6667
channels = ["#desertbus"]
admins = ["HubbeKing"]

finger = "Y U DO DIS"
version = 0.1
source = ""

CommandChar = "+"

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
