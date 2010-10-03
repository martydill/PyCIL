from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from Method import Method
from Instructions.Instruction import register

class ldarg(Instruction):

    opcodePrefixTable = {
        '.0' : 0x02,
        '.1' : 0x03,
        '.2' : 0x04,
        '.3' : 0x05,
        '.s' : 0x0E
        # fixme - 16 bit index 
    }


    def __init__(self, suffix):
        self.name = 'ldarg' + suffix
        self.suffix = suffix
        self.index = 0
        if ldarg.opcodePrefixTable.has_key(suffix):
            self.opcode = ldarg.opcodePrefixTable[suffix]
        
        if self.suffix == '.0':
            self.index = 0
        elif self.suffix == '.1':
            self.index = 1
        elif self.suffix == '.2':
            self.index = 2
        elif self.suffix == '.3':
            self.index = 3
        elif self.suffix.startswith('.s '):
            self.index = int(self.suffix[3:])
            self.opcode = ldarg.opcodePrefixTable['.s']
        else:
            self.index = int(self.suffix)
            self.opcode = 0xFE09
        
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        
        variable = m.parameters[self.index]
        stack.push(variable.value) # fixme - value? or variable?

register('ldarg', ldarg)

class LdargTest(unittest.TestCase):

    def test_execute_0(self):
        from VM import VM
        vm = VM()
        x = ldarg('.0')
        m = Method()
        m.parameters.append(Variable(987))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 987)

    def test_execute_1(self):
        from VM import VM
        vm = VM()
        x = ldarg('.1')
        m = Method()
        m.parameters.append(Variable(0))
        m.parameters.append(Variable(987))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 987)
        
    def test_execute_2(self):
        from VM import VM
        vm = VM()
        x = ldarg('.2')
        m = Method()
        m.parameters.append(Variable(0))
        m.parameters.append(Variable(0))
        m.parameters.append(Variable(8888))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 8888)

    def test_execute_3(self):
        from VM import VM
        vm = VM()
        x = ldarg('.3')
        m = Method()
        m.parameters.append(Variable(0))
        m.parameters.append(Variable(0))
        m.parameters.append(Variable(0))
        m.parameters.append(Variable(123))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 123)
        
    def test_execute_s(self):
        from VM import VM
        vm = VM()
        x = ldarg('.s 2')
        m = Method()
        m.parameters.append(Variable(0))
        m.parameters.append(Variable(0))
        m.parameters.append(Variable(987))
        m.parameters.append(Variable(0))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 987)
