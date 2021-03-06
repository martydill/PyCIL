# newobj.py
# The CIL newobj instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction
import unittest
import Types
from MethodDefinition import MethodDefinition
from Instructions.Instruction import register
from ClassDefinition import ClassDefinition
from ReferenceType import ReferenceType
from Variable import Variable


class newobj(Instruction):

    def __init__(self, arguments):
        self.name = 'newobj'
        self.opcode = 0x28 # fixme
        self.arguments = arguments
        params = arguments.split(' ')
        self.scope = params[0]
        self.returnType = params[1] # fixme - use actual type object?
        parts = params[2].split('::')
        self.typeName = parts[0]
        # fixme - parse ctor part? will it always be ctor?
        
    def execute(self, vm):
        t = Types.resolve_type(self.typeName)
        r = ReferenceType()
        r.type = t
        
        for f in t.classRef.fieldDefinitions:
            o = Variable()
            o.type = f.type
            o.name = f.name
            o.value = 0 # fixme - reference types?
            r.fields.append(o)
            r.fieldNames.append(f.name)
        
        vm.stack.push(r)
        
        namespace = t.namespace + '.' + t.name
        name = 'ctor'

        methodDefinition = vm.find_method_by_signature(namespace, name, None, None) # fixme - should name have a . in it?
        if methodDefinition is None:
            raise Exception("Couldn't find " + name + " method for " + namespace)

        
        m = methodDefinition.get_method()
        #parameter = Variable()
        #parameter.value = r
        m.parameters = [r] # fixme - create a new method object so we don't overwrite the parameters?
        #fixme - should we even use parameters? or just the stack?
        vm.execute_method(m)
        
        
register('newobj', newobj)

class newobjTest(unittest.TestCase):

    def test_newobj_no_parameters_calls_constructor(self):
        from VM import VM

        vm = VM()

        m = MethodDefinition()
        m.name = 'ctor'
        m.namespace = 'testnamespace.testclass'
        vm.methods.append(m)
        
        c = ClassDefinition()
        c.name = 'testclass'
        c.namespace = 'testnamespace'
        c.methods.append(m)
        
        t = Types.register_custom_type(c)

        n = newobj('instance void testnamespace.testclass::ctor()')
        n.execute(vm)
        Types.unregister_custom_type(t)
        
        o = vm.stack.pop()
        self.assertEqual(o.type, t)
        self.assertEquals(vm.current_method().methodDefinition, m)
        
    def test_newobj_no_parameters_adds_this_pointer_to_parameters(self):
        from VM import VM

        vm = VM()

        m = MethodDefinition()
        m.name = 'ctor'
        m.namespace = 'testnamespace.testclass'
        vm.methods.append(m)
        
        c = ClassDefinition()
        c.name = 'testclass'
        c.namespace = 'testnamespace'
        c.methods.append(m)
        
        t = Types.register_custom_type(c)

        n = newobj('instance void testnamespace.testclass::.ctor()')
        n.execute(vm)
        self.assertEqual(len(vm.current_method().parameters), 1)
        Types.unregister_custom_type(t)
        
    def test_newobj_no_parameters_initializes_int_field_to_zero(self):
        from VM import VM

        vm = VM()

        m = MethodDefinition()
        m.name = 'ctor'
        m.namespace = 'testnamespace.testclass'
        vm.methods.append(m)
        
        c = ClassDefinition()
        c.name = 'testclass'
        c.namespace = 'testnamespace'
        c.methods.append(m)
        
        v = Variable()
        v.name = 'xyz'
        v.type = Types.Int32
        
        c.fieldDefinitions.append(v)
        
        t = Types.register_custom_type(c)

        n = newobj('instance void testnamespace.testclass::.ctor()')
        n.execute(vm)
        Types.unregister_custom_type(t)
        
        o = vm.stack.pop()
        self.assertEqual(o.type, t)
        self.assertEqual(len(o.fields), 1)
        self.assertEqual(o.fields[0].value, 0)
        
        self.assertEqual(len(o.fieldNames), 1)
        self.assertEqual(o.fieldNames[0], 'xyz')