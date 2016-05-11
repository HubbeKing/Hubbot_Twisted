import random
import re
import sqlite3

from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface
from hubbot.Utils.webutils import pasteEE


class Headcanon(ModuleInterface):
    triggers = ["headcanon"]
    subCommands = ["add", "search", "list", "remove"]
    runInThread = True
    timeout = 15

    def help(self, message):
        helpDict = {
            u"headcanon": u"headcanon [function] -- Used to store Symphony's headcanon!\nHeadcanon functions: {}".format(u", ".join(self.subCommands)),
            u"headcanon add": u"headcanon add <string> -- Used to add lines to the headcanon.",
            u"headcanon search": u"headcanon search <string> -- Used to search within the headcanon.",
            u"headcanon list": u"headcanon list -- Posts a list of all headcanon entries to paste.ee",
            u"headcanon remove": u"headcanon remove <string> -- Used to remove lines from the headcanon."
        }
        if len(message.ParameterList) == 1:
            return helpDict[message.ParameterList[0]].lower()
        else:
            return helpDict[u" ".join([word.lower() for word in message.ParameterList[:2]])]

    def onEnable(self):
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS headcanon (canon text)")
            conn.commit()

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        headcanon = []
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM headcanon"):
                headcanon.append(row[0])

        if len(message.ParameterList) == 0:
            subCommand = "list"
        else:
            subCommand = message.ParameterList[0]

        if subCommand.lower() == "add" and message.User.Name in self.bot.admins:
            if len(message.ParameterList) == 1:
                return IRCResponse(ResponseType.Say, "Maybe you should read the help text?", message.ReplyTo)
            addString = ""
            for word in message.ParameterList[1:]:
                addString = addString + word + " "
            headcanon.append(addString)
            with sqlite3.connect(self.bot.databaseFile) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO headcanon VALUES (?)", (addString,))
                conn.commit()
            return IRCResponse(ResponseType.Say, "Successfully added line!", message.ReplyTo)

        elif subCommand.lower() == "search":
            returnString = "Search term not found in database!"
            try:
                hc = headcanon
                random.shuffle(hc)
                re_string = "{}".format(" ".join(message.ParameterList[1:]))
                for canon in hc:
                    match = re.search(re_string, canon, re.IGNORECASE)
                    if match:
                        returnString = match.string
                        break
                return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)
            except:
                return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)

        elif subCommand.lower() == "list":
            pasteBinString = ""
            if len(headcanon) == 0:
                return IRCResponse(ResponseType.Say, "The database is empty! D:", message.ReplyTo)
            else:
                for item in headcanon:
                    pasteBinString = pasteBinString + item + "\n"
                try:
                    response = pasteEE(pasteBinString, "Headcanon", "10M")
                    return IRCResponse(ResponseType.Say, "Link posted! (Expires in 10 minutes) {}".format(response), message.ReplyTo)
                except Exception:
                    self.bot.logger.exception("Exception in module \"Headcanon\"")
                    return IRCResponse(ResponseType.Say, "Uh-oh, something broke!", message.ReplyTo)

        elif subCommand.lower() == "remove" and message.User.Name in self.bot.admins:
            try:
                re_string = "{}".format(" ".join(message.ParameterList[1:]))
                for canon in headcanon:
                    match = re.search(re_string, canon, re.IGNORECASE)
                    if match:
                        headcanon.remove(match.string)
                        with sqlite3.connect(self.bot.databaseFile) as conn:
                            c = conn.cursor()
                            c.execute("DELETE FROM headcanon WHERE canon=?", (match.string,))
                            conn.commit()
                        return IRCResponse(ResponseType.Say, 'Removed "' + match.string + '"', message.ReplyTo)
                return IRCResponse(ResponseType.Say, '"' + re_string + '"was not found!', message.ReplyTo)
            except Exception:
                self.bot.logger.exception("Exception in module \"Headcanon\"")
                return IRCResponse(ResponseType.Say, "Something broke!", message.ReplyTo)
