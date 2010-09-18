from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest

class add(Instruction):

    def __init__(self):
        self.name = 'add'
        self.opcode = 0x58

    def execute(self, vm):
        stack = vm.stack
        if stack.get_frame_count() < 2:
            raise StackStateException('Not enough values on the stack')

        rhs = stack.pop()
        lhs = stack.pop()
        stack.push(lhs + rhs)


class addTest(unittest.TestCase):

    def testExecute_notEnoughStackValues(self):
        from VM import VM
        vm = VM()
        vm.stack.push(1)
        x = add()

        self.assertRaises(StackStateException, x.execute, vm)

    def testExecute_ints(self):
        from VM import VM
        vm = VM()
        vm.stack.push(5)
        vm.stack.push(999)
        x = add()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 999+5)

    def testExecute_floats(self):
        from VM import VM
        vm = VM()
        vm.stack.push(123.4)
        vm.stack.push(0.01)
        x = add()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 123.4 + 0.01)
