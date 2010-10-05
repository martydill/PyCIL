import unittest
from Class import Class, ClassFlags
from Parser.MethodParser import MethodParser
from Variable import Variable
from Types import Type
import Types

class ClassParser(object):

    def parse(self, parserContext):
        c = Class()

        while True:
            token = parserContext.get_next_token()
            if token in ClassFlags:
                c.flags.append(token)
            elif token == 'extends':
                c.base = parserContext.get_next_token()
            elif token == '.method':
                m = MethodParser().parse(parserContext)            
                c.methods.append(m)
            elif token == '.field':
                v = Variable()
                visibility = parserContext.get_next_token()
                type = parserContext.get_next_token() # fixme - type, visibility
                if Types.BuiltInTypes.has_key(type):
                    v.type = Types.BuiltInTypes[type]
                name = parserContext.get_next_token()
               
                v.name = name
                c.fieldDefinitions.append(v)
            elif token == '}':
                break
            elif token != '{':
                fullyQualifiedName = token.split('.')
                c.name = fullyQualifiedName[-1]
                c.namespace = '.'.join(fullyQualifiedName[:-1])
                
        return c
        
class ClassParserTests(unittest.TestCase):
    
    def test_parse_empty_class(self):
        from ParserContext import ParserContext
        s = ('.class private auto ansi beforefieldinit ConsoleApplication1.foo\n'
        '   extends [mscorlib]System.Object\n'
        '{\n'
        '.method public hidebysig specialname rtspecialname\n' 
        '        instance void  .ctor() cil managed\n'
        '{\n'
        '  // Code size       7 (0x7)\n'
        '  .maxstack  8\n'
        '  IL_0000:  ldarg.0\n'
        '  IL_0001:  call       instance void [mscorlib]System.Object::.ctor()\n'
        '  IL_0006:  ret\n'
        '} // end of method foo::.ctor\n'
     '} // end of class ConsoleApplication1.foo\n')

        p = ParserContext(s)
        cp = ClassParser()
        c = cp.parse(p)
        
        self.assertEquals(c.name, 'foo')
        self.assertEqual(c.namespace, 'ConsoleApplication1')
        self.assertEquals(len(c.methods), 1)
        self.assertEqual(len(c.flags), 4)
        
    def test_parse_class_with_field(self):
        from ParserContext import ParserContext
        s = ('.class private auto ansi beforefieldinit ConsoleApplication1.foo\n'
        '   extends [mscorlib]System.Object\n'
        '{\n'
        '  .field public int32 z\n'
        '} // end of class ConsoleApplication1.foo\n')

        p = ParserContext(s)
        cp = ClassParser()
        c = cp.parse(p)
        
        self.assertEquals(c.name, 'foo')
        self.assertEqual(c.namespace, 'ConsoleApplication1')
        self.assertEquals(len(c.fieldDefinitions), 1)
        f = c.fieldDefinitions[0]
        self.assertEqual(f.name, 'z')
        self.assertEqual(f.type, Types.Int32)    