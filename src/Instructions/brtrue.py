from Instruction import Instruction
import unittest
from Instructions.ldc import ldc
from Instructions.Instruction import register

class brtrue(Instruction):

    def __init__(self, suffix):
        self.name = 'brtrue' + suffix
        self.target = ''
        
        if suffix.startswith('s'):
            self.suffix = '.s'
            self.opcode = 0x2D
        else:
            self.opcode = 0x3A
            self.suffix = ''
            
    def execute(self, vm):
        # fixme check if there aren't enough stack values
        value = vm.stack.pop()
        if value != 0:
            index = vm.find_instruction_pointer_by_label(self.target)
            vm.current_stack_frame().instructionPointer = index
        # fixme - check for null objects

register('brtrue', brtrue)

class brtrueTest(unittest.TestCase):

    def test_execute_true(self):
        from VM import VM
        from Method import Method

        vm = VM()
        m = Method()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(1)
        x = brtrue('') # fixme optional parameters
        x.target = 'asdf'
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        self.assertEqual(vm.stack.count(), 0)

    def test_execute_false(self):
        from VM import VM
        from Method import Method

        vm = VM()
        m = Method()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(0)
        x = brtrue('') # fixme optional parameters
        x.target = 'asdf'
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(0, index);
        self.assertEqual(vm.stack.count(), 0)

        
    def test_execute_true_s(self):
        from VM import VM
        from Method import Method

        vm = VM()
        m = Method()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(1)
        x = brtrue('s') # fixme optional parameters
        x.target = 'asdf'
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        self.assertEqual(vm.stack.count(), 0)

    def test_execute_false_s(self):
        from VM import VM
        from Method import Method

        vm = VM()
        m = Method()
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(0)
        x = brtrue('s') # fixme optional parameters
        x.target = 'asdf'
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(0, index);
        self.assertEqual(vm.stack.count(), 0)
