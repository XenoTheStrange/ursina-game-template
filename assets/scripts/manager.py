#!/usr/bin/python3

import os
import traceback
import importlib
import json
from scripts.logger import log
from classes.Scene import Scene
import ursina

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
    log.info("Loading scene: %s", name)
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
        scene_mod=importlib.import_module(f"mods.{folder}.scenes.{name}").scene_mod
        #if the scene exists in our list, this is a modification
        exstant_scene = get_scene(scene_mod.name)
        if exstant_scene:
            log.debug("Modifying scene: %s", exstant_scene.name)
            if scene_mod.prefix is not None:
                exstant_scene.mods_prefix.append(scene_mod.prefix)
            if scene_mod.postfix is not None:
                exstant_scene.mods_postfix.append(scene_mod.postfix)
            if scene_mod.loader is not None:
                exstant_scene.loader = scene_mod.loader
            if len(scene_mod.entities) > 0:
                exstant_scene.add_entities(scene_mod.entities)
        else:
            #If the scene doesn't already exist then the scene_mod object should be converted into a scene and added to the array
            new_scene=Scene(name=scene_mod.name, loader=scene_mod.loader)
            log.debug("Loaded unique modded scene: %s", scene_mod.name)
            globals()['Scenes'].append(new_scene)

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
    scene = "scene_select" if devmode else "language_select"
    change_scene(scene)
