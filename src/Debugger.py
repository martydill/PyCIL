from VM import VM, DebugHooks

class Debugger():
    
    def __init__(self):
        self.vm = VM()
        self.vm.add_hook(DebugHooks.PreInstruction, self.pre_instruction_hook)
        
    def pre_instruction_hook(self, instruction):
        print 'Next: ' + instruction.name + ' ' + hex(instruction.opcode)
        self.handle_input()

    def handle_input(self):
        r = raw_input('> ')
        if r == 's':
            print 'stack'
        elif r == 'm':
            print 'method'
        elif r.startswith('l '):
            filename = '../tests/' + r[2:] + ".il"
            self.vm.load(filename)
            print 'Loaded ' + filename
            self.vm.start()
            print 'Execution finished'

    def start(self):
        while True:
            self.handle_input()
        
if __name__ == '__main__':
    debugger = Debugger()
    debugger.start()