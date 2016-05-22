from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Triggers(ModuleInterface):
    triggers = ["triggers"]
    help = "triggers [module] -- returns a list of all commands, if no module is specified, " \
           "returns all commands currently loaded."

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            if message.User.Name != message.ReplyTo:
                return IRCResponse(ResponseType.Say, "{} must be used over PM!".format(message.Command),
                                   message.ReplyTo)
            else:
                response = ", ".join(sorted(self.bot.moduleHandler.mappedTriggers.keys()))
                return IRCResponse(ResponseType.Say, response, message.ReplyTo)
        else:
            if message.ParameterList[0].lower() in self.bot.moduleHandler.mappedTriggers:
                properName = self.bot.moduleHandler.mappedTriggers[message.ParameterList[0].lower()].__class__.__name__
                return IRCResponse(ResponseType.Say,
                                   "Module {!r} contains the triggers: {}".format(properName, ", ".join(self.bot.moduleHandler.mappedTriggers[message.ParameterList[0].lower()].triggers)),
                                   message.ReplyTo)

            elif message.ParameterList[0].lower() not in self.bot.moduleHandler.moduleCaseMap:
                return IRCResponse(ResponseType.Say,
                                   "No module named {!r} is currently loaded!".format(message.ParameterList[0].lower()),
                                   message.ReplyTo)

            else:
                properName = self.bot.moduleHandler.moduleCaseMap[message.ParameterList[0].lower()]
                module = self.bot.moduleHandler.modules[properName]

                return IRCResponse(ResponseType.Say,
                                   "Module {!r} contains the triggers: {}".format(properName, ", ".join(module.triggers)),
                                   message.ReplyTo)
