import random
try:
    import re2 as re
except ImportError:
    import re
import sqlite3

from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface
from hubbot.Utils.webutils import pasteEE


class Headcanon(ModuleInterface):
    triggers = ["headcanon"]
    sub_commands = ["add", "search", "list", "remove"]
    api_key = None

    def help(self, message):
        help_dict = {
            u"headcanon": u"headcanon [function] -- Used to store Symphony's headcanon!\nHeadcanon functions: {}".format(u", ".join(self.sub_commands)),
            u"headcanon add": u"headcanon add <string> -- Used to add lines to the headcanon.",
            u"headcanon search": u"headcanon search <string> -- Used to search within the headcanon.",
            u"headcanon list": u"headcanon list -- Posts a list of all headcanon entries to paste.ee",
            u"headcanon remove": u"headcanon remove <string> -- Used to remove lines from the headcanon."
        }
        if len(message.parameter_list) == 1:
            return help_dict[message.parameter_list[0]].lower()
        else:
            return help_dict[u" ".join([word.lower() for word in message.parameter_list[:2]])]

    def on_load(self):
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS headcanon (canon text)")
            conn.commit()
        self.api_key = self.get_api_key()

    def get_api_key(self):
        """
        Get the API key for paste.ee from the sqlite database.
        """
        api_key = None
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT apikey FROM keys WHERE name='paste'"):
                api_key = row[0]
        return api_key

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        headcanon = []
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM headcanon"):
                headcanon.append(row[0])

        if len(message.parameter_list) == 0:
            sub_command = "list"
        else:
            sub_command = message.parameter_list[0]

        if sub_command.lower() == "add" and message.user.name in self.bot.admins:
            if len(message.parameter_list) == 1:
                return IRCResponse(ResponseType.SAY, "Maybe you should read the help text?", message.reply_to)
            add_string = ""
            for word in message.parameter_list[1:]:
                add_string = add_string + word + " "
            headcanon.append(add_string)
            with sqlite3.connect(self.bot.database_file) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO headcanon VALUES (?)", (add_string,))
                conn.commit()
            return IRCResponse(ResponseType.SAY, "Successfully added line!", message.reply_to)

        elif sub_command.lower() == "search":
            return_string = "Search term not found in database!"
            try:
                hc = headcanon
                random.shuffle(hc)
                re_string = "{}".format(" ".join(message.parameter_list[1:]))
                for canon in hc:
                    match = re.search(re_string, canon, re.IGNORECASE)
                    if match:
                        return_string = match.string
                        break
                return IRCResponse(ResponseType.SAY, return_string, message.reply_to)
            except:
                return IRCResponse(ResponseType.SAY, return_string, message.reply_to)

        elif sub_command.lower() == "list":
            if self.api_key is None:
                return IRCResponse(ResponseType.SAY, "No API key for paste.ee was found, please add one.", message.reply_to)
            paste_ee_string = ""
            if len(headcanon) == 0:
                return IRCResponse(ResponseType.SAY, "The database is empty! D:", message.reply_to)
            else:
                for item in headcanon:
                    paste_ee_string = paste_ee_string + item + "\n"
                try:
                    response = pasteEE(self.api_key, paste_ee_string, "Headcanon", 10)
                    return IRCResponse(ResponseType.SAY, "Link posted! (Expires in 10 minutes) {}".format(response), message.reply_to)
                except Exception:
                    self.bot.logger.exception("Exception in module 'Headcanon'")
                    return IRCResponse(ResponseType.SAY, "Uh-oh, something broke!", message.reply_to)

        elif sub_command.lower() == "remove" and message.user.name in self.bot.admins:
            try:
                re_string = "{}".format(" ".join(message.parameter_list[1:]))
                for canon in headcanon:
                    match = re.search(re_string, canon, re.IGNORECASE)
                    if match:
                        headcanon.remove(match.string)
                        with sqlite3.connect(self.bot.database_file) as conn:
                            c = conn.cursor()
                            c.execute("DELETE FROM headcanon WHERE canon=?", (match.string,))
                            conn.commit()
                        return IRCResponse(ResponseType.SAY, 'Removed "' + match.string + '"', message.reply_to)
                return IRCResponse(ResponseType.SAY, '"' + re_string + '"was not found!', message.reply_to)
            except Exception:
                self.bot.logger.exception("Exception in module 'Headcanon'")
                return IRCResponse(ResponseType.SAY, "Something broke!", message.reply_to)
