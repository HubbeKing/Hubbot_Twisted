from hubbot.moduleinterface import ModuleInterface

logFuncs = {
    'PRIVMSG': lambda m: u'<{0}> {1}'.format(m.User.Name, m.MessageString),
    'NOTICE': lambda m: u'[{0}] {1}'.format(m.User.Name, m.MessageString),
    'NICK': lambda m: u'{0} is now known as {1}'.format(m.User.Name, m.MessageString),
    'KICK': lambda m: u'!<< {0} was kicked by {1}{2}'.format(m.Kickee, m.User.Name, m.MessageString),
    'TOPIC': lambda m: u'# {0} set the topic to: {1}'.format(m.User.Name, m.MessageString),
    'MODE': lambda m: u'# {0} sets mode: {1}{2} {3}'.format(m.User.Name, m.ModeOperator, m.Modes, ' '.join(m.ModeArgs))
}


class Log(ModuleInterface):
    priority = -1

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return True

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Type in logFuncs:
            logString = logFuncs[message.Type](message)
            if message.Type == "PRIVMSG":
                for trigger in self.bot.moduleHandler.mappedTriggers.keys():
                    if message.Command.lower() == trigger.lower():
                        self.bot.logger.info(logString)
                        return None
            else:
                self.bot.logger.info(logString)
                return None
