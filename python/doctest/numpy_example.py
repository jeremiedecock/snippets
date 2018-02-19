#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a doctest example with Numpy arrays.

For more information about doctest, see
https://docs.python.org/3/library/doctest.html.
"""

import numpy as np

def example1():
    """A very basic doctest example.

    Notes
    -----
    The numpy module is imported at the end of this file, in the test::

        if __name__ == "__main__":
            import doctest
            import numpy
            doctest.testmod()

    Examples
    --------
    >>> numpy.array([1, 2, 3])
    array([1, 2, 3])
    """
    pass


def example2():
    """A very basic doctest example to test values returned by this function.

    Examples
    --------
    >>> example2()
    array([1, 2, 3])
    """
    return numpy.array([1, 2, 3])


def example3(a):
    """A very basic example.

    Examples
    --------
    >>> a = numpy.array([3, 1, 2])
    >>> example3(a)
    >>> a
    array([1, 2, 3])
    """
    a.sort()


def example4(a):
    """Replace *in-place* `NaN` values in `a` by zeros.

    Replace `NaN` ("Not a Number") values in `a` by zeros.

    Parameters
    ----------
    image : array_like
        The image to process. `NaN` values are replaced **in-place** thus this
        function changes the provided object.

    Returns
    -------
    array_like
        Returns a boolean mask array indicating whether values in `a`
        initially contained `NaN` values (`True`) of not (`False`). This array
        is defined by the instruction `np.isnan(a)`.

    Notes
    -----
        `NaN` values are replaced **in-place** in the provided `a`
        parameter.

    Examples
    --------
    >>> a = numpy.array([1., 2., numpy.nan])
    >>> a
    array([  1.,   2.,  nan])
    >>> example4(a)
    array([False, False,  True], dtype=bool)
    >>> a
    array([ 1.,  2.,  0.])
    """
    nan_mask = np.isnan(a)
    a[nan_mask] = 0
    return nan_mask


if __name__ == "__main__":
    import doctest
    import numpy
    doctest.testmod()
