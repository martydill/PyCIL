from Instruction import Instruction
import unittest
from Stack import StackStateException
from Instructions.Instruction import register
from Variable import Variable


class conv(Instruction):
    opcodePrefixTable = {
        'i1' : 0x67,
        'i2' : 0x68,
        'i4' : 0x69,
        'i8' : 0x6A,
        'r4' : 0x6B,
        'r8' : 0x6C,
        'u1' : 0xD2,
        'u2' : 0xD1,
        'u4' : 0x6D,
        'u8' : 0x6E,
        'i' : 0xD3,
        'u' : 0xE0,
        'r.u' : 0x76,
    }
    def __init__(self, arguments):
        self.name = 'conv'
   
        suffix = arguments
        if suffix.find(' ') != -1:
            parts = suffix.partition(' ')
            suffix = parts[0]
            self.value = parts[2]
            
        self.suffix = suffix
        self.opcode = conv.opcodePrefixTable[suffix]
        
    def execute(self, vm):
        stack = vm.stack
        if stack.get_frame_count() < 1:
            raise StackStateException('Not enough values on the stack')

        rhs = stack.pop().value
        lhs = stack.pop().value
        stack.push(Variable(lhs + rhs))

register('conv', conv)


class convTest(unittest.TestCase):

    def test_execute_notEnoughStackValues(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(1))
        x = conv('i1')

        self.assertRaises(StackStateException, x.execute, vm)

    def test_execute_ints(self):
        from VM import VM
        vm = VM()
        vm.stack.push(Variable(5))
        vm.stack.push(Variable(999))
        x = conv('')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 999+5)