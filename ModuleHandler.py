import importlib
import os, sys, traceback
from glob import glob
from IRCResponse import ResponseType
import GlobalVars


class MessageHandler(object):

    def __init__(self, bot):
        self.bot = bot

    def sendResponse(self, response):
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
                elif response.Type == ResponseType.Do:
                    self.bot.describe(response.Target, response.Response.encode("utf-8"))
                elif response.Type == ResponseType.Notice:
                    self.bot.notice(response.Target, response.Response.encode("utf-8"))
                elif response.Type == ResponseType.Raw:
                    self.bot.sendLine(response.Response.encode("utf-8"))
            except Exception:
                print "Python Execution Error sending responses '{}': {}".format(responses, str(sys.exc_info()))
                traceback.print_tb(sys.exc_info()[2])


    def handleMessage(self, message):
        for name, module in GlobalVars.modules.iteritems():
            try:
                if module.hasAlias(message):
                    message = message.aliasedMessage()
                if module.shouldTrigger(message):
                    response = module.onTrigger(self.bot, message)
                    if response is None:
                        continue
                    if hasattr(response, "__iter__"):
                        for r in response:
                            self.sendResponse(r)
                    else:
                        self.sendResponse(response)
            except Exception:
                print "Python Execution Error in '{}': {}".format(module.__name__, str(sys.exc_info()))
                traceback.print_tb(sys.exc_info()[2])

def LoadModule(name, loadAs=''):

    name = name.lower()

    moduleList = GetModuleDirList()
    moduleListCaseMap = {key.lower(): key for key in moduleList}

    if name not in moduleListCaseMap:
        return False

    alreadyExisted = False

    if loadAs != '':
        name = loadAs.lower()
    if name in GlobalVars.moduleCaseMapping:
        UnloadModule(name)
        alreadyExisted = True

    #src = __import__('Modules.' + moduleListCaseMap[name], globals(), locals(), [])

    module = importlib.import_module("Modules." + moduleListCaseMap[name])

    reload(module)

    if alreadyExisted:
        print '-- {0} reloaded'.format(module.__name__)
    else:
        print '-- {0} loaded'.format(module.__name__)

    module = module.Module()

    GlobalVars.modules.update({moduleListCaseMap[name]:module})
    GlobalVars.moduleCaseMapping.update({name : moduleListCaseMap[name]})

    return True

def UnloadModule(name):

    if name.lower() in GlobalVars.moduleCaseMapping.keys():
        properName = GlobalVars.moduleCaseMapping[name.lower()]
        del GlobalVars.modules[GlobalVars.moduleCaseMapping[name]]
        del GlobalVars.moduleCaseMapping[name.lower()]
        del sys.modules["{}.{}".format("Modules", properName)]
        for f in glob("{}/{}.pyc".format("Modules", properName)):
            os.remove(f)
    else:
        return False

    return True

def AutoLoadModules():

    for module in GetModuleDirList():
        if module not in GlobalVars.nonDefaultModules:
            try:
                LoadModule(module)
            except Exception, x:
                print x.args

def GetModuleDirList():

    root = os.path.join('.', 'Modules')

    for item in os.listdir(root):
        if not os.path.isfile(os.path.join(root, item)):
            continue
        if not item.endswith('.py'):
            continue
        if item.startswith('__init__'):
            continue

        yield item[:-3]