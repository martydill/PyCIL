# throw.py
# The CIL throw instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
import unittest
from Instructions.Instruction import register

class throw(Instruction):

    def __init__(self, arguments):
        self.name = 'throw'
        self.target = ''
            
    def execute(self, vm):
        pass

register('throw', throw)

class throwTest(unittest.TestCase):

    def test_throw_no_arguments_throws_exception(self):
        from VM import VM

        vm = VM()
        x = throw('asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        
    def test_throw_object(self):
        from VM import VM

        vm = VM()
        x = throw()
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
