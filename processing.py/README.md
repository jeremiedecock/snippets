# Processing.py

* Official web site: http://py.processing.org/
* Source code: https://github.com/jdf/processing.py/
* Wiki: https://github.com/jdf/processing.py/wiki

## Additional information

### Is it possible to use processing.py with SciPy or NumPy?

    "No. Processing's Python Mode is implemented in Java, and relies on the
    Jython project's implementation of the Python programming language. You can
    use any "pure Python" module, meaning any Python module that has no "native
    code" component. Just copy the module (individual .py files or a directory
    tree of .py files) into your sketch directory, and import it as usual.

    The Python standard library is included."
