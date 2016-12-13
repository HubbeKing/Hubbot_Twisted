from __future__ import unicode_literals
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
import sqlite3
try:
    import re2 as re
except ImportError:
    import re


class Hugs(ModuleInterface):
    triggers = ["hugs"]
    accepted_types = ["PRIVMSG", "ACTION"]
    help = "hugs [nick] -- How many hugs has this person given and received?"
    # hug_dict is : {"nick":[given, received]}
    common_words = [
        "and", "of", "all", "to", "the", "both", "back", "again",
        "any", "one", "<3", "with", "", "<3s", "so", "hard", "right",
        "in", "him", "her", "booper", "up", "on", ":)", "against", "its",
        "harder", "teh", "sneakgrabs", "people", ":3"
        ]

    def should_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.type == "ACTION":
            pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
            match = re.search(pattern, message.message_list[0], re.IGNORECASE)
            if match:
                return True
        elif message.type == "PRIVMSG":
            if message.command in self.triggers:
                return True
        else:
            return False

    def on_load(self):
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS hugs (nick text, given int, received int)")
            conn.commit()

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.type == "ACTION":
            pattern = "hu+g|cuddle|snu+ggle|snu+g|squeeze|glomp"
            match = re.search(pattern, message.message_list[0], re.IGNORECASE)
            if match:
                self.bot.logger.info('{} *{} {}*'.format(message.reply_to, message.user.name, message.message_string))
                hug_dict = {}
                with sqlite3.connect(self.bot.database_file) as conn:
                    c = conn.cursor()
                    for row in c.execute("SELECT * FROM hugs"):
                        hug_dict[row[0]] = [row[1], row[2]]
                receivers = []
                for nick in message.message_list[1:]:
                    if nick.lower() not in self.common_words:
                        nick = nick.rstrip("\x01")
                        nick = nick.rstrip(".")
                        nick = nick.rstrip("!")
                        nick = nick.rstrip(",")
                        nick = nick.lower()
                        regex_pattern = r"^[^a-zA-Z0-9`_\[\]\{\}\|\^\\]+$"
                        invalid = re.match(regex_pattern, nick)
                        if not invalid and nick != message.user.name.lower():
                            receivers.append(nick)
                for index in range(0, len(receivers)):
                    giver = message.user.name.lower()
                    receiver = receivers[index]
                    if giver not in hug_dict:
                        hug_dict[giver] = [1, 0]
                        with sqlite3.connect(self.bot.database_file) as conn:
                            c = conn.cursor()
                            c.execute("INSERT INTO hugs VALUES (?,?,?)", (giver, 1, 0))
                            conn.commit()
                    else:
                        hug_dict[giver] = list(hug_dict[giver])
                        hug_dict[giver][0] += 1
                        with sqlite3.connect(self.bot.database_file) as conn:
                            c = conn.cursor()
                            c.execute("UPDATE hugs SET given=? WHERE nick=?", (hug_dict[giver][0], giver))
                            conn.commit()
                    if receiver not in hug_dict:
                        hug_dict[receiver] = [0, 1]
                        with sqlite3.connect(self.bot.database_file) as conn:
                            c = conn.cursor()
                            c.execute("INSERT INTO hugs VALUES (?,?,?)", (receiver, 0, 1))
                            conn.commit()
                    else:
                        hug_dict[receiver] = list(hug_dict[receiver])
                        hug_dict[receiver][1] += 1
                        with sqlite3.connect(self.bot.database_file) as conn:
                            c = conn.cursor()
                            c.execute("UPDATE hugs SET received=? WHERE nick=?", (hug_dict[receiver][1], receiver))
                            conn.commit()

        elif message.type == "PRIVMSG":
            hug_dict = {}
            with sqlite3.connect(self.bot.database_file) as conn:
                c = conn.cursor()
                for row in c.execute("SELECT * FROM hugs"):
                    hug_dict[row[0]] = [row[1], row[2]]
            if len(message.parameter_list) == 0:
                target = message.user.name
            else:
                target = message.parameter_list[0]

            hug_data = [0, 0]
            matches = []
            for (user, hugCounts) in hug_dict.items():
                try:
                    match = re.search(target, user, re.IGNORECASE)
                except:
                    match = False
                if match:
                    matches.append(match.string)
                    hug_data[0] += hugCounts[0]
                    hug_data[1] += hugCounts[1]

            hug_string = "{} has received {} hugs and given {} hugs.".format(target, hug_data[1], hug_data[0])
            matched_nicks_string = "Matches found: "
            number_of_matches = 0
            for name in matches:
                if number_of_matches > 9:
                    matched_nicks_string += "..."
                    break
                elif matches.index(name) == len(matches) - 1:
                    matched_nicks_string += name
                    number_of_matches += 1
                else:
                    matched_nicks_string = matched_nicks_string + name + ", "
                    number_of_matches += 1
            if len(matches) > 30:
                matched_nicks_string = "Matches found: LOTS."
            return IRCResponse(ResponseType.SAY, matched_nicks_string, message.reply_to), IRCResponse(ResponseType.SAY,
                                                                                                      hug_string,
                                                                                                      message.reply_to)
