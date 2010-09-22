from Instruction import Instruction
import unittest
from Instructions.ldc import ldc

class br(Instruction):

    def __init__(self, suffix):
        self.name = 'br' + suffix
        self.target = ''
        
        if suffix.startswith('.s'):
            self.suffix = '.s'
            self.opcode = 0x2b
        else:
            self.opcode = 0x38
            self.suffix = ''
            
    def execute(self, vm):
        stack = vm.stack
        index = vm.find_instruction_pointer_by_label(self.target)
        stack.currentFrame.instructionPointer = index


class brTest(unittest.TestCase):

    def testExecute(self):
        from VM import VM
        from Method import Method

        vm = VM()
        m = Method()
        x = ldc('.i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('.i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        x = br('') # fixme optional parameters
        x.target = 'asdf'
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        
        
    def testExecute_s(self):
        from VM import VM
        from Method import Method

        vm = VM()
        m = Method()
        x = ldc('.i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('.i4.3')
        dest.label = 'zzz'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        x = br('.s')
        x.target = 'zzz'
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
