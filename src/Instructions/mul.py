from Instruction import Instruction
import unittest
from Stack import StackStateException
from Instructions.Instruction import register

class mul(Instruction):

    def __init__(self, arguments):
        self.name = 'mul'
        self.opcode = 0x5A

    def execute(self, vm):
        stack = vm.stack
        if stack.get_frame_count() < 2:
            raise StackStateException('Not enough values on the stack')

        rhs = stack.pop()
        lhs = stack.pop()
        stack.push(lhs * rhs)
        # fixme - overflow

register('mul', mul)

class addTest(unittest.TestCase):

    def test_execute_not_enough_stack_values(self):
        from VM import VM
        vm = VM()
        vm.stack.push(1)
        x = mul()

        self.assertRaises(StackStateException, x.execute, vm)

    def test_execute_ints(self):
        from VM import VM
        vm = VM()
        vm.stack.push(5)
        vm.stack.push(999)
        x = mul()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 999 * 5)

    def test_execute_floats(self):
        from VM import VM
        vm = VM()
        vm.stack.push(123.4)
        vm.stack.push(0.01)
        x = mul()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 123.4 * 0.01)
