from MethodDefinition import MethodDefinition
import unittest

ClassFlags = ['private', 'auto', 'ansi', 'beforefieldinit']

class ClassDefinition(object):
    
    def __init__(self):
        self.namespace = None
        self.name = None
        self.baseClass = None
        self.methods = []
        self.methods.append(self.get_constructor_definition())
        self.flags = []
        self.fieldDefinitions = []
        self.assemblyName = ''
        
    def get_constructor_definition(self):
        m = MethodDefinition()
        m.name = 'ctor'
        return m
        
        
class ClassDefinitionTest(unittest.TestCase):
    
    def test_class_definition_has_default_constructor(self):
        c = ClassDefinition()
        self.assertEqual(1, len(c.methods))
        self.assertEqual('ctor', c.methods[0].name)