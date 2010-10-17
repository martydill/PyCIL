from Instruction import Instruction
import unittest
from Stack import StackStateException
from Instructions.Instruction import register
from Variable import Variable

class clt(Instruction):

    def __init__(self, arguments = None):
        self.name = 'clt'
        self.opcode = 0x58

    def execute(self, vm):
        stack = vm.stack
        if stack.get_frame_count() < 2:
            raise StackStateException('Not enough values on the stack')

        v2 = stack.pop()
        v1 = stack.pop()
        if v1.value < v2.value:
            stack.push(Variable(1))
        else:
            stack.push(Variable(0))
        
        # fixme - floats?

register('clt', clt)

class cltTest(unittest.TestCase):

    def test_execute_not_enough_stack_values(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(1))
        x = clt()

        self.assertRaises(StackStateException, x.execute, vm)

    def test_execute_v1_less_than_v2_ints(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(5))
        vm.stack.push(Variable(999))
        x = clt()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 1)

    def test_execute_v1_greater_than_v2_ints(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(777))
        vm.stack.push(Variable(44))
        x = clt()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 0)

    def test_execute_equal_ints(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(555))
        vm.stack.push(Variable(555))
        x = clt()
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 0)
