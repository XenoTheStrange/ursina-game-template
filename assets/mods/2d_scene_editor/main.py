import ursina as u
from classes.draggable_entity import Draggable_Entity

class Entity_Parent(u.Entity):
    def __init__(self, entity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entity = entity
        self.entity.model
        self.draggable = Draggable_Entity(parent=entity.parent, scale=entity.scale, model=u.copy(entity.model), position=self.entity.position+(0,0,-0.1), color=u.hsv(0,0,0,a=0))
        self.parent = entity.parent
        self.entity.parent = self
        self.draggable.parent = self
    def input(self, key):
        self.scale(key)
    def update(self):
        self.entity.position = self.draggable.position
    def scale(self, key):
        base = 0.01
        mod = 10 if u.held_keys['shift'] else 1
        if key == "scroll up":
            if u.held_keys['control']:
                self.entity.scale += (0,base)*mod
            if u.held_keys['alt']:
                self.entity.scale += (base,0)*mod
            if not u.held_keys['alt'] and not u.held_keys['control']:
                self.entity.scale += (base,base)*mod
            self.draggable.scale = self.entity.scale
        if key == "scroll down":
            if u.held_keys['control']:
                self.entity.scale += (0,-base)*mod
            if u.held_keys['alt']:
                self.entity.scale += (-base,0)*mod
            if not u.held_keys['alt'] and not u.held_keys['control']:
                self.entity.scale += (-base,-base)*mod
            self.draggable.scale = self.entity.scale