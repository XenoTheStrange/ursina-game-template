import ursina as u
from scripts import manager
from classes.Scene import Scene

def loader(scene):
    bg = u.Entity(parent = u.camera.ui, model="quad", scale=(1,1), color=u.color.black)
    window = u.Entity(parent = u.camera.ui, model="quad", scale=(0.95,1), color=u.color.hsv(0,0,0.1))
    border = u.Entity(parent = u.camera.ui, model="quad", scale=(0.01,1), color=u.color.black)
    return [bg, window]

manager.add_scene(
    Scene(name="mod_menu", loader=loader)
    )