import sqlite3
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType


class Ignore(ModuleInterface):
    triggers = ["ignore", "unignore", "ignores"]
    access_level = ModuleAccessLevel.ADMINS

    def help(self, message):
        help_dict = {
            u"ignore": u"ignore [nick] -- Add someone to the ignore list.\n"
                       u"unignore [nick] -- Remove someone from the ignore list.\n"
                       u"ignores -- Returns the current ignore list.",
            u"unignore": u"unignore [nick] -- Remove someone from the ignore list.",
            u"ignores": u"ignores -- Returns the current ignore list."
        }
        command = message.parameter_list[0].lower()
        return help_dict[command]

    def on_load(self):
        ignores = []
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS ignores (nick text)")
            conn.commit()
            for row in c.execute("SELECT nick FROM ignores"):
                ignores.append(row[0])
        self.bot.ignores = ignores
        self.bot.logger.debug("Loaded {!r} into ignores list.".format(", ".join(ignores)))

    def on_unload(self):
        self.bot.ignores = []
        self.bot.logger.debug("Unloaded all ignores.")

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.command == "ignore":
            if len(message.parameter_list) == 1:
                with sqlite3.connect(self.bot.database_file) as conn:
                    c = conn.cursor()
                    c.execute("SELECT max(id) FROM ignores")
                    max_id = c.fetchone()[0]
                    if max_id is None:
                        max_id = 0
                    c.execute("INSERT INTO ignores VALUES (?,?)", (max_id + 1, message.parameter_list[0]))
                    conn.commit()
                self.bot.ignores.append(message.parameter_list[0])
                return IRCResponse(ResponseType.SAY,
                                   "Successfully added '{}' to the ignores list.".format(message.parameter_list[0]),
                                   message.reply_to)
            else:
                return IRCResponse(ResponseType.SAY, "Ignore who?", message.reply_to)
        elif message.command == "unignore":
            if len(message.parameter_list) == 1:
                with sqlite3.connect(self.bot.database_file) as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM ignores WHERE nick=?", (message.parameter_list[0],))
                    conn.commit()
                self.bot.ignores.remove(message.parameter_list[0])
                return IRCResponse(ResponseType.SAY,
                                   "Successfully removed '{}' from the ignores list.".format(message.parameter_list[0]),
                                   message.reply_to)
            else:
                return IRCResponse(ResponseType.SAY, "Unignore who?", message.reply_to)
        elif message.command == "ignores":
            return IRCResponse(ResponseType.SAY,
                               "Currently ignoring: {}".format(", ".join(self.bot.ignores)),
                               message.reply_to)
