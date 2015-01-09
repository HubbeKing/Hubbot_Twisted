import importlib
from glob import glob
import logging
import os
import sys

from twisted.internet import reactor

from hubbot.factory import HubbotFactory
from hubbot.channel import IRCChannel


class BotHandler:
    def __init__(self, config):
        self.botfactories = {}
        self.modules = {}
        self.moduleCaseMap = {}
        self.autoLoadModules()

        self.config = config
        for server in self.config["servers"]:
            port = self.config.serverItemWithDefault(server, "port", 6667)
            channels = self.config.serverItemWithDefault(server, "channels", [])
            self.startBotFactory(server, port, channels)
        reactor.run()

    def startBotFactory(self, server, port, channels):
        if server in self.botfactories:
            logging.warning("Bot for server \"{}\" was requested but one is already running!".format(server))
        else:
            logging.info("New bot for server \"{}\" requested, starting...".format(server))
            if type(channels) == list:
                chanObjects = {}
                for channel in channels:
                    chanObjects[channel] = IRCChannel(channel)
                botfactory = HubbotFactory(server, port, chanObjects, self)
            else:
                botfactory = HubbotFactory(server, port, channels, self)
            self.botfactories[server] = botfactory
            return True

    def stopBotFactory(self, server, quitmessage=None):
        if quitmessage is None:
            quitmessage = "ohok".encode("utf-8")
        if server not in self.botfactories:
            logging.warning("Bot for \"{}\" does not exist yet was asked to stop.".format(server))
        else:
            logging.info("Shutting down bot for server \"{}\"".format(server))
            self.botfactories[server].bot.Quitting = True
            for (name, module) in self.botfactories[server].bot.moduleHandler.modules.items():
                try:
                    module.onUnload()
                except:
                    logging.exception("Module \"{}\" threw an exception on unload.".format(name))
            try:
                self.botfactories[server].bot.quit(quitmessage)
            except:
                # this most likely means the bot in question has yet to establish a connection for whatever reason
                logging.exception("Bot for server \"{}\" could not quit properly!".format(server))
                self.botfactories[server].stopTrying()
            self.unregisterFactory(server)
            logging.info("Successfully shut down bot for server \"{}\"".format(server))

    def unregisterFactory(self, server):
        if server in self.botfactories:
            del self.botfactories[server]

        if len(self.botfactories) == 0:
            logging.info("No more bots are running, stopping reactor.")
            reactor.callLater(2.0, reactor.stop)

    def shutdown(self, quitmessage="Shutting down..."):
        logging.info("Shutdown command received, shutting down EVERYTHING.")
        for server in self.botfactories.keys():
            self.stopBotFactory(server, quitmessage.encode("utf-8"))

    def restart(self, quitmessage="Restarting..."):
        logging.info("Restart command received, going down for restart.")
        reactor.addSystemEventTrigger("after", "shutdown", lambda: os.execl(sys.executable, sys.executable, *sys.argv))
        self.shutdown(quitmessage.encode("utf-8"))

    def loadModule(self, name):
        name = name.lower()

        moduleList = self.getModuleDirList()
        moduleListCaseMap = {key.lower(): key for key in moduleList}

        if name not in moduleListCaseMap:
            logging.warning("Module \"{}\" was requested to load but it does not exist!".format(name))
            return False

        alreadyExisted = False

        if name in self.moduleCaseMap:
            self.unloadModule(name)
            alreadyExisted = True

        module = importlib.import_module("hubbot.Modules." + moduleListCaseMap[name])

        reload(module)

        class_ = getattr(module, moduleListCaseMap[name])

        self.modules.update({moduleListCaseMap[name]: class_})
        self.moduleCaseMap.update({name: moduleListCaseMap[name]})

        if alreadyExisted:
            logging.info('-- {} reloaded.'.format(module.__name__.split(".")[-1]))
        else:
            logging.info('-- {} loaded.'.format(module.__name__.split(".")[-1]))

        return True

    def unloadModule(self, name):
        if name.lower() in self.moduleCaseMap.keys():
            properName = self.moduleCaseMap[name.lower()]

            if len(self.botfactories) != 0:
                for botfactory in self.botfactories.values():
                    for moduleName in botfactory.bot.moduleHandler.modules.keys():
                        botfactory.bot.moduleHandler.disableModule(moduleName, check=False)

            del self.modules[self.moduleCaseMap[name.lower()]]
            del self.moduleCaseMap[name.lower()]
            del sys.modules["{}.{}".format("hubbot.Modules", properName)]
            for f in glob("{}/{}.pyc".format("hubbot.Modules", properName)):
                os.remove(f)
            logging.info("-- {} unloaded.".format(properName))
        else:
            logging.warning("Module \"{}\" was requested to unload but it is not loaded!".format(name))
            return False

        return True

    def checkModuleUsage(self, moduleName):
        loaded = False
        for botfactory in self.botfactories.values():
            if moduleName.lower() in botfactory.bot.moduleHandler.moduleCaseMap:
                loaded = True

        if not loaded:
            self.unloadModule(moduleName)

    def reloadModule(self, moduleName):
        moduleUsages = []
        if moduleName.lower() in self.moduleCaseMap:
            properName = self.moduleCaseMap[moduleName.lower()]
            for botfactory in self.botfactories.values():
                if moduleName in botfactory.bot.moduleHandler.moduleCaseMap.keys():
                    botfactory.bot.moduleHandler.disableModule(properName)
                    moduleUsages.append(botfactory)
            success = self.loadModule(properName)
            if len(moduleUsages) != 0:
                for botfactory in moduleUsages:
                    botfactory.bot.moduleHandler.enableModule(properName)
            return success

    def autoLoadModules(self):
        for module in self.getModuleDirList():
            try:
                self.loadModule(module)
            except:
                logging.exception("Exception when loading module \"{}\".".format(str(module)))

    def getModuleDirList(self):
        root = os.path.join('.', "hubbot", 'Modules')

        for item in os.listdir(root):
            if not os.path.isfile(os.path.join(root, item)):
                continue
            if not item.endswith('.py'):
                continue
            if item.startswith('__init__'):
                continue

            yield item[:-3]
