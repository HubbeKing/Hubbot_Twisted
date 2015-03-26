import re
import sqlite3
import random

from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from hubbot.Utils.webutils import pasteEE


class RPG(ModuleInterface):
    campaigns = {
        "pf": {"displayname": "Pathfinder", "tablename": "pathfinder", "isAddingAllowed": True},
        "lp": {"displayname": "Let's Play", "tablename": "lp", "isAddingAllowed": True},
        "mm": {"displayname": "Mutants & Masterminds", "tablename": "mm", "isAddingAllowed": True},
        "advice": {"displayname": "Advice", "tablename": "advice", "isAddingAllowed": True},
        "welch": {"displayname": "Welch", "tablename": "welch", "isAddingAllowed": False}
    }

    def help(self, message):
        helpDict = {
            u"rpg": u"pf/lp/mm/welch <number>/add <thing>/list/search <term> -- \"helpful\" RPG advice and stuff",

            u"pf": u"pf [number] -- Fetches a random or given entry from the Pathfinder list.",
            u"pf add": u"pf add <string> -- Adds the specified string as an entry in the Pathfinder list.",
            u"pf list": u"pf list [searchterm] -- Posts the Pathfinder list to paste.ee, with optional searchterm matching.",
            u"pf search": u"pf search <text> [number] -- Searches the Pathfinder list for the specified text, with optional numbered matching.",

            u"lp": u"lp [number] -- Fetches a random or given entry from the Let's Play list.",
            u"lp add": u"lp add <string> -- Adds the specified string as an entry in the Let's Play list.",
            u"lp list": u"lp list [searchterm] -- Posts the Let's Play list to paste.ee, with optional searchterm matching.",
            u"lp search": u"lp search <text> [number] -- Searches the Let's Play list for the specified text, with optional numbered matching.",

            u"mm": u"mm [number] -- Fetches a random or given entry from the Mutants & Masterminds list.",
            u"mm add": u"mm add <string> -- Adds the specified string as an entry in the Mutants & Masterminds list.",
            u"mm list": u"mm list [searchterm] -- Posts the Mutants & Masterminds list to paste.ee, with optional searchterm matching.",
            u"mm search": u"mm search <text> [number] -- Searches the Mutants & Masterminds list for the specified text, with optional numbered matching.",

            u"advice": u"advice [number] -- Fetches a random or given entry from the Advice list.",
            u"advice add": u"advice add <string> -- Adds the specified string as a bit of advice.",
            u"advice list": u"advice list [searchterm] -- Posts the Advice list to paste.ee, with optional searchterm matching",
            u"advice search": u"advice <text> [number] -- Searches the Advice list for the specified text, with optional numbered matching.",

            u"welch": u"welch [number] -- Fetches a random or given entry from the Welch list.",
            u"welch list": u"welch list [searchterm] -- Posts the Welch list to paste.ee, with optional searchterm matching.",
            u"welch search": u"welch search <text> [number] -- Searches the Welch list for the specified text, with optional numbered matching."
        }
        if len(message.ParameterList) == 1:
            return helpDict[message.ParameterList[0]]
        else:
            return helpDict[u" ".join([word.lower() for word in message.ParameterList[:2]])]

    def onEnable(self):
        self.triggers = self.campaigns.keys()

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, self.getRandom(self.campaigns[message.Command]["tablename"]),
                               message.ReplyTo)
        elif message.ParameterList[0] == "list":
            params = ""
            if len(message.ParameterList) > 1:
                params = " ".join(message.ParameterList[1:])
            return IRCResponse(ResponseType.Say, self.getList(self.campaigns[message.Command]["tablename"],
                                                              self.campaigns[message.Command]["displayname"], params),
                               message.ReplyTo)
        elif message.ParameterList[0] == "add" and self.campaigns[message.Command]["isAddingAllowed"]:
            lineToAdd = " ".join(message.ParameterList[1:])
            newIndex = self.addLine(self.campaigns[message.Command]["tablename"], lineToAdd)
            return IRCResponse(ResponseType.Say, "Successfully added line '{}. {}'".format(newIndex, lineToAdd),
                               message.ReplyTo)
        elif message.ParameterList[0] == "search":
            return IRCResponse(ResponseType.Say, self.search(self.campaigns[message.Command]["tablename"],
                                                             " ".join(message.ParameterList[1:])), message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say,
                               self.getSpecific(self.campaigns[message.Command]["tablename"], message.ParameterList[0]),
                               message.ReplyTo)

    def getRandom(self, table):
        messageDict = {}
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                messageDict[row[0]] = row[1]
        choice = random.choice(messageDict.keys())
        return "{}. {}".format(str(choice), messageDict[choice])

    def getSpecific(self, table, number):
        try:
            choice = int(number)
        except:
            return "I don't know what you mean by '{}'.".format(number)
        messageDict = {}
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                messageDict[row[0]] = row[1]
        if choice in messageDict.keys():
            return "{}. {}".format(str(choice), messageDict[choice])
        else:
            return "Invalid number, valid numbers are <{}-{}>".format(min(messageDict.keys()), max(messageDict.keys()))

    def getList(self, table, name, params):
        messageDict = {}
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                messageDict[row[0]] = row[1]
        pasteString = ""
        if len(params) == 0:
            for number, string in messageDict.iteritems():
                pasteString += str(number) + ". " + string + "\n"
        else:
            for number, string in messageDict.iteritems():
                match = re.search(params, string, re.IGNORECASE)
                if match:
                    pasteString += str(number) + ". " + string + "\n"
        pasteLink = pasteEE(pasteString, name, 10)
        return "Link posted! {}".format(pasteLink)

    def addLine(self, table, line):
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("SELECT max(id) FROM {}".format(table))
            maxNumber = c.fetchone()[0]
            c.execute("INSERT INTO {} VALUES (?,?)".format(table), (maxNumber + 1, line))
            conn.commit()
        return maxNumber + 1

    def search(self, table, line):
        messageDict = {}
        matches = []
        try:
            choice = int(line.split(" ")[-1])
            line = line.replace(line.split(" ")[-1], "", 1).strip()
            specific = True
        except:
            specific = False
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                messageDict[row[0]] = row[1]
        for number, text in messageDict.iteritems():
            match = re.search(line, text, re.IGNORECASE)
            if match:
                for number, text in messageDict.iteritems():
                    if text == match.string:
                        foundNumber = number
                        matches.append("{}. {}".format(foundNumber, match.string))
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
