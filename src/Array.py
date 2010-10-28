
from ReferenceType import ReferenceType
import Types

class Array(ReferenceType):
    
    def __init__(self, length):
        super(Array, self).__init__()
        self.length = length
        self.type = Types.Array
        self.arrayType = None
        self.values = [None] * length 
          
        