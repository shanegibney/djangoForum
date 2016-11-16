import unittest
from fun import add

class test_function(unittest.TestCase):
     def test_one(self):
           result = add(2,3)
           self.assertEquals(result, 5)
