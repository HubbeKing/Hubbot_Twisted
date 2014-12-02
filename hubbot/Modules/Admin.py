from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel
from hubbot.response import IRCResponse, ResponseType
import sqlite3


class Admin(ModuleInterface):
    triggers = ["admin", "unadmin"]
    help = "admin/unadmin [nick] -- add/remove a user from the admin list"
    accessLevel = ModuleAccessLevel.ADMINS

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command == "admin" and len(message.ParameterList) == 1 and message.ParameterList[0] == "save":
            self.saveAdmins()
        elif message.Command == "admin":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, "Current admins: {}".format(", ".join(self.bot.admins)), message.ReplyTo)
            else:
                for admin in message.ParameterList:
                    self.newAdmin(admin)
                return IRCResponse(ResponseType.Say, "Added {} to the admin list.".format(", ".join(message.ParameterList)), message.ReplyTo)
        elif message.Command == "unadmin":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, "Unadmin who?", message.ReplyTo)
            else:
                for admin in message.ParameterList:
                    self.deleteAdmin(admin)
                return IRCResponse(ResponseType.Say, "Removed {} from the admin list.". format(", ".join(message.ParameterList)), message.ReplyTo)

    def newAdmin(self, admin):
        for (server, botfactory) in self.bot.bothandler.botfactories.iteritems():
            botfactory.protocol.admins.append(admin)
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO admins VALUES (?)", (admin,))
            conn.commit()

    def deleteAdmin(self, admin):
        for (server, botfactory) in self.bot.bothandler.botfactories.iteritems():
            botfactory.protocol.admins.remove(admin)
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
