from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import GlobalVars


class Module(ModuleInterface):
    triggers = ["alias"]
    help = "alias <alias> <command> -- create a new alias, Ex. {}alias hugs do hugs".format(GlobalVars.CommandChar)

    def onTrigger(self, Hubbot, message):
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, "Only my admins may create new aliases!", message.ReplyTo)
        if len(message.ParameterList) <= 1:
            return IRCResponse(ResponseType.Say, "Alias what?", message.ReplyTo)
        for (name, module) in GlobalVars.modules.items():
            if message.ParameterList[0] in module.triggers:
                return IRCResponse(ResponseType.Say, "A new alias may not be the same as an existing command trigger!", message.ReplyTo)
        newAlias = []
        for word in message.ParameterList[1:]:
            newAlias.append(word.lower())
        GlobalVars.commandAliases[message.ParameterList[0]] = newAlias
        return IRCResponse(ResponseType.Say, "Created a new alias '{}' for '{}'.".format(message.ParameterList[0], " ".join(message.ParameterList[1:])), message.ReplyTo)