# Types.py - PyCIL type handling
# Copyright 2010 Marty Dill
# See LICENSE for details

import unittest
from ClassDefinition import ClassDefinition
import Types

UserDefinedTypes = []
SystemTypes = []
Aliases = {}
NativeIntSize = 4
NativeFloatSize = 4
NativePointerSize = 4

def register_custom_type(c, is_system_type = False):
    '''Registers and returns a custom type based on the given class definition'''
    t = Type(c.namespace + '.' + c.name, c)
    t.assembly = c.assembly
    if is_system_type:
        SystemTypes.append(t)
    else:
        UserDefinedTypes.append(t)
        
    return t

def unregister_custom_type(t):
    '''Unregisters the given custom type'''
    UserDefinedTypes.remove(t)

def unregister_all_custom_types():
    '''Clears the list of user defined types'''
    del UserDefinedTypes[:]

def add_type_alias(type, alias):
    '''Adds an alias name for the given type (i.e. string for System.String)'''
    Aliases[alias] = type
    

def FindTypeInList(typeList, typename, assemblyName):
    resolvedType = None
    
    for type in typeList:
        if type.namespace + '.' + type.name == typename and assemblyName == type.assembly:
            resolvedType = type
    
    return resolvedType


def resolve_type(typename):
    '''Returns the type object corresponding to the given name. Throws an exception if it can't be found.'''
    
    # Handle array types
    isArray = False
    if typename.endswith('[]'):
        isArray = True
        typename = typename[0:-2]
    
    # Parse the assembly name    
    assemblyName = None
    if typename.startswith('['):
        assemblyName = typename[1:typename.find(']')]
        typename = typename[typename.find(']') + 1:]
        
    # Support types both directly and with this prefix (as per newobj instruction)
    if typename.endswith('::.ctor()'):
        typename = typename[:-9]
    
    resolvedType = None
    if BuiltInTypes.has_key(typename):
        resolvedType = BuiltInTypes[typename]
    elif Aliases.has_key(typename):
        resolvedType = Aliases[typename]
    else:
        resolvedType = FindTypeInList(UserDefinedTypes, typename, assemblyName)
        if resolvedType == None:
            resolvedType = FindTypeInList(SystemTypes, typename, assemblyName)
    
    # If we didn't find the type, throw an exception    
    if resolvedType == None:
        if assemblyName == None:
            assemblyName = '<no assembly specified>'
        if isArray:
            typename = typename + '[]' # fixme - use originalTypeName variable    
        raise Exception('Could not find type ' + typename + ' in assembly ' + assemblyName)
    else:
        if isArray:
            type = Type('array', 4)   # TODO - is this right? Should somehow be the built-in array type?
            type.arrayType = resolvedType
            return type
        else:
            return resolvedType
        
        
class InvalidTypeException(Exception):
    '''Exception that gets thrown when a type resolution operation fails'''
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Type():
    '''Stores information about types in the system'''
    
    def __init__(self, typeName, classRef, dataSize = 0):
        parts = typeName.rpartition('.')
        self.namespace = parts[0]
        self.name = parts[2]
        self.dataSize = dataSize
        self.classRef = classRef
        self.assembly = None
        self.arrayType = None
        
    def __str__(self):
        return self.name + ' (' + str(self.dataSize) + ' B)'


# Defined in ECMA-335 12.1 - Supported Data Types
BuiltInTypes = {
    'int8':Type('int8', 1),
    'uint8':Type('uint8', 1),
    'int16':Type('int16', 2),
    'uint16':Type('uint16', 2),
    'int32':Type('int32', 4),
    'uint32':Type('uint32', 4),
    'int64':Type('int64', 8),
    'uint64':Type('uint64', 8),
    'float32':Type('float32', 4),
    'float64':Type('float64', 8),
    'nativeint':Type('native int', NativeIntSize),
    'native unsigned int':Type('native unsigned int', NativeIntSize),
    'F':Type('F', NativeFloatSize),
    'O':Type('O', NativePointerSize),
    '&':Type('&', NativePointerSize),
    'void':Type('void', 0),
    'bool':Type('bool', 4)
}

# fixme - need a better method for defining aliases
#BuiltInTypes['System.Int32'] = BuiltInTypes['int32'] 

Int8 = BuiltInTypes['int8']
UInt8 = BuiltInTypes['uint8']
Int16 = BuiltInTypes['int16']
UInt16 = BuiltInTypes['uint16']
Int32 = BuiltInTypes['int32']
UInt32 = BuiltInTypes['uint32']
Int64 = BuiltInTypes['int64']
UInt64 = BuiltInTypes['uint64']
Float32 = BuiltInTypes['float32']
Float64 = BuiltInTypes['float64']
Void = BuiltInTypes['void']
Bool = BuiltInTypes['bool'] # CLR type, not VES type

Array = Type('array', 4)

# TODO - do these in a nicer place
c = ClassDefinition()
c.namespace = 'System'
c.name = 'Exception'
c.assembly = 'mscorlib'
register_custom_type(c, True)

c = ClassDefinition()
c.namespace = 'System'
c.name = 'String'
c.assembly = 'mscorlib'
stringType = register_custom_type(c, True)

add_type_alias(stringType, 'string')
add_type_alias(BuiltInTypes['int32'], 'int')
add_type_alias(BuiltInTypes['int32'], 'System.Int32')

class TypeTests(unittest.TestCase): 
    
    def test_resolve_builtin_type_returns_builtin_type(self):
        result = resolve_type('System.Int32')
        self.assertEqual(Int32, result)

    def test_resolve_type_array_returns_corect_array_type(self):
        result = resolve_type('System.Int32[]')
        self.assertEqual('array', result.name)
        self.assertEqual(Int32, result.arrayType)
                
    def test_resolve_mscorlib_type_returns_custom_type(self):
        from ClassDefinition import ClassDefinition
        c = ClassDefinition()
        c.namespace = 'System'
        c.name = 'FooBar'
        c.assembly = 'mscorlib'
        
        t = register_custom_type(c)
        result = resolve_type('[mscorlib]System.FooBar::.ctor()')
        self.assertEqual(t, result)
        unregister_custom_type(t)
    
    def test_resolve_string_array_aliased_type_returns_string_arrary_type(self):
        result = resolve_type('string[]')
        self.assertEqual(result.arrayType, resolve_type('string'))
       
    def test_int_types_are_equal(self):
        self.assertEqual(Types.Int32, BuiltInTypes['int32'])    
        self.assertEqual(Types.Int32, resolve_type('System.Int32'))
        self.assertEqual(Types.Int32, resolve_type('int'))