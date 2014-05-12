from IRCResponse import IRCResponse, ResponseType
from CommandInterface import CommandInterface
import GlobalVars


class Command(CommandInterface):
    Help = "mumble, gmod, starbound, starbound2, jcmp, tetri, cockatrice, kf -- Used to post server info for games! Usage: {}<server>".format(GlobalVars.CommandChar)
    gmodMods = 'List of mods needed for GMOD: http://steamcommunity.com/sharedfiles/filedetails/?id=185811989'
    gmodIP = "The Garrys Mod server is hosted at: gmod.dahou.se"

    def onStart(self):
        serverDict = \
            {
                "servers":"",
                "mumble":'The mumble server is hosted at: mumble.dahou.se',
                "gmod":"",
                "starbound":"The Starbound server is hosted at: starbound.dahou.se",
                "starbound2":"Ricin's Starbound server is hosted at: sb.117.me",
                "jcmp":"Ricin's Just Cause 2 MP server is hosted at: jcmp.117.me",
                "tetri":"Ricin's Tetrinet server is hosted at: tn.ricin.us",
                "cockatrice":"The Cockatrice server is hosted at: cockatrice.dahou.se:4747",
                "kf":"The Killing Floor server is hosted at: kf.dahou.se"
            }
        self.triggers.extend(serverDict.keys())

    def shouldExecute(self, message):
        if message.Command in self.serverDict and message.Type in self.acceptedTypes:
            return True
        else:
            return False

    def execute(self, Hubbot, message):
        if message.Command == "servers":
            return IRCResponse(ResponseType.Say, self.Help, message.ReplyTo)
        elif message.Command == "gmod":
            return IRCResponse(ResponseType.Say, self.gmodMods, message.ReplyTo), IRCResponse(ResponseType.Say, self.gmodIP, message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, self.serverDict[message.Command], message.ReplyTo)