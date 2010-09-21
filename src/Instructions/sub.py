from Instruction import Instruction
import unittest
from Stack import StackStateException

class sub(Instruction):

    def __init__(self):
        self.name = 'sub'
        self.opcode = 0x59

    def execute(self, vm):
        stack = vm.stack
        if stack.get_frame_count() < 2:
            raise StackStateException('Not enough values on the stack')

        rhs = stack.pop()
        lhs = stack.pop()
        stack.push(lhs - rhs)


class subTest(unittest.TestCase):

    def testExecute_notEnoughStackValues(self):
        from VM import VM
        vm = VM()
        vm.stack.push(1)
        x = sub()

        self.assertRaises(StackStateException, x.execute, vm)

    def testExecute_ints(self):
        from VM import VM
        vm = VM()
        vm.stack.push(999)
        vm.stack.push(5)
        x = sub()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 999-5)

    def testExecute_floats(self):
        from VM import VM
        vm = VM()
        vm.stack.push(123.4)
        vm.stack.push(0.01)
        x = sub()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 123.4 - 0.01)
