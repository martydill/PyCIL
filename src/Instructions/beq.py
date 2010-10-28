from Instruction import Instruction
import unittest
from Instructions.ldc import ldc
from Instructions.Instruction import register
from Variable import Variable

class beq(Instruction):

    def __init__(self, args):
        self.name = 'beq.' + args
        
        if args.startswith('s'):
            self.suffix = '.s'
            self.target = args[2:]
            self.opcode = 0x2E
        else:
            self.opcode = 0x3B
            self.suffix = '' 
            self.target = args
            
    def execute(self, vm):
        # fixme check if there aren't enough stack values
        
        value2 = vm.stack.pop()
        value1 = vm.stack.pop()
        if value1.value == value2.value:
            index = vm.find_instruction_pointer_by_label(self.target)
            vm.current_stack_frame().instructionPointer = index
        # fixme - check for null objects

register('beq', beq)

class beqTest(unittest.TestCase):

    def test_execute_true(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        m.maxStack = 3
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(Variable(1))
        vm.stack.push(Variable(1))
        x = beq('asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        self.assertEqual(vm.stack.count(), 0)

    def test_execute_false(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        m.maxStack = 3
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(Variable(0))
        vm.stack.push(Variable(987))
        x = beq('asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(0, index);
        self.assertEqual(vm.stack.count(), 0)

        
    def test_execute_true_s(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        m.maxStack = 3
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(Variable(222))
        vm.stack.push(Variable(222))
        x = beq('s asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(3, index);
        self.assertEqual(vm.stack.count(), 0)

    def test_execute_false_s(self):
        from VM import VM
        from MethodDefinition import MethodDefinition

        vm = VM()
        m = MethodDefinition()
        m.maxStack = 3
        x = ldc('i4.1')
        m.instructions.append(x)
        m.instructions.append(x)
        m.instructions.append(x)
        dest = ldc('i4.3')
        dest.label = 'asdf'
        m.instructions.append(dest)
        
        vm.set_current_method(m)
        vm.stack.push(Variable(0))
        vm.stack.push(Variable(987))
        x = beq('s asdf') # fixme optional parameters
        x.execute(vm)

        index = vm.get_instruction_pointer()
        self.assertEqual(0, index);
        self.assertEqual(vm.stack.count(), 0)
