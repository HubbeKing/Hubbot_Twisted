from __future__ import unicode_literals

try:
    import re2 as re
except ImportError:
    import re
import sqlite3
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from hubbot.message import IRCMessage


class Alias(ModuleInterface):
    triggers = ["alias", "unalias", "aliases", "aliashelp"]

    def __init__(self, bot):
        """
        @type bot: hubbot.bot.Hubbot
        """
        self.aliases = {}
        self.alias_help_dict = {}
        super(Alias, self).__init__(bot)

    def help(self, message):
        """
        @type message: IRCMessage
        """
        help_dict = {
            "alias": "alias <alias> <command/alias> <params> - aliases <alias> to the specified command/alias and parameters\n"
                     "you can specify where parameters given to the alias should be inserted with $1, $2, $n. "
                     "The whole parameter string is $0. $sender and $channel can also be used.",
            "unalias": "unalias <alias> - deletes the alias <alias>",
            "aliases": "aliases [<alias>] - lists all defined aliases, or the contents of the specified alias",
            "aliashelp": "aliashelp <alias> <helptext> - sets the helptext of the specified alias to the specified string"
        }
        command = message.parameter_list[0].lower()
        if command in help_dict:
            return help_dict[command]
        elif command in self.aliases:
            if command in self.alias_help_dict:
                return self.alias_help_dict[command]
            else:
                return "'{}' is an alias for: {}".format(command, " ".join(self.aliases[command]))

    def on_load(self):
        self.aliases = {}
        self.alias_help_dict = {}
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS aliashelp (alias TEXT, help TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS aliases (alias TEXT, command TEXT)")
            for row in c.execute("SELECT * FROM aliashelp"):
                self.alias_help_dict[row[0].lower()] = row[1].split(" ")
            for row in c.execute("SELECT * FROM aliases"):
                self.aliases[row[0].lower()] = row[1].split(" ")
            conn.commit()
        for alias in self.aliases:
            self.bot.module_handler.mapped_triggers[alias.lower()] = self

    def on_unload(self):
        for alias in self.aliases:
            del self.bot.module_handler.mapped_triggers[alias.lower()]

    def should_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.command in self.bot.module_handler.mapped_triggers:
            return True
        return False

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.command in self.triggers:
            if message.command == "alias":
                if message.user.name not in self.bot.admins:
                    return IRCResponse(ResponseType.SAY, "Only my admins may create new aliases!", message.reply_to)

                if len(message.parameter_list) <= 1:
                    return IRCResponse(ResponseType.SAY, "Alias what?", message.reply_to)

                if message.parameter_list[0].lower() in self.bot.module_handler.mapped_triggers:
                    return IRCResponse(ResponseType.SAY,
                                       "'{}' is already a command!".format(message.parameter_list[0].lower()),
                                       message.reply_to)

                if message.parameter_list[1].lower() not in self.bot.module_handler.mapped_triggers and \
                                message.parameter_list[1].lower() not in self.aliases:
                    return IRCResponse(ResponseType.SAY, "'{}' is not a valid command or alias!".format(
                        message.parameter_list[1].lower()), message.reply_to)
                if message.parameter_list[0].lower() in self.aliases:
                    return IRCResponse(ResponseType.SAY,
                                       "'{}' is already an alias!".format(message.parameter_list[0].lower()),
                                       message.reply_to)

                alias_params = []
                for word in message.parameter_list[1:]:
                    alias_params.append(word)
                self._new_alias(message.parameter_list[0].lower(), alias_params)

                return IRCResponse(ResponseType.SAY,
                                   "Created a new alias '{}' for '{}'.".format(message.parameter_list[0].lower(),
                                                                               " ".join(message.parameter_list[1:])),
                                   message.reply_to)
            elif message.command == "unalias":
                if message.user.name not in self.bot.admins:
                    return IRCResponse(ResponseType.SAY, "Only my admins may remove aliases!", message.reply_to)

                if len(message.parameter_list) == 0:
                    return IRCResponse(ResponseType.SAY, "Unalias what?", message.reply_to)

                if message.parameter_list[0].lower() in self.aliases:
                    self._delete_alias(message.parameter_list[0].lower())
                    return IRCResponse(ResponseType.SAY, "Deleted alias '{}'".format(message.parameter_list[0].lower()),
                                       message.reply_to)
                else:
                    return IRCResponse(ResponseType.SAY,
                                       "I don't have an alias '{}'".format(message.parameter_list[0].lower()),
                                       message.reply_to)
            elif message.command == "aliases":
                if len(message.parameter_list) == 0:
                    return_string = "Current aliases: {}".format(", ".join(sorted(self.aliases.keys())))
                    return IRCResponse(ResponseType.SAY, return_string, message.reply_to)
                elif message.parameter_list[0].lower() in self.aliases:
                    return IRCResponse(ResponseType.SAY,
                                       "{} is an alias for: {}".format(message.parameter_list[0].lower(), " ".join(
                                           self.aliases[message.parameter_list[0].lower()])), message.reply_to)
                else:
                    return IRCResponse(ResponseType.SAY,
                                       "'{}' does not match any known alias!".format(message.parameter_list[0].lower()),
                                       message.reply_to)
            elif message.command == "aliashelp":
                if message.user.name not in self.bot.admins:
                    return IRCResponse(ResponseType.SAY, "Only my admins may set alias help text!", message.reply_to)
                if len(message.parameter_list) == 0:
                    return IRCResponse(ResponseType.SAY, "Set the help text for what alias to what?", message.reply_to)
                if message.parameter_list[0].lower() not in self.aliases:
                    return IRCResponse(ResponseType.SAY,
                                       "I have no alias called {!r}.".format(message.parameter_list[0].lower()),
                                       message.reply_to)
                if len(message.parameter_list) == 1:
                    return IRCResponse(ResponseType.SAY, "You didn't give me any help text to set for {!r}!".format(
                        message.parameter_list[0].lower()), message.reply_to)
                alias = message.parameter_list[0].lower()
                alias_help = " ".join(message.parameter_list[1:])
                self.alias_help_dict[alias] = alias_help
                with sqlite3.connect(self.bot.database_file) as conn:
                    c = conn.cursor()
                    c.execute("INSERT INTO aliashelp VALUES (?,?)", (alias, alias_help))
                    conn.commit()
                return IRCResponse(ResponseType.SAY, "{!r} help text set to {!r}.".format(alias, alias_help),
                                   message.reply_to)

        elif message.command in self.aliases:
            new_message = self._aliased_message(message)
            if new_message.command in self.bot.module_handler.mapped_triggers:
                return self.bot.module_handler.mapped_triggers[new_message.command].on_trigger(new_message)

    def _new_alias(self, alias, command):
        self.aliases[alias] = command
        self.bot.module_handler.mapped_triggers[alias] = self
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO aliases VALUES (?,?)", (alias, " ".join(command)))
            conn.commit()

    def _delete_alias(self, alias):
        del self.aliases[alias]
        del self.bot.module_handler.mapped_triggers[alias]
        with sqlite3.connect(self.bot.database_file) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM aliases WHERE alias=?", (alias,))
            c.execute("DELETE FROM aliashelp WHERE alias=?", (alias,))
            conn.commit()

    def _aliased_message(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.command in self.aliases.keys():
            alias = self.aliases[message.command]
            new_msg = u'{}{}'.format(self.bot.command_char, ' '.join(alias))
            if "$sender" in new_msg:
                new_msg = new_msg.replace("$sender", message.user.name)
            if "$channel" in new_msg and message.channel is not None:
                new_msg = new_msg.replace("$channel", message.channel.name)

            if re.search(r'\$[0-9]+', new_msg):  # if the alias contains numbered param replacement points, replace them
                new_msg = new_msg.replace('$0', u' '.join(message.parameter_list))
                for i, param in enumerate(message.parameter_list):
                    if new_msg.find(u"${}+".format(i + 1)) != -1:
                        new_msg = new_msg.replace(u"${}+".format(i + 1), u" ".join(message.parameter_list[i:]))
                    else:
                        new_msg = new_msg.replace(u"${}".format(i + 1), param)
            else:  # if there are no numbered replacement points, append the full parameter list instead
                new_msg += u' {}'.format(u' '.join(message.parameter_list))
            return IRCMessage(message.type, str(message.user), message.channel, new_msg, self.bot)
        return
