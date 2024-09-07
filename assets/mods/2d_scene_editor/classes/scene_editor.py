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
        self.window_templates = ListWindow(content=self.load_templates())
        self.window_entities = ListWindow()
        self.window_classes = ListWindow()


