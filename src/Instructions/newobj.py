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
        # fixme - parse ctor part? will it always be ctor?
        
    def execute(self, vm):
        t = Types.resolve_type(self.typeName)
        r = ReferenceType()
        r.type = t
        vm.stack.push(r)
        
        m = vm.find_method_by_signature(t.namespace + '.' + t.name, '.ctor()', None, None)
        vm.execute_method(m)
        
        
register('newobj', newobj)

class newobjTest(unittest.TestCase):

    def test_newobj_no_parameters_calls_constructor(self):
        from VM import VM

        vm = VM()

        m = Method()
        m.name = '.ctor()'
        m.namespace = 'testnamespace.testclass'
        vm.methods.append(m)
        
        c = Class()
        c.name = 'testclass'
        c.namespace = 'testnamespace'
        c.methods.append(m)
        
        t = Types.register_custom_type(c)

        n = newobj('instance void testnamespace.testclass::.ctor()')
        n.execute(vm)
        Types.unregister_custom_type(t)
        
        o = vm.stack.pop()
        self.assertEqual(o.type, t)
        self.assertEquals(vm.current_method(), m)
        