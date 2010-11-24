'''
Helper instruction use to signal the end of try blocks
'''

import unittest
from Stack import StackStateException
from Instructions.Instruction import Instruction
from Variable import Variable

class EndTry(Instruction):

    def __init__(self, arguments):
        self.name = 'EndTry'

    def execute(self, vm):
        stack = vm.stack
       

class EndTryTest(unittest.TestCase):
  
    def test_execute_with_no_begin_try_throws_exception(self):
        from VM import VM
        vm = VM()
        x = EndTry('')
        
    def test_execute_ends_try_block(self):
        from VM import VM
        vm = VM()
        x = EndTry('')
        