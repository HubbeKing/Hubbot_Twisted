from response import IRCResponse, ResponseType
from moduleinterface import ModuleInterface


class Help(ModuleInterface):
    triggers = ['help','command','commands']
    help = 'command(s)/help (<function>) - returns a list of loaded modules, or the help text of a particular command if one is specified'
    
    def onTrigger(self, message):
        """
        @type message: IRCMessage.IRCMessage
        """
        if len(message.ParameterList) > 0:
            if message.ParameterList[0].lower() in self.bot.moduleHandler.moduleCaseMapping:
                func = self.bot.moduleHandler.modules[self.bot.moduleHandler.moduleCaseMapping[message.ParameterList[0].lower()]]
                return IRCResponse(ResponseType.Say, func.help, message.ReplyTo)
            elif message.ParameterList[0].lower() in self.bot.moduleHandler.mappedTriggers:
                func = self.bot.moduleHandler.mappedTriggers[message.ParameterList[0].lower()]
                return IRCResponse(ResponseType.Say, func.help, message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, '"{}" not found, try "{}" without parameters to see a list of loaded modules'.format(message.ParameterList[0], message.Command), message.ReplyTo)
        else:
            funcs = ', '.join(sorted(self.bot.moduleHandler.modules.iterkeys(), key=lambda s: s.lower()))
            return [IRCResponse(ResponseType.Say, "Modules loaded are:", message.ReplyTo),
                    IRCResponse(ResponseType.Say, funcs, message.ReplyTo),
                    IRCResponse(ResponseType.Say, "Use {}help <module> for module commands.".format(self.bot.CommandChar), message.ReplyTo)]
