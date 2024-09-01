# mod_utils.py
import importlib
import json
import os, sys

from classes import Scene
from scripts.logger import log
#cannot directly import scripts.manager otherwise it causes a circular import


# This will keep track of function modifications
modifications = {}

def get_function_from_string(function_path):
    """Helper function to get a function object from a string path."""
    module_name, func_name = function_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return module, func_name, func

def apply_modifications():
    """Apply all recorded modifications in the order they were added."""
    for function_path, hooks in modifications.items():
        module, func_name, original_func = get_function_from_string(function_path)
        
        # Apply hooks in reverse order
        for hook_func in reversed(hooks):
            wrapped_func = hook_func(original_func)
        
        setattr(module, func_name, wrapped_func)
        replaced_func = getattr(module, func_name)
        print(f"{function_path} is replaced: {replaced_func is wrapped_func}")

def before_hook(function_path):
    """Decorator to insert code before the specified function."""
    def decorator(hook_func):
        print(f"[MOD_LOADER] Applying before_hook to {function_path}")
        if function_path not in modifications:
            modifications[function_path] = []
        
        def wrapper(original_func):
            def wrapped(*args, **kwargs):
                hook_func(*args, **kwargs)
                return original_func(*args, **kwargs)
            return wrapped
        
        modifications[function_path].append(wrapper)
        return hook_func
    return decorator

def after_hook(function_path):
    """Decorator to insert code after the specified function."""
    def decorator(hook_func):
        print(f"[MOD_LOADER] Applying after_hook to {function_path}")
        if function_path not in modifications:
            modifications[function_path] = []
        
        def wrapper(original_func):
            def wrapped(*args, **kwargs):
                result = original_func(*args, **kwargs)
                return hook_func(result, *args, **kwargs)
            return wrapped
        
        modifications[function_path].append(wrapper)
        return hook_func
    return decorator

def override_hook(function_path):
    """Decorator to completely replace the specified function."""
    def decorator(hook_func):
        print(f"[MOD_LOADER] Applying override_hook to {function_path}")
        if function_path not in modifications:
            modifications[function_path] = []
        
        modifications[function_path].append(lambda _: hook_func)
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