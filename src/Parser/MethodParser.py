from Method import Method
import Types
from Variable import Variable
import unittest
from Class import Class

BlockStart = '{'
BlockEnd = '}'

class MethodParser(object):
    
    def __init__(self):
        self.context = None
    
    def parse(self, parserContext):
        self.context = parserContext
        method = Method()

        token = self.context.get_next_token()

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
                
            token = self.context.get_next_token()

        token = self.context.get_next_token()
        while token != BlockEnd:
            print token
            if token == '.maxstack':
                method.maxStack = int(self.context.get_next_token())
            elif token == '.entrypoint':
                method.attributes.append(token)
            elif token == '.locals':
                method.locals = self.parse_locals(self.context)
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
        while token != ')':
            # fixme
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
            locals.append(v)
            if token.startswith('['):
                v.alias = token[1:-1]
                lastToken = token
                token = context.get_next_token()
            if token == 'class':
                v.type = Types.resolve_type(context.get_next_token())
            else:
                v.type = Types.BuiltInTypes[token] # fixme - non-builtin types
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
    
    
class MethodParserTest(unittest.TestCase):

    def test_parse_class_local_with_alias(self):
        from ParserContext import ParserContext
        s = 'init ([0] class NS.C f)'
        
        p = ParserContext()
        p.set_parse_data(s);
        mp = MethodParser()

        c = Class()
        c.name = 'C'
        c.namespace = 'NS'
        Types.register_custom_type(c)
        
        locals = mp.parse_locals(p)
        self.assertEqual(len(locals), 1)
        self.assertEqual(locals[0].name, 'f')
        self.assertEqual(locals[0].alias, '0')
        self.assertEqual(locals[0].type.name, 'NS.C')
        
    
    def test_parse_single_local_with_alias(self):
        from ParserContext import ParserContext
        s = 'init ([0] int32 j)'
        
        p = ParserContext()
        p.set_parse_data(s);
        mp = MethodParser()

        locals = mp.parse_locals(p)
        self.assertEqual(len(locals), 1)
        self.assertEqual(locals[0].name, 'j')
        self.assertEqual(locals[0].alias, '0')
        self.assertEqual(locals[0].type, Types.Int32)
        
    def test_parse_single_local_with_no_alias(self):
        from ParserContext import ParserContext
        s = 'init (int32 j)'
        p = ParserContext()
        p.set_parse_data(s);
        mp = MethodParser()

        locals = mp.parse_locals(p)
        self.assertEqual(len(locals), 1)
        self.assertEqual(locals[0].name, 'j')
        self.assertEqual(locals[0].alias, None)
        self.assertEqual(locals[0].type, Types.Int32)
        
    def test_parse_multiple_local_with_no_alias(self):
        from ParserContext import ParserContext
        s = ('init (int32 first,'
             'int32 second,'
             'int32 result)')
        p = ParserContext()
        p.set_parse_data(s);
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
        
        p = ParserContext()
        p.set_parse_data(s);
        mp = MethodParser()
        m = mp.parse(p)
        
        self.assertEqual(len(m.instructions), 1)
        self.assertEqual('ret', m.instructions[0].name)
        self.assertEqual('IL_0001', m.instructions[0].label)

    def test_parse_multiple_methods_with_parameters(self):
        from ParserContext import ParserContext
        s = ('.method public void main(string[] args) {\n '
             'IL_0001:    ret\n'
             ' }\n'
             '\n'
             '.method public void main2(string[] args) {\n '
             'IL_0001:    ret\n'
             ' }\n')
        
        p = ParserContext(s)
        p.parse(s) # fixme - don't pass s to both
        
        self.assertEqual(2, len(p.methods))
        self.assertEqual('main', p.methods[0].name)
        self.assertEqual(1, len(p.methods[0].parameters))
        self.assertEqual('main2', p.methods[1].name)
        self.assertEqual(1, len(p.methods[1].parameters))
        
        
    def test_parse_multiple_methods_no_parameters(self):
        from ParserContext import ParserContext
        s = ('.method public void main() {\n '
             'IL_0001:    ret\n'
             ' }\n'
             '\n'
             '.method public void main2() {\n '
             'IL_0001:    ret\n'
             ' }\n')
        
        p = ParserContext(s)
        p.parse(s) # fixme - don't pass s to both
        
        self.assertEqual(2, len(p.methods))
        self.assertEqual('main', p.methods[0].name)
        self.assertEqual('main2', p.methods[1].name)
   