# br.py
# The CIL br instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
import unittest
from Instructions.ldc import ldc
from Instructions.Instruction import register

class br(Instruction):

    def __init__(self, arguments):
        self.name = 'br'
        self.target = ''
        
        if arguments.startswith('s '):
            self.suffix = '.s'
            self.opcode = 0x2b
            self.target = arguments[2:]
        else:
            self.opcode = 0x38
            self.suffix = ''
            self.target = arguments
            
    def execute(self, vm):
        stack = vm.stack
        index = vm.find_instruction_pointer_by_label(self.target)
        vm.current_stack_frame().instructionPointer = index

register('br', br)

class brTest(unittest.TestCase):

    def test_br(self):
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
        x = br('asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        
        
    def test_br_s(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'zzz'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        x = br('s zzz')
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
