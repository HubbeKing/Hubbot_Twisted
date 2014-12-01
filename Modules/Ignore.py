import sqlite3
from ModuleInterface import ModuleInterface, ModuleAccessLevel
from IRCResponse import IRCResponse, ResponseType


class Ignore(ModuleInterface):
    triggers = ["ignore", "unignore"]
    help = "ignore/unignore <name> -- ignore <name> as much as possible, stop ignoring <name>"
    filename = "data/data.db"
    accessLevel = ModuleAccessLevel.ADMINS

    def onTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        if message.Command == "ignore":
            if len(message.ParameterList) == 1:
                with sqlite3.connect(self.filename) as conn:
                    c = conn.cursor()
                    c.execute("SELECT max(id) FROM ignores")
                    maxID = c.fetchone()[0]
                    if maxID is None:
                        maxID = 0
                    c.execute("INSERT INTO ignores VALUES (?,?)", (maxID+1, message.ParameterList[0]))
                    conn.commit()
                for (server, botfactory) in self.bot.bothandler.botfactories.iteritems():
                    botfactory.protocol.ignore.append(message.ParameterList[0])
                return IRCResponse(ResponseType.Say, "Successfully added '{}' to the ignores list.".format(message.ParameterList[0]), message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, "Currently ignoring: {}".format(", ".join(self.bot.ignores)), message.ReplyTo)
        elif message.Command == "unignore":
            if len(message.ParameterList) == 1:
                with sqlite3.connect(self.filename) as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM ignores WHERE nick=?", (message.ParameterList[0],))
                    conn.commit()
                for (server, botfactory) in self.bot.bothandler.botfactories.iteritems():
                    botfactory.ignores.remove(message.ParameterList[0])
                return IRCResponse(ResponseType.Say, "Successfully removed '{}' from the ignores list.".format(message.ParameterList[0]), message.ReplyTo)
