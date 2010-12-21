# brtrue.py
# The CIL brtrue instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
import unittest
from Instructions.ldc import ldc
from Instructions.Instruction import register
from Variable import Variable

class brtrue(Instruction):

    def __init__(self, args):
        self.name = 'brtrue.' + args
        
        if args.startswith('s'):
            self.suffix = '.s'
            self.target = args[2:]
            self.opcode = 0x2D
        else:
            self.opcode = 0x3A
            self.suffix = '' 
            self.target = args
            
    def execute(self, vm):
        # fixme check if there aren't enough stack values
        
        variable = vm.stack.pop()
        if variable.value != 0:
            index = vm.find_instruction_pointer_by_label(self.target)
            vm.current_stack_frame().instructionPointer = index
        # fixme - check for null objects

register('brtrue', brtrue)

class brtrueTest(unittest.TestCase):

    def test_execute_true(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(Variable(1))
        x = brtrue('asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        self.assertEqual(vm.stack.count(), 0)

    def test_execute_false(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(Variable(0))
        x = brtrue('asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(0, index);
        self.assertEqual(vm.stack.count(), 0)

        
    def test_execute_true_s(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(Variable(1))
        x = brtrue('s asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        self.assertEqual(vm.stack.count(), 0)

    def test_execute_false_s(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(Variable(0))
        x = brtrue('s asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(0, index);
        self.assertEqual(vm.stack.count(), 0)
