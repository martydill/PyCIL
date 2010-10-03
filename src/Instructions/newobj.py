from Instruction import Instruction
import unittest
import Types
from Method import Method
from Instructions.Instruction import register
from Class import Class
from ReferenceType import ReferenceType

class newobj(Instruction):

    def __init__(self, arguments):
        self.name = 'newobj'
        self.opcode = 0x28 # fixme
        self.arguments = arguments
        params = arguments.split(' ')
        self.scope = params[0]
        self.returnType = params[1] # fixme - use actual type object?
        parts = params[2].split('::')
        self.typeName = parts[0]
        
    def execute(self, vm):
        t = Types.resolve_type(self.typeName)
        r = ReferenceType()
        r.type = t
        vm.stack.push(r)
           
register('newobj', newobj)

class newobjTest(unittest.TestCase):

    def test_newobj_no_parameters(self):
        from VM import VM

        vm = VM()

        c = Class()
        c.name = 'testclass'
        c.namespace = 'testnamespace'
        t = Types.register_custom_type(c)

        n = newobj('instance void testnamespace.testclass::.ctor()')
        n.execute(vm)

        o = vm.stack.pop()
        #self.assertEqual(o.__class__.__name__, ReferenceType.__class__.__name__)
        self.assertEqual(o.type, t)