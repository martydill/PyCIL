# ldlen.py
# The CIL ldlen instruction
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

class ldlen(Instruction):

    def __init__(self, args):
        super(ldlen, self).__init__()
        # fixme - set opcode
        self.name = 'ldlen'
        
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        if stack.get_frame_count() < 1:
            raise StackStateException('Not enough values on the stack')
        
        array = vm.stack.pop()
        result = Variable(array.length)
        result.type = Types.UInt32
        vm.stack.push(result)
        # fixme - should be native unsigned int
        
register('ldlen', ldlen)

class ldlenTest(unittest.TestCase):

    def test_execute_not_enough_stack_values(self):
        from VM import VM
        vm = VM()
               
        x = ldlen('')
        
        self.assertRaises(StackStateException, x.execute, vm)
 
    def test_execute_valid_array(self):
        from VM import VM
        vm = VM()
        
        a = Array()
        a.length = 9876        
        x = ldlen('')
        vm.stack.push(a)
        
        x.execute(vm)
        self.assertEqual(vm.stack.pop().value, 9876)
    