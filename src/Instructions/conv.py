from Instruction import Instruction
import unittest
from Stack import StackStateException
from Instructions.Instruction import register
from Variable import Variable
import Types


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

        input = stack.pop()
        result = None
        if self.suffix == 'i4':
            result = self.convert_to_i4(input)
        else:
            raise Exception('Unimplemented conversion ' + self.suffix)
        
        stack.push(result)

    def convert_to_i4(self, input):
        type = Types.Int32
        value = None
        if input.type == Types.UInt32:
            value = input.value # fixme - truncate/overflow/etc
        else:
            raise Exception('Unimplemented i4 conversion ' + input.type)
        result = Variable(value)
        result.type = type
        return result
    
register('conv', conv)


class convTest(unittest.TestCase):

    def test_execute_notEnoughStackValues(self):
        from VM import VM
        vm = VM()
        x = conv('i1')

        self.assertRaises(StackStateException, x.execute, vm)

    def test_execute_i4_no_overflow(self):
        from VM import VM
        vm = VM()
        v = Variable(999)
        v.type = Types.UInt32
        vm.stack.push(v)
        x = conv('i4')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        result = vm.stack.pop()
        self.assertEqual(result.value, 999)
        self.assertEqual(result.type, Types.Int32)