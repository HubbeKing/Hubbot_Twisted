from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
import logging


class CustomHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self, logging.INFO)
        self.buffer = {}

    def emit(self, record):
        self.buffer[record.levelname] = record

    def getLatest(self, level):
        if level in self.buffer:
            record = self.format(self.buffer[level])
            return "Latest message of level {}: > {}".format(level, record)
        else:
            return "No messages of level {} have been logged.".format(level)


class Log(ModuleInterface):
    triggers = ["log"]
    help = "log <level> - Used to retrieve the latest record the specified log level. Also handles most server logging."
    priority = -1

    logFuncs = {
        'PRIVMSG': lambda m: u'<{0}> {1}'.format(m.User.Name, m.MessageString),
        'NOTICE': lambda m: u'[{0}] {1}'.format(m.User.Name, m.MessageString),
        'KICK': lambda m: u'!<< {0} was kicked by {1}{2}'.format(m.Kickee, m.User.Name, m.MessageString),
        'TOPIC': lambda m: u'# {0} set the topic to: {1}'.format(m.User.Name, m.MessageString)
    }

    def onEnable(self):
        logger = logging.getLogger(self.bot.server)
        self.handler = CustomHandler()
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s', '%H:%M:%S'))
        logger.addHandler(self.handler)

    def onDisable(self):
        logger = logging.getLogger(self.bot.server)
        if self.handler in logger.handlers:
            logger.removeHandler(self.handler)

    def shouldTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return True

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.Type in self.acceptedTypes and message.Command in self.triggers:
            if len(message.ParameterList) == 1 and message.User.Name in self.bot.admins:
                handlerMsg = self.handler.getLatest((message.ParameterList[0]))
                if "\n" not in handlerMsg:
                    return IRCResponse(ResponseType.Say, handlerMsg, message.ReplyTo)
                else:
                    returnMessage = handlerMsg.split("\n")[0]
                    exceptionInfo = " ".join(handlerMsg.split("\n")[1:])
                    return IRCResponse(ResponseType.Say, returnMessage, message.ReplyTo), \
                           IRCResponse(ResponseType.Notice, exceptionInfo, message.ReplyTo)

        if message.Type is not None and message.Type in self.logFuncs:
            logString = self.logFuncs[message.Type](message)
            if message.Type == "PRIVMSG":
                for trigger in self.bot.moduleHandler.mappedTriggers.keys():
                    if message.Command.lower() == trigger.lower():
                        self.bot.logger.info(logString)
                        break
            else:
                self.bot.logger.info(logString)
