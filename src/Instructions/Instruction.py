
Instructions = {}

def register(name, type):
    Instructions[name] = type
    
    
class InvalidOpCodeException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Instruction(object):
       
    def __init__(self):
        self.name = 'unnamed'
        self.opcode = 0x0
        self.label = ''
        
    def execute(self, stack):
        pass



