'''
Helper instruction use to signal the end of try blocks
'''

import unittest
from Stack import StackStateException
from Instructions.Instruction import Instruction
from Variable import Variable
from ProtectedBlock import ProtectedBlock


class EndTry(Instruction):

    def __init__(self, arguments = None):
        self.name = 'EndTry'

    def execute(self, vm):
        if len(vm.get_protected_blocks()) == 0:
            raise Exception('Cannot end try block with no try block started!')
        
        vm.get_protected_blocks().pop()

class EndTryTest(unittest.TestCase):
  
    def test_execute_with_no_begin_try_throws_exception(self):
        from VM import VM
        vm = VM()
        x = EndTry('')
        self.assertRaises(Exception, x.execute, vm)
        
    def test_execute_ends_try_block(self):
        from VM import VM
        vm = VM()
        vm.get_protected_blocks().append(ProtectedBlock())
        x = EndTry()
        x.execute(vm)
        
        self.assertEqual(len(vm.get_protected_blocks()), 0)