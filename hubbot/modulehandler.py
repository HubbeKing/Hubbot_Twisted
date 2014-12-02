import importlib
import os
import sys
import traceback
from glob import glob
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
        self.moduleCaseMapping = {}
        self.mappedTriggers = {}
        self.nonDefaultModules = bot.bothandler.config.serverItemWithDefault(bot.server, "nonDefaultModules", ["Roll"])

    def sendResponse(self, response):
        """
        @type response: hubbot.response.IRCResponse
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
                    self.bot.msg(response.Target, response.Response.encode("utf-8"))
                    self.bot.log(u'<{0}> {1}'.format(self.bot.nickname, response.Response), response.Target)
                elif response.Type == ResponseType.Do:
                    self.bot.describe(response.Target, response.Response.encode("utf-8"))
                    self.bot.log(u'*{0} {1}*'.format(self.bot.nickname, response.Response), response.Target)
                elif response.Type == ResponseType.Notice:
                    self.bot.notice(response.Target, response.Response.encode("utf-8"))
                    self.bot.log(u'[{0}] {1}'.format(self.bot.nickname, response.Response), response.Target)
                elif response.Type == ResponseType.Raw:
                    self.bot.sendLine(response.Response.encode("utf-8"))
            except Exception:
                print "Python Execution Error sending responses '{}': {}".format(responses, str(sys.exc_info()))
                traceback.print_tb(sys.exc_info()[2])

    def handleMessage(self, message):
        """
        @type message: hubbot.message.IRCMessage
        """
        for (name, module) in self.modules.items():
            try:
                if module.shouldTrigger(message):
                    if module.accessLevel != ModuleAccessLevel.ANYONE and message.User.Name not in self.bot.admins:
                        self.sendResponse(IRCResponse(ResponseType.Say, "Only my admins can use {}!".format(message.Command), message.ReplyTo))
                    elif message.User.Name not in self.bot.ignores:
                        if not module.runInThread:
                            response = module.onTrigger(message)
                            self.sendResponse(response)
                        else:
                            d = threads.deferToThread(module.onTrigger, message)
                            d.addCallback(self.sendResponse)
            except Exception:
                print "Python Execution Error in '{}': {}".format(name, str(sys.exc_info()))
                traceback.print_tb(sys.exc_info()[2])

    def LoadModule(self, name):
        name = name.lower()

        moduleList = self.GetModuleDirList()
        moduleListCaseMap = {key.lower(): key for key in moduleList}

        if name not in moduleListCaseMap:
            return False

        alreadyExisted = False

        if name in self.moduleCaseMapping:
            self.UnloadModule(name)
            alreadyExisted = True

        module = importlib.import_module("hubbot.Modules." + moduleListCaseMap[name])

        reload(module)

        class_ = getattr(module, moduleListCaseMap[name])

        if alreadyExisted:
            print '-- {0} reloaded ({1})'.format(module.__name__, self.bot.server)
        else:
            print '-- {0} loaded ({1})'.format(module.__name__, self.bot.server)

        constructedModule = class_(self.bot)

        self.modules.update({moduleListCaseMap[name]:constructedModule})
        self.moduleCaseMapping.update({name : moduleListCaseMap[name]})
        constructedModule.onLoad()

        # map module triggers
        for trigger in constructedModule.triggers:
            self.mappedTriggers[trigger] = constructedModule

        return True

    def UnloadModule(self, name):
        if name.lower() in self.moduleCaseMapping.keys():
            properName = self.moduleCaseMapping[name.lower()]

            # unmap module triggers
            for trigger in self.modules[properName].triggers:
                del self.mappedTriggers[trigger]

            self.modules[properName].onUnload()

            del self.modules[self.moduleCaseMapping[name.lower()]]
            del self.moduleCaseMapping[name.lower()]
            del sys.modules["{}.{}".format("hubbot.Modules", properName)]
            for f in glob("{}/{}.pyc".format("hubbot.Modules", properName)):
                os.remove(f)
        else:
            return False

        return True

    def AutoLoadModules(self):
        for module in self.GetModuleDirList():
            if module not in self.nonDefaultModules:
                try:
                    self.LoadModule(module)
                except Exception, x:
                    print x.args

    def GetModuleDirList(self):
        root = os.path.join('.', 'Modules')

        for item in os.listdir(root):
            if not os.path.isfile(os.path.join(root, item)):
                continue
            if not item.endswith('.py'):
                continue
            if item.startswith('__init__'):
                continue

            yield item[:-3]
