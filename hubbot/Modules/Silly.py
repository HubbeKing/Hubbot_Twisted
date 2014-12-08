from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Silly(ModuleInterface):
    sillyDict = {
        "silly": "",
        "both": "http://www.youtube.com/watch?v=OawrlVoQqSs",
        "disappointed": "https://31.media.tumblr.com/cea6574a24b490ada8bec694e87b307b/tumblr_n3blu9k5CW1tsipf6o6_400.gif",
        "donotwant": "http://www.youtube.com/watch?v=oKI-tD0L18A",
        "fixyou": "http://www.youtube.com/watch?v=oin0KNElSG0",
        "goat": "http://www.youtube.com/watch?v=SIaFtAKnqBU",
        "heya": "http://www.youtube.com/watch?v=ZZ5LpwO-An4",
        "hngh": "http://24.media.tumblr.com/tumblr_malzltlKk21rggqwfo1_500.gif",
        "hunt": "LAPTOP CHAT ENGAGE\nTHRUSTERS TO MAXIMUM POWER\nFLOOD TUBES THREE AND FOUR\nHUNT FOR RED OCTOBER",
        "mybrand": "http://www.youtube.com/watch?v=V-fRuoMIfpw",
        "nope": "http://www.youtube.com/watch?v=gvdf5n-zI14",
        "psc": "https://docs.google.com/document/d/1C4Maba3fXrLYMMIXK67OOn7C2c31V6nff5inGAZStsw/edit?pli=1",
        "store": "http://www.youtube.com/watch?v=iRZ2Sh5-XuM",
        "stupid": "http://www.youtube.com/watch?v=yytbDZrw1jc",
        "yes": "http://www.youtube.com/watch?v=P3ALwKeSEYs",
        "yup": "http://www.youtube.com/watch?v=K0QHw7iy1Rg",
        "what": "http://www.youtube.com/watch?v=PDXrXBsTFSE",
        "whoa": "http://www.youtube.com/watch?v=6q-gHrEaEAs"
    }

    def onLoad(self):
        self.triggers = self.sillyDict.keys()
        sillyList = [item for item in self.triggers if item != "silly"]
        self.sillyDict["silly"] = "{} -- Used to post silly things!".format(", ".join(sorted(sillyList)))

    def help(self, message):
        command = message.ParameterList[0].lower()
        if command != "hunt":
            return self.sillyDict[command]

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command == "hunt":
            if message.User.Name in self.bot.admins:
                return IRCResponse(ResponseType.Say, self.sillyDict["hunt"], message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, self.sillyDict[message.Command], message.ReplyTo)
