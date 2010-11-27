from MethodDefinition import MethodDefinition
import Types
from Variable import Variable
import unittest
from ClassDefinition import ClassDefinition
from ReferenceType import ReferenceType
from Instructions.Special.BeginTry import BeginTry
from Instructions.Special.EndTry import EndTry
from Instructions.Special.BeginCatch import BeginCatch
from Instructions.Special.EndCatch import EndCatch

BlockStart = '{'
BlockEnd = '}'

class MethodParser(object):
    
    def __init__(self):
        self.context = None
        self.try_block_count = 0
        self.end_block_instructions = []
        
    def parse(self, parserContext):
        self.context = parserContext
        method = MethodDefinition()

        token = self.context.get_next_token()

        while token != BlockStart:
            if token == '(':
                self.parse_parameters(method)
            elif token in MethodDefinition.AttributeTypes.keys():
                method.attributes.append(token)
            elif token in Types.BuiltInTypes:
                method.returnType = Types.BuiltInTypes[token]
            elif token == '.method':
                pass
            else:
                parts = token.rpartition('.')
                method.namespace = parts[0]
                method.name = parts[2]
                self.parse_parameters(method)
                
            token = self.context.get_next_token()

        token = self.context.get_next_token()
        while token != BlockEnd or len(self.end_block_instructions) > 0:
            if token == '.maxstack':
                method.maxStack = int(self.context.get_next_token())
            elif token == '.entrypoint':
                method.attributes.append(token)
            elif token == '.locals':
                method.locals = self.parse_locals(self.context)
            elif token == '.try':
                self.parse_try_block(method)
            elif token == 'catch':
                self.parse_catch_block(method)
            elif token == BlockEnd:
                self.parse_end_block(method)
            else:
                from InstructionParser import InstructionParser
                instruction = InstructionParser().parse_instruction(token, self.context)
                method.instructions.append(instruction)

                if token == 'ret':
                    break
                
            token = self.context.get_next_token()

        return method

    def parse_parameters(self, method):
        token = self.context.get_next_token()
        while token != ')' and token != '':
            if token != '(':
                type = Types.resolve_type(token)
                name = self.context.get_next_token()
                v = Variable()
                v.type = type
                v.name = name
                method.parameters.append(v)
                
            token = self.context.get_next_token()
            
                   
    def parse_locals(self, context):
        from ParserContext import ParseException
        locals = []
        token = context.get_next_token()
        if token != 'init':
            raise ParseException('Expected init, found ' + token) # fixme - only required for verifiable methods
        token = context.get_next_token()
        if token != '(':
            raise ParseException('Expected (, found' + token)
        token = context.get_next_token()
        lastToken = ''
        while not token.endswith(')'):
            v = Variable()
            if token.startswith('['):
                v.alias = token[1:-1]
                lastToken = token
                token = context.get_next_token()
            if token == 'class':
                v2 = ReferenceType()
                v2.alias = v.alias
                v2.type = Types.resolve_type(context.get_next_token())
                v = v2
            elif token.endswith('[]'): # array
                v.type = Types.Array
                v.arrayType = Types.resolve_type(token[:-2])
            else:
                v.type = Types.BuiltInTypes[token] # fixme - non-builtin types
            
            locals.append(v)
            lastToken = token
            token = context.get_next_token()
            #if token.endswith(')'):
            #    v.name = token[:-1]
            #    token = ')'
            #else:
            v.name = token
            lastToken= token
            token = context.get_next_token()
            
        return locals
        
    def parse_try_block(self, method):
        method.instructions.append(BeginTry())
        self.context.get_next_token()  # eat up the bracket
        self.end_block_instructions.append(EndTry())
        
    def parse_catch_block(self, method):
        method.instructions.append(BeginCatch())
        self.context.get_next_token()   # TODO - grab the exception type we are catching
        self.context.get_next_token()   # eat up the bracket
        self.end_block_instructions.append(EndCatch())
        
    def parse_end_block(self, method):
        endBlockInstruction = self.end_block_instructions.pop()
        method.instructions.append(endBlockInstruction)
        
class MethodParserTest(unittest.TestCase):

    def test_parse_class_local_with_alias(self):
        from ParserContext import ParserContext
        s = 'init ([0] class NS.C f)'
        
        p = ParserContext(s)
        mp = MethodParser()

        c = ClassDefinition()
        c.name = 'C'
        c.namespace = 'NS'
        Types.register_custom_type(c)
        
        locals = mp.parse_locals(p)
        self.assertEqual(len(locals), 1)
        self.assertTrue(isinstance(locals[0], ReferenceType))
        self.assertEqual(locals[0].name, 'f')
        self.assertEqual(locals[0].alias, '0')
        self.assertEqual(locals[0].type.name, 'C')
        self.assertEqual(locals[0].type.namespace, 'NS')
    
    def test_parse_single_local_with_alias(self):
        from ParserContext import ParserContext
        s = 'init ([0] int32 j)'
        
        p = ParserContext(s)
        mp = MethodParser()

        locals = mp.parse_locals(p)
        self.assertEqual(len(locals), 1)
        self.assertEqual(locals[0].name, 'j')
        self.assertEqual(locals[0].alias, '0')
        self.assertEqual(locals[0].type, Types.Int32)
        
    def test_parse_single_local_with_no_alias(self):
        from ParserContext import ParserContext
        s = 'init (int32 j)'
        p = ParserContext(s)
        mp = MethodParser()

        locals = mp.parse_locals(p)
        self.assertEqual(len(locals), 1)
        self.assertEqual(locals[0].name, 'j')
        self.assertEqual(locals[0].alias, None)
        self.assertEqual(locals[0].type, Types.Int32)

    def test_parse_single_local_array_with_no_alias(self):
        from ParserContext import ParserContext
        s = 'init (int32[] j)'
        p = ParserContext(s)
        mp = MethodParser()

        locals = mp.parse_locals(p)
        self.assertEqual(len(locals), 1)
        self.assertEqual(locals[0].name, 'j')
        self.assertEqual(locals[0].alias, None)
        self.assertEqual(locals[0].type, Types.Array)
        self.assertEqual(locals[0].arrayType, Types.Int32)
        
    def test_parse_multiple_local_with_no_alias(self):
        from ParserContext import ParserContext
        s = ('init (int32 first,'
             'int32 second,'
             'int32 result)')
        p = ParserContext(s)
        mp = MethodParser()

        locals = mp.parse_locals(p)
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
        from ParserContext import ParserContext
        s = ('.method public void main() {\n '
             'IL_0001:    ret\n'
             ' }')
        
        p = ParserContext(s)
        mp = MethodParser()
        m = mp.parse(p)
        
        self.assertEqual(len(m.instructions), 1)
        self.assertEqual('ret', m.instructions[0].name)
        self.assertEqual('IL_0001', m.instructions[0].label)

    def test_parse_single_method_with_parameters(self):
        from ParserContext import ParserContext
        s = """.method public hidebysig instance void 
              SetCount(int32 c) cil managed
              {
                // Code size       9 (0x9)
                .maxstack  8
                IL_0000:  nop
              } // end of method foo::SetCount"""
    
        p = ParserContext()
        p.parse(s)
        self.assertEqual(len(p.methods[0].parameters), 1)
        self.assertEqual(p.methods[0].parameters[0].name, 'c')
        self.assertEqual(p.methods[0].parameters[0].type, Types.Int32)
        
    def test_parse_multiple_methods_with_parameters(self):
        from ParserContext import ParserContext
        s = ('.method public void main(int args) {\n '
             'IL_0001:    ret\n'
             ' }\n'
             '\n'
             '.method public void main2(int args) {\n '
             'IL_0001:    ret\n'
             ' }\n')
        
        p = ParserContext()
        p.parse(s)
        
        self.assertEqual(2, len(p.methods))
        self.assertEqual('main', p.methods[0].name)
        self.assertEqual(1, len(p.methods[0].parameters))
        self.assertEqual('main2', p.methods[1].name)
        self.assertEqual(1, len(p.methods[1].parameters))
        
    
    def test_parse_multiple_methods_no_parameters(self):
        from ParserContext import ParserContext
        s = ('.method public void A.B.main() {\n '
             'IL_0001:    ret\n'
             ' }\n'
             '\n'
             '.method public void N.S.main2() {\n '
             'IL_0001:    ret\n'
             ' }\n')
        
        p = ParserContext()
        p.parse(s)
        
        self.assertEqual(2, len(p.methods))
        self.assertEqual('main', p.methods[0].name)
        self.assertEqual('A.B', p.methods[0].namespace)
        self.assertEqual('main2', p.methods[1].name)
        self.assertEqual('N.S', p.methods[1].namespace)
   
   
    def test_parse_empty_try_block(self):
        from ParserContext import ParserContext
        s = ('.method private hidebysig static int32  Main(string[] args) cil managed\n'
            '{\n'
            '  .entrypoint\n'
            '  .maxstack  1\n'
            '  .locals init ([0] int32 CS$1$0000)\n'
            '  .try\n'
            '  {\n'
            '    IL_0008:  leave.s    IL_0010\n'
            '  }  // end .try\n'
            '  catch [mscorlib]System.Object \n'
            '  {\n'
            '    IL_000e:  leave.s    IL_0010\n'
            '  }  // end handler\n'
            '  IL_0010:  nop\n'
            '  IL_0011:  ldloc.0\n'
            '  IL_0012:  ret\n'
            '} // end of method Program::Main')
        
        p = ParserContext()
        p.parse(s)
        
        self.assertEqual(1, len(p.methods))
        m = p.methods[0]
        self.assertIsInstance(m.instructions[0], BeginTry)
        self.assertIsInstance(m.instructions[2], EndTry)
        