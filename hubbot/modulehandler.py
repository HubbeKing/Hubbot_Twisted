import operator
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
        self.modules = {}
        self.moduleCaseMap = {}
        self.mappedTriggers = {}
        self.modulesToLoad = bot.bothandler.config.itemWithDefault("modulesToLoad", ["all"])

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
                    self.bot.logger.info(u"Sent raw \"{}\"".format(response.Response))
                    self.bot.sendLine(response.Response.encode("utf-8"))
            except Exception:
                self.bot.logger.exception("Python Execution Error sending responses \"{}\"".format(responses))

    def handleMessage(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        for module in sorted(self.modules.values(), key=operator.attrgetter("priority")):
            try:
                if module.shouldTrigger(message):
                    if module.accessLevel != ModuleAccessLevel.ANYONE and len(self.bot.admins) != 0 and message.User.Name not in self.bot.admins:
                        self.bot.logger.info("User {} tried to use {} but was denied access.".format(message.User.Name, message.Command))
                        self.sendResponse(IRCResponse(ResponseType.Say, "Only my admins can use {}!".format(message.Command), message.ReplyTo))
                    elif message.User.Name not in self.bot.ignores:
                        if not module.runInThread:
                            response = module.onTrigger(message)
                            self.sendResponse(response)
                        else:
                            d = threads.deferToThread(module.onTrigger, message)
                            d.addCallback(self.sendResponse)
            except Exception:
                self.bot.logger.exception("Python Execution Error in \"{}\"".format(module.__class__.__name__))

    def loadModule(self, moduleName):
        moduleName = moduleName.lower()

        moduleList = self.getModuleDirList()
        moduleListCaseMap = {key.lower(): key for key in moduleList}

        if moduleName not in moduleListCaseMap:
            self.bot.logger.warning("Module \"{}\" was requested to load but it does not exist!".format(moduleName))
            return False

        alreadyExisted = False
        reloaded = False

        if moduleName in self.moduleCaseMap:
            reloaded = self.bot.bothandler.loadModule(moduleName)
            if reloaded:
                self.reloadModule(moduleName)
            alreadyExisted = True

        module = sys.modules["{}.{}".format("hubbot.Modules", moduleListCaseMap[moduleName])]

        class_ = getattr(module, moduleListCaseMap[moduleName])

        constructedModule = class_(self.bot)

        self.modules.update({moduleListCaseMap[moduleName]: constructedModule})
        self.moduleCaseMap.update({moduleName: moduleListCaseMap[moduleName]})
        constructedModule.onLoad()

        # map module triggers
        for trigger in constructedModule.triggers:
            self.mappedTriggers[trigger] = constructedModule

        if not alreadyExisted:
            self.bot.logger.info('-- {} enabled.'.format(self.moduleCaseMap[moduleName]))
        if alreadyExisted and not reloaded:
            self.bot.logger.warning("Module \"{}\" failed to reload!".format(self.moduleCaseMap[moduleName]))
        return True

    def reloadModule(self, moduleName):
        properName = self.moduleCaseMap[moduleName.lower()]
        for botfactory in self.bot.bothandler.botfactories.values():
            wasLoaded = False
            if moduleName in botfactory.bot.moduleHandler.moduleCaseMap.keys():
                wasLoaded = True
                botfactory.bot.moduleHandler.unloadModule(moduleName)
            if wasLoaded:
                module = sys.modules["{}.{}".format("hubbot.Modules", properName)]
                class_ = getattr(module, properName)
                constructedModule = class_(botfactory.bot)
                botfactory.bot.moduleHandler.modules.update({properName: constructedModule})
                constructedModule.onLoad()
        return True

    def unloadModule(self, moduleName):
        if moduleName.lower() in self.moduleCaseMap.keys():
            properName = self.moduleCaseMap[moduleName.lower()]

            # unmap module triggers
            for trigger in self.modules[properName].triggers:
                del self.mappedTriggers[trigger]

            self.modules[properName].onUnload()

            del self.modules[self.moduleCaseMap[moduleName.lower()]]
            del self.moduleCaseMap[moduleName.lower()]
            self.bot.logger.info("-- {} disabled.".format(properName))
            self.bot.bothandler.checkModuleUsage(properName)
        else:
            self.bot.logger.warning("Module \"{}\" was requested to unload but it is not loaded!".format(moduleName))
            return False

        return True

    def autoLoadModules(self):
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
                self.loadModule(module)
            except Exception:
                self.bot.logger.exception("Exception when enabling \"{}\"".format(str(module)))

    def getModuleDirList(self):
        return self.bot.bothandler.modules.keys()
