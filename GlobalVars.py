import os

functions = {}

CurrentNick = "Hubbot"
connections = {"irc.desertbus.org":["#desertbus", "#unmoderated", "#help", "#games"], "irc.applejack.me":["#survivors"]}

port = 6667

admins = ["HubbeKing", "HubbeWork", "HubbePhone", "DoctorGyarados",\
           "DoctorGyaradroid", "DoctorGyarados|GAEM",\
           "DoctorGyarados|Away", "Docket", "Gyaradroid",\
		   "Symphony", "Symphone", "Sympho|afk",\
           "Symphosewing", "Symphonom", "Symphonomnom"]

finger = "Y U DO DIS"
version = "1.0.0"
source = "https://github.com/HubbeKing/Hubbot_Twisted/"

CommandChar = "+"

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
logPath = os.path.join(dname, "logs")
