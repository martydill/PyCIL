from Instruction import Instruction

import unittest


class ldstr(Instruction):

    def __init__(self):
        self.name = 'ldstr'
        self.opcode = 72
        self.value = None

    def execute(self, vm):
        stack = vm.stack
        stack.push(self.value)



class ldstrTest(unittest.TestCase):
        
    def testExecute(self):
        from VM import VM
        vm = VM()
        x = ldstr()
        x.value = 'Hello world'
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 'Hello world')

