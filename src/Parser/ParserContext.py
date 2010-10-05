from Instructions.Ret import Ret
from Instructions.ldstr import ldstr

import Types
import unittest
from Instructions.ldc import ldc
from Instructions import sub
from Instructions.add import add
from Instructions.nop import nop
from Instructions.ldloc import ldloc
from Instructions.stloc import stloc
from Instructions.br import br
from Instructions.call import call
from Instructions.brtrue import brtrue
from Instructions.clt import clt
from Instructions.mul import mul
from Instructions.stfld import stfld
from Instructions.ldfld import ldfld

BlockStart = '{'
BlockEnd = '}'

class ParseException(Exception):
    pass

class ParserContext:

    def __init__(self, data = None):
        self.methods = []
        self.tokens = []
        self.classes = []
        
        if data != None:
            self.set_parse_data(data)
            
    def set_parse_data(self, data):
        self.lines = data.splitlines()
        
    def parse(self, fileData):
        
        self.set_parse_data(fileData)

        token = self.get_next_token()

        while token != '':

            #if line != '\n' and line != '\r':

            if token.startswith('.method'):
                from MethodParser import MethodParser
                mp = MethodParser();
                self.methods.append(mp.parse(self))
            elif token.startswith('.class'):
                from ClassParser import ClassParser
                cp = ClassParser()
                self.classes.append(cp.parse(self))
            token = self.get_next_token()

    def fill_token_buffer(self):
        while True:
            if len(self.lines) == 0:
                return
            line = self.lines.pop(0).strip()
            if line.startswith('//'):
                continue
            self.tokens = my_split(line, ['(', ')'])
            return
        
    def get_next_token(self):

        while True:
            if self.tokens is None or len(self.tokens) == 0 or self.tokens[0].startswith('//'):
                if len(self.lines) == 0:
                    return ''
                
                self.fill_token_buffer()
        
            if len(self.tokens) > 0:                 
                token = self.tokens.pop(0).strip()
                if len(token) > 0:
                    return token

    def peek_next_token(self):
        # fixme - won't work if token is on next line
        if len(self.tokens) == 0:
            self.fill_token_buffer()
        
        if len(self.tokens) == 0:
                return ''
            
        return self.tokens[-1]

    def read_to_end_of_line(self):
        result = ' '.join(self.tokens)
        self.tokens = None
        return result
 
   
def my_split(s, seps):
    splitters = [' ', ',']
    res = [s]
    for sep in splitters:
        s, res = res, []
        for seq in s:
            #res += seq.split(sep)
            temp = seq.split(sep)
            
            for string in temp:
                if len(string) == 0:
                    continue
                
                if string[0] in seps:
                    res += [string[0]]
                    if len(string) > 1:
                        res += [string[1:]]
                elif string[-1] in seps:
                    if len(string) > 1:
                        res += [string[0:-1]]
                    res += [string[-1]]
                else:
                    added = False
                    for i in range(len(string)):
                        c = string[i]
                        if c in seps:
                            res+= [string[0:i]]
                            res += [string[i + 1:]]
                            added = True
                            break
                    
                    if not added:
                        res += [string]
    return res

class parseTest(unittest.TestCase):

    def test_fill_token_buffer_with_comment_on_last_line(self):
        str = """ // this is a comment """
        
        p = ParserContext(str)
        p.fill_token_buffer()
        self.assertEqual(p.get_next_token(), '')
        
    def test_get_next_token_ignore_comments_after_statements(self):
        str = ('hello // comment 1 \n'
               '// comment 1\n'
               'world // comment 3\n'
               ' // comment 2\n'
               'abc // comment z') 
        
        p = ParserContext(str);
        self.assertEqual(p.get_next_token(), 'hello')
        self.assertEqual(p.get_next_token(), 'world')
        self.assertEqual(p.get_next_token(), 'abc')
        
    def test_get_next_token_ignore_comments(self):
        str = ('hello\n'
               '// comment 1\n'
               'world\n'
               ' // comment 2\n'
               'abc') 
        
        p = ParserContext(str);
        self.assertEqual(p.get_next_token(), 'hello')
        self.assertEqual(p.get_next_token(), 'world')
        self.assertEqual(p.get_next_token(), 'abc')
        
    def test_get_next_token_multiple_lines(self):
        str = ('hello\n'
               'world\n'
               'abc') 
        
        p = ParserContext(str);
        self.assertEqual(p.get_next_token(), 'hello')
        self.assertEqual(p.get_next_token(), 'world')
        self.assertEqual(p.get_next_token(), 'abc')
        
    def test_my_split_chars_on_end_of_words(self):
        str = 'hello (world abc)'
        result = my_split(str, ['(', ')'])
        
        self.assertEqual(len(result), 5)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], 'hello')
        self.assertEqual(result[1], '(')
        self.assertEqual(result[2], 'world')
        self.assertEqual(result[3], 'abc')
        self.assertEqual(result[4], ')')
        
    def test_my_split_locals_line(self):
        str =  'init (int32 j)'
        result = my_split(str, ['(', ')'])
        
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], 'init')
        self.assertEqual(result[1], '(')
        self.assertEqual(result[2], 'int32')
        self.assertEqual(result[3], 'j')
        self.assertEqual(result[4], ')')
        

    def test_peek_next_token(self):
        str = ('hello\n'
           'world\n'
           'abc') 
        
        p = ParserContext(str);
        self.assertEqual(p.get_next_token(), 'hello')
        self.assertEqual(p.peek_next_token(), 'world')
        self.assertEqual(p.get_next_token(), 'world')
        self.assertEqual(p.get_next_token(), 'abc')
        
#    def testParseMultipleMethods(self):
#
#        data = ('.method static void main()\n'
#        '{\n'
#        '    .entrypoint\n'
#        '    .maxstack 1\n'
#        '    ldstr "Hello world!"\n'
#        '    ret\n'
#        '}'
#        '\n'
#        '.method private hidebysig static void  Hello() cil managed\n'
#        '{\n'
#        '  .maxstack  8\n'
#        ' .locals init ([0] int32 j)'
#        'IL_0000:  ldarg.0'
#        'IL_0001:  ldc.i4.2'
#        'IL_0002:  mul'
#        'IL_0003:  stloc.0'
#        'IL_0004:  ldloc.0'
#        'IL_0005:  ret'
#        '}\n'
#        )
#
#
#        p = Parser()
#        p.parse(data)
#        self.assertEqual(len(p.methods), 2)
#
#        m = p.methods[0]
#        self.assertEqual(m.name, 'main()')
#        self.assertEqual(m.maxStack, 1)
#        self.assertTrue('static' in m.attributes)
#        self.assertTrue('.entrypoint' in m.attributes)
#        self.assertTrue(len(m.instructions), 2)
#
#        m = p.methods[1]
#        self.assertEqual(m.name, 'Hello()')
#        self.assertEqual(m.maxStack, 8)
#        self.assertTrue('static' in m.attributes)
#        self.assertTrue('.entrypoint' not in m.attributes)
#        self.assertTrue('cil' in m.attributes)
#        self.assertTrue('managed' in m.attributes)
#        self.assertTrue(len(m.instructions), 1)
#
#
#  


if __name__ == "__main__":
	unittest.main()

