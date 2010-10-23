from Instruction import Instruction
import unittest
import Types
from Method import Method
from Instructions.Instruction import register
from MethodDefinition import MethodDefinition
from Variable import Variable

class Ret(Instruction):
  
    def __init__(self, arguments = None):
        super(Ret, self).__init__()
        self.name = 'ret'
        self.opcode = 0x2A
        self.value = None

    def execute(self, vm):
        t = vm.current_method()

        if t.returnType != None and t.returnType != Types.Void:
            value = vm.stack.pop()
            vm.stack.endFrame()
            vm.stack.push(value)
        else:
            vm.stack.endFrame()
        
        # fixme - return value?


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

    def test_execute_instance_clears_stack_with_void_return_type(self):
        from VM import VM
        vm = VM()
        m = Method()
        m.name = 'TestMethod'
        m.attributes.append(MethodDefinition.AttributeTypes['instance'])
        m.returnType = Types.Void
        m.maxStack = 99
        m.parameters = []
        vm.methods.append(m)
        vm.stack.push(111)
        vm.execute_method(m)
        vm.stack.push(124)
        vm.stack.push(987)
        
        r = Ret()
        r.execute(vm)
        self.assertEqual(vm.current_method(), None)
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 111)
        
    def test_execute_int_no_parameters_returns_value_on_stack(self):
        from VM import VM
        vm = VM()
        m = Method()
        m.name = 'TestMethod'
        m.returnType = Types.Int32
        m.parameters = []
        vm.methods.append(m)

        v = Variable(888)
        self.assertEqual(vm.current_method(), None)
        self.assertEqual(vm.stack.get_frame_count(), 0)
        vm.execute_method(m)
        vm.stack.push(v)
        self.assertEqual(vm.current_method(), m)
        # fixme - test return value too
        r = Ret()
        r.execute(vm)
        self.assertEqual(vm.current_method(), None)
        self.assertEqual(vm.stack.get_frame_count(), 1)
        self.assertEqual(vm.stack.pop(), v)