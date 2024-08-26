import ursina as u
from classes.SceneMod import SceneMod

def controls(key):
    if key == "space":
        for entity in u.scene.entities:
            if entity.getTag("type") == "grid":
                entity.toggle_visibility()

def Prefix(scene):
    entities = []
    entities.append(
        u.Entity(input=controls)
    )
    return entities

scene_mod = SceneMod(name="scene_select", prefix=Prefix)
