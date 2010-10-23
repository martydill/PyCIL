from VM import VM, DebugHooks
import traceback
import sys

class Debugger():
    
    def __init__(self):
        self.vm = VM()
        self.vm.add_hook(DebugHooks.PreInstruction, self.pre_instruction_hook)
        self.vm.add_hook(DebugHooks.PreMethod, self.pre_method_hook)
        self.vm.add_hook(DebugHooks.PostMethod, self.post_method_hook)
                
    def pre_instruction_hook(self, instruction):
        print instruction.label + ':\t' + instruction.name + ' ' + hex(instruction.opcode)
        self.handle_input()
    
    def pre_method_hook(self, method):
        print 'Entered method ' + method.methodDefinition.namespace + '::' + method.methodDefinition.name
        
    def post_method_hook(self, method):
        print 'Exited method ' + method.methodDefinition.namespace + '::' + method.methodDefinition.name
        
    def handle_input(self):
        while True:
            r = raw_input('> ')
            if r == 's':
                for item in reversed(self.vm.stack.stack):
                    print item
            elif r == 'q':
                exit()
            elif r == 'g':
                self.vm.remove_hook(DebugHooks.PreInstruction, self.pre_instruction_hook)
                return
            elif r == 'm':
                print 'method'
            elif r.startswith('l '):
                filename = '../tests/' + r[2:] + ".il"
                try:
                    self.vm.load(filename)
                    print 'Loaded ' + filename
                    self.vm.start()
                    print 'Execution finished'
                    print 'Return code: ' + str(self.vm.stack.pop())
                    return
                except IOError:
                    print 'Unable to load file'
                except Exception as e:
                    print 'Error: ' + str(e)
                    traceback.print_exc(file=sys.stdout)

            else:
                return
            
    def start(self):
        while True:
            self.handle_input()
        
if __name__ == '__main__':
    debugger = Debugger()
    debugger.start()