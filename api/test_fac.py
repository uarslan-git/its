import unittest
from fac import factorial


class TestFactorial(unittest.TestCase):
    def test_factorial(self):
        # Test factorial of 0
        self.assertEqual(factorial(0), 1)
        
        # Test factorial of positive numbers
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)
        
        # Test factorial of negative numbers (should raise ValueError)
        with self.assertRaises(ValueError):
            factorial(-5)
    
    def test_large_factorial(self):
        # Test factorial of a large number
        self.assertEqual(factorial(20), 2432902008176640000)

if __name__ == '__main__':
    unittest.main()