from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from MethodDefinition import MethodDefinition
from Instructions.Instruction import register
from Utility import is_number


class stloc(Instruction):

    opcodePrefixTable = {
        '0' : 0x0A,
        '1' : 0x0B,
        '2' : 0x0C,
        '3' : 0x0D,
        's' : 0x13
        # fixme - 16 bit index 
    }

    def __init__(self, suffix):
        super(stloc, self).__init__()
        self.name = 'stloc.' + suffix
        self.suffix = suffix
        self.index = 0
        self.targetName = None
        
        if(stloc.opcodePrefixTable.has_key(suffix)):
            self.opcode = stloc.opcodePrefixTable[suffix]
        
        if self.suffix == '0':
            self.index = 0
        elif self.suffix == '1':
            self.index = 1
        elif self.suffix == '2':
            self.index = 2
        elif self.suffix == '3':
            self.index = 3
        elif self.suffix.startswith('s '):
            if is_number(self.suffix[2:]): #index
                self.index = int(self.suffix[2:])
                self.op = stloc.opcodePrefixTable['s']
            else:   # label
                self.op = stloc.opcodePrefixTable['s']
                self.targetName = self.suffix[2:]
                
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        if stack.get_frame_count() < 1:
            raise StackStateException('Not enough values on the stack')
        
        if self.targetName is None:
            variable = m.locals[self.index]
        else:
            for x in m.locals:
                if x.name == self.targetName:
                    variable = x
            
        variable.value = stack.pop()            

register('stloc', stloc)

class stlocTest(unittest.TestCase):

    def test_execute_0(self):
        from VM import VM
        vm = VM()
        x = stloc('0')
        m = MethodDefinition()
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        vm.stack.push(987)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(m.locals[0].value, 987)

    def test_execute_1(self):
        from VM import VM
        vm = VM()
        x = stloc('1')
        m = MethodDefinition()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        vm.stack.push(987)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(m.locals[0].value, 0)
        self.assertEqual(m.locals[1].value, 987)
        
    def test_execute_2(self):
        from VM import VM
        vm = VM()
        x = stloc('2')
        m = MethodDefinition()
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

    def test_execute_3(self):
        from VM import VM
        vm = VM()
        x = stloc('3')
        m = MethodDefinition()
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
        
    def test_execute_s_index(self):
        from VM import VM
        vm = VM()
        x = stloc('s 2')
        m = MethodDefinition()
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
        
    def test_execute_s_label(self):
        from VM import VM
        vm = VM()
        x = stloc('s def')
        m = MethodDefinition()
        m.locals.append(Variable(0, name='xyz'))
        m.locals.append(Variable(0, name='abc'))
        m.locals.append(Variable(0, name='def'))
        m.locals.append(Variable(0, name='ghi'))
        vm.set_current_method(m)
        vm.stack.push(987)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(m.locals[0].value, 0)
        self.assertEqual(m.locals[1].value, 0)
        self.assertEqual(m.locals[2].value, 987)
        self.assertEqual(m.locals[3].value, 0)