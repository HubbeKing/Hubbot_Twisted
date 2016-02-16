from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
import string
import sqlite3
import re


class Hugs(ModuleInterface):
    triggers = ["hugs"]
    acceptedTypes = ["PRIVMSG", "ACTION"]
    help = "hugs [nick] -- How many hugs has this person given and received?"
    # hug_dict is : {"nick":[given, received]}
    commonWords = [
       "and","of","all","to","the","both","back","again",
        "any","one","<3","with","","<3s","so","hard","right",
        "in","him","her","booper","up","on",":)","against","its",
        "harder","teh","sneakgrabs","people",":3"
    ]

    def shouldTrigger(self, message):
        if message.Type == "ACTION":
            pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
            match = re.search(pattern, message.MessageList[0], re.IGNORECASE)
            if match:
                return True
        elif message.Type == "PRIVMSG":
            if message.Command in self.triggers:
                return True
        else:
            return False

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Type == "ACTION":
            pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
            match = re.search(pattern, message.MessageList[0], re.IGNORECASE)
            if match:
                self.bot.logger.info(u'{} *{} {}*'.format(message.ReplyTo, message.User.Name, message.MessageString))
                hug_dict = {}
                with sqlite3.connect(self.bot.databaseFile) as conn:
                    c = conn.cursor()
                    for row in c.execute("SELECT * FROM hugs"):
                        hug_dict[row[0]] = [row[1], row[2]]
                receivers = []
                for nick in message.MessageList[1:]:
                    if string.lower(nick) not in self.commonWords:
                        nick = string.rstrip(nick, "\x01")
                        nick = string.rstrip(nick, ".")
                        nick = string.rstrip(nick, "!")
                        nick = string.rstrip(nick, ",")
                        nick = string.lower(nick)
                        regexPattern = r"^[^a-zA-Z0-9`_\[\]\{\}\|\^\\]+$"
                        invalid = re.match(regexPattern, nick)
                        if not invalid:
                            receivers.append(nick)
                for index in range(0, len(receivers)):
                    giver = string.lower(message.User.Name)
                    receiver = receivers[index]
                    if giver not in hug_dict:
                        hug_dict[giver] = [1, 0]
                        with sqlite3.connect(self.bot.databaseFile) as conn:
                            c = conn.cursor()
                            c.execute("INSERT INTO hugs VALUES (?,?,?)", (giver, 1, 0))
                            conn.commit()
                    else:
                        hug_dict[giver] = list(hug_dict[giver])
                        hug_dict[giver][0] += 1
                        with sqlite3.connect(self.bot.databaseFile) as conn:
                            c = conn.cursor()
                            c.execute("UPDATE hugs SET given=? WHERE nick=?", (hug_dict[giver][0], giver))
                            conn.commit()
                    if receiver not in hug_dict:
                        hug_dict[receiver] = [0, 1]
                        with sqlite3.connect(self.bot.databaseFile) as conn:
                            c = conn.cursor()
                            c.execute("INSERT INTO hugs VALUES (?,?,?)", (receiver, 0, 1))
                            conn.commit()
                    else:
                        hug_dict[receiver] = list(hug_dict[receiver])
                        hug_dict[receiver][1] += 1
                        with sqlite3.connect(self.bot.databaseFile) as conn:
                            c = conn.cursor()
                            c.execute("UPDATE hugs SET received=? WHERE nick=?", (hug_dict[receiver][1], receiver))
                            conn.commit()

        elif message.Type == "PRIVMSG":
            hug_dict = {}
            with sqlite3.connect(self.bot.databaseFile) as conn:
                c = conn.cursor()
                for row in c.execute("SELECT * FROM hugs"):
                    hug_dict[row[0]] = [row[1], row[2]]
            if len(message.ParameterList) == 0:
                target = message.User.Name
            else:
                target = message.ParameterList[0]

            hugData = [0, 0]
            matches = []
            for (user, hugCounts) in hug_dict.items():
                try:
                    match = re.search(target, user, re.IGNORECASE)
                except:
                    match = False
                if match:
                    matches.append(match.string)
                    hugData[0] += hugCounts[0]
                    hugData[1] += hugCounts[1]

            HugString = "{} has received {} hugs and given {} hugs.".format(target, hugData[1], hugData[0])
            matchedNicksString = "Matches found: "
            numberOfMatches = 0
            for name in matches:
                if numberOfMatches > 9:
                    matchedNicksString += "..."
                    break
                elif matches.index(name) == len(matches) - 1:
                    matchedNicksString += name
                    numberOfMatches += 1
                else:
                    matchedNicksString = matchedNicksString + name + ", "
                    numberOfMatches += 1
            if len(matches) > 30:
                matchedNicksString = "Matches found: LOTS."
            return IRCResponse(ResponseType.Say, matchedNicksString, message.ReplyTo), IRCResponse(ResponseType.Say, HugString, message.ReplyTo)
