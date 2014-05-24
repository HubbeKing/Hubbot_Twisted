import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
logPath = os.path.join(dname, "logs")

bothandler = None

connections = {"irc.desertbus.org:6667":["#desertbus", "#unmoderated"], "applejack.me:6667":["#survivors"]}

nonDefaultModules = ["Roll", "Grapheme", "GraphemeLearning"]

finger = "Y U DO DIS"
version = "1.0.0"
source = "https://github.com/HubbeKing/Hubbot_Twisted/"
