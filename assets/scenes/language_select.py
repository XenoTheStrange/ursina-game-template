import ursina as u
from scripts import manager
from classes.Scene import Scene
from classes.buttons import glow_button

def select_language(lang):
    manager.Language = lang
    manager.change_scene("scene_select")

def loader(scene):
    return [
        #entities.append(u.Entity(model="quad", scale=(2,2), color=u.color.black, position=(0,0,0), parent=u.camera.ui))
        u.Entity(name="img.bg", model="quad", scale=(1,1.1), position=(0,0,-0.5), texture="bg_language_select", parent=u.camera.ui),
        #buttons
        glow_button(name="btn.lang.english", text="English", scale=(.175,.128), position=(0,0.075,-1), texture="english_flag", parent=u.camera.ui, onclick=(lambda:select_language("English"), None)),
        glow_button(name="btn.lang.german", text="German", scale=(.175,.128), position=(0,-0.075,-1), texture="german_flag", parent=u.camera.ui, onclick=(lambda:select_language("German"), None))
    ]

scene = Scene(name="language_select", loader=loader)
