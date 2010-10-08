from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from MethodDefinition import MethodDefinition
from Instructions.Instruction import register
from ClassDefinition import ClassDefinition
import Types
from ReferenceType import ReferenceType


class ldfld(Instruction):

    def __init__(self, field):
        self.name = 'ldfld.' + field
        self.field = field
        
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        if stack.get_frame_count() < 1:
            raise StackStateException('Not enough values on the stack')
        
        object = vm.stack.pop()
        for field in object.fields:
            if field.name == self.field:
                vm.stack.push(field)    # fixme - address...
                
        #variable = m.locals[self.index]
        #variable.value = stack.pop()

register('ldfld', ldfld)

class ldfldTest(unittest.TestCase):

    def test_execute_single_field(self):
        from VM import VM
        vm = VM()
        
        c = ClassDefinition()
        c.namespace = 'a'
        c.name = 'b'
        v = Variable()
        v.name = 'abc'
        v.type = Types.Int32
        
        c.fieldDefinitions.append(v)
        
        r = ReferenceType()
        t = Types.register_custom_type(c)
        r.type = t
        
        r.fields.append(v)
        vm.stack.push(r)
        
        x = ldfld('abc')
        
        x.execute(vm)
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(r.fields[0], vm.stack.pop())

    def test_execute_multiple_fields(self):
        from VM import VM
        vm = VM()
        
        c = ClassDefinition()
        c.namespace = 'a'
        c.name = 'b'
        
        v = Variable()
        v.name = 'abc'
        v.type = Types.Int32
        c.fieldDefinitions.append(v)

        v2 = Variable()
        v2.name = 'def'
        v2.type = Types.Int32
        c.fieldDefinitions.append(v2)
        
        r = ReferenceType()
        t = Types.register_custom_type(c)
        r.type = t
        
        r.fields.append(v)
        r.fields.append(v2)
        vm.stack.push(r)
        
        x = ldfld('def')
        
        x.execute(vm)
        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(r.fields[1], vm.stack.pop())
                