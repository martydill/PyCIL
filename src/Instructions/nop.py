from Instruction import Instruction
import unittest
import Types
from Method import Method

class nop(Instruction):

    def __init__(self):
        self.name = 'nop'
        self.opcode = 0x28

    def execute(self, vm):
        pass


class nopTes(unittest.TestCase):

    def test_nop(self):
        from VM import VM

        vm = VM()

        m = Method()
        m.name = 'TestMethod'
        m.returnType = Types.Void
        m.parameters = []
        vm.methods.append(m)

        self.assertEqual(vm.currentMethod, None)

        c = nop()
        c.execute(vm)

        self.assertEqual(vm.stack.get_number_of_frames(), 1)
        