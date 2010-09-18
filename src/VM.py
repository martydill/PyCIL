from Stack import Stack
import Types
import unittest
from Method import Method
from Parser import Parser


class VM:

    def __init__(self):
        self.assemblies = []
        self.methods = []
        self.currentMethod = None
        self.stack = Stack(8)

    def start(self):
        pass

    def find_method_by_signature(self, name, returnType, params):
        for m in self.methods:
            if m.name == name and m.returnType == returnType and len(m.parameters) == len(params):
                equal = True
                for i in range(len(params)):
                    if params[i] != m.parameters[i]:
                        equal = False
                        break

                if equal:
                    return m

        return None
    
    def current_method(self):
        return self.stack.currentFrame.method
    
    def execute_method(self, method):
        self.stack.beginFrame(method.maxStack, method)
        self.currentMethod = method


class VMTest(unittest.TestCase):

    def test_find_when_empty(self):
        vm = VM()
        m = vm.find_method_by_signature('nonexistent', Types.Int8, [])
        self.assertEqual(m, None)

    def test_find_different_params(self):
        vm = VM()
        method = Method()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16, Types.Int32]
        vm.methods.append(method)
        m = vm.find_method_by_signature('hello', Types.Int8, [Types.Int8, Types.Int32])
        self.assertEqual(m, None)

    def test_find_different_return_type(self):
        vm = VM()
        method = Method()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16, Types.Int32]
        vm.methods.append(method)
        m = vm.find_method_by_signature('hello', Types.Int8, [])
        self.assertEqual(m, None)

    def test_find_different_name(self):
        vm = VM()
        method = Method()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16]
        vm.methods.append(method)
        m = vm.find_method_by_signature('hello2', Types.Int8, [Types.Int16])
        self.assertEqual(m, None)

    def test_find_match(self):
        vm = VM()
        method = Method()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16, Types.Int32]
        vm.methods.append(method)
        m = vm.find_method_by_signature('hello', Types.Int8, [Types.Int16, Types.Int32])
        self.assertEqual(m, method)
        
    def test_execute_method(self):
        vm = VM()
        method = Method()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16, Types.Int32]
        method.maxStack = 77
        
        self.assertEqual(vm.current_method(), None)
        
        vm.execute_method(method)
        self.assertEqual(vm.current_method(), method)
        self.assertEqual(vm.stack.get_frame_size(), 77)
        
        
    def test_parse_method_ret(self):
        s = ('.method public void main() {\n '
            '.locals init (int32 first,\n'
             'int32 second,\n'
             'int32 result)\n'
             'ret\n'
             ' }')
        
        vm = VM()
        p = Parser(s)
        m = p.parseMethod()
        
        locals = m.locals
        self.assertEqual(len(locals), 3)
        self.assertEqual(locals[0].name, 'first')
        self.assertEqual(locals[0].alias, None)
        self.assertEqual(locals[0].type, Types.Int32)
        self.assertEqual(locals[1].name, 'second')
        self.assertEqual(locals[1].alias, None)
        self.assertEqual(locals[1].type, Types.Int32)   
        self.assertEqual(locals[2].name, 'result')
        self.assertEqual(locals[2].alias, None)
        self.assertEqual(locals[2].type, Types.Int32)       

        self.assertEqual(len(m.instructions), 1)
        self.assertEqual('ret', m.instructions[0].name)

    def test_execute_method_add(self):
        s = ('.method public void main() {\n '
             'ldc.i4.1\n'
             'ldc.i4.5\n'
             'add\n'
             'ret\n'
             ' }')
        
        vm = VM()
        p = Parser(s)
        m = p.parseMethod()
        self.assertEqual(len(m.instructions), 4)
        
        vm.execute_method(m)
