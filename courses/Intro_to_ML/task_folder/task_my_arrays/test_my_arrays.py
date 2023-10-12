from example_solution import my_arrays as my_arrays
import numpy as np
#!cut_imports!#
def test_my_arrays():
    n = 3
    # Test is arbitrary, but you should use assert.
    assert my_arrays(n)[0] == np.zeros(n), "The array of zeros is not created or presented in a false order"
    assert my_arrays(n)[1] == np.ones(n), "The array of ones is not created or presented in a false order"
    assert my_arrays(n)[2] == np.full(n, 5), "The array of fives is not created or presented in a false order"

