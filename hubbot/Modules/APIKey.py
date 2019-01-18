import sqlite3
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType


class APIKey(ModuleInterface):
    triggers = ["apikey"]
    help = "apikey <name> <api_key> -- adds an API key to the database"
    access_level = ModuleAccessLevel.ADMINS

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) == 2:
            with sqlite3.connect(self.bot.database_file) as conn:
                c = conn.cursor()
                c.execute("CREATE TABLE IF NOT EXISTS keys (name text, apikey text)")
                c.execute("INSERT OR REPLACE INTO keys VALUES (?,?)", (message.parameter_list[0], message.parameter_list[1]))
                conn.commit()
            return IRCResponse(ResponseType.SAY, "Inserted API key into database as {!r}.".format(message.parameter_list[0]), message.reply_to)
