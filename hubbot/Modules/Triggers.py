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
                response = ", ".join(sorted(self.bot.module_handler.mapped_triggers.keys()))
                return IRCResponse(ResponseType.NOTICE, response, message.reply_to)
            else:
                response = ", ".join(sorted(self.bot.module_handler.mapped_triggers.keys()))
                return IRCResponse(ResponseType.SAY, response, message.reply_to)
        else:
            if message.parameter_list[0].lower() in self.bot.module_handler.mapped_triggers:
                proper_name = self.bot.module_handler.mapped_triggers[message.parameter_list[0].lower()].__class__.__name__
                return IRCResponse(ResponseType.SAY,
                                   "Module {!r} contains the triggers: {}".format(proper_name, ", ".join(self.bot.module_handler.mapped_triggers[message.parameter_list[0].lower()].triggers)),
                                   message.reply_to)

            elif message.parameter_list[0].lower() not in self.bot.module_handler.module_case_map:
                return IRCResponse(ResponseType.SAY,
                                   "No module named {!r} is currently loaded!".format(message.parameter_list[0].lower()),
                                   message.reply_to)

            else:
                proper_name = self.bot.module_handler.module_case_map[message.parameter_list[0].lower()]
                loaded_module = self.bot.module_handler.modules[proper_name]

                return IRCResponse(ResponseType.SAY,
                                   "Module {!r} contains the triggers: {}".format(proper_name, ", ".join(loaded_module.triggers)),
                                   message.reply_to)
