import ursina as u
from classes.SceneMod import SceneMod
from scripts.logger import error_handler

from scripts.manager import log
from ..classes.import_test import Test

@error_handler
def toggle_grid(scene):
    grid = scene.get_entity_named("grid.scenes")
    grid.toggle_visibility()

def controls(key, scene):
    if key == "space":
        toggle_grid(scene)

def Prefix(scene):
    entities = []
    entities.append(
        u.Entity(input=lambda key: controls(key, scene))
    )
    test = Test()
    #log.debug(test.speak())
    return entities

scene_mod = SceneMod(name="scene_select", prefix=Prefix)
