from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import GlobalVars


class Module(ModuleInterface):
    help = "donotwant, yes, yup, store, goat, stupid, fixyou, heya, HNGH, PS, whoa, what, mybrand, both, no, disappointed -- Used to post silly things! Usage: {}<thing>".format(GlobalVars.CommandChar)

    def onStart(self):
        self.linkDict = \
            {
                "silly":"",
                "nope":"http://www.youtube.com/watch?v=gvdf5n-zI14",
                "donotwant":"http://www.youtube.com/watch?v=oKI-tD0L18A",
                "yes":"http://www.youtube.com/watch?v=P3ALwKeSEYs",
                "store":"http://www.youtube.com/watch?v=iRZ2Sh5-XuM",
                "stupid":"http://www.youtube.com/watch?v=yytbDZrw1jc",
                "fixyou":"http://www.youtube.com/watch?v=oin0KNElSG0",
                "yup":"http://www.youtube.com/watch?v=K0QHw7iy1Rg",
                "heya":"http://www.youtube.com/watch?v=ZZ5LpwO-An4",
                "what":"http://www.youtube.com/watch?v=PDXrXBsTFSE",
                "goat":"http://www.youtube.com/watch?v=SIaFtAKnqBU",
                "mybrand":"http://www.youtube.com/watch?v=V-fRuoMIfpw",
                "whoa":"http://www.youtube.com/watch?v=6q-gHrEaEAs",
                "hngh":"http://24.media.tumblr.com/tumblr_malzltlKk21rggqwfo1_500.gif",
                "ps":"https://docs.google.com/document/d/1C4Maba3fXrLYMMIXK67OOn7C2c31V6nff5inGAZStsw/edit?pli=1",
                "psc":"https://docs.google.com/document/d/1C4Maba3fXrLYMMIXK67OOn7C2c31V6nff5inGAZStsw/edit?pli=1",
                "both":"http://www.youtube.com/watch?v=OawrlVoQqSs",
                "no":"http://www.youtube.com/watch?v=YKss2uYpih8",
                "hunt":"",
                "<thing>":"Har Har.",
                "disappointed":"https://31.media.tumblr.com/cea6574a24b490ada8bec694e87b307b/tumblr_n3blu9k5CW1tsipf6o6_400.gif"
            }
        self.triggers.extend(self.linkDict.keys())

    def shouldTrigger(self, message):
        if message.Command in self.linkDict.keys() and message.Type in self.acceptedTypes:
            return True
        else:
            return False

    def onTrigger(self, Hubbot, message):
        if message.Command == "silly":
            return IRCResponse(ResponseType.Say, self.help, message.ReplyTo)
        elif message.Command == "hunt":
            if message.User.Name in GlobalVars.admins:
                line1 = "LAPTOP CHAT ENGAGE"
                line2 = "THRUSTERS TO MAXIMUM POWER"
                line3 = "FLOOD TUBES THREE AND FOUR"
                line4 = "HUNT FOR RED OCTOBER"
                return IRCResponse(ResponseType.Say, line1, message.ReplyTo), IRCResponse(ResponseType.Say, line2, message.ReplyTo), IRCResponse(ResponseType.Say, line3, message.ReplyTo), IRCResponse(ResponseType.Say, line4, message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, self.linkDict[message.Command], message.ReplyTo)