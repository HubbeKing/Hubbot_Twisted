from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType
import sqlite3


class Admin(ModuleInterface):
    triggers = ["admin", "unadmin", "admins"]
    access_level = ModuleAccessLevel.ADMINS

    def help(self, message):
        help_dict = {
            u"admin": u"admin [nick] -- add a user to the admin list.\n"
                      u"unadmin [nick] -- remove a user from the admin list.\n"
                      u"admins -- returns the current admin list.",
            u"unadmin": u"unadmin [nick] -- remove a user from the admin list.",
            u"admins": u"admins -- returns the current admin list."
        }
        command = message.parameter_list[0].lower()
        return help_dict[command]

    def on_load(self):
        admins = []
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS admins (nick text)")
            conn.commit()
            for row in c.execute("SELECT nick FROM admins"):
                admins.append(row[0])
        self.bot.admins = admins
        self.bot.logger.debug("Loaded {!r} into admins list.".format(", ".join(admins)))

    def on_unload(self):
        self._save_admins()
        self.bot.admins = []
        self.bot.logger.debug("Unloaded all admins.")

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.command == "admins":
            return IRCResponse(ResponseType.SAY,
                               "Current admins: {}".format(", ".join(self.bot.admins)),
                               message.reply_to)
        elif message.command == "admin":
            if len(message.parameter_list) == 0:
                return IRCResponse(ResponseType.SAY, "Admin who?", message.reply_to)
            else:
                for admin in message.parameter_list:
                    self._new_admin(admin)
                return IRCResponse(ResponseType.SAY,
                                   "Added {} to the admin list.".format(", ".join(message.parameter_list)),
                                   message.reply_to)
        elif message.command == "unadmin":
            if len(message.parameter_list) == 0:
                return IRCResponse(ResponseType.SAY, "Unadmin who?", message.reply_to)
            else:
                for admin in message.parameter_list:
                    self._delete_admin(admin)
                return IRCResponse(ResponseType.SAY,
                                   "Removed {} from the admin list.". format(", ".join(message.parameter_list)),
                                   message.reply_to)

    def _new_admin(self, admin):
        self.bot.admins.append(admin)
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO admins VALUES (?)", (admin,))
            conn.commit()

    def _delete_admin(self, admin):
        self.bot.admins.remove(admin)
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM admins WHERE nick=?", (admin,))
            conn.commit()

    def _save_admins(self):
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("DROP TABLE IF EXISTS admins")
            c.execute("CREATE TABLE admins (nick text)")
            for admin in self.bot.admins:
                c.execute("INSERT INTO admins VALUES (?)", (admin,))
            conn.commit()
