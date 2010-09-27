from Instructions.Ret import Ret
from Instructions.ldstr import ldstr
from Method import Method
from Variable import Variable
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

BlockStart = '{'
BlockEnd = '}'

class ParseException(Exception):
    pass

class Parser:

    def __init__(self, data = None):
        self.methods = []
        self.tokens = []
        
        if data != None:
            self.set_parse_data(data)
            
    def set_parse_data(self, data):
        self.lines = data.splitlines()
        
    def parse(self, fileData):
        
        self.set_parse_data(fileData)

        token = self.getNextToken()

        while token != '':

            #if line != '\n' and line != '\r':

            if token.startswith('.method'):
                self.methods.append(self.parseMethod())

            token = self.getNextToken()

    def fill_token_buffer(self):
        if len(self.lines) == 0:
            return
        while True:
            line = self.lines.pop(0).strip()
            if line.startswith('//'):
                continue
            self.tokens = my_split(line, ['(', ')'])
            return
        
    def getNextToken(self):

        while True:
            if self.tokens is None or len(self.tokens) == 0:
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
        
    def parseLocals(self):
        locals = []
        token = self.getNextToken()
        if token != 'init':
            raise ParseException('Expected init, found ' + token) # fixme - only required for verifiable methods
        token = self.getNextToken()
        if token != '(':
            raise ParseException('Expected (, found' + token)
        token = self.getNextToken()
        lastToken = ''
        while not token.endswith(')'):
            v = Variable()
            locals.append(v)
            if token.startswith('['):
                v.alias = token[1:-1]
                lastToken = token
                token = self.getNextToken()
            v.type = Types.BuiltInTypes[token] # fixme - non-builtin types
            lastToken = token
            token = self.getNextToken()
            #if token.endswith(')'):
            #    v.name = token[:-1]
            #    token = ')'
            #else:
            v.name = token
            lastToken= token
            token = self.getNextToken()
            
        return locals
    
    def parseMethod(self):
        method = Method()

        token = self.getNextToken()

        while token != BlockStart:

            print '*' + token + '*'
            if token == '(':
                self.parse_parameters(method)
            elif token in Method.AttributeTypes.keys():
                method.attributes.append(token)
            elif token in Types.BuiltInTypes:
                method.returnType = Types.BuiltInTypes[token]
            elif token == '.method':
                pass
            else:
                method.name = token
                self.parse_parameters(method)
                
            token = self.getNextToken()

        token = self.getNextToken()
        while token != BlockEnd:
            print token
            if token == '.maxstack':
                method.maxStack = int(self.getNextToken())
            elif token == '.entrypoint':
                method.attributes.append(token)
            elif token == '.locals':
                method.locals = self.parseLocals()
            else:
                instruction = self.parseInstruction(token)
                method.instructions.append(instruction)

                if token == 'ret':
                    break
                
            token = self.getNextToken()

        return method


    def parseInstruction(self, instructionName):
        
        label = ''
        if instructionName.endswith(':'):
            label = instructionName[:-1]
            instructionName = self.getNextToken()
        
        if instructionName == 'ldstr':
            instruction = ldstr()
        elif instructionName == 'ret':
            instruction = Ret()
        elif instructionName.startswith('ldc'):
            instruction = ldc(instructionName.rpartition('ldc')[2], self.peek_next_token())
            # fixme this is ugly
            # Eat up the next token if it was used by the ldc instruction 
            if instruction.value != None:
                self.getNextToken()
        elif instructionName == 'sub':
            instruction = sub()
        elif instructionName == 'add':
            instruction = add()
        elif instructionName == 'nop':
            instruction = nop()
        elif instructionName.startswith('call'):
            instruction = call(self.read_to_end_of_line())
        elif instructionName.startswith('ldloc'):
            instruction = ldloc(instructionName.rpartition('ldloc')[2])
        elif instructionName.startswith('stloc'):
            instruction = stloc(instructionName.rpartition('stloc')[2])
        elif instructionName.startswith('brtrue'):
            instruction = brtrue(instructionName.rpartition('brtrue')[2])
            instruction.target = self.getNextToken()
        elif instructionName.startswith('br'):
            instruction = br(instructionName.rpartition('br')[2])
            instruction.target = self.getNextToken()
        elif instructionName == 'clt':
            instruction = clt()
        else:
            raise ParseException('Unknown instruction ' + instructionName)
        
        instruction.label = label
        return instruction
    
    def parse_parameters(self, method):
        token = self.getNextToken()
        while token != ')':
            # fixme
            token = self.getNextToken()
        
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

    def test_get_next_token_ignore_comments(self):
        str = ('hello\n'
               '// comment 1\n'
               'world\n'
               ' // comment 2\n'
               'abc') 
        
        p = Parser(str);
        self.assertEqual(p.getNextToken(), 'hello')
        self.assertEqual(p.getNextToken(), 'world')
        self.assertEqual(p.getNextToken(), 'abc')
        
    def test_get_next_token_multiple_lines(self):
        str = ('hello\n'
               'world\n'
               'abc') 
        
        p = Parser(str);
        self.assertEqual(p.getNextToken(), 'hello')
        self.assertEqual(p.getNextToken(), 'world')
        self.assertEqual(p.getNextToken(), 'abc')
        
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
        
    def test_parse_single_local_with_alias(self):
        s = 'init ([0] int32 j)'
        p = Parser(s)

        locals = p.parseLocals()
        self.assertEqual(len(locals), 1)
        self.assertEqual(locals[0].name, 'j')
        self.assertEqual(locals[0].alias, '0')
        self.assertEqual(locals[0].type, Types.Int32)
        
    def test_parse_single_local_with_no_alias(self):
        s = 'init (int32 j)'
        p = Parser(s)

        locals = p.parseLocals()
        self.assertEqual(len(locals), 1)
        self.assertEqual(locals[0].name, 'j')
        self.assertEqual(locals[0].alias, None)
        self.assertEqual(locals[0].type, Types.Int32)
        
    def test_parse_multiple_local_with_no_alias(self):
        s = ('init (int32 first,'
             'int32 second,'
             'int32 result)')
        p = Parser(s)

        locals = p.parseLocals()
        self.assertEqual(len(locals), 3)
        self.assertEqual(locals[0].name, 'first')
        self.assertEqual(locals[0].alias, None)
        self.assertEqual(locals[0].type, Types.Int32)
        self.assertEqual(locals[1].name, 'second')
        self.assertEqual(locals[1].alias, None)
        self.assertEqual(locals[1].type, Types.Int32)   
        self.assertEqual(locals[2].name, 'result')
        self.assertEqual(locals[2].alias, None)
        self.assertEqual(locals[2].type, Types.Int32)       

    def test_parse_method_with_labels(self):
        s = ('.method public void main() {\n '
             'IL_0001:    ret\n'
             ' }')
        
        p = Parser(s)
        m = p.parseMethod()
        
        self.assertEqual(len(m.instructions), 1)
        self.assertEqual('ret', m.instructions[0].name)
        self.assertEqual('IL_0001', m.instructions[0].label)

    def test_parse_multiple_methods_with_parameters(self):
        s = ('.method public void main(string[] args) {\n '
             'IL_0001:    ret\n'
             ' }\n'
             '\n'
             '.method public void main2(string[] args) {\n '
             'IL_0001:    ret\n'
             ' }\n')
        
        p = Parser(s)
        p.parse(s) # fixme - don't pass s to both
        
        self.assertEqual(2, len(p.methods))
        self.assertEqual('main', p.methods[0].name)
        self.assertEqual(1, len(p.methods[0].parameters))
        self.assertEqual('main2', p.methods[1].name)
        self.assertEqual(1, len(p.methods[1].parameters))
        
        
    def test_parse_multiple_methods_no_parameters(self):
        s = ('.method public void main() {\n '
             'IL_0001:    ret\n'
             ' }\n'
             '\n'
             '.method public void main2() {\n '
             'IL_0001:    ret\n'
             ' }\n')
        
        p = Parser(s)
        p.parse(s) # fixme - don't pass s to both
        
        self.assertEqual(2, len(p.methods))
        self.assertEqual('main', p.methods[0].name)
        self.assertEqual('main2', p.methods[1].name)

    def test_peek_next_token(self):
        str = ('hello\n'
           'world\n'
           'abc') 
        
        p = Parser(str);
        self.assertEqual(p.getNextToken(), 'hello')
        self.assertEqual(p.peek_next_token(), 'world')
        self.assertEqual(p.getNextToken(), 'world')
        self.assertEqual(p.getNextToken(), 'abc')
        
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

