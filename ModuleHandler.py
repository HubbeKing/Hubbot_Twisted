import importlib
import os, sys
from glob import glob
import GlobalVars


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