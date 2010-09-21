

class InvalidOpCodeException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Instruction:

       
    def __init__(self, name, opcode):
        self.name = name
        self.opcode = opcode
        self.label = ''
        
    def execute(self, stack):
        pass



