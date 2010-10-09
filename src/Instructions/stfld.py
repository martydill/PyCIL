from Instruction import Instruction
from Stack import Stack, StackStateException
import unittest
from Variable import Variable
from MethodDefinition import MethodDefinition
from Instructions.Instruction import register
from ClassDefinition import ClassDefinition
import Types
from ReferenceType import ReferenceType


class stfld(Instruction):

    def __init__(self, field):
        super(stfld, self).__init__() # fixme - set opcode
        self.name = 'stfld ' + field
        
        parts = field.split(' ')[1].rpartition('::')
        self.fieldName = parts[2]
        self.className = parts[0].rpartition('.')[2]
        self.namespaceName = parts[0].rpartition('.')[0]
        
    def execute(self, vm):
        stack = vm.stack
        m = vm.current_method()
        if stack.get_frame_count() < 2:
            raise StackStateException('Not enough values on the stack')
        
        value = vm.stack.pop()
        object = vm.stack.pop()
        for field in object.fields:
            if field.name == self.fieldName:
                field.value = value.value
                
        #variable = m.locals[self.index]
        #variable.value = stack.pop()

register('stfld', stfld)

class stfldTest(unittest.TestCase):

    def test_execute_int_parameter(self):
        from VM import VM
        vm = VM()
        
        c = ClassDefinition()
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
        vm.stack.push(Variable(9876))
        
        x = stfld('int32 a.b::xyz')
        
        x.execute(vm)
        self.assertEqual(vm.stack.count(), 0)
        self.assertEqual(r.fields[0].value, 9876)
        