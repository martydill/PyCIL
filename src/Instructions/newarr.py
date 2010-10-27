from Instruction import Instruction
import unittest
import Types
from MethodDefinition import MethodDefinition
from Instructions.Instruction import register
from ClassDefinition import ClassDefinition
from ReferenceType import ReferenceType
from Variable import Variable
from Array import Array


class newarr(Instruction):

    def __init__(self, arguments):
        self.name = 'newarr'
        self.opcode = 0x28 # fixme
        self.arguments = arguments
        self.type = Types.resolve_type(arguments)
        
    def execute(self, vm):
        a = Array()
        a.length = vm.stack.pop().value
        a.arrayType = self.type
        vm.stack.push(a)
    
register('newarr', newarr)

class newarrTest(unittest.TestCase):

    def test_newarr_one(self):
        from VM import VM

        vm = VM()
       
        vm.stack.push(Variable(1))
        n = newarr('[mscorlib]System.Int32')
        n.execute(vm)
        
        o = vm.stack.pop()
        self.assertEqual(o.type, Types.Array)
        self.assertIsInstance(o, Array)
        self.assertEqual(o.length, 1)
        self.assertEqual(o.arrayType, Types.Int32)
        
        