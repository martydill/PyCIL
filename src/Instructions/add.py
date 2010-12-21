# add.py
# The CIL add instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
import unittest
from Stack import StackStateException
from Instructions.Instruction import register
from Variable import Variable


class add(Instruction):

    def __init__(self, arguments):
        self.name = 'add'
        self.opcode = 0x58

    def execute(self, vm):
        stack = vm.stack
        if stack.get_frame_count() < 2:
            raise StackStateException('Not enough values on the stack')

        rhs = stack.pop().value
        lhs = stack.pop().value
        stack.push(Variable(lhs + rhs))

register('add', add)


class addTest(unittest.TestCase):

    def test_execute_notEnoughStackValues(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(1))
        x = add('')

        self.assertRaises(StackStateException, x.execute, vm)

    def test_execute_ints(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(5))
        vm.stack.push(Variable(999))
        x = add('')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 999+5)

    def test_execute_floats(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(123.4))
        vm.stack.push(Variable(0.01))
        x = add('')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 123.4 + 0.01)
