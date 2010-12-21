# leave.py
# The CIL leave instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
import unittest
from Instructions.ldc import ldc
from Instructions.Instruction import register

class leave(Instruction):

    def __init__(self, arguments):
        self.name = 'leave'
        self.target = ''
        
        if arguments.startswith('s '):
            self.suffix = '.s'
            self.opcode = 0xdd
            self.target = arguments[2:]
        else:
            self.opcode = 0xde
            self.suffix = ''
            self.target = arguments
            
    def execute(self, vm):
        stack = vm.stack
        index = vm.find_instruction_pointer_by_label(self.target)
        vm.current_stack_frame().instructionPointer = index

register('leave', leave)

class leaveTest(unittest.TestCase):

    def test_leave(self):
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
        x = leave('asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        
        
    def test_leave_s(self):
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
        x = leave('s zzz')
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
