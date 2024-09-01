import ursina as u
from scripts import manager
from scripts.logger import log
from classes.Scene import Scene

def loader(scene):
    return [
        u.Entity(name="img.bg", model="quad", scale=(1,1.1), position=(0,0,-0.5), texture="bg_title", parent=u.camera.ui),
        u.Entity(name="img.title_sonny", model="quad", scale=(0.88, 0.44), position=(0,0.22,-1), texture="title_sonny_03", parent=u.camera.ui)
    ]

def get_scene():
    return Scene("title", loader=loader)
