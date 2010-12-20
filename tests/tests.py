import unittest
from VM import VM
from VM import Types

class tests(unittest.TestCase):
    
    def run_test(self, fileName):
        vm = VM()
        vm.load(fileName)
        vm.start()
        return vm.stack.pop()
                
    def tearDown(self):
        Types.unregister_all_custom_types()
    
    # Misc language features tests
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

    def test_switch(self):
        result = self.run_test('switch.il')
        self.assertEqual(result.value, 555)

    def test_call_static_method_with_return_value(self):
        result = self.run_test('method.il')
        self.assertEqual(result.value, 5)
    
    def test_fibbonacci_recursion(self):
        result = self.run_test('fib.il')
        self.assertEqual(result.value, 21)    
        
        
    # Class tests            
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
    
    def test_class_method_with_return_value(self):
        result = self.run_test('class6.il')
        self.assertEqual(result.value, 987654)
    
    def test_class_method_with_parameter(self):
        result = self.run_test('class7.il')
        self.assertEqual(result.value, 999)
    
    
    # Array tests
    def test_array_length(self):
        result = self.run_test('arraylength.il')
        self.assertEqual(result.value, 100)
        
    def test_array_get_and_set_elements(self):
        result = self.run_test('arrayelements.il')
        self.assertEqual(result.value, 987987)
        
    def test_pass_array_as_function_parameter(self):
        result = self.run_test('arrayparameter.il')
        self.assertEqual(result.value, 232232)
    
    
    # Exception handling tests
    def test_try_catch_all_not_throwing_exception(self):
        result = self.run_test('try1.il')
        self.assertEqual(result.value, 1234)
        
    def test_try_catch_all_nested_not_throwing_exception(self):
        result = self.run_test('try2.il')
        self.assertEqual(result.value, 1234)
        