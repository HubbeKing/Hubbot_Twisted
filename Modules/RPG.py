import re
import sqlite3
import random
from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
from WebUtils import pasteEE


class RPG(ModuleInterface):
    help = 'pf/lp/mm/welch <number>/add <thing>/list/search <term> -- "helpful" RPG advice and stuff'
    filename = "data/data.db"
    
    campaigns = {"pf": {"displayname": "Pathfinder", "tablename": "pathfinder", "isAddingAllowed": True},
                "lp": {"displayname": "Let's Play", "tablename": "lp", "isAddingAllowed": True},
                "mm": {"displayname": "Mutants & Masterminds", "tablename": "mm", "isAddingAllowed": True},
                "welch": {"displayname": "Welch", "tablename": "welch", "isAddingAllowed": False}}
    
    def onLoad(self):
        self.triggers = self.campaigns.keys()
        
    def onTrigger(self, message):
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, self.getRandom(self.campaigns[message.Command]["tablename"]), message.ReplyTo)
        elif message.ParameterList[0] == "list":
            params = ""
            if len(message.ParameterList) == 1:
                params = " ".join(message.ParameterList[1:])
            return IRCResponse(ResponseType.Say, self.getList(self.campaigns[message.Command]["tablename"], self.campaigns[message.Command]["displayname"], params), message.ReplyTo)
        elif message.ParameterList[0] == "add" and self.campaigns[message.Command]["isAddingAllowed"]:
            lineToAdd = " ".join(message.ParameterList[1:])
            newIndex = self.addLine(self.campaigns[message.Command]["tablename"], lineToAdd)
            return IRCResponse(ResponseType.Say, "Successfully added line '{}. {}'".format(newIndex, lineToAdd), message.ReplyTo)
        elif message.ParameterList[0] == "search":
            return IRCResponse(ResponseType.Say, self.search(self.campaigns[message.Command]["tablename"], " ".join(message.ParameterList[1:])), message.ReplyTo)
        else:
            return IRCResponse(ResponseType.Say, self.getSpecific(self.campaigns[message.Command]["tablename"], message.ParameterList[0]), message.ReplyTo)
            

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
        try:
            choice = int(line.split(" ")[-1])
            line = line.replace(line.split(" ")[-1], "", 1).strip()
            specific = True
        except:
            specific = False
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
            if not specific:
                choice = random.choice(matches)
                return "Match #{}/{} - {}".format(matches.index(choice)+1, len(matches), choice)
            elif choice <= len(matches):
                return "Match #{}/{} - {}".format(choice, len(matches), matches[choice - 1])
            else:
                return "There is no '#{}' entry of '{}'!".format(choice, line)
        else:
            return "Could not find '{}'!".format(line)
