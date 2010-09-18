from Instruction import Instruction
from VM import VM
import unittest
import Types
from Variable import Variable
from Method import Method

class call(Instruction):

    def __init__(self, method_name, method_type, method_parameters):
        self.name = 'call'
        self.method_name = method_name
        self.method_type = method_type
        self.method_parameters = method_parameters
        self.opcode = 0x28
        self.value = None

    def execute(self, vm):
        targetMethod = vm.find_method_by_signature(self.method_name, self.method_type, self.method_parameters)
        vm.execute_method(targetMethod)


class callTest(unittest.TestCase):

    def test_call_no_parameters(self):
        vm = VM()

        m = Method()
        m.name = 'TestMethod'
        m.returnType = Types.Void
        m.parameters = []
        vm.methods.append(m)

        self.assertEqual(vm.currentMethod, None)

        c = call('TestMethod', Types.Void, [])
        c.execute(vm)

        self.assertEqual(vm.currentMethod, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)
        
    def test_call_one_parameter(self):
        vm = VM()

        m = Method()
        m.name = 'TestMethod'
        m.returnType = Types.Void
        m.parameters = [Types.Int32]
        vm.methods.append(m)
        
        param = Variable()
        param.value = 123
        param.type = Types.Int32
        vm.stack.push(param)
        
        c = call('TestMethod', Types.Void, [Types.Int32])
        c.execute(vm)
        
        self.assertEqual(vm.currentMethod, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)
        self.assertEqual(vm.stack.pop(), param)
        
        