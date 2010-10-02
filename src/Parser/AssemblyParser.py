import unittest
from Assembly import Assembly

class AssemblyParser(object):
    
    def __init__(self):
        pass
    
    def parse(self, parserContext):
        assembly = Assembly()
        
        while True:
            token = parserContext.get_next_token()
            if token == 'extern':
                assembly.extern = True
                assembly.name = parserContext.get_next_token()
            elif token == '.ver':
                assembly.version = parserContext.get_next_token()
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
            ' .publickeytoken = (B7 7A 5C 56 19 34 E0 89 )                         // .z\V.4..\n'
            ' .ver 2:0:0:0\n'
            '}\n')
        
        ap = AssemblyParser()
        p = ParserContext(s);
        a = ap.parse(p)
        
        self.assertEqual(a.name, 'mscorlib')
        self.assertEqual(a.extern, True)
        self.assertEqual(a.version, '2:0:0:0')
        self.assertEqual(a.extern, True)