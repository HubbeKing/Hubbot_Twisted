import re
import sqlite3
from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
from hubbot.message import IRCMessage


class Alias(ModuleInterface):
    triggers = ["alias", "unalias", "aliases", "aliashelp"]
    runInThread = True
    aliases = {}
    aliasHelpDict = {}

    def help(self, message):
        """
        @type message: IRCMessage
        """
        helpDict = {
            u"alias":   u"alias <alias> <command/alias> <params> - aliases <alias> to the specified command/alias and parameters\n" \
                        u"you can specify where parameters given to the alias should be inserted with $1, $2, $n. " \
                        u"The whole parameter string is $0. $sender and $channel can also be used.",
            u"unalias": u"unalias <alias> - deletes the alias <alias>",
            u"aliases": u"aliases [<alias>] - lists all defined aliases, or the contents of the specified alias",
            u"aliashelp": u"aliashelp <alias> <helptext> - sets the helptext of the specified alias to the specified string"
        }
        command = message.ParameterList[0].lower()
        if command in helpDict:
            return helpDict[command]
        elif command in self.aliases:
            if command in self.aliasHelpDict:
                return self.aliasHelpDict[command]
            else:
                return u"'{}' is an alias for: {}".format(command, u" ".join(self.aliases[command]))

    def onEnable(self):
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM aliashelp"):
                self.aliasHelpDict[row[0].lower()] = row[1].split(" ")
            for row in c.execute("SELECT * FROM aliases"):
                self.aliases[row[0].lower()] = row[1].split(" ")
        for alias in self.aliases:
            self.bot.moduleHandler.mappedTriggers[alias.lower()] = self

    def onUnload(self):
        for alias in self.aliases:
            del self.bot.moduleHandler.mappedTriggers[alias.lower()]

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command in self.bot.moduleHandler.mappedTriggers:
            return True
        return False

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command in self.triggers:
            if message.Command == "alias":
                if message.User.Name not in self.bot.admins:
                    return IRCResponse(ResponseType.Say, "Only my admins may create new aliases!", message.ReplyTo)

                if len(message.ParameterList) <= 1:
                    return IRCResponse(ResponseType.Say, "Alias what?", message.ReplyTo)

                if message.ParameterList[0].lower() in self.bot.moduleHandler.mappedTriggers:
                    return IRCResponse(ResponseType.Say, "'{}' is already a command!".format(message.ParameterList[0].lower()), message.ReplyTo)

                if message.ParameterList[1].lower() not in self.bot.moduleHandler.mappedTriggers and message.ParameterList[1].lower() not in self.aliases:
                    return IRCResponse(ResponseType.Say, "'{}' is not a valid command or alias!".format(message.ParameterList[1].lower()), message.ReplyTo)
                if message.ParameterList[0].lower() in self.aliases:
                    return IRCResponse(ResponseType.Say, "'{}' is already an alias!".format(message.ParameterList[0].lower()), message.ReplyTo)

                aliasParams = []
                for word in message.ParameterList[1:]:
                    aliasParams.append(word)
                self._newAlias(message.ParameterList[0].lower(), aliasParams)

                return IRCResponse(ResponseType.Say, "Created a new alias '{}' for '{}'.".format(message.ParameterList[0].lower(), " ".join(message.ParameterList[1:])), message.ReplyTo)
            elif message.Command == "unalias":
                if message.User.Name not in self.bot.admins:
                    return IRCResponse(ResponseType.Say, "Only my admins may remove aliases!", message.ReplyTo)

                if len(message.ParameterList) == 0:
                    return IRCResponse(ResponseType.Say, "Unalias what?", message.ReplyTo)

                if message.ParameterList[0].lower() in self.aliases:
                    self._deleteAlias(message.ParameterList[0].lower())
                    return IRCResponse(ResponseType.Say, "Deleted alias '{}'".format(message.ParameterList[0].lower()), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, "I don't have an alias '{}'".format(message.ParameterList[0].lower()), message.ReplyTo)
            elif message.Command == "aliases":
                if len(message.ParameterList) == 0:
                    returnString = "Current aliases: {}".format(", ".join(sorted(self.aliases.keys())))
                    return IRCResponse(ResponseType.Say, returnString, message.ReplyTo)
                elif message.ParameterList[0].lower() in self.aliases:
                    return IRCResponse(ResponseType.Say, "{} is an alias for: {}".format(message.ParameterList[0].lower(), " ".join(self.aliases[message.ParameterList[0].lower()])), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, "'{}' does not match any known alias!".format(message.ParameterList[0].lower()), message.ReplyTo)
            elif message.Command == "aliashelp":
                if message.User.Name not in self.bot.admins:
                    return IRCResponse(ResponseType.Say, "Only my admins may set alias help text!", message.ReplyTo)
                if len(message.ParameterList) == 0:
                    return IRCResponse(ResponseType.Say, "Set the help text for what alias to what?", message.ReplyTo)
                if message.ParameterList[0].lower() not in self.aliases:
                    return IRCResponse(ResponseType.Say, "I have no alias called \"{}\".".format(message.ParameterList[0].lower()), message.ReplyTo)
                if len(message.ParameterList) == 1:
                    return IRCResponse(ResponseType.Say, "You didn't give me any help text to set for \"{}\"!".format(message.ParameterList[0].lower()), message.ReplyTo)
                alias = message.ParameterList[0].lower()
                aliasHelp = " ".join(message.ParameterList[1:])
                self.aliasHelpDict[alias] = aliasHelp
                with sqlite3.connect(self.bot.databaseFile) as conn:
                    c = conn.cursor()
                    c.execute("INSERT INTO aliashelp VALUES (?,?)", (alias, aliasHelp))
                    conn.commit()
                return IRCResponse(ResponseType.Say, "\"{}\" help text set to \"{}\".".format(alias, aliasHelp), message.ReplyTo)

        elif message.Command in self.aliases:
            newMessage = self._aliasedMessage(message)
            if newMessage.Command in self.bot.moduleHandler.mappedTriggers:
                return self.bot.moduleHandler.mappedTriggers[newMessage.Command].onTrigger(newMessage)

    def _newAlias(self, alias, command):
        self.aliases[alias] = command
        self.bot.moduleHandler.mappedTriggers[alias] = self
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO aliases VALUES (?,?)", (alias, " ".join(command)))
            conn.commit()

    def _deleteAlias(self, alias):
        del self.aliases[alias]
        del self.bot.moduleHandler.mappedTriggers[alias]
        with sqlite3.connect(self.bot.databaseFile) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM aliases WHERE alias=?", (alias,))
            c.execute("DELETE FROM aliashelp WHERE alias=?", (alias,))
            conn.commit()

    def _aliasedMessage(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Command in self.aliases.keys():
            alias = self.aliases[message.Command]
            newMsg = u'{}{}'.format(self.bot.commandChar, ' '.join(alias))
            if "$sender" in newMsg:
                newMsg = newMsg.replace("$sender", message.User.Name)
            if "$channel" in newMsg and message.Channel is not None:
                newMsg = newMsg.replace("$channel", message.Channel.Name)

            if re.search(r'\$[0-9]+', newMsg):  # if the alias contains numbered param replacement points, replace them
                newMsg = newMsg.replace('$0',  u' '.join(message.ParameterList))
                for i, param in enumerate(message.ParameterList):
                    if newMsg.find(u"${}+".format(i+1)) != -1:
                        newMsg = newMsg.replace(u"${}+".format(i+1), u" ".join(message.ParameterList[i:]))
                    else:
                        newMsg = newMsg.replace(u"${}".format(i+1), param)
            else:  # if there are no numbered replacement points, append the full parameter list instead
                newMsg += u' {}'.format(u' '.join(message.ParameterList))
            return IRCMessage(message.Type, message.User.String, message.Channel, newMsg, self.bot)
        return
