'''
Created on 2010-10-09

@author: Marty
'''
import unittest

def is_number(s):
    try:
        int(s)
        return True
    except:
        return False


class UtilityTest(unittest.TestCase):
    
    def test_is_number_valid_number(self):
        self.assertTrue(is_number('234'))
        
    def test_is_number_invalid_number(self):
        self.assertFalse(is_number('CS$4$0001'))