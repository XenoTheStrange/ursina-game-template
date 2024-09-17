import ursina as u
from ursina.prefabs.window_panel import WindowPanel
from ursina.collider import BoxCollider

from classes.draggable_entity import Draggable_Entity
from scripts.manager import add_scene, change_scene, get_current_scene
from classes.Scene import Scene
from .classes.list_window import ListWindow
selected_entity = None

def select_entity(entity):
    globals()['selected_entity'] = entity

def create_text(entities_window, *args, **kwargs):
    scene = get_current_scene()
    #text don't have colliders normally so we need to make one.
    entity = u.Text(editor_obj=True, *args, **kwargs)
    entity.collider = BoxCollider(entity, center=entity.position+(entity.width/2,-entity.height/2,0), size=(entity.width,entity.height,.1))
    button = u.Button(text=str(entity.name), entity=entity)
    button.on_click = lambda: select_entity(entity)
    entities_window.content.append(button)
    entities_window.layout()
    scene.add_entities([entity])

def create_entity(entities_window, text="yeet", *args, **kwargs):
    scene = get_current_scene()
    #entity = Entity_Parent(entity=u.Entity(*args, **kwargs))
    entity = u.Entity(editor_obj=True, collider="box", *args, **kwargs)
    text = u.Text(parent=entity, text=text, origin=(0,0), position=entity.position+(0,0,-0.01))
    text.world_scale = u.Vec3(20 * text.scale)
    scene.add_entities([entity])
    button = u.Button(text=str(entity.name), entity=entity)
    button.on_click = lambda: select_entity(entity)
    entities_window.content.append(button)
    entities_window.layout()

def remove_thing(entity, entities_window):
    for i, item in enumerate(entities_window.content):
        if item.entity is entity:
            button = entities_window.content.pop(i)
            u.destroy(button)
    scene = get_current_scene()
    for i, item in enumerate(scene.entities):
        if item is entity:
            scene.entities.pop(i)
    u.destroy(entity)
    globals()['selected_entity'] = None
    entities_window.layout()

def resize(entity, key):
    base = 0.01
    mod = 1
    if u.held_keys['shift']: mod = 10
    if key == "scroll up":
        if u.held_keys['control']:
            entity.scale += (0,base*mod)
        if u.held_keys['alt']:
            entity.scale += (base*mod,0)
        if not u.held_keys['alt'] and not u.held_keys['control']:
            entity.scale += (base,base)*mod
    if key == "scroll down":
        if u.held_keys['control']:
            entity.scale += (0,-base*mod)
        if u.held_keys['alt']:
            entity.scale += (-base*mod,0)
        if not u.held_keys['alt'] and not u.held_keys['control']:
            entity.scale += (-base*mod,-base*mod)

def move(entity, direction):
    base = 0.01
    mod = 1
    if u.held_keys['shift']: mod = 10
    if u.held_keys['alt']: mod = 0.1
    if u.held_keys['tab']:
        if direction == "up arrow" or direction == "up arrow hold" or direction == "scroll up":
            entity.position += (0,0,-base*mod)
        if direction == "down arrow" or direction == "down arrow hold" or direction == "scroll down":
            entity.position += (0,0,base*mod)
    elif direction == "left arrow" or direction == "left arrow hold":
        entity.position += (-base*mod,0,0)
    elif direction == "right arrow" or direction == "right arrow hold":
        entity.position += (base*mod,0,0)
    elif direction == "down arrow" or direction == "down arrow hold":
        entity.position += (0,-base*mod,0)
    elif direction == "up arrow" or direction == "up arrow hold":
        entity.position += (0,base*mod,0)

def loader(scene):
    entities_list = []

    def dragger_controls(key):
        if key == "left mouse down":
            dragger.mouse_pos = u.mouse.position
            if hasattr(u.mouse.hovered_entity, "editor_obj"):
                dragger.target = u.mouse.hovered_entity
                dragger.entity_pos = dragger.target.position
                globals()['selected_entity'] = u.mouse.hovered_entity
            else:
                globals()['selected_entity'] = None
        if key == "left mouse up":
                dragger.target = None
        if (key == "scroll up" or key == "scroll down") and not u.held_keys['tab']:
            if globals()['selected_entity'] is not None:
                resize(globals()['selected_entity'], key)
        if "left" in key or "right" in key or "up" in key or "down" in key:
            if globals()['selected_entity'] is not None:
                move(globals()['selected_entity'], key)
    
    def dragger_update():
        if dragger.target is not None:
            dragger.target.position = dragger.entity_pos + (u.mouse.position - dragger.mouse_pos)
    
    dragger = u.Entity(name="controller.dragger", input=dragger_controls, update=dragger_update, target=None, mouse_pos=None, entity_pos=None)
    
    entities_window = WindowPanel(name="window.entities", title="Entities", content=[], parent=u.camera.ui, position=u.window.top_right)
    entities_window.position += (-entities_window.scale.x/2, 0, -99)

    content = [
        u.Button(text="fuck"),
        u.Button(text="entity"),
        u.Button(text="text 3")
        ]
    content[0].on_click = lambda:create_text(entities_window, name="fucktext", text="fuck", parent=u.camera.ui)
    content[1].on_click = lambda:create_entity(entities_window, name="entity", model="quad", parent=u.camera.ui, scale=(.1,.1), color=u.color.black33)
    content[2].on_click = lambda:create_entity(entities_window, name="entity_green", model="quad", parent=u.camera.ui, scale=(.1,.1), color=u.color.green)

    templates_window = WindowPanel(name="window.templates", title='Templates', content=content, parent=u.camera.ui, position=u.window.top_left)
    templates_window.position += (templates_window.scale.x/2, 0, -98)

    properties_window = WindowPanel(name="window.properties", title="Properties", content=[], parent=u.camera.ui, position=u.window.top)
    properties_window.position += (0,0,-97)
    
    def toggle_visibility(entity):
        entity.visible = False if entity.visible else True

    def controls(key):
        if key == "delete":
            if globals()['selected_entity'] is not None:
                remove_thing(globals()['selected_entity'], entities_window)
        if key == "enter":
            scene = get_current_scene()
            for entity in scene.entities:
                if hasattr(entity, "editor_obj"):
                    print(f"""{entity.__class__.__name__}(name="{entity.name}", scale={(round(entity.scale[0],3), round(entity.scale[1],3), round(entity.scale[2],3))}, position={(round(entity.position[0],3), round(entity.position[1],3), round(entity.position[2],3))}""")

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

    window=ListWindow(
        scale = (.5, .7), 
        editor_obj = True, 
        title = "Title", 
        style = {
            'padding':(0.1,0.1)
        }, 
        title_style = {
            'color':u.color.black33, 
            'scale':(1,0.05)
            }, 
        title_text_style = {
            'color': u.color.white, 
            'font':'fonts/Helvetica.ttf', 
            'origin':(0,0.1)
            }, 
        draggable = True
        )
    #window.add_button(name="oh_jeez", text="oh_jeez", on_click=lambda:window.remove_button(name="oh_jeez"), glows=True)
    window.add_button(name="oh_jeez", text="oh_jeez", on_click=lambda:window.remove_button(name="oh_jeez"), on_middle_click=lambda:print("middle clicked"), glows=True)
    window.add_button(name="fuck", text="fuck", on_click=lambda:window.remove_button(name="fuck"), glows=True)
    window.add_button(name="oh", text="print children", on_click=lambda:print([i for i in window.content]), glows=True)
    window.add_button(name="test", text="test", on_click=lambda:window.remove_button(name="oh_jeez"), glows=True, text_style={'glow_color':u.color.white})
    window.add_button(on_click=lambda:print("click works"), glows=True, style={'color':u.color.green, 'glow_color': u.color.red})

    button = u.Button(text="ListWindow", entity=window)
    button.on_click = lambda: select_entity(window)
    entities_window.content.append(button)
    entities_window.layout()
    entities_list.append(window)

    return entities_list

add_scene(Scene(name="2d_editor", loader=loader))