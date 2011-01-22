import unittest
from Variable import Variable
from Method import Method
import copy


class MethodDefinition():

    AttributeTypes = {
        'static':0,
        'cil':1,
        'managed':2,
        'public':3,
        'private':4,
        'hidebysig':5,
        'cil':6,
        'specialname':7,
        'rtspecialname':8,
        'instance':9
    }

    def __init__(self):
        self.name = 'unnamed'
        self.namespace = None
        self.attributes = []
        self.maxStack = 1
        self.locals = []
        self.returnType = None
        self.instructions = []
        self.parameters = []

    def get_method(self):
        m = Method()
        m.methodDefinition = self;
        m.locals = copy.deepcopy(self.locals)
        #m.parameters= copy.deepcopy(self.parameters)
        m.instructions = self.instructions
        m.maxStack = self.maxStack
        m.returnType = self.returnType
        m.attributes = self.attributes
        return m
    
    def __str__(self):
        return self.returnType + ' ' + self.namespace + '::' + self.name
    
class MethodDefinitionTests(unittest.TestCase):
    
    def test_create_method_references_definition(self):
        import Types
        md = MethodDefinition()
        md.name = 'foobar'
        v = Variable()
        v.name = 'asdf'
        v.type = Types.Int32
        
        md.locals.append(v)
        
        m = md.get_method()
        self.assertEqual(m.methodDefinition, md)

    def test_create_method_has_new_copy_of_locals(self):
        import Types
        md = MethodDefinition()
        md.name = 'foobar'
        v = Variable()
        v.name = 'asdf'
        v.type = Types.Int32
        
        md.locals.append(v)
        
        m = md.get_method()
        self.assertEqual(len(m.locals), 1)
        self.assertNotEqual(v, m.locals[0])
        
    def test_create_method_has_new_copy_of_locals(self):
        import Types
        md = MethodDefinition()
        md.name = 'foobar'
        v = Variable()
        v.name = 'asdf'
        v.type = Types.Int32
        
        md.parameters.append(v)
        
        m = md.get_method()
        self.assertEqual(len(m.parameters), 1)
        self.assertNotEqual(v, m.parameters[0])
        
    def test_create_method_has_pointer_to_instructions(self):
        import Types
        from Instructions.Ret import Ret
        md = MethodDefinition()
        md.name = 'foobar'
        v = Variable()
        v.name = 'asdf'
        v.type = Types.Int32
        md.instructions.append(Ret())
        md.instructions.append(Ret())
        md.instructions.append(Ret())
        
        m = md.get_method()
        self.assertEqual(m.instructions, md.instructions)
        
    def test_create_method_has_reference_type_instead_of_value(self):
        from Instructions.Ret import Ret
        import Types
        md = MethodDefinition()
        md.name = 'foobar'
        v = Variable()
        v.name = 'asdf'
        v.type = Types.Int32
        md.instructions.append(Ret())
        md.instructions.append(Ret())
        md.instructions.append(Ret())
        
        m = md.get_method()
        self.assertEqual(m.instructions, md.instructions)
