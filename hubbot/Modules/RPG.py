from __future__ import unicode_literals
try:
    import re2 as re
except ImportError:
    import re
import sqlite3
import random

from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from hubbot.Utils.webutils import paste_ee


class RPG(ModuleInterface):
    campaigns = {
        "pf": {"displayname": "Pathfinder", "tablename": "pathfinder", "isAddingAllowed": True},
        "sprawl": {"displayname": "SPRAWL", "tablename": "sprawl", "isAddingAllowed": True},
        "welch": {"displayname": "Welch", "tablename": "welch", "isAddingAllowed": False}
    }
    api_key = None

    def help(self, message):
        help_dict = {
            "rpg": "pf/sprawl/welch [number]/add <thing>/list [term]/search <term> -- Quotes and advice from various RPGs",

            "pf": "pf [number] -- Fetches a random or given entry from the Pathfinder list.",
            "pf add": "pf add <string> -- Adds the specified string as an entry in the Pathfinder list.",
            "pf list": "pf list [searchterm] -- Posts the Pathfinder list to paste.ee, with optional searchterm matching.",
            "pf search": "pf search <text> [number] -- Searches the Pathfinder list for the specified text, with optional numbered matching.",

            "sprawl": "sprawl [number] -- Fetches a random or given entry from the SPRAWL list.",
            "sprawl add": "sprawl add <string> -- Adds the specified string as an entry in the SPRAWL list.",
            "sprawl list": "sprawl list [searchterm] -- Posts the SPRAWL list to paste.ee, with optional searchterm matching.",
            "sprawl search": "sprawl search <text> [number] -- Searches the SPRAWL list for the specified text, with optional numbered matching.",

            "welch": "welch [number] -- Fetches a random or given entry from the Welch list.",
            "welch list": "welch list [searchterm] -- Posts the Welch list to paste.ee, with optional searchterm matching.",
            "welch search": "welch search <text> [number] -- Searches the Welch list for the specified text, with optional numbered matching."
        }
        if len(message.parameter_list) == 1:
            command = message.parameter_list[0].lower()
            return help_dict[command]
        else:
            command = u" ".join([word.lower() for word in message.parameter_list[:2]])
            if command in help_dict:
                return help_dict[command]

    def on_load(self):
        self.triggers = self.campaigns.keys()
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS pathfinder (id int, message text)")
            c.execute("CREATE TABLE IF NOT EXISTS sprawl (id int, message text)")
            c.execute("CREATE TABLE IF NOT EXISTS welch (id int, message text)")
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
        if len(message.parameter_list) == 0:
            return IRCResponse(ResponseType.SAY, self.get_random(self.campaigns[message.command]["tablename"]),
                               message.reply_to)
        elif message.parameter_list[0] == "list":
            params = ""
            if len(message.parameter_list) > 1:
                params = " ".join(message.parameter_list[1:])
            return IRCResponse(ResponseType.SAY, self.get_list(self.campaigns[message.command]["tablename"],
                                                               self.campaigns[message.command]["displayname"], params),
                               message.reply_to)
        elif message.parameter_list[0] == "add" and self.campaigns[message.command]["isAddingAllowed"]:
            line_to_add = " ".join(message.parameter_list[1:])
            new_index = self.add_line(self.campaigns[message.command]["tablename"], line_to_add)
            return IRCResponse(ResponseType.SAY, "Successfully added line '{} - {}'".format(new_index, line_to_add),
                               message.reply_to)
        elif message.parameter_list[0] == "search":
            return IRCResponse(ResponseType.SAY, self.search(self.campaigns[message.command]["tablename"],
                                                             " ".join(message.parameter_list[1:])), message.reply_to)
        else:
            return IRCResponse(ResponseType.SAY,
                               self.get_specific(self.campaigns[message.command]["tablename"], message.parameter_list[0]),
                               message.reply_to)

    def get_random(self, table):
        message_dict = {}
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                message_dict[row[0]] = row[1]
        choice = random.choice(message_dict.keys())
        return "Entry #{}/{} - {}".format(str(choice), max(message_dict.keys()), message_dict[choice])

    def get_specific(self, table, number):
        try:
            choice = int(number)
        except Exception:
            return "I don't know what you mean by '{}'.".format(number)
        message_dict = {}
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                message_dict[row[0]] = row[1]
        if choice in message_dict.keys():
            return "Entry #{}/{} - {}".format(str(choice), max(message_dict.keys()), message_dict[choice])
        else:
            return "Invalid number, valid numbers are <{}-{}>".format(min(message_dict.keys()), max(message_dict.keys()))

    def get_list(self, table, name, params):
        if self.api_key is None:
            return "No API key for paste.ee was found, please add one."
        message_dict = {}
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                message_dict[row[0]] = row[1]
        paste_string = ""
        if len(params) == 0:
            for number, string in message_dict.iteritems():
                paste_string += str(number) + ". " + string + "\n"
        else:
            for number, string in message_dict.iteritems():
                match = re.search(params, string, re.IGNORECASE)
                if match:
                    paste_string += str(number) + ". " + string + "\n"
        paste_link = paste_ee(self.api_key, paste_string, name, 10)
        return "Link posted! {}".format(paste_link)

    def add_line(self, table, line):
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO {} VALUES (NULL, ?)".format(table), (line,))
            c.execute("SELECT max(id) FROM {}".format(table))
            max_number = c.fetchone()[0]
            conn.commit()
        return max_number

    def search(self, table, line):
        message_dict = {}
        matches = []
        try:
            choice = int(line.split(" ")[-1])
            line = line.replace(line.split(" ")[-1], "", 1).strip()
            specific = True
        except Exception:
            choice = None
            specific = False
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                message_dict[row[0]] = row[1]
        for number, text in message_dict.iteritems():
            match = re.search(line, text, re.IGNORECASE)
            if match:
                for nr, txt in message_dict.iteritems():
                    if txt == match.string:
                        found_number = nr
                        matches.append("{}. {}".format(found_number, match.string))
        if len(matches) > 0:
            if not specific:
                choice = random.choice(matches)
                return "Match #{}/{} - {}".format(matches.index(choice) + 1, len(matches), choice)
            elif choice <= len(matches):
                return "Match #{}/{} - {}".format(choice, len(matches), matches[choice - 1])
            else:
                return "There is no '#{}' entry of '{}'!".format(choice, line)
        else:
            return "Could not find '{}'!".format(line)
