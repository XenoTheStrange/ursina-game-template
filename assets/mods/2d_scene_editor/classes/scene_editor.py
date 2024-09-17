#!/usr/bin/python3
import ursina as u
from .classes.list_window import ListWindow

class SceneEditor(u.Entity):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_templates = None
        self.window_entities = None
        self.window_classes = None
        self.create_windows()

    def create_windows(self):
        self.window_templates = ListWindow(content=self.load_custom_entities())
        self.window_entities = ListWindow()
        self.window_classes = ListWindow()
    
    def load_custom_entities(self):
        pass
        #import python file and scan it for classes which inherit from u.Entity at some point.
        #load these files from groot/assets/entities and mod/entities
        #create buttons in the templates pane for each entity imported this way

