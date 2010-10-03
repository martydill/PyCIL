from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from Method import Method
from Instructions.Instruction import register


class stloc(Instruction):

    opcodePrefixTable = {
        '.0' : 0x0A,
        '.1' : 0x0B,
        '.2' : 0x0C,
        '.3' : 0x0D,
        '.s' : 0x13
        # fixme - 16 bit index 
    }

    def __init__(self, suffix):
        self.name = 'stloc' + suffix
        self.suffix = suffix
        self.index = 0
        if(stloc.opcodePrefixTable.has_key(suffix)):
            self.opcode = stloc.opcodePrefixTable[suffix]
        
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
            self.op = stloc.opcodePrefixTable['.s']
            
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        if stack.get_frame_count() < 1:
            raise StackStateException('Not enough values on the stack')
        
        variable = m.locals[self.index]
        variable.value = stack.pop()

register('stloc', stloc)

class stlocTest(unittest.TestCase):

    def testExecute_0(self):
        from VM import VM
        vm = VM()
        x = stloc('.0')
        m = Method()
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        vm.stack.push(987)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(m.locals[0].value, 987)

    def testExecute_1(self):
        from VM import VM
        vm = VM()
        x = stloc('.1')
        m = Method()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        vm.stack.push(987)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(m.locals[0].value, 0)
        self.assertEqual(m.locals[1].value, 987)
        
    def testExecute_2(self):
        from VM import VM
        vm = VM()
        x = stloc('.2')
        m = Method()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        vm.stack.push(987)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(m.locals[0].value, 0)
        self.assertEqual(m.locals[1].value, 0)
        self.assertEqual(m.locals[2].value, 987)

    def testExecute_3(self):
        from VM import VM
        vm = VM()
        x = stloc('.3')
        m = Method()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        vm.stack.push(987)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(m.locals[0].value, 0)
        self.assertEqual(m.locals[1].value, 0)
        self.assertEqual(m.locals[2].value, 0)
        self.assertEqual(m.locals[3].value, 987)
        
    def testExecute_s(self):
        from VM import VM
        vm = VM()
        x = stloc('.s 2')
        m = Method()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        vm.stack.push(987)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(m.locals[0].value, 0)
        self.assertEqual(m.locals[1].value, 0)
        self.assertEqual(m.locals[2].value, 987)
        self.assertEqual(m.locals[3].value, 0)