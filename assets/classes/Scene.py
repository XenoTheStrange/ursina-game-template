import ursina
from scripts.logger import log

class Scene:
    """Encapsulation for scenes"""
    def __init__(self, name=None, entities=None, controls=None, parent=None, loader=None):
        self.name = name
        if not entities is None:
            self.entities = entities
        else:
            self.entities = []
        self.controls = controls
        self.controller = None
        self.loader = loader
        self.parent = parent
        self.controller = ursina.Entity(input=self.controls)
        self.entities.append(self.controller)
        self.mods_prefix=[]
        self.mods_postfix=[]
    def add_entities(self, entities):
        for entity in entities:
            self.entities.append(entity)
    def load(self):
        if self.loader is not None:
            self.add_entities(self.loader(self))
    def load_mods(self, func_list):
        for func in func_list:
            entities = func(self)
            if entities is not None:
                self.add_entities(entities)
    def destroy(self):
        #log.debug(f"Destroying scene: {self.name}")
        for entity in self.entities:
            try:
                ursina.destroy(entity)
            except AttributeError as e:
                #log.debug("Failed to destroy item: ", e)
                #'NoneType' object has no attribute 'eternal'
                pass
    def create(self):
        self.load_mods(self.mods_prefix)
        self.load()
        self.load_mods(self.mods_postfix)

