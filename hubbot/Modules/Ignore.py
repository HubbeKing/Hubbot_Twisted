import sqlite3
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType


class Ignore(ModuleInterface):
    triggers = ["ignore", "unignore", "ignores"]
    accessLevel = ModuleAccessLevel.ADMINS

    def help(self, message):
        helpDict = {
            u"ignore": u"ignore [nick] -- Add someone to the ignore list.\n"
                       u"unignore [nick] -- Remove someone from the ignore list.\n"
                       u"ignores -- Returns the current ignore list.",
            u"unignore": u"unignore [nick] -- Remove someone from the ignore list.",
            u"ignores": u"ignores -- Returns the current ignore list."
        }
        command = message.ParameterList[0].lower()
        return helpDict[command]

    def onEnable(self):
        ignores = []
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT nick FROM ignores"):
                ignores.append(row[0])
        self.bot.ignores = ignores
        self.bot.logger.info("Loaded \"{}\" into ignores list.".format(", ".join(ignores)))

    def onDisable(self):
        self.bot.ignores = []
        self.bot.logger.info("Unloaded all ignores.")

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command == "ignore":
            if len(message.ParameterList) == 1:
                with sqlite3.connect(self.bot.databaseFile) as conn:
                    c = conn.cursor()
                    c.execute("SELECT max(id) FROM ignores")
                    maxID = c.fetchone()[0]
                    if maxID is None:
                        maxID = 0
                    c.execute("INSERT INTO ignores VALUES (?,?)", (maxID + 1, message.ParameterList[0]))
                    conn.commit()
                for (server, botfactory) in self.bot.bothandler.botfactories.iteritems():
                    botfactory.bot.ignore.append(message.ParameterList[0])
                return IRCResponse(ResponseType.Say,
                                   "Successfully added '{}' to the ignores list.".format(message.ParameterList[0]),
                                   message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, "Ignore who?", message.ReplyTo)
        elif message.Command == "unignore":
            if len(message.ParameterList) == 1:
                with sqlite3.connect(self.bot.databaseFile) as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM ignores WHERE nick=?", (message.ParameterList[0],))
                    conn.commit()
                for (server, botfactory) in self.bot.bothandler.botfactories.iteritems():
                    botfactory.bot.ignores.remove(message.ParameterList[0])
                return IRCResponse(ResponseType.Say,
                                   "Successfully removed '{}' from the ignores list.".format(message.ParameterList[0]),
                                   message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, "Unignore who?", message.ReplyTo)
        elif message.Command == "ignores":
            return IRCResponse(ResponseType.Say,
                               "Currently ignoring: {}".format(", ".join(self.bot.ignores)),
                               message.ReplyTo)
