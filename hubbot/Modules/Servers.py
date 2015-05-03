from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Servers(ModuleInterface):
    serverDict = {
        "servers": "",
        "cockatrice": "The Cockatrice server is hosted at: cockatrice.dahou.se:4747",
        "gmod": "List of mods needed for GMOD: http://bit.ly/dahousegmod\n"
                "The Garry's Mod server is hosted at: gmod.dahou.se",
        "jcmp": "Ricin's Just Cause 2 MP server is hosted at: jcmp.117.me",
        "kf": "The Killing Floor server is hosted at: kf.dahou.se",
        "kf2": "The Killing Floor 2 server is hosted at: kf2.dahou.se",
        "ksp": "The Kerbal Space Program DMP server is hosted at: ksp.dahou.se",
        "mc": "The vanilla Minecraft server is hosted at lrrmc.dahou.se",
        "moddedmc": "The Bevo's Tech Pack server is hosted at craft.dahou.se (Contact a moderator to get whitelisted)",
        "mumble": 'The mumble server is hosted at: mumble.dahou.se',
        "starbound": "The Starbound server is hosted at: starbound.dahou.se",
        "starbound2": "Ricin's Starbound server is hosted at: sb.117.me",
        "tetri": "Ricin's Tetrinet server is hosted at: tn.ricin.us",
        "tf2": "The Team Fortress 2 server is hosted at tf2.dahou.se"
    }

    def help(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        helpDict = {
            "ksp": "In order to play on ksp.dahou.se, you need MechJeb and Kerbal Engineer installed.",
            "moddedmc": "In order to play on craft.dahou.se, you need Bevo's Tech Pack v11 Full.\n"
                        "The easiest way to get it is with AT Launcher (http://www.atlauncher.com/downloads)\n"
                        "You also have to enable Biomes O' Plenty, Blood Magic and Thaumcraft when installing the pack."
        }
        command = message.ParameterList[0].lower()
        if command in helpDict:
            return helpDict[command]
        else:
            return self.serverDict[command]

    def onEnable(self):
        self.triggers = self.serverDict.keys()
        serverList = [item for item in self.triggers if item != "servers"]
        self.serverDict["servers"] = "{} -- Used to post server info for games!".format(", ".join(sorted(serverList)))

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return IRCResponse(ResponseType.Say, self.serverDict[message.Command], message.ReplyTo)
