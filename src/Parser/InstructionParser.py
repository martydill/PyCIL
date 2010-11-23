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
from Instructions.ldelem import ldelem
from Instructions.beq import beq
from Instructions.leave import leave

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
        else:
            from Parser.ParserContext import ParseException
            raise ParseException('Unknown instruction ' + instructionName)
        
        instruction.label = label
        return instruction
    