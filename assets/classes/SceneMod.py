class SceneMod:
    def __init__(self, name=None, entities=None, prefix=None, postfix=None, loader=None):
        self.name = name
        self.entities = [] if entities == None else entities
        #both of these must instantiate and return a list of entities
        self.prefix = prefix
        self.postfix = postfix
        #if this is defined it will overwrite the loader for the original scene
        self.loader = loader
