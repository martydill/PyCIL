

class Method():

    AttributeTypes = {
        'static':0,
        'cil':1,
        'managed':2,
        'public':3,
        'private':4,
        'hidebysig':5,
        'cil':6,
        'specialname':7,
        'rtspecialname':8,
        'instance':9
    }

    def __init__(self):
        self.name = 'unnamed'
        self.namespace = None
        self.attributes = []
        self.maxStack = 1
        self.locals = []
        self.returnType = None
        self.instructions = []
        self.parameters = []

