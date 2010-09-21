from Instruction import Instruction
import unittest
import Types
from Method import Method

class Ret(Instruction):
  
    def __init__(self):
        self.name = 'ret'
        self.opcode = 0x2A
        self.value = None

    def execute(self, vm):
        vm.stack.endFrame()
        # fixme - return value?
        pass


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
