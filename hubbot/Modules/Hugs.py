from __future__ import unicode_literals
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
import sqlite3
try:
    import re2 as re
except ImportError:
    import re


class Hugs(ModuleInterface):
    triggers = ["hugs", "consolidatehugs"]
    accepted_types = ["PRIVMSG", "ACTION"]
    help = "hugs [nick] -- How many hugs has this person given and received?"
    # hugs table is nick; given; received
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

    def consolidate_hugs(self, from_nick, to_nick):
        with sqlite3.connect(self.bot.database_file) as conn:
            temp_dict = {}
            c = conn.cursor()
            c.execute("SELECT * FROM hugs WHERE nick LIKE ?", (from_nick,))
            for row in c.fetchall():
                temp_dict[row[0]] = [row[1], row[2]]
            consolidated_hugs_count = [0, 0]
            for nick, hug_list in temp_dict.iteritems():
                c.execute("DELETE FROM hugs WHERE nick=?", (nick,))
                consolidated_hugs_count[0] += hug_list[0]
                consolidated_hugs_count[1] += hug_list[1]
            c.execute("INSERT INTO hugs VALUES (?,?,?)", (to_nick, consolidated_hugs_count[0], consolidated_hugs_count[1]))
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
                    with sqlite3.connect(self.bot.database_file) as conn:
                        c = conn.cursor()
                        c.execute("SELECT count(*) FROM hugs WHERE nick=?", (giver,))
                        giver_exists = c.fetchone()[0]
                        if giver_exists == 0:
                            # Giver not in database
                            c.execute("INSERT INTO hugs VALUES (?,?,?)", (giver, 1, 0))
                        else:
                            c.execute("UPDATE hugs SET given = given + 1 WHERE nick=?", (giver,))
                        c.execute("SELECT count(*) FROM hugs WHER nick=?", (receiver,))
                        receiver_exists = c.fetchone()[0]
                        if receiver_exists == 0:
                            c.execute("INSERT INTO hugs VALUES (?,?,?)", (receiver, 0, 1))
                        else:
                            c.execute("UPDATE hugs SET received = received + 1 WHERE nick=?", (receiver,))
                        conn.commit()

        elif message.type == "PRIVMSG" and message.command == "hugs":
            if len(message.parameter_list) == 0:
                target = message.user.name
            else:
                target = message.parameter_list[0]

            hug_data = [0, 0]
            matches = []

            with sqlite3.connect(self.bot.database_file) as conn:
                wrapped_target = "%{}%".format(target)
                c = conn.cursor()
                c.execute("SELECT * FROM hugs WHERE nick LIKE ?", (wrapped_target,))

                for row in c.fetchall():
                    matches.append(row[0])
                    hug_data[0] += row[1]
                    hug_data[1] += row[2]

            hug_string = "{} has received {} hugs and given {} hugs.".format(target, hug_data[1], hug_data[0])
            matched_nicks_string = "Matches found with '{}': ".format(wrapped_target)
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
                matched_nicks_string = "Matches found with '{}': LOTS.".format(wrapped_target)
            return IRCResponse(ResponseType.SAY, matched_nicks_string, message.reply_to), IRCResponse(ResponseType.SAY,
                                                                                                      hug_string,
                                                                                                      message.reply_to)
        elif message.type == "PRIVMSG" and message.command == "consolidatehugs":
            if message.user.name in self.bot.admins:
                from_nick = message.parameter_list[0]
                to_nick = message.parameter_list[1]
                self.consolidate_hugs(from_nick, to_nick)

                wrapped_to_nick = "%{}%".format(to_nick)
                hug_data = [0, 0]
                with sqlite3.connect(self.bot.database_file) as conn:
                    c = conn.cursor()
                    c.execute("SELECT * FROM hugs WHERE nick LIKE ?", (wrapped_to_nick,))
                    for row in c.fetchall():
                        hug_data[0] += row[1]
                        hug_data[1] += row[2]
                return IRCResponse(ResponseType.SAY, "Success, probably.", message.reply_to), \
                       IRCResponse(ResponseType.SAY, "{} now has received {} hugs and given {} hugs.".format(to_nick, hug_data[1], hug_data[0]), message.reply_to)
