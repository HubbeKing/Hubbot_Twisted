import sqlite3
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType


class APIKey(ModuleInterface):
    triggers = ["apikey"]
    help = "apikey <name> <api_key> -- adds an API key to the database"
    accessLevel = ModuleAccessLevel.ADMINS

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 2:
            with sqlite3.connect(self.bot.databaseFile) as conn:
                c = conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS keys (name text, apikey text)")
                c.execute("INSERT INTO keys VALUES (?,?)", (message.ParameterList[0], message.ParameterList[1]))
                conn.commit()
            return IRCResponse(ResponseType.Say, "Inserted API key into database as \"{}\".".format(message.ParameterList[0]), message.ReplyTo)