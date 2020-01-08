"""This module contains (bogus) functions to be tested."""

import numpy as np
import warnings

def divide1(a, b):
    return a/b

def divide2(a, b):
    if b == 0:
        warnings.warn("Division by zero !")
        return float("nan")
    else:
        return a/b

def mse(y_true, y_pred, sample_weight=None):
    """Mean squared error

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground truth (correct) target values.
    y_pred : array-like of shape (n_samples,)
        Estimated target values.
    sample_weight : array-like of shape (n_samples,), optional
        Sample weights.

    Returns
    -------
    loss : float
        A non-negative floating point value (the best value is 0.0).

    Examples
    --------
    >>> from ailib.tsa.metrics import mse
    >>> import numpy as np
    >>> y_true = np.array([3, -0.5, 2, 7])
    >>> y_pred = np.array([2.5, 0.0, 2, 8])
    >>> mse(y_true, y_pred)
    0.375
    """
    #assert y_true.ndim == 1
    #assert y_pred.ndim == 1

    _mse = np.average((y_true - y_pred) ** 2, axis=0, weights=sample_weight)
    return _mse

def ones_list(n):
    l = [1 for x in range(n)]
    return l

def ones_array(n):
    l = [[1 for x in range(n)] for y in range(n)]
    return np.array(l)

def divide_array(a, b):
    return a/b