from Instructions.ldstr import ldstr
from Instructions.Ret import Ret
from Instructions.ldc import ldc
from Instructions.sub import sub
from Instructions.add import add
from Instructions.mul import mul
from Instructions.nop import nop
from Instructions.call import call
from Instructions.callvirt import callvirt
from Instructions.ldloc import ldloc
from Instructions.stloc import stloc
from Instructions.brtrue import brtrue
from Instructions.br import br
from Instructions.clt import clt
from Instructions.ldarg import ldarg
from Instructions.Instruction import Instruction, Instructions
from Instructions.newobj import newobj
from Instructions.ceq import ceq
from Instructions.newarr import newarr
from Instructions.ldlen import ldlen
from Instructions.conv import conv
from Instructions.stelem import stelem

class InstructionParser(object):
    
    def __init__(self):
        pass
    
    def parse_instruction(self, instructionName, parserContext):
        
        label = ''
        
        if instructionName.endswith(':'):
            label = instructionName[:-1]
            instructionName = parserContext.get_next_token()
        
        if instructionName.find('.') != -1:
            parts = instructionName.partition('.')
            instructionName = parts[0]
            instructionArguments = parts[2]
        else:
            instructionArguments = ''
            
        if Instructions.has_key(instructionName):
            instruction  = Instructions[instructionName]((instructionArguments + ' ' + parserContext.read_to_end_of_line()).strip())
        #=======================================================================
        #    
        # if instructionName == 'ldstr':
        #    instruction = ldstr()
        # elif instructionName == 'ret':
        #    instruction = Ret()
        # elif instructionName.startswith('ldc'):
        #    instruction = ldc(instructionName.rpartition('ldc')[2], parserContext.peek_next_token())
        #    # fixme this is ugly
        #    # Eat up the next token if it was used by the ldc instruction 
        #    if instruction.value != None:
        #        parserContext.get_next_token()
        # elif instructionName == 'sub':
        #    instruction = sub()
        # elif instructionName == 'add':
        #    instruction = add()
        # elif instructionName == 'mul':
        #    instruction = mul()
        # elif instructionName == 'nop':
        #    instruction = nop()
        # elif instructionName.startswith('call'):
        #    instruction = call(parserContext.read_to_end_of_line())
        # elif instructionName.startswith('ldloc'):
        #    instruction = ldloc(instructionName.rpartition('ldloc')[2])
        # elif instructionName.startswith('ldarg'):
        #    instruction = ldarg(instructionName.rpartition('ldarg')[2])
        # elif instructionName.startswith('stloc'):
        #    instruction = stloc(instructionName.rpartition('stloc')[2])
        # elif instructionName.startswith('brtrue'):
        #    instruction = brtrue(instructionName.rpartition('brtrue')[2])
        #    instruction.target = parserContext.get_next_token()
        # elif instructionName.startswith('br'):
        #    instruction = br(instructionName.rpartition('br')[2])
        #    instruction.target = parserContext.get_next_token()
        # elif instructionName == 'clt':
        #    instruction = clt()
        # else:
        #=======================================================================
        else:
            from Parser.ParserContext import ParseException
            raise ParseException('Unknown instruction ' + instructionName)
        
        instruction.label = label
        return instruction
    