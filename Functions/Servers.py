from IRCMessage import IRCMessage
from IRCResponse import IRCResponse, ResponseType
from Function import Function

class Instantiate(Function):
    Help = "mumble, gmod, theship/ship, starbound, starbound2, jcmp, tetri, cockatrice -- Used to post server info for games!"
    mumbleIP = 'The mumble server is hosted at: mumble.dahou.se:64740'
    gmodMods = 'List of mods needed for GMOD: http://steamcommunity.com/sharedfiles/filedetails/?id=185811989'
    gmodIP = "The Garrys Mod server is hosted at: gmod.dahou.se"
    theShipIP = 'The Ship server is hosted at: ash.dahou.se:27025'
    starboundIP = "The Starbound server is hosted at: starbound.dahou.se"
    jcmpIP = "Ricin's Just Cause 2 MP server is hosted at: jcmp.117.me"
    ricinStarboundIP = "Ricin's Starbound server is hosted at: sb.117.me"
    tetrinetIP = "Ricin's Tetrinet server is hosted at: tn.ricin.us"
    cockatriceIP = "The Cockatrice server is hosted at: cockatrice.dahou.se:4747"

    filename = "data/data.db"

    def GetResponse(self, message):
        if message.Command == "servers":
            return IRCResponse(ResponseType.Say, self.Help, message.ReplyTo)
        if message.Command == "mumble":
            return IRCResponse(ResponseType.Say, self.mumbleIP, message.ReplyTo)
        elif message.Command == "gmod":
            return IRCResponse(ResponseType.Say, self.gmodMods, message.ReplyTo), IRCResponse(ResponseType.Say, self.gmodIP, message.ReplyTo)
	elif message.Command == "theship" or message.Command == "ship":
            return IRCResponse(ResponseType.Say, self.theShipIP, message.ReplyTo)
        elif message.Command == "starbound":
            return IRCResponse(ResponseType.Say, self.starboundIP, message.ReplyTo)
        elif message.Command == "starbound2":
            return IRCResponse(ResponseType.Say, self.ricinStarboundIP, message.ReplyTo)
        elif message.Command == "jcmp":
            return IRCResponse(ResponseType.Say, self.jcmpIP, message.ReplyTo)
        elif message.Command == "tetri":
            return IRCResponse(ResponseType.Say, self.tetrinetIP, message.ReplyTo)
        elif message.Command == "cockatrice":
            return IRCResponse(ResponseType.Say, self.cockatriceIP, message.ReplyTo)
            

