import ursina as u
from ursina.prefabs.window_panel import WindowPanel
from ursina.collider import BoxCollider

from classes.draggable_entity import Draggable_Entity
from scripts.manager import add_scene, change_scene, get_current_scene
from classes.Scene import Scene

selected_entity = None

def select_entity(entity):
    globals()['selected_entity'] = entity

def create_text(entities_window, *args, **kwargs):
    scene = get_current_scene()
    #text don't have colliders normally so we need to make one.
    entity = u.Text(editor_obj=True, *args, **kwargs)
    entity.collider = BoxCollider(entity, center=entity.position+(entity.width/2,-entity.height/2,0), size=(entity.width,entity.height,.1))
    button = u.Button(text=str(entity.name))
    button.on_click = lambda: select_entity(entity)
    entities_window.content.append(button)
    entities_window.layout()
    scene.add_entities([entity])

def create_entity(entities_window, *args, **kwargs):
    scene = get_current_scene()
    #entity = Entity_Parent(entity=u.Entity(*args, **kwargs))
    entity = u.Entity(editor_obj=True, collider="box", *args, **kwargs)
    scene.add_entities([entity])
    button = u.Button(text=str(entity.name))
    button.on_click = lambda: select_entity(entity)
    entities_window.content.append(button)
    entities_window.layout()

def remove_thing(entity, entities_window):
    entities_window.content.pop(entity)
    u.destroy(entity)
    globals()['selected_entity'] = None

def resize(entity, key):
    base = 0.01
    mod = 10 if u.held_keys['shift'] else 1
    if key == "scroll up":
        if u.held_keys['control']:
            entity.scale += (0,base)*mod
        if u.held_keys['alt']:
            entity.scale += (base,0)*mod
        if not u.held_keys['alt'] and not u.held_keys['control']:
            entity.scale += (base,base)*mod
    if key == "scroll down":
        if u.held_keys['control']:
            entity.scale += (0,-base)*mod
        if u.held_keys['alt']:
            entity.scale += (-base,0)*mod
        if not u.held_keys['alt'] and not u.held_keys['control']:
            entity.scale += (-base,-base)*mod

def loader(scene):
    entities_list = []

    def dragger_controls(key):
        if key == "left mouse down":
            if hasattr(u.mouse.hovered_entity, "editor_obj"):
                dragger.target = u.mouse.hovered_entity
                globals()['selected_entity'] = u.mouse.hovered_entity
            else:
                globals()['selected_entity'] = None
        if key == "left mouse up":
                dragger.target = None
        if key == "scroll up" or key == "scroll down":
            if globals()['selected_entity'] is not None:
                resize(globals()['selected_entity'], key)
    
    def dragger_update():
        if dragger.target is not None:
            dragger.target.position = u.mouse.position
    
    dragger = u.Entity(name="controller.dragger", input=dragger_controls, update=dragger_update, target=None)
    
    entities_window = WindowPanel(name="window.entities", title="Entities", content=[], parent=u.camera.ui, position=u.window.top_right)
    entities_window.position += (-entities_window.scale.x/2, 0, -99)

    content = [
        u.Button(text="fuck"),
        u.Button(text="entity"),
        u.Button(text="text 3")
        ]
    content[0].on_click = lambda:create_text(entities_window, name="fucktext", text="fuck", parent=u.camera.ui)
    content[1].on_click = lambda:create_entity(entities_window, name="entity", model="quad", parent=u.camera.ui, scale=(.1,.1), color=u.color.black33)

    templates_window = WindowPanel(name="window.templates", title='Templates', content=content, parent=u.camera.ui, position=u.window.top_left)
    templates_window.position += (templates_window.scale.x/2, 0, -98)

    properties_window = WindowPanel(name="window.properties", title="Properties", content=[], parent=u.camera.ui, position=u.window.top+(0,0,-97))
    
    def toggle_visibility(entity):
        entity.visible = False if entity.visible else True

    def controls(key):
        if key == "f1":
            toggle_visibility(templates_window)
        if key == "f2":
            toggle_visibility(properties_window)
        if key == "f3":
            toggle_visibility(entities_window)
    
    controller = u.Entity(name="controller", input=controls)

    entities_list.append(properties_window)
    entities_list.append(templates_window)
    entities_list.append(controller)
    return entities_list

add_scene(Scene(name="2d_editor", loader=loader))