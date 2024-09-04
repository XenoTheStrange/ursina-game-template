import ursina as u

from scripts import manager
from scripts.mod_utils import after_hook
from classes.buttons import language_flag
from classes.Scene import Scene

@after_hook("scenes.title.loader")
def my_scene_postfix(entities_list, *args, **kwargs):
    entities_list.append(
        language_flag(name="mod_menu",text="Mod Menu", scale=(0.2,0.1), position=(0,0,-1), texture="german_flag", onclick=(lambda: manager.change_scene("mod_menu"), None), parent=u.camera.ui)
    )
    return entities_list

