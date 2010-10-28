from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from MethodDefinition import MethodDefinition
from Instructions.Instruction import register
from ClassDefinition import ClassDefinition
import Types
from ReferenceType import ReferenceType
from Array import Array


class ldelem(Instruction):

    opcodePrefixTable = {
        'i1' : 0x90,
        'i2' : 0x92,
        'i4' : 0x94,
        'i8' : 0x96,
        'u1' : 0x91,
        'u2' : 0x93,
        'u4' : 0x95,
        'u8' : 0x96,
        'r4' : 0x98,
        'r8' : 0x99,
        'i' : 0x97,
        'ref' : 0x9A
    }


    def __init__(self, suffix):
        super(ldelem, self).__init__()
        self.name = 'ldelem.' + suffix
        self.suffix = suffix
        
        if(ldelem.opcodePrefixTable.has_key(suffix)):
            self.opcode = ldelem.opcodePrefixTable[suffix]
        
        
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        if stack.get_frame_count() < 2:
            raise StackStateException('Not enough values on the stack')
        
        index = vm.stack.pop()
        array = vm.stack.pop()
        
        vm.stack.push(array.values[index.value])
        
register('ldelem', ldelem)

class ldelemTest(unittest.TestCase):
    def test_execute_not_enough_stack_values(self):
        from VM import VM
        vm = VM()
               
        x = ldelem('')
        
        self.assertRaises(StackStateException, x.execute, vm)
        
    def test_execute_get_array_element_i4(self):
        from VM import VM
        vm = VM()
        
        a = Array(100)
        a.values[5] = Variable(1122)  
        vm.stack.push(a)
        vm.stack.push(Variable(5))
        
        x = ldelem('i4')
        
        x.execute(vm)
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(a.values[5].value, 1122)
    