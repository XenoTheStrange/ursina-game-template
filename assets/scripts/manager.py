#!/usr/bin/python3

import os
import traceback
import importlib
import json
from scripts.logger import log

Scenes = []
Mods = []
CurrentScene = ""
Language = ""
devmode = False

def get_scene(name):
    if name == "all":
        return globals()['Scenes']
    for scene in globals()['Scenes']:
        if scene.name == name:
            return scene
    return False

def change_scene(name):
    """Destroy the current scene and load a new one"""
    global CurrentScene
    log.info("Trying to start scene: %s", name)
    try:
        scene = get_scene(name)
        if scene is False:
            log.error(f"Scene not found: {name}")
            return
        if CurrentScene != "":
            CurrentScene.destroy()
        CurrentScene = scene
        scene.create()
    except Exception as error:
        log.error(f"Exception occurred while changing scenes.\nScene name: {name}\nException: {error.__repr__() + ''.join(traceback.format_tb(error.__traceback__))}\n")

def load_scene(name):
    """Calls the loader for a scene, then returns it as an object without destroying the previous scene"""
    log.debug("Trying to sideload scene: %s", name)
    try:
        scene = get_scene(name)
        if scene is False:
            log.error(f"Scene not found: {name}")
            return
        scene.create()
        return scene
    except Exception as error:
        log.error(f"Exception occurred while changing scenes.\nScene name: {name}\nException: {error.__repr__() + ''.join(traceback.format_tb(error.__traceback__))}\n")

def get_folders(dir):
    return [folder for folder in os.listdir(dir) if os.path.isdir(f"{dir}/{folder}")]

def get_scene_names(dir):
    return [i.split(".")[:-1][0] for i in os.listdir(dir) if not i=="__init__.py" and ".py" in i]

def load_scenes():
    globals()['Scenes'] = []
    log.debug("Loading scenes from %s", "./scenes")
    scene_names = get_scene_names("./scenes")
    for name in scene_names:
        scene=importlib.import_module(f"scenes.{name}")
        globals()['Scenes'].append(scene.scene)
    log.debug(f"Scenes loaded: {', '.join([scene.name for scene in globals()['Scenes']])}")

def load_mod(path, folder):
    """Load one mod from a folder"""
    log.debug("Loading folder: %s", folder)
    #Get and save mod_info into global variable
    with open(f"{path}/{folder}/mod_info.json", "r", encoding="utf-8") as file:
        mod_info=json.loads(file.read())
        mod_info['location'] = f"{path}"
    globals()['Mods'].append(mod_info)
    #Get scenes from mod and attach their methods to the actual scenes, or add them to the scenes array if they're whole scenes
    scene_names = get_scene_names(f"{path}/{folder}/scenes")
    for name in scene_names:
        scene=importlib.import_module(f"mods.{folder}.scenes.{name}")
        #if the scene exists in our list, this is a modification
        exstant_scene = get_scene(scene.name)
        if exstant_scene:
            log.debug("Modifying scene: %s", exstant_scene.name)
            exstant_scene.mods_prefix.append(scene.Prefix)
            exstant_scene.mods_postfix.append(scene.Postfix)
            if scene.Replace_Loader():
                exstant_scene.loader = scene.loader
                log.debug("Loader replaced for scene: %s", exstant_scene.name)
        else:
            #If the scene doesn't already exist then this is a unique scene and it should be loaded
            log.debug("Loaded unique modded scene: %s", scene.name)
            globals()['Scenes'].append(scene)

def load_mods():
    globals()['Mods'] = []
    log.debug("Loading mods from ./mods")
    folders = get_folders("./mods")
    for folder in folders:
        load_mod(f"./mods", folder)
    log.debug(f"Mods loaded: {', '.join([mod['name'] for mod in globals()['Mods']])}")

def initialize():
    load_scenes()
    load_mods()
    #TODO add function to load mods, followed by modifying the Scene object template to interact with the mods list
    #TODO add debug statement for scene modifications loaded
    if devmode:
        change_scene("scene_select")
    else:
        change_scene("language_select")