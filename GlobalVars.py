import os

modules = {}
moduleCaseMapping = {}

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
logPath = os.path.join(dname, "logs")

commonWords = ["and","of","all","to","the","both","back","again",
               "any","one","<3","with","","<3s","so","hard","right",
               "in","him","her","booper","up","on",":)","against","its",
               "harder","teh","sneakgrabs","people",":3"]

bothandler = None


CurrentNick = "Hubbot"
connections = {"irc.desertbus.org:6667":["#desertbus", "#unmoderated"], "applejack.me:6667":["#survivors"]}
nonDefaultModules = ["IdentCheck"]

admins = ["HubbeKing", "HubbeWork", "HubbePhone", "DoctorGyarados",
          "DoctorGyaradroid", "DoctorGyarados|GAEM",
          "DoctorGyarados|Away", "Docket", "Gyaradroid",
          "Symphony", "Symphone", "Sympho|afk",
          "Symphosewing", "Symphonom", "Symphonomnom",
          "Heufy|Work", "HeufyDroid", "Heufneutje",
          "T-M|Work", "T-M|Phone", "Tyranic-Moron"]

finger = "Y U DO DIS"
version = "1.0.0"
source = "https://github.com/HubbeKing/Hubbot_Twisted/"

CommandChar = "+"



