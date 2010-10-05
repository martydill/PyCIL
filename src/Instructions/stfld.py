from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from Method import Method
from Instructions.Instruction import register
from Class import Class
import Types
from ReferenceType import ReferenceType


class stfld(Instruction):

    def __init__(self, field):
        self.name = 'stfld.' + field
        self.field = field
        
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        if stack.get_frame_count() < 2:
            raise StackStateException('Not enough values on the stack')
        
        value = vm.stack.pop()
        object = vm.stack.pop()
        for field in object.fields:
            if field.name == self.field:
                field.value = value
                
        #variable = m.locals[self.index]
        #variable.value = stack.pop()

register('stfld', stfld)

class stfldTest(unittest.TestCase):

    def test_execute_int_parameter(self):
        from VM import VM
        vm = VM()
        
        c = Class()
        c.namespace = 'a'
        c.name = 'b'
        v = Variable()
        v.name = 'xyz'
        v.type = Types.Int32
        
        c.fieldDefinitions.append(v)
        
        r = ReferenceType()
        t = Types.register_custom_type(c)
        r.type = t
        
        r.fields.append(v)
        vm.stack.push(r)
        vm.stack.push(9876)
        
        x = stfld('xyz')
        
        x.execute(vm)
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(r.fields[0].value, 9876)
        