'''
Helper instruction use to signal the start of catch blocks
'''

import unittest
from Stack import StackStateException
from Instructions.Instruction import Instruction
from Variable import Variable
from ProtectedBlock import ProtectedBlock


class BeginCatch(Instruction):

    def __init__(self, arguments = None):
        self.name = 'BeginCatch'

    def execute(self, vm):
        vm.get_protected_blocks().append(ProtectedBlock())
       

class BeginCatchTest(unittest.TestCase):

    def test_execute_starts_catch_block(self):
        from VM import VM
        vm = VM()
        x = Begincatch()
        x.execute(vm)
        self.assertEquals(len(vm.protected_blocks), 1)
        
    def test_execute_multiple_times_starts_nested_catch_blocks(self):
        from VM import VM
        vm = VM()
        x = BeginCatch()
        x.execute(vm)
        x.execute(vm)
        x.execute(vm)
        self.assertEquals(len(vm.protected_blocks), 3)