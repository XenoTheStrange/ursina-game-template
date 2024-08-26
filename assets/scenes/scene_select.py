import ursina as u
from scripts import manager
from scripts.logger import log
from classes.grid import Grid
from classes.Scene import Scene

def controls(key):
    if key == "a":
        log.debug("Scene select button pressed: a")

def create_nav_button(name, position=(0,0), scale=(1,1), parent=u.camera.ui):
    #Create buttons to travel to specific scenes for development purposes
    return u.Button(
        name=name,
        text="\n".join(name.split("_")),
        scale=scale,
        text_size=0.4,
        color=u.color.black,
        text_color=u.color.white,
        position=position,
        on_click=lambda:manager.change_scene(name),
        parent=parent
        )

def loader(scene):
    #global scene
    entities = [] #list of entities
    grid = Grid(width=6, height=6, cell_size=1).render()
    if manager.Language == "":
        manager.Language = "English"
    x_pos = 0
    y_pos = 0
    scene_names = [scene.name for scene in manager.get_scene(True)]
    for name in scene_names:
        width, height = 0.8,0.8
        position = grid.grid_to_world(x_pos, y_pos, origin="top left", coc=True)
        entities.append(create_nav_button(name, position, scale=(width,height), parent=grid))
        x_pos+=1
        if x_pos % grid.width == 0:
            x_pos = 0
            y_pos -= 1
    position = grid.grid_to_world(0, 0, origin="center", coc=True)
    entities.append(u.Button(text=f"Language: {manager.Language}", position=position, scale=(.1,.05)))
    entities.append(grid)
    return entities
    #scene.add_entities(entities)

scene = Scene("scene_select", loader=loader, controls=controls)
