import ursina as u
from scripts.logger import error_handler

from scripts.mod_utils import after_hook

@error_handler
def toggle_grid(grid):
    if grid is not None:
        grid.toggle_visibility()

def controls(key, grid):
    if key == "space":
        toggle_grid(grid)

@after_hook("scenes.scene_select.loader")
def my_scene_postfix(entities_list, *args, **kwargs):
    print("BBBBBBB This should happen second")
    #After the scene is changed, if it was changed to scene_select, change the text of an existing entity and add a new one to the scene.
    grid=None
    #Iterate through the entities in the scene. This will fail if any item does not have a name
    for entity in entities_list:
        #Change the text of the scene_select button in the list
        if entity.name == "scene_select":
            entity.text = "Here"
        #Get a reference to the grid we want to toggle
        if entity.name == "grid.scenes":
            grid = entity
    #Add our controller to the entity list
    entities_list.append(
        u.Entity(name="tmod2.controller", input=lambda key: controls(key, grid))
        )
    return entities_list
