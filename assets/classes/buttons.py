import ursina as u

class language_flag_button(u.Entity):
    def __init__(self, position=(0,0,0), scale=(1,1), parent=u.Default, model=u.Default, texture=None, onclick=(None, None), collider=None, **kwargs):
        super().__init__()
        self.position = position
        self.scale = scale
        self.parent = parent
        self.model = model
        self.texture = texture
        self.onclick = onclick
        self.collider = collider
        self.glowing = False
        self.glow_entity = u.Entity(scale=(1,1), position=(0,0,-1), parent=self, model=model, color=u.hsv(0,0,100,a=0))
        self.drop_shadow_entity = u.Entity(scale=(1,1), parent=self, position=(0.02,-0.04,0.01), model=model, color=u.hsv(0,0,0,a=0.5))
        self.lmd=False # left mouse down

    def destroy(self):
        u.destroy(self)
    def input(self, key):
        if key == "left mouse down":
            self.lmd = True
        if key == "left mouse up":
            self.lmd = False
        if self.hovered:
            if self.onclick[0] is not None:
                if self.lmd:
                    self.glow_entity.animate_color(u.hsv(0,0,100, a=0.1), duration=.02, interrupt='stop')
                if key == "left mouse up":
                    self.onclick[0]()
    def update(self):
        if self.hovered and not self.glowing:
            self.glowing = True
            self.start_glowing()
        if not self.hovered and self.glowing:
            self.stop_glowing()
            self.glowing=False
    def start_glowing(self):
        if self.lmd:
            self.glow_entity.animate_color(u.hsv(0,0,100, a=0.1), duration=.02, interrupt='stop')
        else:    
            self.glow_entity.animate_color(u.hsv(0,0,100, a=0.2), duration=.02, interrupt='stop')
        print("todo")
    def stop_glowing(self):
        self.glow_entity.animate_color(u.hsv(0,0,100, a=0), duration=.02, interrupt='stop')

