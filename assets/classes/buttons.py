import ursina as u
from scripts.manager import Cursor

class glow_button(u.Entity):
    """A button for the flags in the language-select screen"""
    def __init__(self, position=(0,0,0), scale=(1,1), parent=u.Default, model="quad", texture=None, onclick=(None, None), collider="box", text=None, text_scale=(10,12), text_position=(0.6,0.1,-2), text_font="fonts/Helvetica-Bold.ttf", **kwargs):
        super().__init__()
        self.position = position
        self.scale = scale
        self.parent = parent
        self.model = model
        self.texture = texture
        self.onclick = onclick
        self.collider = collider

        self.glowing = False
        self.lmd=False # left mouse down

        self.glow_entity = u.Entity(scale=(1,1), position=(0,0,-1), parent=self, model=model, color=u.hsv(0,0,100,a=0))
        self.drop_shadow_entity = u.Entity(scale=(1,1), parent=self, position=(0.02,-0.04,0.01), model=model, color=u.hsv(0,0,0,a=0.5))
        if text is not None:
            self.language_text = u.Text(text=text, scale=text_scale, parent=self, position=text_position, font=text_font)
            self.language_text_shadow = u.Text(text=text, scale=text_scale, parent=self, position=text_position+(0.02,-0.04,1), color=u.color.black, font=text_font)

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
    def on_mouse_exit(self):
        Cursor.texture = "cursor_default"
        if self.glowing:
            self.stop_glowing()
    def on_mouse_enter(self):
        Cursor.texture = "cursor_fat"
        if not self.glowing:
            self.start_glowing()
    def start_glowing(self):
        #if the left mouse button is already held down, use the second glow effect instead
        self.glowing = True
        if self.lmd:
            self.glow_entity.animate_color(u.hsv(0,0,100, a=0.1), duration=.02, interrupt='finish')
        else:    
            self.glow_entity.animate_color(u.hsv(0,0,100, a=0.2), duration=.02, interrupt='finish')
    def stop_glowing(self):
        self.glowing = False
        self.glow_entity.animate_color(u.hsv(0,0,100, a=0), duration=.02, interrupt='finish')
