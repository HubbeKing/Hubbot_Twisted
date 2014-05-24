from IRCResponse import IRCResponse, ResponseType
from ModuleInterface import ModuleInterface, ModuleAccessLevels


class ModuleLoader(ModuleInterface):
    triggers = ['load', 'reload', 'unload']
    help = "load/reload <function>, unload <function> - handles loading/unloading/reloading of functions. Use 'all' with load/reload to reload all active functions"
    accessLevel = ModuleAccessLevels.ADMINS

    def onTrigger(self, message):
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say, "You didn't specify a function name! Usage: {0}".format(self.help), message.ReplyTo)

        if message.Command.lower() in ['load', 'reload']:
            successes, failures, exceptions = self.load(message.ParameterList)

        elif message.Command.lower() == "unload":
            successes, failures, exceptions = self.unload(message.ParameterList)

        responses = []
        if len(successes) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' {1}ed successfully".format(', '.join(successes), message.Command.lower()), message.ReplyTo))
        if len(failures) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' failed to {1}, or (they) do not exist".format(', '.join(failures), message.Command.lower()), message.ReplyTo))
        if len(exceptions) > 0:
            responses.append(IRCResponse(ResponseType.Say, "'{0}' threw an exception (printed to console)".format(', '.join(exceptions)), message.ReplyTo))

        return responses

    def load(self, moduleNames):

        moduleNameCaseMap = {f.lower(): f for f in moduleNames}

        successes = []
        failures = []
        exceptions = []

        if len(moduleNames) == 1 and 'all' in moduleNameCaseMap:
            for name, module in self.bot.moduleHandler.modules.iteritems():
                if name == 'ModuleLoader':
                    continue

                self.bot.moduleHandler.LoadModule(name)

            return ['all functions'], [], []

        for moduleName in moduleNameCaseMap.keys():

            if moduleName == 'moduleloader':
                failures.append("ModuleLoader (I can't reload myself)")

            else:
                try:
                    success = self.bot.moduleHandler.LoadModule(moduleName)
                    if success:
                        successes.append(self.bot.moduleHandler.moduleCaseMapping[moduleName])
                    else:
                        failures.append(moduleNameCaseMap[moduleName])

                except Exception, x:
                    exceptions.append(moduleNameCaseMap[moduleName])
                    print x.args

        return successes, failures, exceptions

    def unload(self, moduleNames):

        moduleNameCaseMap = {f.lower(): f for f in moduleNames}

        successes = []
        failures = []
        exceptions = []

        for moduleName in moduleNameCaseMap.keys():
            try:
                success = self.bot.moduleHandler.UnloadModule(moduleName)
                if success:
                    successes.append(moduleNameCaseMap[moduleName])
                else:
                    failures.append(moduleNameCaseMap[moduleName])
            except Exception, x:
                exceptions.append(moduleNameCaseMap[moduleName])
                print x.args

        return successes, failures, exceptions