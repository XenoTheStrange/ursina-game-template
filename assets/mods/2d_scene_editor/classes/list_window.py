import ursina as u
from scripts.logger import log

class ListWindow(u.Entity):
    def __init__(self, scale=(.25, .5), title=None, content=None, num_buttons_shown=5, padding=(0,0), draggable=False, style=None, title_style=None, title_text_style=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = u.camera.ui
        self.model = "quad"
        self.color=u.color.black66
        self.num_buttons_shown = num_buttons_shown
        self.scale = scale
        self.padding = padding
        #need to set the style before stuff is set that relies on other stuff, i.e. button_scale relying on padding.
        if style is not None:
            for item in style.items():
                setattr(self, item[0], item[1])
        self.button_scale = (1-self.padding[0], (self.scale[1]/self.num_buttons_shown))
        self.content = content if type(content) is list else []
        self.title_bar = None
        self.layout()
        if title is not None or draggable == True:
            self.set_title(title=title, draggable=draggable, style=title_style, text_style=title_text_style)
    def create_dragger(self, target=None):
        if target is None:
            log.error("Function create_dragger requires a target entity")
            return
        def dragger_controls(key):
            if key == "left mouse down":
                if dragger.target.hovered:
                    dragger.mouse_pos = u.mouse.position
                    dragger.entity_pos = self.position
                    dragger.active = True
            if key == "left mouse up":
                if dragger.active:
                    dragger.active = False
        def dragger_update():
            if dragger.active:
                self.position = dragger.entity_pos + (u.mouse.position - dragger.mouse_pos)
        dragger = u.Entity(parent=self, target=target, mouse_pos=None, entity_pos=None, active=False, update=dragger_update, input=dragger_controls)
    def add_button(self, name="button", text="button", on_click=None, style=None, *args, **kwargs):
        self.content.append(
            ListButton(name=name, text=text, on_click=on_click, scale=self.button_scale, parent=self, style=style, *args, **kwargs)
        )
        self.layout()
    def remove_button(self, name=None, text=None, index=None):
        if name is None and text is None and index == 0:
            log.error("Function remove_button requires either a name, text, or an index value")
            return
        e = None
        for i, button in enumerate(self.content):
            if button.name == name:
                e = self.content.pop(i)
            elif button.text == text:
                e = self.content.pop(i)
            elif i == index:
                e = self.content.pop(i)
        if e is not None:
            u.destroy(e)
        else:
            log.error(f"list_window.remove_button couldn't find this button: {{'name': {name}, 'text': {text}, 'index': {index}}}")
        self.layout()
    def set_title(self, title=None, draggable=False, style=None, text_style=None):
        if self.title_bar is not None:
            u.destroy(self.title_bar)

        if title is not None or draggable is True:
            entity = u.Entity(parent=self, model="quad", scale=self.scale, color=u.color.black33)
            if style is not None:
                for item in style.items():
                    setattr(entity, item[0], item[1])
            entity.position = (0, self.scale[1]+(entity.scale[1]/2),-0.01)#self.position + (0, self.scale[1] + entity.scale[1]/2, -0.01)
            if draggable is True:
                entity.collider = "box"
                self.create_dragger(target=entity)
            if title is not None:
                text = u.Text(parent=entity, text=title, color=u.color.white, origin=(0,0), position=(0,0,-0.01))
                text.world_scale = u.Vec3(20 * text.scale)
                if text_style is not None:
                    for item in text_style.items():
                        setattr(text, item[0], item[1])
        self.title_bar = entity
    def layout(self):
        top = self.world_position + (0, self.world_scale[1] / 2, 0)
        if self.title_bar is not None:
            self.title_bar.world_position = top + (0, self.title_bar.world_scale[1]/2,-0.01)
        for i, button in enumerate(self.content):
            button.world_position = top + (0,-button.world_scale[1]/2, -0.01) + (0, -i * button.world_scale[1], 0)
            button.position += (0, -(i+1) * (self.padding[1]/2), 0)

class ListButton(u.Entity):
    def __init__(self, name="button", text="button", scale=(1,.1), parent=u.camera.ui, on_click=None, color=u.hsv(0,0,0, a=0.33), style=None, text_style=None, glows=False, glow_color=u.hsv(0,0,0.5, a=0.33), glow_time=0.1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.parent = parent
        self.position += (0,0,-0.01)
        self.model = "quad"
        self.collider = "box"
        if on_click is not None: self.on_click = on_click
        self.color = color
        self.original_color = color
        self.glow_color = glow_color
        self.scale = scale
        self.glow_time = glow_time
        self.glows = glows
        self.text = u.Text(text=text, origin=(0,0), parent=self.model, position=self.position+(0,0,-0.01), color=u.color.white, original_color=u.color.white, glow_color=u.color.black)
        self.text.original_color = self.text.color
        self.text.world_scale = u.Vec3(20 * self.text.scale)
        if style is not None:
            for item in style.items():
                log.debug(f"self.{item[0]} = {item[1]}")
                setattr(self, item[0], item[1])
        if text_style is not None:
            for item in text_style.items():
                setattr(self.text, item[0], item[1])
        self.original_color = self.color
    def update(self):
        if self.glows:
            if self.hovered and not u.mouse.left:
                self.color = self.glow_color
                self.text.color = self.text.glow_color
            elif self.hovered and u.mouse.left:
                self.color = self.glow_color + (0,0,0,-.3)
            else:
                self.color = self.original_color
                self.text.color = self.text.original_color


