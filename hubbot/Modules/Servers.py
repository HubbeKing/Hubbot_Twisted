from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Servers(ModuleInterface):
    serverDict = {
        "servers": "mumble, gmod, starbound, starbound2, jcmp, tetri, cockatrice, kf, tf2, moddedmc, mc -- Used to post server info for games!",
        "mumble": 'The mumble server is hosted at: mumble.dahou.se',
        "gmod": "List of mods needed for GMOD: http://bit.ly/dahousegmod\nThe Garry's Mod server is hosted at: gmod.dahou.se",
        "starbound": "The Starbound server is hosted at: starbound.dahou.se",
        "starbound2": "Ricin's Starbound server is hosted at: sb.117.me",
        "jcmp": "Ricin's Just Cause 2 MP server is hosted at: jcmp.117.me",
        "tetri": "Ricin's Tetrinet server is hosted at: tn.ricin.us",
        "cockatrice": "The Cockatrice server is hosted at: cockatrice.dahou.se:4747",
        "kf": "The Killing Floor server is hosted at: kf.dahou.se",
        "tf2": "The Team Fortress 2 server is hosted at tf2.dahou.se",
        "moddedmc": "The Bevo's Tech Pack v11 server is hosted at craft.dahou.se (Contact a moderator to get whitelisted)",
        "mc": "The vanilla Minecraft server is hosted at mc.dahou.se (Contact a moderator to get whitelisted)",
        "<server>": "Seriously?"
    }

    def help(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        helpDict = {
            "moddedmc": "In order to play on craft.dahou.se, you need Bevo's Tech Pack v11 Full.\n"
                        "You also have to enable Biomes O' Plenty, Blood Magic and Thaumcraft when installing it."
        }
        command = message.ParameterList[0].lower()
        if command in helpDict:
            return helpDict[command]
        else:
            return self.serverDict[command]

    def onLoad(self):
        self.triggers = self.serverDict.keys()

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return IRCResponse(ResponseType.Say, self.serverDict[message.Command], message.ReplyTo)
