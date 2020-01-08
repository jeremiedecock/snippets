import pytest       # Contains some useful helper functions like pytest.raise(), pytest.warns(), ...
import math
import numpy as np  # Contains some useful helper functions like np.testing.assert_array_equal(), ...

import foo          # The module to be tested

# Basic test ####################################

def test_divide1():
    """Assert that the foo.divide1(a, b) returns the value for a given example."""
    expected = 2
    returned = foo.divide1(4, 2)
    assert returned == expected

# Test a decimal values (float) #################

def test_rmse():
    """Check on an example that the returned value is the expected one."""
    y_true = np.array([3, -0.5, 2, 7])
    y_pred = np.array([2.5, 0.0, 2, 8])

    expected = 0.375
    returned = foo.mse(y_true, y_pred)

    assert returned == pytest.approx(expected, rel=1e-3)

# Test the type of a returned value #############

def test_divide1_return():
    returned = foo.divide1(4, 2)
    assert isinstance(returned, float)

# Test a sequences ##############################

def test_ones_list():
    returned = foo.ones_list(4)
    assert all(elem == 1 for elem in returned)

# Test a numpy array (of integers) ##############

def test_ones_array():
    expected = np.array([[1, 1, 1, 1],
                         [1, 1, 1, 1],
                         [1, 1, 1, 1],
                         [1, 1, 1, 1]])

    returned = foo.ones_array(4)

    np.testing.assert_array_equal(returned, expected)

# Test a numpy array (of decimals) ##############

def test_divide_array():
    a = np.array([[1, 1, 1],
                  [1, 1, 1],
                  [1, 1, 1]])

    b = np.array([[1, 2, 3],
                  [1, 2, 3],
                  [1, 2, 3]])

    expected = np.array([[1., 0.5, 0.333],
                         [1., 0.5, 0.333],
                         [1., 0.5, 0.333]])

    returned = foo.divide_array(a, b)

    np.testing.assert_almost_equal(returned, expected, decimal=3)

# Test expected exceptions ######################

def test_divide1_zero_division_error():
    """Assert that the foo.divide1(a, b) function raises a ZeroDivisionError exception when b is zero."""
    with pytest.raises(ZeroDivisionError):
        returned = foo.divide1(4, 0)

# Test expected warnings ########################

def test_divide2_divide_by_zero_warning():
    """Assert that the foo.divide1(a, b) function raises a ZeroDivisionError exception when b is zero."""
    with pytest.warns(UserWarning):
        returned = foo.divide2(4, 0)

def test_divide2_divide_by_zero_value():
    """Assert that the foo.divide1(a, b) function raises a ZeroDivisionError exception when b is zero."""
    with pytest.warns(UserWarning):
        returned = foo.divide2(4, 0)
        assert math.isnan(returned)