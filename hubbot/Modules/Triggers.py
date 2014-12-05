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
            if message.ParameterList[0].lower() not in self.bot.moduleHandler.moduleCaseMapping:
                return IRCResponse(ResponseType.Say, "No module named \"{}\" is currently loaded!", message.ReplyTo)
            moduleToGet = self.bot.moduleHandler.moduleCaseMapping[message.ParameterList[0].lower()]
            commands = []
            for trigger, module in self.bot.moduleHandler.mappedTriggers.items():
                if module == moduleToGet:
                    commands.append(trigger)
            return IRCResponse(ResponseType.Say,
                               "Module \"{}\" contains the triggers: {}".format(message.ParameterList[0],
                                                                                ", ".join(commands)),
                               message.ReplyTo)
