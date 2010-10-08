import unittest
from Variable import Variable
import Types
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
        return m
    
    
class MethodDefinitionTests(unittest.TestCase):
    
    def test_create_method_references_definition(self):
        md = MethodDefinition()
        md.name = 'foobar'
        v = Variable()
        v.name = 'asdf'
        v.type = Types.Int32
        
        md.locals.append(v)
        
        m = md.get_method()
        self.assertEqual(m.methodDefinition, md)

    def test_create_method_has_new_copy_of_locals(self):
        md = MethodDefinition()
        md.name = 'foobar'
        v = Variable()
        v.name = 'asdf'
        v.type = Types.Int32
        
        md.locals.append(v)
        
        m = md.get_method()
        self.assertEqual(len(m.locals), 1)
        self.assertNotEqual(v, m.locals[0])