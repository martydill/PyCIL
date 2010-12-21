# nop.py
# The CIL nop instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
import unittest
import Types
from MethodDefinition import MethodDefinition
from Instructions.Instruction import register

class nop(Instruction):

    def __init__(self, arguments = None):
        self.name = 'nop'
        self.opcode = 0x28

    def execute(self, vm):
        pass

register('nop', nop)

class nopTes(unittest.TestCase):

    def test_nop(self):
        from VM import VM

        vm = VM()

        m = MethodDefinition()
        m.name = 'TestMethod'
        m.returnType = Types.Void
        m.parameters = []
        vm.methods.append(m)

        self.assertEqual(vm.currentMethod, None)

        c = nop()
        c.execute(vm)

        self.assertEqual(vm.stack.get_number_of_frames(), 1)
        