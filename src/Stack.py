import unittest
from MethodDefinition import MethodDefinition

class StackStateException(Exception):
    pass
    
class StackSizeException(Exception):
    pass

class StackFrame:
    def __init__(self, frameSize):
        self.frameSize = frameSize
        self.count = 0
        self.method = None
        self.instructionPointer = 0
        
class Stack ():

    def __init__(self, initialSize):
        self.stack = []
        self.stackFrames = []
        self.currentFrame = None
        self.beginFrame(initialSize)

    def push(self, value):
        if self.currentFrame.frameSize == self.currentFrame.count:
            raise StackSizeException('Stack size exceeded')

        self.currentFrame.count += 1
        self.stack.append(value)

    def pop(self):
        self.currentFrame.count -=1
        return self.stack.pop()

    def count(self):
        return len(self.stack)

    def get_number_of_frames(self):
        return len(self.stackFrames)
        
    def get_frame_size(self):
        if self.currentFrame is None:
            return 0

        return self.currentFrame.frameSize

    def get_frame_count(self):
        if self.currentFrame is None:
            return 0

        return self.currentFrame.count

    def beginFrame(self, frameSize, method = None):
        self.currentFrame = StackFrame(frameSize)
        self.currentFrame.method = method
        self.stackFrames.append(self.currentFrame)

    def endFrame(self):
        self.stackFrames.pop();

        if len(self.stackFrames) > 0:
            self.currentFrame = self.stackFrames[-1]
        else:
            self.currentFrame = None


class StackTest(unittest.TestCase):

    def test_single_push_and_pop(self):
        s = Stack(123)
        s.push('hello world')
        self.assertEqual(s.count(), 1)
        self.assertEqual(s.pop(), 'hello world')
        self.assertEqual(s.count(), 0);

    def test_multiple_pushes_and_pops_lifo(self):
        s = Stack(123)
        s.push('hello world')
        s.push(123)
        s.push('def');
        self.assertEqual(s.count(), 3)

        self.assertEqual(s.pop(), 'def')
        self.assertEqual(s.pop(), 123)
        self.assertEqual(s.pop(), 'hello world')
        self.assertEqual(s.count(), 0)

    def test_exceeding_max_stack(self):
        s = Stack(3)
        s.push(123)
        s.push(456)
        s.push(789)

        self.assertRaises(StackSizeException, s.push, 'fail')

    def test_multiple_frames_frame_size(self):
        s = Stack(3)
        self.assertEqual(s.get_frame_size(), 3)

        s.beginFrame(95)
        self.assertEqual(s.get_frame_size(), 95)

        s.beginFrame(127)
        self.assertEqual(s.get_frame_size(), 127)
        s.endFrame()

        self.assertEquals(s.get_frame_size(), 95)
        s.endFrame()
        self.assertEqual(s.get_frame_size(), 3)

    def test_currentframe_stack_count(self):
        s = Stack(5)
        s.push(1)
        self.assertEqual(s.get_frame_count(), 1)

        s.push(5)
        s.push('abc')
        self.assertEqual(s.get_frame_count(), 3)

        s.beginFrame(99)
        self.assertEqual(s.get_frame_count(), 0)

        s.push(0)
        self.assertEqual(s.get_frame_count(), 1)
        s.endFrame()

        self.assertEqual(s.get_frame_count(), 3)
        
    def test_get_number_of_frames(self):
        s = Stack(5)
        self.assertEqual(s.get_number_of_frames(), 1)
        
        s.beginFrame(42)
        s.beginFrame(99)
        s.beginFrame(234)
        s.beginFrame(123423)
        self.assertEqual(s.get_number_of_frames(), 5)
        s.endFrame()
        self.assertEqual(s.get_number_of_frames(), 4)

    def test_frame_methods(self):
        s = Stack(5)
        
        m1 = MethodDefinition()
        s.beginFrame(5, m1)
        self.assertEqual(s.currentFrame.method, m1)
        
        m2 = MethodDefinition()
        s.beginFrame(999, m2)
        self.assertEqual(s.currentFrame.method, m2)
        
        s.endFrame()
        self.assertEqual(s.currentFrame.method, m1)
        
        s.endFrame()
        self.assertEqual(s.currentFrame.method, None)
        
    def test_push_creates_frame(self):
        s = Stack(123);
        s.push(444)
        self.assertEqual(s.get_number_of_frames(), 1)
        self.assertEqual(s.currentFrame, s.stackFrames[0])