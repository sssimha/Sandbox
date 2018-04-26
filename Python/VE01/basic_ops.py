'''
*******************************************************************************
Module DOCSTRING: Defines basic stuff used in general programming
*******************************************************************************
'''
import importlib
import pip
import pip._internal

__var1 = 'test'
# Import Reload shortcut
rl = importlib.reload
# Pip Install shortcut
pipin = lambda pkg: pip._internal.main(['install', pkg, '--upgrade'])


def LoadModuleLocal(mod_name, gl=globals(), skip_dun=True, only_funcs=False):
    exec('import ' + mod_name, gl)
    # print(globals())
    try:
        print(eval(mod_name, gl))
    except:
        print('error')
    exec('\n'.join([(name + '=' + mod_name + '.'+name if (((name[:2] != '__')
            or not skip_dun) and ((eval('callable(' + mod_name + '.' + name
            + ')', gl)) or not only_funcs)) else '') for name in
            eval(mod_name, gl).__dict__]).lstrip()+'\n', gl)
