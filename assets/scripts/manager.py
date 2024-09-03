#!/usr/bin/python3

import os
import sys
import traceback
import importlib
import json
from scripts.logger import log
from scripts import mod_utils
from classes.Scene import Scene
import ursina

Scenes = []
Mods = []
Cursor = None
cursor_default_texture = "cursor_default"
CurrentScene = None
Language = ""
devmode = False

def get_scene_names(dir):
    return [i.split(".")[:-1][0] for i in os.listdir(dir) if not i=="__init__.py" and ".py" in i]
def get_folders(dir):
    return [folder for folder in os.listdir(dir) if os.path.isdir(f"{dir}/{folder}")]
    
def get_scene(name):
    if name is True:
        return globals()['Scenes']
    for scene in globals()['Scenes']:
        if scene.name == name:
            return scene
    return False

def add_scene(scene):
    globals()['Scenes'].append(scene)

def change_scene(name):
    """Destroy the current scene and load a new one"""
    global CurrentScene
    globals()["Cursor"].texture = globals()["cursor_default_texture"]
    log.info("Loading scene: %s", name)
    try:
        scene = get_scene(name)
        if scene is False:
            log.error(f"Scene not found: {name}")
            return
        if CurrentScene != None:
            CurrentScene.destroy()
        CurrentScene = scene
        scene.load()
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
        scene.load()
        return scene
    except Exception as error:
        log.error(f"Exception occurred while changing scenes.\nScene name: {name}\nException: {error.__repr__() + ''.join(traceback.format_tb(error.__traceback__))}\n")

def load_all_scenes():
    #globals()['Scenes'] = []
    log.debug("Loading scenes from %s", "./scenes")
    scene_names = get_scene_names("./scenes")
    for name in scene_names:
        scene=importlib.import_module(f"scenes.{name}")
        globals()['Scenes'].append(scene.get_scene())
    log.debug(f"Scenes loaded: {', '.join([scene.name for scene in globals()['Scenes']])}")

def hide_cursor_if_outside():
    global Cursor
    if ursina.mouse.is_outside:
        if Cursor.visible:
            Cursor.visible = False
    elif not Cursor.visible:
        Cursor.visible = True

def initialize():
    globals()['Cursor'] = ursina.Cursor(name="game_cursor", texture="cursor_default", eternal=True)
    cursor_hider = ursina.Entity("cursor_hider").update = hide_cursor_if_outside
    ursina.mouse.visible = False
    mod_utils.load_all_mods() #we MUST load mod info _before_ the scenes and stuff are loaded into memory.
    load_all_scenes()
    scene = "scene_select" if devmode else "language_select"
    change_scene(scene)
