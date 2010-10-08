
ClassFlags = ['private', 'auto', 'ansi', 'beforefieldinit']

class ClassDefinition(object):
    
    def __init__(self):
        self.namespace = None
        self.name = None
        self.baseClass = None
        self.methods = []
        self.flags = []
        self.fieldDefinitions = []