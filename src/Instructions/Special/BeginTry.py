'''
Helper instruction use to signal the start of try blocks
'''

import unittest
from Stack import StackStateException
from Instructions.Instruction import Instruction
from Variable import Variable
from ProtectedBlock import ProtectedBlock


class BeginTry(Instruction):

    def __init__(self, arguments = None):
        self.name = 'BeginTry'
        self.label = None
        
    def execute(self, vm):
        vm.get_protected_blocks().append(ProtectedBlock())
       

class BeginTryTest(unittest.TestCase):

    def test_execute_starts_try_block(self):
        from VM import VM
        vm = VM()
        x = BeginTry()
        x.execute(vm)
        self.assertEquals(len(vm.protected_blocks), 1)
        
    def test_execute_multiple_times_starts_nested_try_blocks(self):
        from VM import VM
        vm = VM()
        x = BeginTry()
        x.execute(vm)
        x.execute(vm)
        x.execute(vm)
        self.assertEquals(len(vm.protected_blocks), 3)