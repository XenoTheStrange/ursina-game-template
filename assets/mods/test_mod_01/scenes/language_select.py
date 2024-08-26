import ursina as u
from classes.SceneMod import SceneMod

class test_button(u.Entity):
    def __init__(self, position=(0,0,0), scale=(1,1), parent=u.Default, model=u.Default, texture=None, onclick=(None, None), collider=None, **kwargs):
        super().__init__()
        self.position = position
        self.scale = scale
        self.parent = parent
        self.model = model
        self.texture = texture
        self.onclick = onclick
        self.collider=collider
    def destroy(self):
        u.destroy(self)
    def input(self, key):
        if self.hovered:
            if self.onclick[0] is not None:
                if key == "left mouse down":
                    self.onclick[0]()
                if key == "right mouse down":
                    self.onclick[1]()

def swap_texture(button):
    if button.texture.name == "sun.png":
        button.texture = "sun_yara"
    else:
        button.texture = "sun"

def Prefix(scene):
    button = test_button(
        position=(0,0.35,-2),
        scale=(0.3,0.3),
        parent=u.camera.ui,
        model="quad",
        texture="sun",
        )
    button.onclick = (lambda:swap_texture(button), lambda:print("Right clicked yarasun"))
    button.collider = u.SphereCollider(button, radius=.15)
    return [button]

scene_mod = SceneMod("language_select", prefix=Prefix)
