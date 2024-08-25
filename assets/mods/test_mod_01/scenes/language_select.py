import ursina as u

name = "language_select"

def Prefix(scene):
    entities = []
    button = u.Button(text="Mods are working", position=(0,0.3,-2), scale=(0.3,0.1), parent=u.camera.ui)
    button.on_click=lambda:u.destroy(button)
    entities.append(button)
    return entities

def Postfix(scene):
    print("This is where you would modify entities spawned in the edited scene")
    return None

def loader():
    print("This will run instead of the normal scene loader if the below function returns true")

def Replace_Loader():
    return False
