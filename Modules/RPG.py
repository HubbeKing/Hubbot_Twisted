from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import sqlite3
import random
from WebUtils import pasteEE


class Module(ModuleInterface):
    triggers = ["pf", "lp", "mm", "welch"]
    help = 'pf/lp/mm/welch <number>/add <thing>/list -- "helpful" RPG advice and stuff'

    def onTrigger(self, Hubbot, message):
        filename = "data/data.db"
        if message.Command == "pf":
            if len(message.ParameterList) == 0:
                messageDict = {}
                with sqlite3.connect(filename) as conn:
                    c = conn.cursor()
                    for row in c.execute("SELECT * FROM pathfinder"):
                        messageDict[row[0]] = row[1]
                choice = random.choice(messageDict.keys())
                string = "{}. {}".format(str(choice), messageDict[choice])
                return IRCResponse(ResponseType.Say, string, message.ReplyTo)
            else:
                if message.ParameterList[0] == "list":
                    messageDict = {}
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        for row in c.execute("SELECT * FROM pathfinder"):
                            messageDict[row[0]] = row[1]
                    pasteString = ""
                    for number, message in messageDict.iteritems():
                        pasteString += str(number) + ". " + message
                    pasteLink = pasteEE(pasteString, "Pathfinder", 10)
                    return IRCResponse(ResponseType.Say, "Link posted! {}".format(pasteLink), message.ReplyTo)
                elif message.ParameterList[0] == "add":
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        c.execute("SELECT max(number) FROM pathfinder")
                        maxNumber = c.fetchone()[0]
                        c.execute("INSERT INTO pathfinder VALUES (?,?)", (maxNumber+1, " ".join(message.ParameterList[1:])))
                        conn.commit()
                else:
                    messageDict = {}
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        for row in c.execute("SELECT * FROM pathfinder"):
                            messageDict[row[0]] = row[1]
                    if message.ParameterList[0] in messageDict.keys():
                        choice = message.ParameterList[0]
                        return IRCResponse(ResponseType.Say, "{}. {}".format(str(choice), messageDict[choice]), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "Invalid number, valid numbers are <{}-{}>".format(messageDict.keys[0], messageDict.keys()[-1]), message.ReplyTo)
        elif message.Command == "lp":
            if len(message.ParameterList) == 0:
                messageDict = {}
                with sqlite3.connect(filename) as conn:
                    c = conn.cursor()
                    for row in c.execute("SELECT * FROM lp"):
                        messageDict[row[0]] = row[1]
                choice = random.choice(messageDict.keys())
                string = "{}. {}".format(str(choice), messageDict[choice])
                return IRCResponse(ResponseType.Say, string, message.ReplyTo)
            else:
                if message.ParameterList[0] == "list":
                    messageDict = {}
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        for row in c.execute("SELECT * FROM lp"):
                            messageDict[row[0]] = row[1]
                    pasteString = ""
                    for number, message in messageDict.iteritems():
                        pasteString += str(number) + ". " + message
                    pasteLink = pasteEE(pasteString, "Let's Play", 10)
                    return IRCResponse(ResponseType.Say, "Link posted! {}".format(pasteLink), message.ReplyTo)
                elif message.ParameterList[0] == "add":
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        c.execute("SELECT max(number) FROM lp")
                        maxNumber = c.fetchone()[0]
                        c.execute("INSERT INTO lp VALUES (?,?)", (maxNumber+1, " ".join(message.ParameterList[1:])))
                        conn.commit()
                else:
                    messageDict = {}
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        for row in c.execute("SELECT * FROM lp"):
                            messageDict[row[0]] = row[1]
                    if message.ParameterList[0] in messageDict.keys():
                        choice = message.ParameterList[0]
                        return IRCResponse(ResponseType.Say, "{}. {}".format(str(choice), messageDict[choice]), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "Invalid number, valid numbers are <{}-{}>".format(messageDict.keys[0], messageDict.keys()[-1]), message.ReplyTo)
        elif message.Command == "mm":
            if len(message.ParameterList) == 0:
                messageDict = {}
                with sqlite3.connect(filename) as conn:
                    c = conn.cursor()
                    for row in c.execute("SELECT * FROM mm"):
                        messageDict[row[0]] = row[1]
                choice = random.choice(messageDict.keys())
                string = "{}. {}".format(str(choice), messageDict[choice])
                return IRCResponse(ResponseType.Say, string, message.ReplyTo)
            else:
                if message.ParameterList[0] == "list":
                    messageDict = {}
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        for row in c.execute("SELECT * FROM mm"):
                            messageDict[row[0]] = row[1]
                    pasteString = ""
                    for number, message in messageDict.iteritems():
                        pasteString += str(number) + ". " + message
                    pasteLink = pasteEE(pasteString, "Mutants & Masterminds", 10)
                    return IRCResponse(ResponseType.Say, "Link posted! {}".format(pasteLink), message.ReplyTo)
                elif message.ParameterList[0] == "add":
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        c.execute("SELECT max(number) FROM mm")
                        maxNumber = c.fetchone()[0]
                        c.execute("INSERT INTO mm VALUES (?,?)", (maxNumber+1, " ".join(message.ParameterList[1:])))
                        conn.commit()
                else:
                    messageDict = {}
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        for row in c.execute("SELECT * FROM mm"):
                            messageDict[row[0]] = row[1]
                    if message.ParameterList[0] in messageDict.keys():
                        choice = message.ParameterList[0]
                        return IRCResponse(ResponseType.Say, "{}. {}".format(str(choice), messageDict[choice]), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "Invalid number, valid numbers are <{}-{}>".format(messageDict.keys[0], messageDict.keys()[-1]), message.ReplyTo)
        elif message.Command == "welch":
            if len(message.ParameterList) == 0:
                messageDict = {}
                with sqlite3.connect(filename) as conn:
                    c = conn.cursor()
                    for row in c.execute("SELECT * FROM welch"):
                        messageDict[row[0]] = row[1]
                choice = random.choice(messageDict.keys())
                string = "{}. {}".format(str(choice), messageDict[choice])
                return IRCResponse(ResponseType.Say, string, message.ReplyTo)
            else:
                if message.ParameterList[0] == "list":
                    messageDict = {}
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        for row in c.execute("SELECT * FROM welch"):
                            messageDict[row[0]] = row[1]
                    pasteString = ""
                    for number, message in messageDict.iteritems():
                        pasteString += str(number) + ". " + message
                    pasteLink = pasteEE(pasteString, "Welch", 10)
                    return IRCResponse(ResponseType.Say, "Link posted! {}".format(pasteLink), message.ReplyTo)
                elif message.ParameterList[0] == "add":
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        c.execute("SELECT max(number) FROM welch")
                        maxNumber = c.fetchone()[0]
                        c.execute("INSERT INTO mm VALUES (?,?)", (maxNumber+1, " ".join(message.ParameterList[1:])))
                        conn.commit()
                else:
                    messageDict = {}
                    with sqlite3.connect(filename) as conn:
                        c = conn.cursor()
                        for row in c.execute("SELECT * FROM welch"):
                            messageDict[row[0]] = row[1]
                    if message.ParameterList[0] in messageDict.keys():
                        choice = message.ParameterList[0]
                        return IRCResponse(ResponseType.Say, "{}. {}".format(str(choice), messageDict[choice]), message.ReplyTo)
                    else:
                        return IRCResponse(ResponseType.Say, "Invalid number, valid numbers are <{}-{}>".format(messageDict.keys[0], messageDict.keys()[-1]), message.ReplyTo)
