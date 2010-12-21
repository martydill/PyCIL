# stelem.py
# The CIL stelem instruction
# Copyright 2010 Marty Dill - see LICENSE for details

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


class stelem(Instruction):

    opcodePrefixTable = {
        'i1' : 0x9C,
        'i2' : 0x9D,
        'i4' : 0x9E,
        'i8' : 0x9F,
        'r4' : 0xA0,
        'r8' : 0xA1,
        'i' : 0x9B,
        'ref' : 0xA2
    }


    def __init__(self, suffix):
        super(stelem, self).__init__()
        self.name = 'stelem.' + suffix
        self.suffix = suffix
        
        if(stelem.opcodePrefixTable.has_key(suffix)):
            self.opcode = stelem.opcodePrefixTable[suffix]
        
        
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        if stack.get_frame_count() < 3:
            raise StackStateException('Not enough values on the stack')
        
        value = vm.stack.pop()
        index = vm.stack.pop()
        array = vm.stack.pop()
        
        array.values[index.value] = value
        
register('stelem', stelem)

class stelemTest(unittest.TestCase):
    def test_execute_not_enough_stack_values(self):
        from VM import VM
        vm = VM()
               
        x = stelem('')
        
        self.assertRaises(StackStateException, x.execute, vm)
        
    def test_execute_set_array_element_i4(self):
        from VM import VM
        vm = VM()
        
        a = Array(100)
             
        vm.stack.push(a)
        vm.stack.push(Variable(5))
        vm.stack.push(Variable(333444))
        
        x = stelem('i4')
        
        x.execute(vm)
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(a.values[5].value, 333444)
    