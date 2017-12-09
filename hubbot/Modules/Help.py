from __future__ import unicode_literals
from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface


class Help(ModuleInterface):
    triggers = ['help', 'command', 'commands']
    help = 'command(s)/help (<function>) - returns a list of loaded modules, or the help text of a particular command if one is specified'
    
    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) > 0:
            if message.parameter_list[0].lower() in self.bot.module_handler.module_case_map:
                func = self.bot.module_handler.modules[self.bot.module_handler.module_case_map[message.parameter_list[0].lower()]]
                if isinstance(func.help, basestring):
                    return IRCResponse(ResponseType.SAY, func.help, message.reply_to)
                else:
                    return IRCResponse(ResponseType.SAY, func.help(message), message.reply_to)
            elif message.parameter_list[0].lower() in self.bot.module_handler.mapped_triggers:
                func_help = self.bot.module_handler.mapped_triggers[message.parameter_list[0].lower()].help
                if isinstance(func_help, basestring):
                    return IRCResponse(ResponseType.SAY, func_help, message.reply_to)
                else:
                    return IRCResponse(ResponseType.SAY, func_help(message), message.reply_to)
            else:
                return IRCResponse(ResponseType.SAY, '"{}" not found, try "{}" without parameters to see a list of loaded modules'.format(message.parameter_list[0], message.command), message.reply_to)
        else:
            funcs = ', '.join(sorted(self.bot.module_handler.modules.iterkeys(), key=lambda s: s.lower()))
            return [IRCResponse(ResponseType.SAY, "Modules loaded are:", message.reply_to),
                    IRCResponse(ResponseType.SAY, funcs, message.reply_to),
                    IRCResponse(ResponseType.SAY, "Use {}help <module> for module commands.".format(self.bot.command_char), message.reply_to)]
