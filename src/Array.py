
from ReferenceType import ReferenceType
import Types

class Array(ReferenceType):
    
    def __init__(self, size):
        super(Array, self).__init__()
        self.length = 0
        self.type = Types.Array
        self.arrayType = None
        self.values = [None] * size 
          
        