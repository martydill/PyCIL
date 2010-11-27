from Instruction import Instruction
import unittest
from Stack import StackStateException
from Instructions.Instruction import register
from Variable import Variable


class pop(Instruction):

    def __init__(self, arguments):
        self.name = 'pop'
        self.opcode = 0x26

    def execute(self, vm):
        stack = vm.stack
        if stack.get_frame_count() < 1:
            raise StackStateException('Not enough values on the stack')

        stack.pop()

register('pop', pop)


class popTest(unittest.TestCase):

    def test_execute_notEnoughStackValues(self):
        from VM import VM
        vm = VM()
        x = pop('')

        self.assertRaises(StackStateException, x.execute, vm)

    def test_execute(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(5))
        x = pop('')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 0)
