from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from Method import Method
from Instructions.Instruction import register

class ldloc(Instruction):

    opcodePrefixTable = {
        '.0' : 0x06,
        '.1' : 0x07,
        '.2' : 0x08,
        '.3' : 0x09,
        '.s' : 0x11
        # fixme - 16 bit index 
    }


    def __init__(self, suffix):
        self.name = 'ldloc' + suffix
        self.suffix = suffix
        self.index = 0
        if(ldloc.opcodePrefixTable.has_key(suffix)):
            self.opcode = ldloc.opcodePrefixTable[suffix]
        
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
            self.opcode = ldloc.opcodePrefixTable['.s']
            
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        
        variable = m.locals[self.index]
        stack.push(variable.value) # fixme - value? or variable?

register('ldloc', ldloc)

class ldlocTest(unittest.TestCase):

    def testExecute_0(self):
        from VM import VM
        vm = VM()
        x = ldloc('.0')
        m = Method()
        m.locals.append(Variable(987))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 987)

    def testExecute_1(self):
        from VM import VM
        vm = VM()
        x = ldloc('.1')
        m = Method()
        m.locals.append(Variable(0))
        m.locals.append(Variable(987))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 987)
        
    def testExecute_2(self):
        from VM import VM
        vm = VM()
        x = ldloc('.2')
        m = Method()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(8888))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 8888)

    def testExecute_3(self):
        from VM import VM
        vm = VM()
        x = ldloc('.3')
        m = Method()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(123))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 123)
        
    def testExecute_s(self):
        from VM import VM
        vm = VM()
        x = ldloc('.s 2')
        m = Method()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(987))
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 987)
