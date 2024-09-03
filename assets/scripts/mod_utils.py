# mod_utils.py
import importlib
import json
import os, sys

from scripts.logger import log

# Dictionary to track hooks separately
modifications = {}

def get_function_from_string(function_path):
    """Helper function to get a function object from a string path."""
    module_name, func_name = function_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return module, func_name, func

def make_wrapped_func(original_func, hooks):
    def wrapped(*args, **kwargs):
        # Run before hooks
        for func in hooks['before']:
            func(*args, **kwargs)
        # Call the original function
        result = original_func(*args, **kwargs)
        # Run after hooks
        for func in hooks['after']:
            result = func(result, *args, **kwargs)
        return result
    return wrapped

def apply_modifications():
    for function_path, hooks in modifications.items():
        module, func_name, original_func = get_function_from_string(function_path)    
        wrapped_func = make_wrapped_func(original_func, hooks)
        setattr(module, func_name, wrapped_func)
    log.debug("Finished applying modifications")

def before_hook(function_path):
    """Decorator to insert code before the specified function."""
    def decorator(hook_func):
        if function_path not in modifications:
            modifications[function_path] = {'before': [], 'after':[], 'override':[]}
        modifications[function_path]['before'].append(hook_func)
        return hook_func
    return decorator

def after_hook(function_path):
    """Decorator to insert code after the specified function."""
    def decorator(hook_func):
        if function_path not in modifications:
            modifications[function_path] = {'before': [], 'after':[], 'override':[]}
        modifications[function_path]['after'].append(hook_func)
        return hook_func
    return decorator

def override_hook(function_path):
    """Decorator to completely replace the specified function."""
    def decorator(hook_func):
        if function_path not in modifications:
            modifications[function_path] = {'before': [], 'after':[], 'override':[]}
        module, func_name, _ = get_function_from_string(function_path)
        modifications[function_path]['override'] = [hook_func]
        return hook_func
    return decorator

def load_mod(path, folder):
    """Load one mod from a folder"""
    log.debug("Loading folder: %s", folder)
    #Get and save mod_info into global variable
    with open(f"{path}/{folder}/mod_info.json", "r", encoding="utf-8") as file:
        mod_info=json.loads(file.read())
        mod_info['location'] = path
    globals()['Mods'].append(mod_info)
    #Get scenes from mod and attach their methods to the actual scenes, or add them to the scenes array if they're whole scenes
    importlib.import_module(f"mods.{folder}.main")

def load_all_mods():
    from scripts.manager import get_folders
    #add the mods dir to the path so they can use relative imports
    mods_dir = os.path.abspath('./mods')
    sys.path.insert(0, mods_dir)
    globals()['Mods'] = []
    log.debug("Loading mods from ./mods")
    folders = get_folders("./mods")
    for folder in folders:
        load_mod("./mods", folder)
    apply_modifications()
    log.debug(f"Mods loaded: {', '.join([mod['name'] for mod in globals()['Mods']])}")

