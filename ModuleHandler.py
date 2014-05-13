import os, sys
from glob import glob
import GlobalVars


def LoadModule(name, loadAs=''):

    name = name.lower()

    cmdList = GetModuleDirList()
    cmdListCaseMap = {key.lower(): key for key in cmdList}

    if name not in cmdListCaseMap:
        return False

    alreadyExisted = False

    src = __import__('Modules.' + cmdListCaseMap[name], globals(), locals(), [])
    if loadAs != '':
        name = loadAs.lower()
    if name in GlobalVars.moduleCaseMapping:
        alreadyExisted = True
        properName = GlobalVars.moduleCaseMapping[name]
        del sys.modules['Modules.{0}'.format(properName)]
        for f in glob ('Modules/{0}.pyc'.format(properName)):
            os.remove(f)

    reload(src)

    components = cmdListCaseMap[name].split('.')
    for comp in components[:1]:
        src = getattr(src, comp)

    if alreadyExisted:
        print '-- {0} reloaded'.format(src.__name__)
    else:
        print '-- {0} loaded'.format(src.__name__)

    module = src.Module()

    GlobalVars.modules.update({cmdListCaseMap[name]:module})
    GlobalVars.moduleCaseMapping.update({name : cmdListCaseMap[name]})

    return True


def UnloadModule(name):

    if name.lower() in GlobalVars.moduleCaseMapping.keys():
        del GlobalVars.modules[GlobalVars.moduleCaseMapping[name]]
        del GlobalVars.moduleCaseMapping[name.lower()]
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