import os

functions = {}

CurrentNick = "Hubbot"
connections = {"irc.desertbus.org":["#desertbus", "#unmoderated"], "irc.applejack.me":["#survivors"]}

port = 6667

admins = ["HubbeKing", "HubbeWork", "HubbePhone", "DoctorGyarados",\
          "DoctorGyaradroid", "DoctorGyarados|GAEM",\
          "DoctorGyarados|Away", "Docket", "Gyaradroid",\
          "Symphony", "Symphone", "Sympho|afk",\
          "Symphosewing", "Symphonom", "Symphonomnom"\
          "Heufy|Work", "HeufyDroid", "Heufneutje"]

finger = "Y U DO DIS"
version = "1.0.0"
source = "https://github.com/HubbeKing/Hubbot_Twisted/"

CommandChar = "+"

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
logPath = os.path.join(dname, "logs")

commonWords = ["and","of","all","to","the","both","back","again","any","one","<3","with","","<3s","so","hard","right","in","him","her","booper","up","on",":)","against","its","harder","teh","sneakgrabs","people",":3"]
