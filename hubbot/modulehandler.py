import multiprocessing
import operator
import os
import sys

from twisted.internet import threads

from hubbot.response import IRCResponse, ResponseType
from hubbot.moduleinterface import ModuleAccessLevel


class ModuleHandler(object):

    def __init__(self, bot):
        """
        @type bot: hubbot.bot.Hubbot
        """
        self.bot = bot
        self.manager = multiprocessing.Manager()
        self.modules = self.manager.dict()
        self.moduleCaseMap = self.manager.dict()
        self.mappedTriggers = self.manager.dict()
        self.modulesToLoad = bot.bothandler.config.serverItemWithDefault(self.bot.server, "modulesToLoad", ["all"])

    def sendResponse(self, response):
        """
        @type response: hubbot.response.IRCResponse || list
        """
        responses = []

        if hasattr(response, "__iter__"):
            for r in response:
                if r is None or r.Response is None or r.Response == "":
                    continue
                responses.append(r)
        elif response is not None and response.Response is not None and response.Response != "":
            responses.append(response)

        for response in responses:
            try:
                if response.Type == ResponseType.Say:
                    self.bot.msg(response.Target.encode("utf-8"), response.Response.encode("utf-8"))
                    self.bot.logger.info(u'{} | <{}> {}'.format(response.Target, self.bot.nickname, response.Response))
                elif response.Type == ResponseType.Do:
                    self.bot.describe(response.Target.encode("utf-8"), response.Response.encode("utf-8"))
                    self.bot.logger.info(u'{} | *{} {}*'.format(response.Target, self.bot.nickname, response.Response))
                elif response.Type == ResponseType.Notice:
                    self.bot.notice(response.Target.encode("utf-8"), response.Response.encode("utf-8"))
                    self.bot.logger.info(u'{} | [{}] {}'.format(response.Target, self.bot.nickname, response.Response))
                elif response.Type == ResponseType.Raw:
                    self.bot.logger.info(u"Sent raw {!r}".format(response.Response))
                    self.bot.sendLine(response.Response.encode("utf-8"))
            except Exception:
                self.bot.logger.exception("Python Execution Error sending responses {!r}".format(responses))

    def handleMessage(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        for module in sorted(self.modules.values(), key=operator.attrgetter("priority")):
            try:
                if module.shouldTrigger(message):
                    if module.accessLevel == ModuleAccessLevel.ADMINS and len(self.bot.admins) != 0 and message.User.Name not in self.bot.admins:
                        self.bot.logger.info("User {} tried to use {} but was denied access.".format(message.User.Name, message.Command))
                        self.sendResponse(IRCResponse(ResponseType.Say, "Only my admins can use {}!".format(message.Command), message.ReplyTo))
                    elif len(self.bot.ignores) == 0 or message.User.Name not in self.bot.ignores:
                        if not module.runInThread:
                            response = module.onTrigger(message)
                            self.sendResponse(response)
                        else:
                            d = threads.deferToThread(self._handleInThread, module, message)
            except Exception:
                self.bot.logger.exception("Python Execution Error in {!r}".format(module.__class__.__name__))

    def _handleInThread(self, module, message):
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=self._threadTriggerModule, args=(module, message, q))
        p.start()
        p.join(timeout=module.timeout)
        if p.is_alive() and message.Command != "":
            self.sendResponse(IRCResponse(ResponseType.Say,
                                          "Command {!r} timed out and was killed.".format(message.Command),
                                          message.ReplyTo))
            os.kill(p.pid, 9)
            self.bot.logger.warning("Module {!r} timed out on execution.".format(module.__class__.__name__))
        elif p.is_alive():
            os.kill(p.pid, 9)
            self.bot.logger.warning("Module {!r} timed out on execution.".format(module.__class__.__name__))
        else:
            self.sendResponse(q.get())

    def _threadTriggerModule(self, module, message, queue):
        response = module.onTrigger(message)
        queue.put(response)

    def enableModule(self, moduleName):
        moduleName = moduleName.lower()

        moduleList = self.getModuleDirList()
        moduleListCaseMap = {key.lower(): key for key in moduleList}

        if moduleName not in moduleListCaseMap:
            self.bot.logger.warning("Module {!r} was requested to enable but it is not loaded!".format(moduleName))
            return False

        if moduleName in self.moduleCaseMap:
            self.bot.logger.warning("Module {!r} was requested to enable but it is already enabled!".format(moduleName))
            return False

        module = sys.modules["{}.{}".format("hubbot.Modules", moduleListCaseMap[moduleName])]

        class_ = getattr(module, moduleListCaseMap[moduleName])

        constructedModule = class_(self.bot)

        self.modules.update({moduleListCaseMap[moduleName]: constructedModule})
        self.moduleCaseMap.update({moduleName: moduleListCaseMap[moduleName]})
        constructedModule.onEnable()

        # map module triggers
        for trigger in constructedModule.triggers:
            self.mappedTriggers[trigger] = constructedModule

        self.bot.logger.debug('-- {} enabled.'.format(self.moduleCaseMap[moduleName]))
        return True

    def disableModule(self, moduleName, check=True):
        if moduleName.lower() in self.moduleCaseMap.keys():
            properName = self.moduleCaseMap[moduleName.lower()]
            try:
                # unmap module triggers
                for trigger in self.modules[properName].triggers:
                    del self.mappedTriggers[trigger]
                self.modules[properName].onDisable()
            except:
                self.bot.logger.exception("Exception when disabling module {}".format(moduleName))
                raise
            finally:
                del self.modules[self.moduleCaseMap[moduleName.lower()]]
                del self.moduleCaseMap[moduleName.lower()]
                self.bot.logger.debug("-- {} disabled.".format(properName))
                if check:
                    self.bot.bothandler.unloadModuleIfNotEnabled(properName)
        else:
            self.bot.logger.warning("Module {!r} was requested to disable but it is not enabled!".format(moduleName))
            return False

        return True

    def enableAllModules(self):
        modulesToLoad = []
        for moduleName in self.modulesToLoad:
            if moduleName.lower() == "all":
                for module in self.getModuleDirList():
                    modulesToLoad.append(module)
            elif moduleName[0] != "-":
                modulesToLoad.append(moduleName)
            else:
                modulesToLoad.remove(moduleName[1:])

        for module in modulesToLoad:
            try:
                self.enableModule(module)
            except Exception:
                self.bot.logger.exception("Exception when enabling {!r}".format(str(module)))

    def getModuleDirList(self):
        return self.bot.bothandler.modules.keys()
