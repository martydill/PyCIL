'''
Helper instruction use to signal the end of catch blocks
'''

import unittest
from Stack import StackStateException
from Instructions.Instruction import Instruction
from Variable import Variable
from ProtectedBlock import ProtectedBlock


class EndCatch(Instruction):

    def __init__(self, arguments = None):
        self.name = 'EndCatch'

    def execute(self, vm):
        if len(vm.get_protected_blocks()) == 0:
            raise Exception('Cannot end catch block with no catch block started!')
        
        vm.get_protected_blocks().pop()

class EndCatchTest(unittest.TestCase):
  
    def test_execute_with_no_begin_catch_throws_exception(self):
        from VM import VM
        vm = VM()
        x = Endcatch('')
        self.assertRaises(Exception, x.execute, vm)
        
    def test_execute_ends_catch_block(self):
        from VM import VM
        vm = VM()
        vm.get_protected_blocks().append(ProtectedBlock())
        x = Endcatch()
        x.execute(vm)
        
        self.assertEqual(len(vm.get_protected_blocks()), 0)