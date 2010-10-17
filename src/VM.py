from Stack import Stack
import Types
import unittest
from Parser.ParserContext import ParserContext
from MethodDefinition import MethodDefinition
from Parser.MethodParser import MethodParser
from Method import Method
from Instructions.Ret import Ret

class DebugHooks:
    PreMethod, PostMethod, PreInstruction, PostInstruction = range(4)

class VM:

    def __init__(self):
        self.assemblies = []
        self.methods = []
        self.currentMethod = None
        self.stack = Stack(8)
        self.hooks = [None, None, None, None] 
        self.instructionPointer = 0
        
    def start(self):
        self.add_builtins()
        md = self.find_method_by_signature(None, 'Main', None, None)
        
        self.execute_method(md.get_method())
        pass
    
    def add_builtins(self):
        m = MethodDefinition()
        m.instructions.append(Ret())
        m.name = 'ctor'
        m.namespace = '[mscorlib]System.Object'
        m.returnType = Types.Void
        self.methods.append(m)
        
    def load(self, fileName):
        f = open(fileName, 'r')
        s = f.read()
        p = ParserContext()
        p.parse(s)
        self.methods = p.methods
        
    def find_instruction_pointer_by_label(self, label):
        for i in range(len(self.current_method().instructions)):
            instruction = self.current_method().instructions[i]
            if instruction.label == label:
                return i
            
        return -1
    
    #fixme - check for instance/static
    def find_method_by_signature(self, namespace, name, returnType, params):
        for m in self.methods:
            # fixme - namexpaces not parsed
            if namespace != None and m.namespace != namespace:
                continue
            if returnType != None and m.returnType != returnType:
                continue
            if name != None and m.name != name:
                continue
            if params == None:
                return m # fixme - shoudl always do checks
            if len(m.parameters) == len(params):
                equal = True
                for i in range(len(params)):
                    if params[i] != m.parameters[i]:
                        equal = False
                        break

                if equal:
                    return m

        raise "method not found"
        return None
    
    def current_method(self):
        return self.current_stack_frame().method
    
    def current_stack_frame(self):
        return self.stack.currentFrame;
    
    def set_current_method(self, method):
        self.stack.beginFrame(method.maxStack, method)
        self.currentMethod = method

    def execute_method(self, method):
        self.set_current_method(method)
        
        if self.hooks[DebugHooks.PreMethod] is not None:
            self.hooks[DebugHooks.PreMethod](method)
        
        frame = self.current_stack_frame()
        frame.instructionPointer = 0
        while frame == self.current_stack_frame() and frame.instructionPointer < len(method.instructions):
            
            instruction = method.instructions[self.current_stack_frame().instructionPointer]
            self.current_stack_frame().instructionPointer += 1 
            if self.hooks[DebugHooks.PreInstruction] is not None:
                self.hooks[DebugHooks.PreInstruction](instruction)
                
            instruction.execute(self)
        
            if self.hooks[DebugHooks.PostInstruction] is not None:
                self.hooks[DebugHooks.PostInstruction](instruction)

        if self.hooks[DebugHooks.PostMethod] is not None:
            self.hooks[DebugHooks.PostMethod](method)
        
    def add_hook(self, hookType, method):
        self.hooks[hookType] = method
    
    def remove_hook(self, hookType, method):
        self.hooks[hookType] = None        
        
    def get_instruction_pointer(self):
        return self.current_stack_frame().instructionPointer
    
class VMTest(unittest.TestCase):

    def test_find_when_empty(self):
        vm = VM()
        m = vm.find_method_by_signature(None, 'nonexistent', Types.Int8, [])
        self.assertEqual(m, None)

    def test_find_different_params(self):
        vm = VM()
        method = MethodDefinition()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16, Types.Int32]
        vm.methods.append(method)
        m = vm.find_method_by_signature(None, 'hello', Types.Int8, [Types.Int8, Types.Int32])
        self.assertEqual(m, None)

    def test_find_different_return_type(self):
        vm = VM()
        method = MethodDefinition()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16, Types.Int32]
        vm.methods.append(method)
        m = vm.find_method_by_signature(None, 'hello', Types.Int8, [])
        self.assertEqual(m, None)

    def test_find_different_name(self):
        vm = VM()
        method = MethodDefinition()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16]
        vm.methods.append(method)
        m = vm.find_method_by_signature(None, 'hello2', Types.Int8, [Types.Int16])
        self.assertEqual(m, None)

    def test_find_match(self):
        vm = VM()
        method = MethodDefinition()
        method.name = 'hello'
        method.returnType = Types.Int8
        method.parameters = [Types.Int16, Types.Int32]
        vm.methods.append(method)
        m = vm.find_method_by_signature(None, 'hello', Types.Int8, [Types.Int16, Types.Int32])
        self.assertEqual(m, method)
        
    def test_execute_method(self):
        vm = VM()
        md = MethodDefinition()
        md.name = 'hello'
        md.returnType = Types.Int8
        md.parameters = [Types.Int16, Types.Int32]
        md.maxStack = 77
        
        m = md.get_method()
        self.assertEqual(vm.current_method(), None)
        
        vm.execute_method(m)
        self.assertEqual(vm.current_method(), m)
        self.assertEqual(vm.stack.get_frame_size(), 77)
        
    def test_recursive_execute_method_each_instance_has_new_instance_variables(self):
        vm = VM()
        md = MethodDefinition()
        md.name = 'hello'
        md.returnType = Types.Int8
        md.parameters = [Types.Int16, Types.Int32]
        md.maxStack = 77
        
        self.assertEqual(vm.current_method(), None)
        
        m = md.get_method()
     
        vm.execute_method(m)
        self.assertEqual(vm.current_method(), m)
        self.assertEqual(vm.stack.get_frame_size(), 77)
        
        
        
    def test_parse_method_ret(self):
        s = ('.method public void main() {\n '
            '.locals init (int32 first,\n'
             'int32 second,\n'
             'int32 result)\n'
             'ret\n'
             ' }')
        
        vm = VM()
        p = ParserContext(s)
        mp = MethodParser()
        m = mp.parse(p)
        
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
        s = ('.method public int main() {\n '
             '.maxstack 10\n'
             'ldc.i4.1\n'
             'ldc.i4.5\n'
             'add\n'
             'ret\n'
             '}')
        
        vm = VM()
        p = ParserContext(s)
        mp = MethodParser()
        m = mp.parse(p)       
        vm.execute_method(m.get_method())
        #self.assertEqual(vm.stack.count(), 1) fixme
        self.assertEqual(vm.stack.lastFrameReturnValue.value, 6)
        
