# ldc.py
# The CIL ldc instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
import unittest
from Instructions.Instruction import register
from Variable import Variable

class ldc(Instruction):

    opcodePrefixTable = {
        'i4' : 0x20,
        'i8' : 0x21,
        'r4' : 0x22,
        'r8' : 0x23,
        'i4.0' : 0x16,
        'i4.1' : 0x17,
        'i4.2' : 0x18,
        'i4.3' : 0x19,
        'i4.4' : 0x1A,
        'i4.5' : 0x1B,
        'i4.6' : 0x1C,
        'i4.7' : 0x1D,
        'i4.8' : 0x1E,
        'i4.m1' : 0x15,
        'i4.M1' : 0x15,
        'i4.s' : 0x1F,
    }

    def __init__(self, arguments):
        
        self.name = 'ldc.' + arguments
        self.value = None
        self.label = ''
        
        suffix = arguments
        if suffix.find(' ') != -1:
            parts = suffix.partition(' ')
            suffix = parts[0]
            self.value = parts[2]
            
        self.suffix = suffix
        self.opcode = ldc.opcodePrefixTable[suffix]
        
    def execute(self, vm):
        stack = vm.stack

        if self.suffix == 'i4':
            stack.push(Variable(self.string_to_number(self.value)))
        elif self.suffix == 'i8':
            stack.push(Variable(long(self.value)))
        elif self.suffix == 'r4':
            stack.push(Variable(float(self.value)))
        elif self.suffix == 'r8':
            stack.push(Variable(float(self.value)))
        elif self.suffix == 'i4.0':
            stack.push(Variable(0))
        elif self.suffix == 'i4.1':
            stack.push(Variable(1))
        elif self.suffix == 'i4.2':
            stack.push(Variable(2))
        elif self.suffix == 'i4.3':
            stack.push(Variable(3))
        elif self.suffix == 'i4.4':
            stack.push(Variable(4))
        elif self.suffix == 'i4.5':
            stack.push(Variable(5))
        elif self.suffix == 'i4.6':
            stack.push(Variable(6))
        elif self.suffix == 'i4.7':
            stack.push(Variable(7))
        elif self.suffix == 'i4.8':
            stack.push(Variable(8))
        elif self.suffix == 'i4.m1' or self.suffix == 'i4.M1':
            stack.push(Variable(-1))
        elif self.suffix == 'i4.s':
            stack.push(Variable(int(self.value)))

    def string_to_number(self, str):
        if str.startswith('0x'):
            return int(str, 16)
        else:
            return int(str)
        
register('ldc', ldc)

class ldcTest(unittest.TestCase):

    def test_execute_i4_hex(self):
        from VM import VM
        vm = VM()
        x = ldc('i4 0x4d2')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 0x4d2)

    def test_execute_i4(self):
        from VM import VM
        vm = VM()
        x = ldc('i4 12345')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 12345)

    def test_execute_i8(self):
        from VM import VM
        vm = VM()
        x = ldc('i8 999988887777')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 999988887777)

    def test_execute_r4(self):
        from VM import VM
        vm = VM()
        x = ldc('r4 1.234')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 1.234)


    def test_execute_r8(self):
        from VM import VM
        vm = VM()
        x = ldc('r8 999988887777.111122223333')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 999988887777.111122223333)

    def test_execute_i4dot0(self):
        from VM import VM
        vm = VM()

        x = ldc('i4.0')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 0)

    def test_execute_i4dot1(self):
        from VM import VM        
        vm = VM()

        x = ldc('i4.1')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 1)

    def test_execute_i4dot2(self):
        from VM import VM        
        vm = VM()

        x = ldc('i4.2')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 2)

    def test_execute_i4dot3(self):
        from VM import VM
        vm = VM()

        x = ldc('i4.3')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 3)

    def test_execute_i4dot4(self):
        from VM import VM 
        vm = VM()

        x = ldc('i4.4')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 4)

    def test_execute_i4dot5(self):
        from VM import VM 
        vm = VM()

        x = ldc('i4.5')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 5)

    def test_execute_i4dot6(self):
        from VM import VM
        vm = VM()

        x = ldc('i4.6')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 6)

    def test_execute_i4dot7(self):
        from VM import VM        
        vm = VM()

        x = ldc('i4.7')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 7)

    def test_execute_i4dot8(self):
        from VM import VM
        vm = VM()

        x = ldc('i4.8')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 8)

    def test_execute_i4dotm1(self):
        from VM import VM
        vm = VM()

        x = ldc('i4.m1')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, -1)

    def test_execute_i4dotM1(self):
        from VM import VM
        vm = VM()

        x = ldc('i4.M1')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, -1)

    def test_execute_i4dots(self):
        from VM import VM
        vm = VM()

        x = ldc('i4.s 123')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 123)
