from Instruction import Instruction
import unittest

class ldc(Instruction):

    opcodePrefixTable = {
        '.i4' : 0x20,
        '.i8' : 0x21,
        '.r4' : 0x22,
        '.r8' : 0x23,
        '.i4.0' : 0x16,
        '.i4.1' : 0x17,
        '.i4.2' : 0x18,
        '.i4.3' : 0x19,
        '.i4.4' : 0x1A,
        '.i4.5' : 0x1B,
        '.i4.6' : 0x1C,
        '.i4.7' : 0x1D,
        '.i4.8' : 0x1E,
        '.i4.m1' : 0x15,
        '.i4.M1' : 0x15,
        '.i4.s' : 0x1F,
    }

    def __init__(self, suffix, value = None):
        
        self.name = 'ldc' + suffix
        self.suffix = suffix
        self.opcode = ldc.opcodePrefixTable[suffix]
        self.value = value
        self.label = '' # fixme
        
    def execute(self, vm):
        stack = vm.stack

        if self.suffix == '.i4':
            stack.push(int(self.value))
        elif self.suffix == '.i8':
            stack.push(long(self.value))
        elif self.suffix == '.r4':
            stack.push(float(self.value))
        elif self.suffix == '.r8':
            stack.push(float(self.value))
        elif self.suffix == '.i4.0':
            stack.push(0)
        elif self.suffix == '.i4.1':
            stack.push(1)
        elif self.suffix == '.i4.2':
            stack.push(2)
        elif self.suffix == '.i4.3':
            stack.push(3)
        elif self.suffix == '.i4.4':
            stack.push(4)
        elif self.suffix == '.i4.5':
            stack.push(5)
        elif self.suffix == '.i4.6':
            stack.push(6)
        elif self.suffix == '.i4.7':
            stack.push(7)
        elif self.suffix == '.i4.8':
            stack.push(8)
        elif self.suffix == '.i4.m1' or self.suffix == '.i4.M1':
            stack.push(-1)
        elif self.suffix == '.i4.s':
            stack.push(self.value)



class ldcTest(unittest.TestCase):

    def testExecute_i4(self):
        from VM import VM
        vm = VM()
        x = ldc('.i4', '12345')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 12345)

    def testExecute_i8(self):
        from VM import VM
        vm = VM()
        x = ldc('.i8', '999988887777')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 999988887777)

    def testExecute_r4(self):
        from VM import VM
        vm = VM()
        x = ldc('.r4', '1.234')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 1.234)


    def testExecute_r8(self):
        from VM import VM
        vm = VM()
        x = ldc('.r8', 999988887777.111122223333)
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 999988887777.111122223333)

    def testExecute_i4dot0(self):
        from VM import VM
        vm = VM()

        x = ldc('.i4.0')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 0)

    def testExecute_i4dot1(self):
        from VM import VM        
        vm = VM()

        x = ldc('.i4.1')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 1)

    def testExecute_i4dot2(self):
        from VM import VM        
        vm = VM()

        x = ldc('.i4.2')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 2)

    def testExecute_i4dot3(self):
        from VM import VM
        vm = VM()

        x = ldc('.i4.3')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 3)

    def testExecute_i4dot4(self):
        from VM import VM 
        vm = VM()

        x = ldc('.i4.4')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 4)

    def testExecute_i4dot5(self):
        from VM import VM 
        vm = VM()

        x = ldc('.i4.5')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 5)

    def testExecute_i4dot6(self):
        from VM import VM
        vm = VM()

        x = ldc('.i4.6')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 6)

    def testExecute_i4dot7(self):
        from VM import VM        
        vm = VM()

        x = ldc('.i4.7')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 7)

    def testExecute_i4dot8(self):
        from VM import VM
        vm = VM()

        x = ldc('.i4.8')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 8)

    def testExecute_i4dotm1(self):
        from VM import VM
        vm = VM()

        x = ldc('.i4.m1')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), -1)

    def testExecute_i4dotM1(self):
        from VM import VM
        vm = VM()

        x = ldc('.i4.M1')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), -1)

    def testExecute_i4dots(self):
        from VM import VM
        vm = VM()

        x = ldc('.i4.s')
        x.value = 123
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 123)
