import sqlite3
from moduleinterface import ModuleInterface
from response import IRCResponse, ResponseType
from IRCMessage import IRCMessage


class Alias(ModuleInterface):
    triggers = ["alias", "unalias"]
    help = 'alias <alias> <command> <params> - aliases <alias> to the specified command and parameters\n' \
           'you can specify where parameters given to the alias should be inserted with $1, $2, $n. ' \
           'you can use $1+, $2+ for all parameters after the first, second one, etc. ' \
           'The whole parameter string is $0. $sender and $channel can also be used.'
    aliases = {}

    def shouldTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        return True

    def onLoad(self):
        with sqlite3.connect("data/data.db") as conn:
            c = conn.cursor()
            for row in c.execute("SELECT * FROM aliases"):
                self.aliases[row[0]] = row[1].split(" ")

    def onTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        if message.Command in self.triggers:
            if message.Command == "alias":
                if message.User.Name not in self.bot.admins:
                    return IRCResponse(ResponseType.Say, "Only my admins may create new aliases!", message.ReplyTo)

                if len(message.ParameterList) <= 1:
                    return IRCResponse(ResponseType.Say, "Alias what?", message.ReplyTo)

                triggerFound = False
                for (name, module) in self.bot.moduleHandler.modules.items():
                    if message.ParameterList[0] in module.triggers:
                        return IRCResponse(ResponseType.Say, "'{}' is already a command!".format(message.ParameterList[0]), message.ReplyTo)
                    if message.ParameterList[1] in module.triggers:
                        triggerFound = True

                if not triggerFound:
                    return IRCResponse(ResponseType.Say, "'{}' is not a valid command!".format(message.ParameterList[1]), message.ReplyTo)
                if message.ParameterList[0] in self.aliases.keys():
                    return IRCResponse(ResponseType.Say, "'{}' is already an alias!".format(message.ParameterList[0]), message.ReplyTo)

                newAlias = []
                for word in message.ParameterList[1:]:
                    newAlias.append(word.lower())
                self.newAlias(message.ParameterList[0], newAlias)

                return IRCResponse(ResponseType.Say, "Created a new alias '{}' for '{}'.".format(message.ParameterList[0], " ".join(message.ParameterList[1:])), message.ReplyTo)
            elif message.Command == "unalias":
                if message.User.Name not in self.bot.admins:
                    return IRCResponse(ResponseType.Say, "Only my admins may remove aliases!", message.ReplyTo)

                if len(message.ParameterList) == 0:
                    return IRCResponse(ResponseType.Say, "Unalias what?", message.ReplyTo)

                if message.ParameterList[0] in self.aliases.keys():
                    self.deleteAlias(message.ParameterList[0])
                    return IRCResponse(ResponseType.Say, "Deleted alias '{}'".format(message.ParameterList[0]), message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, "I don't have an alias '{}'".format(message.ParameterList[0]), message.ReplyTo)

        elif message.Command in self.aliases.keys():
            self.bot.moduleHandler.handleMessage(self.aliasedMessage(message))

    def newAlias(self, alias, command):
        self.aliases[alias] = command
        with sqlite3.connect("data/data.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO aliases VALUES (?,?)", (alias, " ".join(command)))
            conn.commit()

    def deleteAlias(self, alias):
        del self.aliases[alias]
        with sqlite3.connect("data/data.db") as conn:
            c = conn.cursor()
            c.execute("DELETE FROM aliases WHERE alias=?", (alias,))
            conn.commit()

    def aliasedMessage(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        if message.Command in self.aliases.keys():
            alias = self.aliases[message.Command]
            newMsg = message.MessageString.replace(message.Command, " ".join(alias), 1)
            if "$sender" in newMsg:
                newMsg = newMsg.replace("$sender", message.User.Name)
            if "$channel" in newMsg:
                newMsg = newMsg.replace("$channel", message.ChannelObj.Name)
            if "$0" in newMsg:
                newMsg = newMsg.replace(message.Parameters, "")
                newMsg = newMsg.replace("$0", " ".join(message.ParameterList))
            if len(message.ParameterList) >= 1 and "$" in newMsg:
                newMsg = newMsg.replace(message.Parameters, "")
                for i, param in enumerate(message.ParameterList):
                    if newMsg.find("${}+".format(i+1)) != -1:
                        newMsg = newMsg.replace("${}+".format(i+1), " ".join(message.ParameterList[i:]))
                    else:
                        newMsg = newMsg.replace("${}".format(i+1), param)
            return IRCMessage(message.Type, message.User.String, message.ChannelObj, newMsg, self.bot)
