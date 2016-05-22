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

        else:
            successes, failures, exceptions = self.disable(message.ParameterList)

        responses = []
        if len(successes) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{}' {}d successfully.".format(', '.join(successes), message.Command), message.ReplyTo))
            self.bot.logger.info("'{}' {}d successfully.".format(", ".join(successes), message.Command))
        if len(failures) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{}' failed to {}.".format(', '.join(failures), message.Command), message.ReplyTo))
        if len(exceptions) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{}' threw an exception.".format(', '.join(exceptions)), message.ReplyTo))

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
                    self.bot.logger.exception("Exception when enabling module {!r}".format(moduleNameCaseMap[moduleName]))

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
            except:
                exceptions.append(moduleNameCaseMap[moduleName])

        return successes, failures, exceptions
