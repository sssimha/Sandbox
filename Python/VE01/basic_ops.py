'''
*******************************************************************************
Module DOCSTRING: Defines basic stuff used in general programming
*******************************************************************************
'''
import importlib
import pip
import pip._internal
import sys

calling_stack = None
calling_stack_globals = {}
calling_stack_ob_name = ''

print('')
print("Basic Ops Imported!")

try:
    print('append_root' in sys._getframe().f_back.f_globals)
except Exception as e:
    print('Error: ' + repr(e))
finally:
    print('======')
    str_stack = 'basic_ops code called'
    frm_level = 0
    frm = sys._getframe()
    calling_frame_num = 0
    calling_frame_found = False
    while frm is not None:
        str_stack = str_stack.replace('\n', '\n ')
        str_stack = repr(frm_level) + ': "' + frm.f_code.co_name + '" - '\
                    + repr(frm.f_code) + '\n\u2514' + str_stack
        if not calling_frame_found:
            if frm.f_code.co_name == '_find_and_load':
                calling_frame_num = frm_level + 1
                calling_frame_found = True
        frm = frm.f_back
        frm_level = frm_level + 1
    print(str_stack)
    print('======')

    calling_stack = sys._getframe(calling_frame_num)
    calling_stack_globals = sys._getframe(calling_frame_num).f_globals
    calling_stack_ob_name = sys._getframe(calling_frame_num).f_code.co_name

    for v in sys._getframe(calling_frame_num).f_globals.keys():
        print(v + ' '
        + ('***' if v == sys._getframe(calling_frame_num).f_code.co_name
            else ''))

__var1 = 'test'
__imported_mods = {}
__imported_members = {}
# Import Reload shortcut
rl = importlib.reload
# Pip Install shortcut
pipin = lambda pkg: pip._internal.main(['install', pkg, '--upgrade'])
# Error string constants
ERR_MODULE_ALREADY_LOADED = 'The module %s is already imported in the'\
                    + ' globals() provided. Try to load it into a different'\
                    + ' globals() or try to use the ReloadModuleLocal'\
                    + ' function OR set the refresh_module_if_imported'\
                    + ' parameter to True.'
ERR_EXISTING_MODULE_DIFFERENT = 'The module with the name %s in the'\
                    + ' globals() provided is not the same as the one trying'\
                    + ' to be imported. Try a different module alias'\
                    + ' by including a mod_alias parameter OR try to set'\
                    + ' the replace_module_if_different to True, to replace'\
                    + ' the existing module variable (NOT recommended unless'\
                    + ' you know what you\'re doing!).'
ERR_MODULE_MEMBER_DUPLICATION = 'Members [%s] of module %s could not'\
                    + ' be added since they are already defined in specified'\
                    + ' globals(). Use another globals() or set the'\
                    + ' override_existing_global_vars to True (NOT'\
                    + ' recommended).'
ERR_MODULE_IMPORT_FAILURE = 'Module %s was NOT imported successfully'
ERR_IMPORT_DUPLICATION = 'Module(s) [%s] imported within main module %s'\
                            + ' is/are not the same but the name imported'\
                            + ' by conflicts with another local variable'\
                            + ' that already exists in the globals()'\
                            + ' provided.'


def _lml(mod_name, gl=None, skip_dun=True, only_funcs=False,
                    replace_module_if_different=False,
                    refresh_module_if_imported=False,
                    override_existing_global_vars=False,
                    override_existing_global_mods=False, mod_alias=''):
    # Renamed from LoadModuleLocal to lml
    if gl is None:
        if sys._getframe().f_back is None:
            gl = globals()
        else:
            gl = sys._getframe().f_back.f_globals
    exec('__tmp_mod_import = __builtins__.__import__("' + mod_name + '")', gl)
    mod_name = mod_alias if mod_alias != '' else mod_name
    if mod_name in gl:
        if not refresh_module_if_imported:
            raise ImportError(ERR_MODULE_ALREADY_LOADED % mod_name)
        if (not eval(mod_name + ' == __tmp_mod_import', gl)) and\
                (not replace_module_if_different):
            raise ImportError(ERR_EXISTING_MODULE_DIFFERENT % mod_name)
        override_existing_global_vars = True
    exec('__builtins__.__import__("importlib").reload(__tmp_mod_import)', gl)
    exec(mod_name + ' = __tmp_mod_import', gl)
    exec('del __tmp_mod_import', gl)
    if mod_name not in gl:
        raise ImportError(ERR_MODULE_IMPORT_FAILURE % mod_name)
    error_names = []
    dup_named_mods = []
    err_dup_named_mods = []
    for name in eval(mod_name, gl).__dict__:
        if (((name[:2] != '__') or not skip_dun)
                and ((eval('callable(' + mod_name + '.' + name + ')', gl))
                or not only_funcs)):
            if name in gl:
                if eval('type(' + name + ').__name__ == "module"', gl):
                    dup_named_mods.append(name)
                else:
                    error_names.append(name)
    for dup_name in dup_named_mods:
        if eval(mod_name + '.' + dup_name + ' != ' + dup_name, gl):
            err_dup_named_mods.append(dup_name)
    if len(error_names) > 0 and not override_existing_global_vars:
        raise ImportError(ERR_MODULE_MEMBER_DUPLICATION
                            % (', '.join(error_names), mod_name))
    exec('\n'.join([(name + '=' + mod_name + '.' + name if (((name[:2] != '__')
            or not skip_dun) and ((eval('callable(' + mod_name + '.' + name
            + ')', gl)) or not only_funcs)) else '') for name in
            eval(mod_name, gl).__dict__]).lstrip()+'\n', gl)
