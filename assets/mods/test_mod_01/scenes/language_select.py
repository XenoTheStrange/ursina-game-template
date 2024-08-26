import ursina as u
from classes.SceneMod import SceneMod

def Prefix(scene):
    return [
            u.Entity(
            position=(0,0.35,-2),
            scale=(0.3,0.3),
            parent=u.camera.ui,
            model="quad",
            texture="sun"
            )
        ]

scene_mod = SceneMod("language_select", prefix=Prefix)
