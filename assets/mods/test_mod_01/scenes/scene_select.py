import ursina as u
from scripts.mod_utils import after_hook
from scripts.manager import devmode
from classes.draggable_entity import Draggable_Entity

def set_stuff(entity, draggable):
    entity.position = draggable.position
    draggable.scale = entity.scale

def handle_grow_shrink(key, entity, scale):
    if key == "scroll up":
        entity.scale+=scale
    if key == "scroll down":
        entity.scale+=(-scale[0], -scale[1])


@after_hook("scenes.scene_select.loader")
def stacking_wrappers_oh_my(entities_list, *args, **kwargs):
    if devmode:
        print("[TEST_MOD_01] This should happen first")
    button = u.Entity(
        name="btn.dragcat", model="quad", scale=(0.2,0.2), position=(-0.6,0,-1), 
        texture="drag-cat", parent=u.camera.ui
    )
    draggable_button = Draggable_Entity(parent=u.camera.ui, scale=button.scale, position=button.position+(0,0,-1), color=u.hsv(0,0,0,a=0))
    button.update = lambda:set_stuff(button, draggable_button)
    draggable_button.on_click = lambda: print(
        f"{button.__class__.__name__}(scale=({round(button.scale.x,2)},{round(button.scale.y,2)},{round(button.scale.z,2)}), position=({round(button.position.x,2)},{round(button.position.y,2)},{round(button.position.z,2)}), texture='{button.texture.name.split('.')[0]}', parent={button.parent})"
        )
    button.input = lambda key: handle_grow_shrink(key, button, (0.01,0.01))
    entities_list.append(draggable_button)
    entities_list.append(button)
    return entities_list
