import importlib
from glob import glob
import operator
import os
import sys

from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleAccessLevel


class ModuleHandler(object):

    def __init__(self, bot):
        """
        @type bot: hubbot.bot.Hubbot
        """
        self.bot = bot
        self.modules = {}
        self.module_case_map = {}
        self.mapped_triggers = {}
        self.modules_to_load = bot.config.item_with_default("modules", ["all"])

    def send_response(self, response):
        """
        @type response: hubbot.reponse.IRCResponse || list || tuple
        """
        responses = []

        if hasattr(response, "__iter__"):
            for r in response:
                if r is None or r.response is None or r.response == "":
                    continue
                responses.append(r)
        elif response is not None and response.response is not None and response.response != "":
            responses.append(response)

        for response in responses:
            try:
                if response.type == ResponseType.SAY:
                    self.bot.msg(response.target.encode("utf-8"), response.response.encode("utf-8"))
                    self.bot.logger.info(u'{} | <{}> {}'.format(response.target, self.bot.nickname, response.response))
                elif response.type == ResponseType.DO:
                    self.bot.describe(response.target.encode("utf-8"), response.response.encode("utf-8"))
                    self.bot.logger.info(u'{} | *{} {}*'.format(response.target, self.bot.nickname, response.response))
                elif response.type == ResponseType.NOTICE:
                    self.bot.notice(response.target.encode("utf-8"), response.response.encode("utf-8"))
                    self.bot.logger.info(u'{} | [{}] {}'.format(response.target, self.bot.nickname, response.response))
                elif response.type == ResponseType.RAW:
                    self.bot.logger.info(u"Sent raw {!r}".format(response.response))
                    self.bot.sendLine(response.response.encode("utf-8"))
            except:
                self.bot.logger.exception("Python Execution Error sending responses {!r}".format(responses))

    def handle_message(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        for module in sorted(self.modules.values(), key=operator.attrgetter("priority")):
            try:
                if module.should_trigger(message):
                    if module.access_level == ModuleAccessLevel.ADMINS and len(self.bot.admins) != 0 and message.user.name not in self.bot.admins:
                        self.bot.logger.warning("User {!r} tried to use {!r} but was denied access.".format(message.user.name, message.command))
                        self.send_response(IRCResponse(ResponseType.SAY, "Only my admins may use that!", message.reply_to))
                    elif len(self.bot.ignores) == 0 or message.user.name not in self.bot.ignores:
                        self.bot.logger.debug("Responding to message {!r}".format(message.message_string))
                        response = module.on_trigger(message)
                        self.send_response(response)

            except Exception as ex:
                self.bot.logger.exception("Python Execution Error in {!r}".format(module.__class__.__name__))
                self.send_response(IRCResponse(ResponseType.SAY, "Python Execution Error - {!r}".format(ex.message), message.reply_to))

    def load_module(self, module_name):
        module_name = module_name.lower()

        module_list = ModuleHandler.get_all_modules()
        module_list_case_map = {key.lower(): key for key in module_list}

        if module_name not in module_list_case_map:
            self.bot.logger.warning("Module {!r} was requested to load but does not exist!")
            return False

        already_loaded = False

        if module_name in self.module_case_map:
            self.unload_module(module_name)
            already_loaded = True

        module = importlib.import_module("hubbot.Modules." + module_list_case_map[module_name])

        reload(module)

        class_ = getattr(module, module_list_case_map[module_name])

        if already_loaded:
            self.bot.logger.debug("Module {!r} reloaded.".format(module.__name__))
        else:
            self.bot.logger.debug("Module {!r} loaded.".format(module.__name__))

        constructed_module = class_(self.bot)

        self.modules.update({module_list_case_map[module_name]: constructed_module})
        self.module_case_map.update({module_name: module_list_case_map[module_name]})

        if hasattr(constructed_module, "triggers"):
            for trigger in constructed_module.triggers:
                self.mapped_triggers[trigger] = constructed_module

        constructed_module.on_load()

        return True

    def unload_module(self, module_name):
        if module_name.lower() in self.module_case_map.keys():
            proper_name = self.module_case_map[module_name.lower()]

            if hasattr(self.modules[proper_name], "triggers"):
                for trigger in self.modules[proper_name].triggers:
                    del self.mapped_triggers[trigger]

            self.modules[proper_name].on_unload()

            del self.modules[proper_name]
            del self.module_case_map[module_name.lower()]
            del sys.modules["{}.{}".format("hubbot.Modules", proper_name)]
            for f in glob("{}/{}.pyc".format("hubbot.Modules", proper_name)):
                os.remove(f)
            self.bot.logger.debug("Module {!r} unloaded.".format(proper_name))
        else:
            self.bot.logger.warning("Module {!r} was requested to unload but is not loaded!".format(module_name))
            return False

        return True

    def load_add_modules(self):
        modules_to_load = []
        for module_name in self.modules_to_load:
            if module_name.lower() == "all":
                for module in ModuleHandler.get_all_modules():
                    modules_to_load.append(module)
            elif module_name[0] != "-":
                modules_to_load.append(module_name)
            else:
                modules_to_load.remove(module_name[1:])

        self.bot.logger.info("Loading modules...")
        for module in modules_to_load:
            try:
                self.load_module(module)
            except:
                self.bot.logger.exception("Exception when loading module {!r}".format(str(module)))
        self.bot.logger.info("Module loading complete.")

    @staticmethod
    def get_all_modules():
        root = os.path.join(".", "hubbot", "Modules")

        for item in os.listdir(root):
            if not os.path.isfile(os.path.join(root, item)):
                continue
            if not item.endswith(".py"):
                continue
            if item.startswith("__init__"):
                continue
            yield item[:-3]
