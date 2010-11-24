'''
Helper instruction use to signal the start of try blocks
'''

import unittest
from Stack import StackStateException
from Instructions.Instruction import Instruction
from Variable import Variable


class BeginTry(Instruction):

    def __init__(self, arguments):
        self.name = 'BeginTry'

    def execute(self, vm):
        stack = vm.stack
       

class BeginTryTest(unittest.TestCase):

    def test_execute_starts_try_block(self):
        from VM import VM
        vm = VM()
        x = BeginTry('')
        