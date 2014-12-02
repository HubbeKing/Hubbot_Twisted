import sqlite3
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType


class Aliases(ModuleInterface):
    triggers = ["aliases"]
    help = "aliases [alias] -- show information about current aliases"
    aliases = {}

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        self.aliases.clear()
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM aliases"):
                self.aliases[row[0]] = row[1].split(" ")
        if len(message.ParameterList) == 0:
            returnString = "Current aliases: "
            for alias, command in self.aliases.iteritems():
                returnString += alias +", "
            returnString = returnString.rstrip().rstrip(",")
            return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)
        elif message.ParameterList[0] in self.aliases.keys():
            return IRCResponse(ResponseType.Say, " ".join(self.aliases[message.ParameterList[0]]), message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, "'{}' does not match any known alias!".format(message.ParameterList[0]), message.ReplyTo)
