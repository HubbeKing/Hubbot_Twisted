from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class ModuleLoader(ModuleInterface):
    triggers = ["load", "unload", "reload"]
    accessLevel = ModuleAccessLevel.ADMINS

    def help(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        helpDict = {
            u"moduleloader": u"load/unload/reload <modules> - Handles loading, unloading, and reloading of modules.",
            u"load": u"load <modules> - Used to load modules to make them available for enabling.",
            u"unload": u"unload <modules> - Used to unload modules entirely, from all servers.",
            u"reload": u"reload <modules> - Used to reload modules to make new changes take effect."
        }
        return helpDict[message.ParameterList[0].lower()]

    def onTrigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.ParameterList) == 0:
            return IRCResponse(ResponseType.Say,
                               "You didn't specify a module name! Usage: {}".format(self.help(message)),
                               message.ReplyTo)
        command = {"load": self.load, "reload": self.reload,  "unload": self.unload}[message.Command]

        successes, failures, exceptions = command(message.ParameterList)

        responses = []

        if len(successes) > 0:
            responses.append(IRCResponse(ResponseType.Say,
                                         "\"{}\" {}ed successfully.".format(", ".join(successes), message.Command),
                                         message.ReplyTo))
        if len(failures) > 0:
            responses.append(IRCResponse(ResponseType.Say,
                                         "\"{}\" failed to {}, or (they) do not exist.".format(", ".join(failures), message.Command),
                                         message.ReplyTo))
        if len(exceptions) > 0:
            responses.append(IRCResponse(ResponseType.Say,
                                         "\"{}\" threw an exception (printed to console)".format(", ".join(exceptions)),
                                         message.ReplyTo))

        return responses

    def load(self, moduleNames):
        moduleCaseMap = {m.lower(): m for m in moduleNames}

        successes = []
        failures = []
        exceptions = []

        if len(moduleNames) == 1 and "all" in moduleCaseMap:
            for name, _ in self.bot.bothandler.modules.iteritems():
                if name == "ModuleLoader":
                    continue

                self.bot.bothandler.loadModule(name)

            return ["all modules"], [], []

        for moduleName in moduleCaseMap.keys():

            if moduleName == "moduleloader":
                failures.append("ModuleLoader (I can't load myself)")

            else:
                try:
                    success = self.bot.bothandler.loadModule(moduleName)
                    if success:
                        successes.append(self.bot.bothandler.moduleCaseMap[moduleName])
                    else:
                        failures.append(moduleCaseMap[moduleName])
                except:
                    exceptions.append(moduleCaseMap[moduleName])
                    self.bot.logger.exception("Exception when loading module \"{}\"".format(moduleCaseMap[moduleName]))

        return successes, failures, exceptions

    def reload(self, moduleNames):
        moduleCaseMap = {m.lower(): m for m in moduleNames}

        successes = []
        failures = []
        exceptions = []

        if len(moduleNames) == 1 and "all" in moduleCaseMap:
            for name, _ in self.bot.bothandler.modules.iteritems():
                if name == "ModuleLoader":
                    continue

                self.bot.bothandler.reloadModule(name)

            return ["all modules"], [], []

        for moduleName in moduleCaseMap.keys():

            if moduleName == "moduleloader":
                failures.append("ModuleLoader (I can't reload myself)")

            else:
                try:
                    success = self.bot.bothandler.reloadModule(moduleName)
                    if success:
                        successes.append(self.bot.bothandler.moduleCaseMap[moduleName])
                    else:
                        failures.append(moduleCaseMap[moduleName])
                except:
                    exceptions.append(moduleCaseMap[moduleName])
                    self.bot.logger.exception("Exception when reloading module \"{}\"".format(moduleCaseMap[moduleName]))

        return successes, failures, exceptions

    def unload(self, moduleNames):
        moduleCaseMap = {m.lower(): m for m in moduleNames}

        successes = []
        failures = []
        exceptions = []

        for moduleName in moduleCaseMap.keys():
            try:
                success = self.bot.bothandler.unloadModule(moduleName)
                if success:
                    successes.append(moduleCaseMap[moduleName])
                else:
                    failures.append(moduleCaseMap[moduleName])
            except:
                exceptions.append(moduleCaseMap[moduleName])
                self.bot.logger.exception("Exception when unloading module \"{}\"".format(moduleCaseMap[moduleName]))
