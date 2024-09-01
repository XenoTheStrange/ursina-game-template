import traceback

import ursina
from scripts.logger import log
from scripts.logger import error_handler

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
    @error_handler
    def get_entity_named(self, name):
        for entity in self.entities:
            if hasattr(entity, "name"):
                if entity.name == name:
                    return entity
    def add_entities(self, entities):
        for entity in entities:
            self.entities.append(entity)
    def load(self):
        if self.loader is not None:
            entities = self.loader(self)
            if entities is not None:
                self.add_entities(entities)
    def destroy(self):
        for entity in self.entities:
            try:
                ursina.destroy(entity)
            except AttributeError as e:
                #log.debug("Failed to destroy item: ", e)
                #'NoneType' object has no attribute 'eternal'
                pass
        self.entities = []


