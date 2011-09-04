# ldloc.py
# The CIL ldloc instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from MethodDefinition import MethodDefinition
from Instructions.Instruction import register
from Utility import is_number

class ldloc(Instruction):

    opcodePrefixTable = {
        '0' : 0x06,
        '1' : 0x07,
        '2' : 0x08,
        '3' : 0x09,
        's' : 0x11
        # fixme - 16 bit index 
    }


    def __init__(self, suffix):
        super(ldloc, self).__init__()
        self.name = 'ldloc.' + suffix
        self.suffix = suffix
        self.index = 0
        self.targetName = None
        
        if(ldloc.opcodePrefixTable.has_key(suffix)):
            self.opcode = ldloc.opcodePrefixTable[suffix]
        
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
                self.op = ldloc.opcodePrefixTable['s']
            else:   # label
                self.op = ldloc.opcodePrefixTable['s']
                self.targetName = self.suffix[2:]
                
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        
        if self.targetName is None:
            variable = m.locals[self.index]
        else:
            for x in m.locals:
                if x.name == self.targetName:
                    variable = x
            
        stack.push(variable)

register('ldloc', ldloc)

class ldlocTest(unittest.TestCase):

    def test_execute_0(self):
        from VM import VM
        vm = VM()
        x = ldloc('0')
        m = MethodDefinition()
        m.locals.append(Variable(987))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 987)

    def test_execute_1(self):
        from VM import VM
        vm = VM()
        x = ldloc('1')
        m = MethodDefinition()
        m.locals.append(Variable(0))
        m.locals.append(Variable(987))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 987)
        
    def test_execute_2(self):
        from VM import VM
        vm = VM()
        x = ldloc('2')
        m = MethodDefinition()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(8888))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 8888)

    def test_execute_3(self):
        from VM import VM
        vm = VM()
        x = ldloc('3')
        m = MethodDefinition()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(123))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 123)
        
    def test_execute_s_index(self):
        from VM import VM
        vm = VM()
        x = ldloc('s 2')
        m = MethodDefinition()
        m.locals.append(Variable(0))
        m.locals.append(Variable(0))
        m.locals.append(Variable(987))
        m.locals.append(Variable(0))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 987)

    def test_execute_s_label(self):
        from VM import VM
        vm = VM()
        x = ldloc('s ghi')
        m = MethodDefinition()
        m.locals.append(Variable(0, name='abc'))
        m.locals.append(Variable(0, name='def'))
        m.locals.append(Variable(987, name='ghi'))
        m.locals.append(Variable(0, name='jkl'))
        vm.set_current_method(m)
        x.execute(vm)
        
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop().value, 987)

