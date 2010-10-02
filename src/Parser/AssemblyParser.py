import unittest
from Assembly import Assembly
from Parser.ParserContext import ParseException
from Attribute import Attribute

class AssemblyParser(object):
    
    def __init__(self):
        pass
    
    def parse(self, parserContext):
        assembly = Assembly()
        
        token = parserContext.get_next_token()
        if token != '.assembly':
            raise ParseException('Expected .assembly, found ' . token)
        token = parserContext.get_next_token()
        if token == 'extern':
            assembly.extern = True
            token = parserContext.get_next_token()
        
        assembly.name = token
                
        while True:
            token = parserContext.get_next_token()
          
            if token == '.ver':
                assembly.version = parserContext.get_next_token()
            elif token == '.hash':
                if parserContext.get_next_token() != 'algorithm':
                    raise ParseException('Expected token "algorithm"')
                assembly.hashAlgorithm = int(parserContext.get_next_token(), 16)
            elif token == '.custom':
                if parserContext.get_next_token() != 'instance':
                    raise ParseException('Expected token "instance"')
                if parserContext.get_next_token() != 'void':
                    raise ParseException('Expected token "void"')
                attribute = Attribute()
                attribute.name = parserContext.get_next_token() + '(' + parserContext.get_next_token() + ')'
                assembly.customAttributes.append(attribute)
            elif token == '{':
                pass
            elif token == '}':
                break
        #fixme public key token
        return assembly
    
    
class AssemblyParserTests(unittest.TestCase):
    
    def test_parse_extern_assembly(self):
        from ParserContext import ParserContext
        s = ('// Metadata version: v2.0.50727\n'
            '.assembly extern mscorlib\n'
            '{\n'
            '.publickeytoken = (B7 7A 5C 56 19 34 E0 89 )                         // .z\V.4..\n'
            '.hash algorithm 0x00008004\n'
            '.ver 2:0:0:0\n'
            '}\n')
        
        ap = AssemblyParser()
        p = ParserContext(s);
        a = ap.parse(p)
        
        self.assertEqual(a.name, 'mscorlib')
        self.assertEqual(a.extern, True)
        self.assertEqual(a.version, '2:0:0:0')
        self.assertEqual(a.extern, True)
        self.assertEqual(a.hashAlgorithm, 0x8004)
        
    def test_parse_custom_attributes(self):
        from ParserContext import ParserContext
        s  = ('.assembly ConsoleApplication1\n'
              '{\n'
              '.custom instance void [mscorlib]System.Reflection.AssemblyTitleAttribute::.ctor(string) = ( 01 00 13 43 6F 6E 73 6F 6C 65 41 70 70 6C 69 63   // ...ConsoleApplic\n'
              '                                                                                             61 74 69 6F 6E 31 00 00 )\n'
              '.custom instance void [mscorlib]System.Reflection.AssemblyDescriptionAttribute::.ctor(string) = ( 01 00 00 00 00 ) \n'
              '}')
        
        ap = AssemblyParser()
        p = ParserContext(s)
        a = ap.parse(p)
        
        self.assertEqual(a.name, "ConsoleApplication1")
        self.assertEqual(len(a.customAttributes), 2)
        self.assertEqual(a.customAttributes[0].name, '[mscorlib]System.Reflection.AssemblyTitleAttribute::.ctor(string)')
        self.assertEqual(a.customAttributes[1].name, '[mscorlib]System.Reflection.AssemblyDescriptionAttribute::.ctor(string)')