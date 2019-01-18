from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleInterface, ModuleAccessLevel


class ModuleLoader(ModuleInterface):
    triggers = ["load", "unload", "reload"]
    access_level = ModuleAccessLevel.ADMINS

    def help(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        help_dict = {
            "moduleloader": "load/unload/reload <modules> - Handles loading, unloading, and reloading of modules.",
            "load": "load <modules> - Used to load modules to make them available for enabling.",
            "unload": "unload <modules> - Used to unload modules entirely, from all servers.",
            "reload": "reload <modules> - Used to reload modules to make new changes take effect."
        }
        return help_dict[message.parameter_list[0].lower()]

    def on_trigger(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        if len(message.parameter_list) == 0:
            return IRCResponse(ResponseType.SAY,
                               "You didn't specify a module name! Usage: {}".format(self.help(message)),
                               message.reply_to)
        command = {"load": self.load, "reload": self.reload, "unload": self.unload}[message.command]

        successes, failures, exceptions = command(message.parameter_list)

        responses = []

        if len(successes) > 0:
            responses.append(IRCResponse(ResponseType.SAY,
                                         "{!r} {}ed successfully.".format(", ".join(successes), message.command),
                                         message.reply_to))
            self.bot.logger.info("'{}' {}d successfully.".format(", ".join(successes), message.command))
        if len(failures) > 0:
            responses.append(IRCResponse(ResponseType.SAY,
                                         "{!r} failed to {}.".format(", ".join(failures), message.command),
                                         message.reply_to))
        if len(exceptions) > 0:
            responses.append(IRCResponse(ResponseType.SAY,
                                         "{!r} threw an exception.".format(", ".join(exceptions)),
                                         message.reply_to))

        return responses

    def load(self, module_names):
        module_case_map = {m.lower(): m for m in module_names}

        successes = []
        failures = []
        exceptions = []

        if len(module_names) == 1 and "all" in module_case_map:
            for name, _ in self.bot.module_handler.modules.iteritems():
                if name == "ModuleLoader":
                    continue

                self.bot.module_handler.load_module(name)

            return ["all modules"], [], []

        for module_name in module_case_map.keys():

            if module_name == "moduleloader":
                failures.append("ModuleLoader (I can't load myself)")

            else:
                try:
                    success = self.bot.module_handler.load_module(module_name)
                    if success:
                        successes.append(self.bot.module_handler.module_case_map[module_name])
                    else:
                        failures.append(module_case_map[module_name])
                except Exception:
                    exceptions.append(module_case_map[module_name])
                    self.bot.logger.exception("Exception when loading module {!r}".format(module_case_map[module_name]))

        return successes, failures, exceptions

    def reload(self, module_names):
        module_case_map = {m.lower(): m for m in module_names}

        successes = []
        failures = []
        exceptions = []

        if len(module_names) == 1 and "all" in module_case_map:
            for name, _ in self.bot.module_handler.modules.iteritems():
                if name == "ModuleLoader":
                    continue
                try:
                    self.bot.module_handler.load_module(name)
                except Exception:
                    self.bot.logger.exception("Exception when reloading module {!r}".format(name))

            return ["all modules"], [], []

        for module_name in module_case_map.keys():

            if module_name == "moduleloader":
                failures.append("ModuleLoader (I can't reload myself)")

            else:
                try:
                    success = self.bot.module_handler.load_module(module_name)
                    if success:
                        successes.append(self.bot.module_handler.module_case_map[module_name])
                    else:
                        failures.append(module_case_map[module_name])
                except Exception:
                    exceptions.append(module_case_map[module_name])
                    self.bot.logger.exception("Exception when reloading module {!r}".format(module_case_map[module_name]))

        return successes, failures, exceptions

    def unload(self, module_names):
        module_case_map = {m.lower(): m for m in module_names}

        successes = []
        failures = []
        exceptions = []

        for module_name in module_case_map.keys():
            try:
                success = self.bot.module_handler.unload_module(module_name)
                if success:
                    successes.append(module_case_map[module_name])
                else:
                    failures.append(module_case_map[module_name])
            except Exception:
                exceptions.append(module_case_map[module_name])
                self.bot.logger.exception("Exception when unloading module {!r}".format(module_case_map[module_name]))

        return successes, failures, exceptions
