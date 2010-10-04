
UserDefinedTypes = []

NativeIntSize = 4
NativeFloatSize = 4
NativePointerSize = 4

def register_custom_type(c):
    t = Type(c.namespace + '.' + c.name)
    UserDefinedTypes.append(t)
    return t

def unregister_custom_type(t):
    UserDefinedTypes.remove(t)
    
def resolve_type(typename):
    for type in UserDefinedTypes:
        if type.namespace + '.' + type.name == typename:
            return type
        
    return None

class InvalidTypeException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Type():

    def __init__(self, typeName, dataSize = 0):
        parts = typeName.rpartition('.')
        self.namespace = parts[0]
        self.name = parts[2]
        self.dataSize = dataSize
        
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