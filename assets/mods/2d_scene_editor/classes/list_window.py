import ursina as u

class ListWindow(u.Entity):
    def __init__(self, scale=(.25, .5), title=None, content=None, num_buttons_shown=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = u.camera.ui
        self.model = "quad"
        self.color=u.color.black66
        self.title_bar = None
        self.main_window = None
        self.num_buttons_shown = num_buttons_shown
        self.scale = scale
        self.button_scale = (1, self.scale[1]/self.num_buttons_shown)
        self.content = content if type(content) is list else []
    def add_button(self, name="buton", text="button", on_click=None, *args, **kwargs):
        self.content.append(
            ListButton(name=name, text=text, on_click=on_click, scale=self.button_scale, parent=self, *args, **kwargs)
        )
        self.layout()
    def layout(self):
        top = self.position+(0, self.scale[1], 0)
        for i, button in enumerate(self.content):
            #each button should be moved just below the last one....
            button.position = top + (0,-button.scale[1]/2,0) + (0, -i*button.scale[1], 0)

class ListButton(u.Entity):
    def __init__(self, name="button", text="button", scale=(1,.1), parent=u.camera.ui, on_click=None, color=u.color.black33, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.position += (0,0,-0.1)
        self.model = "quad"
        self.collider = "box"
        self.on_click = on_click
        self.color = color
        self.scale = scale
        self.text = u.Text(text=text, origin=(0,0), parent=self.model, position=self.position+(0,0,-0.1))
        self.text.world_scale = u.Vec3(20 * self.text.scale)
    def update(self):
        if self.hovered:
            self.color = u.hsv(0,0,0.5, a=0.33)
        else:
            self.color = u.hsv(0,0,0, a=0.33)


