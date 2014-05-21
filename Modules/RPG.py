import re
import sqlite3
import random
from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
from WebUtils import pasteEE


class Module(ModuleInterface):
    triggers = ["pf", "lp", "mm", "welch"]
    help = 'pf/lp/mm/welch <number>/add <thing>/list/search <term> -- "helpful" RPG advice and stuff'
    filename = "data/data.db"

    def onTrigger(self, Hubbot, message):
        if message.Command == "pf":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, self.getRandom("pathfinder"), message.ReplyTo)
            else:
                if message.ParameterList[0] == "list":
                    if len(message.ParameterList) == 1:
                        return IRCResponse(ResponseType.Say, self.getList("pathfinder", "Pathfinder", ""), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, self.getList("pathfinder", "Pathfinder", " ".join(message.ParameterList[1:])), message.ReplyTo)
                elif message.ParameterList[0] == "add":
                    lineToAdd = " ".join(message.ParameterList[1:])
                    newIndex = self.addLine("pathfinder", lineToAdd)
                    return IRCResponse(ResponseType.Say, "Successfully added line '{}. {}'".format(newIndex, lineToAdd), message.ReplyTo)
                elif message.ParameterList[0] == "search":
                    return IRCResponse(ResponseType.Say, self.search("pathfinder", " ".join(message.ParameterList[1:])), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, self.getSpecific("pathfinder", message.ParameterList[0]), message.ReplyTo)
        elif message.Command == "lp":
            if len(message.ParameterList) == 0:
               return IRCResponse(ResponseType.Say, self.getRandom("lp"), message.ReplyTo)
            else:
                if message.ParameterList[0] == "list":
                    if len(message.ParameterList) == 1:
                        return IRCResponse(ResponseType.Say, self.getList("lp", "Let's Play", ""), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, self.getList("lp", "Let's Play", " ".join(message.ParameterList[1:])), message.ReplyTo)
                elif message.ParameterList[0] == "add":
                    lineToAdd = " ".join(message.ParameterList[1:])
                    newIndex = self.addLine("lp", lineToAdd)
                    return IRCResponse(ResponseType.Say, "Successfully added line '{}. {}'".format(newIndex, lineToAdd), message.ReplyTo)
                elif message.ParameterList[0] == "search":
                    return IRCResponse(ResponseType.Say, self.search("lp", " ".join(message.ParameterList[1:])), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, self.getSpecific("lp", message.ParameterList[0]), message.ReplyTo)
        elif message.Command == "mm":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, self.getRandom("mm"), message.ReplyTo)
            else:
                if message.ParameterList[0] == "list":
                    if len(message.ParameterList) == 1:
                        return IRCResponse(ResponseType.Say, self.getList("mm", "Mutants & Masterminds", ""), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, self.getList("mm", "Mutants & Masterminds", " ".join(message.ParameterList[1:])), message.ReplyTo)
                elif message.ParameterList[0] == "add":
                    lineToAdd = " ".join(message.ParameterList[1:])
                    newIndex = self.addLine("mm", lineToAdd)
                    return IRCResponse(ResponseType.Say, "Successfully added line '{}. {}'".format(newIndex, lineToAdd), message.ReplyTo)
                elif message.ParameterList[0] == "search":
                    return IRCResponse(ResponseType.Say, self.search("mm", " ".join(message.ParameterList[1:])), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, self.getSpecific("mm", message.ParameterList[0]), message.ReplyTo)
        elif message.Command == "welch":
            if len(message.ParameterList) == 0:
                return IRCResponse(ResponseType.Say, self.getRandom("welch"), message.ReplyTo)
            else:
                if message.ParameterList[0] == "list":
                    if len(message.ParameterList) == 1:
                        return IRCResponse(ResponseType.Say, self.getList("welch", "Welch", ""), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, self.getList("welch", "Welch", " ".join(message.ParameterList[1:])), message.ReplyTo)
                elif message.ParameterList[0] == "search":
                    return IRCResponse(ResponseType.Say, self.search("welch", " ".join(message.ParameterList[1:])), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, self.getSpecific("welch", message.ParameterList[0]), message.ReplyTo)

    def getRandom(self, table):
        messageDict = {}
        with sqlite3.connect(self.filename) as conn:
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
        with sqlite3.connect(self.filename) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM {}".format(table)):
                messageDict[row[0]] = row[1]
        if choice in messageDict.keys():
            return "{}. {}".format(str(choice), messageDict[choice])
        else:
            return "Invalid number, valid numbers are <{}-{}>".format(messageDict.keys()[0], messageDict.keys()[-1])

    def getList(self, table, name, params):
        messageDict = {}
        with sqlite3.connect(self.filename) as conn:
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
        with sqlite3.connect(self.filename) as conn:
            c = conn.cursor()
            c.execute("SELECT max(id) FROM {}".format(table))
            maxNumber = c.fetchone()[0]
            c.execute("INSERT INTO {} VALUES (?,?)".format(table), (maxNumber+1, line))
            conn.commit()
        return maxNumber + 1

    def search(self, table, line):
        messageDict = {}
        matches = []
        with sqlite3.connect(self.filename) as conn:
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
            choice = random.choice(matches)
            return "Match #{}/{} - {}".format(matches.index(choice)+1, len(matches), choice)
        else:
            return "Could not find '{}'!".format(line)