from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType
import sqlite3


class Admin(ModuleInterface):
    triggers = ["admin", "unadmin", "admins"]
    accessLevel = ModuleAccessLevel.ADMINS

    def help(self, message):
        helpDict = {
            u"admin": u"admin [nick] -- add a user to the admin list.\n"
                      u"unadmin [nick] -- remove a user from the admin list.\n"
                      u"admins -- returns the current admin list.",
            u"unadmin": u"unadmin [nick] -- remove a user from the admin list.",
            u"admins": u"admins -- returns the current admin list."
        }
        command = message.ParameterList[0].lower()
        return helpDict[command]

    def onEnable(self):
        admins = []
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS admins (nick text)")
            conn.commit()
            for row in c.execute("SELECT nick FROM admins"):
                admins.append(row[0])
        self.bot.admins = admins
        self.bot.logger.debug("Loaded \"{}\" into admins list.".format(", ".join(admins)))

    def onDisable(self):
        self.saveAdmins()
        self.bot.admins = []
        self.bot.logger.debug("Unloaded all admins.")

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command == "admins":
            return IRCResponse(ResponseType.Say,
                               "Current admins: {}".format(", ".join(self.bot.admins)),
                               message.ReplyTo)
        elif message.Command == "admin":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, "Admin who?", message.ReplyTo)
            else:
                for admin in message.ParameterList:
                    self.newAdmin(admin)
                return IRCResponse(ResponseType.Say,
                                   "Added {} to the admin list.".format(", ".join(message.ParameterList)),
                                   message.ReplyTo)
        elif message.Command == "unadmin":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, "Unadmin who?", message.ReplyTo)
            else:
                for admin in message.ParameterList:
                    self.deleteAdmin(admin)
                return IRCResponse(ResponseType.Say,
                                   "Removed {} from the admin list.". format(", ".join(message.ParameterList)),
                                   message.ReplyTo)

    def newAdmin(self, admin):
        for (server, botfactory) in self.bot.bothandler.botfactories.iteritems():
            botfactory.bot.admins.append(admin)
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO admins VALUES (?)", (admin,))
            conn.commit()

    def deleteAdmin(self, admin):
        for (server, botfactory) in self.bot.bothandler.botfactories.iteritems():
            botfactory.bot.admins.remove(admin)
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM admins WHERE nick=?", (admin,))
            conn.commit()

    def saveAdmins(self):
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("DROP TABLE IF EXISTS admins")
            c.execute("CREATE TABLE admins (nick text)")
            for admin in self.bot.admins:
                c.execute("INSERT INTO admins VALUES (?)", (admin,))
            conn.commit()
