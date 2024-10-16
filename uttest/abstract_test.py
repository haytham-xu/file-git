
import unittest

class AbstractTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        # before each class
        pass
    
    @classmethod 
    def tearDownClass(self):
        # after each class
        pass
