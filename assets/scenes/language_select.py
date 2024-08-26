import ursina as u
from scripts import manager
from classes.Scene import Scene

def select_language(lang):
    manager.Language = lang
    manager.change_scene("scene_select")

def loader(scene):
    entities = []
    font="fonts/Helvetica-Bold.ttf"
    text_scale = (10,12)
    #background stuff
    #entities.append(u.Entity(model="quad", scale=(2,2), color=u.color.black, position=(0,0,0), parent=u.camera.ui))
    entities.append(u.Entity(model="quad", scale=(1,1.1), position=(0,0,-0.5), texture="bg_language_select", parent=u.camera.ui))
    #buttons
    english_btn = u.Button(scale=(.175,.128), position=(0,0.075,-1), icon="english_flag", parent=u.camera.ui, on_click=lambda:select_language("English"))
    german_btn = u.Button(scale=(.175,.128), position=(0,-0.075,-1), icon="german_flag", parent=u.camera.ui, on_click=lambda:select_language("German"))
    #fix the icon size scaling
    german_btn.icon_entity.scale_y, german_btn.icon_entity.scale_x = (1.05,1.05)
    english_btn.icon_entity.scale_y, english_btn.icon_entity.scale_x = (1.05,1.05)
    entities.append(english_btn)
    entities.append(german_btn)
    entities.append(u.Text(text="Deutsch", scale=text_scale, parent=german_btn, position=(0.63,0.07,-1), color=u.color.black, font=font))
    entities.append(u.Text(text="Deutsch", scale=text_scale, parent=german_btn, position=(0.6,0.1,-2), font=font))
    entities.append(u.Text(text="English", scale=text_scale, parent=english_btn, position=(0.63,0.07,-1), color=u.color.black, font=font))
    entities.append(u.Text(text="English", scale=text_scale, parent=english_btn, position=(0.6,0.1,-2), font=font))
    #globals()['scene'].add_entities(entities)
    return entities

scene = Scene(name="language_select", loader=loader)
