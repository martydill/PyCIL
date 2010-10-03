import unittest
from Class import Class
from Parser.MethodParser import MethodParser

class ClassParser(object):

    def parse(self, parserContext):
        c = Class()

        while True:
            token = parserContext.get_next_token()
            if token == '.method':
                m = MethodParser().parse(parserContext)            
                c.methods.append(m)
                
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
        self.assertEquals(len(c.methods), 1)
        
        