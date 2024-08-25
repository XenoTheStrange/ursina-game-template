import ursina as u

name = "scene_select"

def controls(key):
    if key == "space":
        for entity in u.scene.entities:
            if entity.getTag("type") == "grid":
                entity.toggle_visibility()

def Prefix(scene):
    entities = []
    entities.append(
        u.Entity(input=controls)
    )
    return entities

def Postfix(scene):
    return None

def Replace_Loader():
    return False
