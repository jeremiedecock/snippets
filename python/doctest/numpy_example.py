#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a doctest example with Numpy arrays.

For more information about doctest, see
https://docs.python.org/3/library/doctest.html (reference)
and
www.fil.univ-lille1.fr/~L1S2API/CoursTP/tp_doctest.html (nice examples in
French).

To run doctest, execute this script (thanks to the
`if __name__ == "__main__": import doctest ; doctest.testmod()` directives) 
or execute the following command in a terminal::

    python3 -m doctest datapipe/io/images.py
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

    Be careful with white space! The following will work...
    >>> a
    array([ 1.,  2.,  0.])

    but this one would't
    # >>> a
    # array([ 1., 2., 0.])

    As an alternative, the `doctest: +NORMALIZE_WHITESPACE` can be used (see
    https://docs.python.org/3/library/doctest.html#doctest.NORMALIZE_WHITESPACE
    and http://www.fil.univ-lille1.fr/~L1S2API/CoursTP/tp_doctest.html)
    >>> a
    ... # doctest: +NORMALIZE_WHITESPACE
    array([ 1., 2., 0.])

    but the space before the '1' is still required...
    """
    nan_mask = np.isnan(a)
    a[nan_mask] = 0
    return nan_mask


if __name__ == "__main__":
    import doctest
    import numpy
    doctest.testmod()
