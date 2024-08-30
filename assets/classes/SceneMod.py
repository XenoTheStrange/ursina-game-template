class SceneMod:
    def __init__(self, name=None, prefix=None, postfix=None, loader=None, entities=None):
        self.name = name
        #both of these must instantiate and return a list of entities
        self.prefix = prefix
        self.postfix = postfix
        #if this is defined it will overwrite the loader for the original scene
        self.loader = loader
        #is added to the scene entities if it contains anything
        self.entities = [] if entities is None else entities
