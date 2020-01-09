# PyTest

Functions to be tested are defined in `foo.py` (these functions have no particular interest and they are just a support to test PyTest).

Unit tests are defined in the `tests/test_foo.py` module.
Unit tests defined there highlight tips and tricks specific to the object to be tested: how to assert a float variable, how to assert a sequence, etc.

## Install PyTest

```
pip install pytest
```

**Note**: PyTest is installed by default with Anaconda.

## Notes

Each module (.py file) having a name starting with `test_` is a test module.
Each function starting with `test_` and defined in a test module is a unit test.

Tests are launched with the `pytest` command:

1. open a terminal
2. move to the root directory of your project
3. type `pytest`

PyTest automatically finds unit tests (based on the previously mentioned naming conventions),
executes them and and highlights those who have failed.

A unit test "fails" when it raises an exception.

## See Also

- Official web site: https://docs.pytest.org
- Naming conventions: https://docs.pytest.org/en/latest/goodpractices.html#test-discovery
- API reference: https://docs.pytest.org/en/latest/reference.html
- Numpy test routines: https://docs.scipy.org/doc/numpy/reference/routines.testing.html