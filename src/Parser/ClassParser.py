import unittest
from ClassDefinition import ClassDefinition, ClassFlags
from Parser.MethodParser import MethodParser
from Variable import Variable
from Types import Type
import Types

class ClassParser(object):

    def parse(self, parserContext):
        c = ClassDefinition()

        while True:
            token = parserContext.get_next_token()
            if token in ClassFlags:
                c.flags.append(token)
            elif token == 'extends':
                c.base = parserContext.get_next_token()
            elif token == '.method':
                m = MethodParser().parse(parserContext)
                m.namespace = c.namespace + '.' + c.name       
                c.methods.append(m)
                parserContext.methods.append(m)
                # fixme - should i add to both?
            elif token == '.field':
                v = Variable()
                visibility = parserContext.get_next_token()
                type = parserContext.get_next_token() # fixme - type, visibility
                if type == 'class':
                    type = parserContext.get_next_token()
                
                if Types.BuiltInTypes.has_key(type):
                    v.type = Types.BuiltInTypes[type]
                else:
                    v.type = Types.resolve_type(type)
                    
                name = parserContext.get_next_token()
               
                v.name = name
                c.fieldDefinitions.append(v)
            elif token == '}':
                break
            elif token != '{':
                fullyQualifiedName = token.split('.')
                c.name = fullyQualifiedName[-1]
                c.namespace = '.'.join(fullyQualifiedName[:-1])
                
        Types.register_custom_type(c)
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
        
    def test_parse_class_registers_type(self):
        from ParserContext import ParserContext
        s = ('.class private auto ansi beforefieldinit ConsoleApplication1.bar\n'
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
     '} // end of class ConsoleApplication1.bar\n')

        p = ParserContext(s)
        cp = ClassParser()
        c = cp.parse(p)
        
        self.assertEqual(Types.resolve_type('ConsoleApplication1.bar').classRef, c)
   
    def test_method_in_class_gets_class_namespace(self):
        from ParserContext import ParserContext
        s = '''.class private auto ansi beforefieldinit ConsoleApplication1.foo
        extends [mscorlib]System.Object
        {
          .field public int32 z
          .method public hidebysig specialname rtspecialname 
                  instance void  .ctor() cil managed
          {
            // Code size       7 (0x7)
            .maxstack  8
            IL_0000:  ldarg.0
            IL_0001:  call       instance void [mscorlib]System.Object::.ctor()
            IL_0006:  ret
          } // end of method foo::.ctor
       } // end of class ConsoleApplication1.foo'''
        
        p = ParserContext(s)
        cp = ClassParser()
        c = cp.parse(p)
        
        self.assertEqual(c.methods[0].name, 'ctor')
        self.assertEqual(c.methods[0].namespace, 'ConsoleApplication1.foo' )

    def test_parse_class_with_class_field(self):
        from ParserContext import ParserContext
        s = '''
            .class private auto ansi beforefieldinit ConsoleApplication1.bar
                   extends [mscorlib]System.Object
            {
              .field public class ConsoleApplication1.foo f
              .method public hidebysig specialname rtspecialname 
                      instance void  .ctor() cil managed
              {
                // Code size       7 (0x7)
                .maxstack  8
                IL_0000:  ldarg.0
                IL_0001:  call       instance void [mscorlib]System.Object::.ctor()
                IL_0006:  ret
              } // end of method bar::.ctor
            
            } // end of class ConsoleApplication1.bar'''

        p = ParserContext(s)
        cp = ClassParser()
        c = cp.parse(p)
        
        self.assertEqual(c.methods[0].name, 'ctor')
        self.assertEqual(c.methods[0].namespace, 'ConsoleApplication1.bar' )
        self.assertEquals(len(c.fieldDefinitions), 1)
        f = c.fieldDefinitions[0]
        self.assertEqual(f.name, 'f')
        self.assertEqual(f.type, Types.resolve_type('ConsoleApplication1.foo'))