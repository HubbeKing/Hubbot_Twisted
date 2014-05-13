from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface
import GlobalVars


class Module(ModuleInterface):
    triggers = ['help','command','commands']
    help = 'command(s)/help (<function>) - returns a list of loaded modules, or the help text of a particular command if one is specified'
    
    def execute(self, Hubbot, message):
        if len(message.ParameterList) > 0:
            if message.ParameterList[0].lower() in GlobalVars.moduleCaseMapping:
                func = GlobalVars.modules[GlobalVars.moduleCaseMapping[message.ParameterList[0].lower()]]
                if isinstance(func.help, basestring):
                    return IRCResponse(ResponseType.Say, func.help, message.ReplyTo)
                else:
                    return IRCResponse(ResponseType.Say, func.help(message), message.ReplyTo)
            else:
                return IRCResponse(ResponseType.Say, '"{}" not found, try "{}" without parameters to see a list of loaded modules'.format(message.ParameterList[0],message.Command), message.ReplyTo)
        else:
            funcs = ', '.join(sorted(GlobalVars.modules.iterkeys(), key=lambda s: s.lower()))
            return [IRCResponse(ResponseType.Say, "Modules loaded are:", message.ReplyTo),
                    IRCResponse(ResponseType.Say, funcs, message.ReplyTo),
                    IRCResponse(ResponseType.Say, "Use {}help <module> for module commands.".format(GlobalVars.CommandChar), message.ReplyTo)]
