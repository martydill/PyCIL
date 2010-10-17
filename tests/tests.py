import unittest
from VM import VM
from VM import Types

class tests(unittest.TestCase):
    
    def run_test(self, fileName):
        vm = VM()
        vm.load(fileName)
        vm.start()
        return vm.stack.lastFrameReturnValue
                
    def tearDown(self):
        Types.unregister_all_custom_types()
        
    def test_add(self):
        result = self.run_test('add.il')
        self.assertEqual(result.value, 7)
        
    def test_mul(self):
        result = self.run_test('mult.il')
        self.assertEqual(result.value, 26)
        
    def test_for(self):
        result = self.run_test('for.il')
        self.assertEqual(result.value, 6)
        
    def test_while(self):
        result = self.run_test('while.il')
        self.assertEqual(result.value, 10)
        
    def test_simple_class(self):
        result = self.run_test('class.il')
        self.assertEqual(result.value, 1234)
        
    def test_class_with_int_field(self):
        result = self.run_test('class2.il')
        self.assertEqual(result.value, 684870)
        
    def test_class_objects_in_loop(self):
        result = self.run_test('class3.il')
        self.assertEqual(result.value, 45)
        
    def test_class_objects_containing_class_fields(self):
        result = self.run_test('class4.il')
        self.assertEqual(result.value, 4444)
        
    def test_class_field_reference_comparison(self):
        result = self.run_test('class5.il')
        self.assertEqual(result.value, 9999)