from __future__ import unicode_literals
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Triggers(ModuleInterface):
    triggers = ["triggers"]
    help = "triggers [module] -- returns a list of all commands, if no module is specified, " \
           "returns all commands currently loaded."

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) == 0:
            if message.user.name != message.reply_to:
                return IRCResponse(ResponseType.SAY, "{} must be used over PM!".format(message.command),
                                   message.reply_to)
            else:
                response = ", ".join(sorted(self.bot.moduleHandler.mappedTriggers.keys()))
                return IRCResponse(ResponseType.SAY, response, message.reply_to)
        else:
            if message.parameter_list[0].lower() in self.bot.moduleHandler.mappedTriggers:
                proper_name = self.bot.moduleHandler.mappedTriggers[message.parameter_list[0].lower()].__class__.__name__
                return IRCResponse(ResponseType.SAY,
                                   "Module {!r} contains the triggers: {}".format(proper_name, ", ".join(self.bot.moduleHandler.mappedTriggers[message.parameter_list[0].lower()].triggers)),
                                   message.reply_to)

            elif message.parameter_list[0].lower() not in self.bot.moduleHandler.moduleCaseMap:
                return IRCResponse(ResponseType.SAY,
                                   "No module named {!r} is currently loaded!".format(message.parameter_list[0].lower()),
                                   message.reply_to)

            else:
                proper_name = self.bot.moduleHandler.moduleCaseMap[message.parameter_list[0].lower()]
                module = self.bot.moduleHandler.modules[proper_name]

                return IRCResponse(ResponseType.SAY,
                                   "Module {!r} contains the triggers: {}".format(proper_name, ", ".join(module.triggers)),
                                   message.reply_to)
