
from Variable import Variable

class ReferenceType(Variable):
    
    def __init__(self):
        super(ReferenceType, self).__init__()
        self.fields = []
        self.fieldNames = []
        
    def add_field(self, field):
        self.fields.append(field)
        self.fieldNames.append(field.name)

        