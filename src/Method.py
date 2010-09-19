

class Method():

    AttributeTypes = {
        'static':0,
        'cil':1,
        'managed':2
    }

    def __init__(self):
        self.name = 'unnamed'
        self.attributes = []
        self.maxStack = 1
        self.locals = []
        self.returnType = None
        self.instructions = []
        self.parameters = []

