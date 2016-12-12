from hubbot.moduleinterface import ModuleInterface
from hubbot.response import IRCResponse, ResponseType
import logging


class CustomHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self, logging.INFO)
        self.buffer = {}

    def emit(self, record):
        self.buffer[record.levelname] = record

    def get_latest(self, level):
        if level in self.buffer:
            record = self.format(self.buffer[level])
            return "Latest message of level {}: > {}".format(level, record)
        else:
            return "No messages of level {} have been logged.".format(level)


class Log(ModuleInterface):
    triggers = ["log"]
    help = "log <level> - Used to retrieve the latest record the specified log level. Also handles most server logging."
    priority = -1

    log_funcs = {
        'PRIVMSG': lambda m: u'<{0}> {1}'.format(m.user.name, m.message_string),
        'NOTICE': lambda m: u'[{0}] {1}'.format(m.user.name, m.message_string),
        'KICK': lambda m: u'!<< {0} was kicked by {1}{2}'.format(m.kickee, m.m.user.name, m.message_string),
        'TOPIC': lambda m: u'# {0} set the topic to: {1}'.format(m.user.name, m.message_string)
    }

    def on_load(self):
        logger = logging.getLogger(self.bot.server)
        self.handler = CustomHandler()
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s', '%H:%M:%S'))
        logger.addHandler(self.handler)

    def on_unload(self):
        logger = logging.getLogger(self.bot.server)
        if self.handler in logger.handlers:
            logger.removeHandler(self.handler)

    def should_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        return True

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if message.type in self.accepted_types and message.command in self.triggers:
            if len(message.parameter_list) == 1 and message.user.name in self.bot.admins:
                handler_msg = self.handler.get_latest((message.parameter_list[0]))
                if "\n" not in handler_msg:
                    return IRCResponse(ResponseType.SAY, handler_msg, message.reply_to)
                else:
                    return_message = handler_msg.split("\n")[0]
                    exception_info = " ".join(handler_msg.split("\n")[1:])
                    return IRCResponse(ResponseType.SAY, return_message, message.reply_to), \
                           IRCResponse(ResponseType.NOTICE, exception_info, message.reply_to)

        if message.type is not None and message.type in self.log_funcs:
            log_string = self.log_funcs[message.type](message)
            if message.type == "PRIVMSG":
                for trigger in self.bot.moduleHandler.mappedTriggers.keys():
                    if message.command.lower() == trigger.lower():
                        self.bot.logger.info(log_string)
                        break
            else:
                self.bot.logger.info(log_string)
