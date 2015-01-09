from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class ModuleEnabler(ModuleInterface):
    triggers = ["enable", "disable"]
    help = "enable <function>, disable <function> - handles enabling and disabling of functions."
    accessLevel = ModuleAccessLevel.ADMINS

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "You didn't specify a function name! Usage: {0}".format(self.help), message.ReplyTo)

        if message.Command == "enable":
            successes, failures, exceptions = self.enable(message.ParameterList)

        elif message.Command.lower() == "disable":
            successes, failures, exceptions = self.disable(message.ParameterList)

        responses = []
        if len(successes) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' {1}ed successfully".format(', '.join(successes), message.Command.lower()), message.ReplyTo))
        if len(failures) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' failed to {1}, or (they) do not exist".format(', '.join(failures), message.Command.lower()), message.ReplyTo))
        if len(exceptions) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' threw an exception (printed to console)".format(', '.join(exceptions)), message.ReplyTo))

        return responses

    def enable(self, moduleNames):

        moduleNameCaseMap = {f.lower(): f for f in moduleNames}

        successes = []
        failures = []
        exceptions = []

        for moduleName in moduleNameCaseMap.keys():

            if moduleName == 'moduleenabled':
                failures.append("ModuleEnabler (I can't enable myself)")

            else:
                try:
                    success = self.bot.moduleHandler.enableModule(moduleName)
                    if success:
                        successes.append(self.bot.moduleHandler.moduleCaseMap[moduleName])
                    else:
                        failures.append(moduleNameCaseMap[moduleName])

                except Exception:
                    exceptions.append(moduleNameCaseMap[moduleName])
                    self.bot.logger.exception("Exception when enabling module \"{}\"".format(moduleNameCaseMap[moduleName]))

        return successes, failures, exceptions

    def disable(self, moduleNames):

        moduleNameCaseMap = {f.lower(): f for f in moduleNames}

        successes = []
        failures = []
        exceptions = []

        for moduleName in moduleNameCaseMap.keys():
            try:
                success = self.bot.moduleHandler.disableModule(moduleName)
                if success:
                    successes.append(moduleNameCaseMap[moduleName])
                else:
                    failures.append(moduleNameCaseMap[moduleName])
            except Exception:
                exceptions.append(moduleNameCaseMap[moduleName])
                self.bot.logger.exception("Exception when disabliong module \"{}\"".format(moduleNameCaseMap[moduleName]))

        return successes, failures, exceptions
