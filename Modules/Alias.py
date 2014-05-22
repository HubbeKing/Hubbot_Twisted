from ModuleInterface import ModuleInterface
from IRCResponse import IRCResponse, ResponseType
import GlobalVars


class Alias(ModuleInterface):
    triggers = ["alias"]
    help = 'alias <alias> <command> <params> - aliases <alias> to the specified command and parameters\n' \
           'you can specify where parameters given to the alias should be inserted with $1, $2, $n. ' \
           'The whole parameter string is $0. $sender and $channel can also be used.'

    def onTrigger(self, message):
        if message.User.Name not in GlobalVars.admins:
            return IRCResponse(ResponseType.Say, "Only my admins may create new aliases!", message.ReplyTo)

        if len(message.ParameterList) <= 1:
            return IRCResponse(ResponseType.Say, "Alias what?", message.ReplyTo)

        triggerFound = False
        for (name, module) in self.bot.moduleHandler.modules.items():
            if message.ParameterList[0] in module.triggers:
                return IRCResponse(ResponseType.Say, "'{}' is already a command!".format(message.ParameterList[0]), message.ReplyTo)
            if message.ParameterList[1] in module.triggers:
                triggerFound = True

        if not triggerFound:
            return IRCResponse(ResponseType.Say, "'{}' is not a valid command!".format(message.ParameterList[1]), message.ReplyTo)
        if message.ParameterList[0] in self.bot.moduleHandler.commandAliases.keys():
            return IRCResponse(ResponseType.Say, "'{}' is already an alias!".format(message.ParameterList[0]), message.ReplyTo)

        newAlias = []
        for word in message.ParameterList[1:]:
            newAlias.append(word.lower())
        self.bot.moduleHandler.commandAliases[message.ParameterList[0]] = newAlias

        return IRCResponse(ResponseType.Say, "Created a new alias '{}' for '{}'.".format(message.ParameterList[0], " ".join(message.ParameterList[1:])), message.ReplyTo)