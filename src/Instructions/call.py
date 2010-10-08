from Instruction import Instruction

import unittest
import Types
from Variable import Variable
from Instructions.Instruction import register


class call(Instruction):

    def __init__(self, method):
        self.name = 'call'
        parts = method.split()
        if parts[0] == 'instance':
            self.instance = True
            parts.pop(0)
        else:
            self.instance = False
            
        self.method_type = Types.BuiltInTypes[parts[0]]
        self.method_namespace, self.method_name = parts[1].split('::')
        
        #self.method_name = method_name
        #self.method_type = method_type
        self.method_parameters = '' #method_parameters
        self.opcode = 0x28
        self.value = None

    def execute(self, vm):
        targetMethod = vm.find_method_by_signature(self.method_namespace, self.method_name, self.method_type, self.method_parameters)
        #fixme throw exception
        vm.execute_method(targetMethod)

register('call', call)

class callTest(unittest.TestCase):

    def test_call_no_parameters_int(self):
        from VM import VM
        from MethodDefinition import MethodDefinition
        vm = VM()

        m = MethodDefinition()
        m.name = 'TestMethod()'
        m.namespace = 'A.B'
        m.returnType = Types.Int32
        m.parameters = []
        m.names = 'A.B'
        vm.methods.append(m)

        self.assertEqual(vm.currentMethod, None)

        c = call('int32 A.B::TestMethod()')
        c.execute(vm)

        self.assertEqual(vm.currentMethod, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)
        
    def test_call_one_parameter_int(self):
        from VM import VM
        from MethodDefinition import MethodDefinition
        vm = VM()

        m = MethodDefinition()
        m.name = 'TestMethod()' # fixme - name shouldn't have brackets
        m.returnType = Types.Int32
        m.parameters = [Types.Int32]
        vm.methods.append(m)
        
        param = Variable()
        param.value = 123
        param.type = Types.Int32
        vm.stack.push(param)
        
        c = call('int32 A.B::TestMethod()')
        c.execute(vm)
        
        self.assertEqual(vm.currentMethod, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)
        self.assertEqual(vm.stack.pop(), param)
        
    def test_call_no_parameters_instance_int(self):
        from VM import VM
        from MethodDefinition import MethodDefinition
        vm = VM()

        m = MethodDefinition()
        m.name = 'TestMethod()'
        m.namespace = 'A.B'
        m.returnType = Types.Int32
        m.parameters = []
        m.names = 'A.B'
        vm.methods.append(m)

        self.assertEqual(vm.currentMethod, None)

        c = call('instance int32 A.B::TestMethod()')
        c.execute(vm)

        self.assertEqual(vm.currentMethod, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)