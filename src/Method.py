

class Method():

    AttributeTypes = {
        'static':0,
        'cil':1,
        'managed':2,
        'public':3
    }

    def __init__(self):
        self.name = 'unnamed'
        self.namespace = ''
        self.attributes = []
        self.maxStack = 1
        self.locals = []
        self.returnType = None
        self.instructions = []
        self.parameters = []

