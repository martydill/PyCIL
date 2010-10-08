from Instruction import Instruction
import unittest
import Types
from Method import Method
from Instructions.Instruction import register

class Ret(Instruction):
  
    def __init__(self, arguments = None):
        self.name = 'ret'
        self.opcode = 0x2A
        self.value = None

    def execute(self, vm):
        t = vm.current_method()
        vm.stack.endFrame()
        if t.returnType is not None:
            vm.current_stack_frame().count += 1
        
        # fixme - return value?
        pass


register('ret', Ret)

class RetTest(unittest.TestCase):

    def test_execute_void_no_parameters(self):
        from VM import VM
        vm = VM()
        m = Method()
        m.name = 'TestMethod'
        m.returnType = Types.Void
        m.parameters = []
        vm.methods.append(m)

        self.assertEqual(vm.current_method(), None)
        
        vm.execute_method(m)
        self.assertEqual(vm.current_method(), m)
        
        r = Ret()
        r.execute(vm)
        self.assertEqual(vm.current_method(), None)

    def test_execute_int_no_parameters_increments_return_frame_count(self):
        from VM import VM
        vm = VM()
        m = Method()
        m.name = 'TestMethod'
        m.returnType = Types.Int32
        m.parameters = []
        vm.methods.append(m)

        self.assertEqual(vm.current_method(), None)
        self.assertEqual(vm.stack.get_frame_count(), 0)
        vm.execute_method(m)
        self.assertEqual(vm.current_method(), m)
        # fixme - test return value too
        r = Ret()
        r.execute(vm)
        self.assertEqual(vm.current_method(), None)
        self.assertEqual(vm.stack.get_frame_count(), 1)