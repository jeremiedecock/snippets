# PySide6 (Qt6)

Source: https://doc.qt.io/qtforpython/quickstart.html

## Creating and activating an environment

You can do this by running the following on a terminal:

```
python -m venv env                 (Your Python executable might be called python3)
source env/bin/activate            (for Linux and macOS)
env\Scripts\activate.bat           (for Windows)
```

## Installation

Now you are ready to install the Qt for Python packages using pip. From the terminal, run the following command:

```
pip install pyside6                (for the latest version)
pip install pyside6==6.0           (for the version 6.0 specifically)
```

## Test your installation

Now that you have Qt for Python installed, test your setup by running the following Python constructs to print version information:

```
import PySide6.QtCore

# Prints PySide6 version
print(PySide6.__version__)

# Prints the Qt version used to compile PySide6
print(PySide6.QtCore.__version__)
```

## Examples

https://doc.qt.io/qtforpython/examples/index.html

## Documentation

https://doc.qt.io/qtforpython/index.html

## API reference

https://doc.qt.io/qtforpython/modules.html

## Misc

- https://doc.qt.io/qtforpython/overviews/model-view-programming.html
- https://doc.qt.io/qtforpython/overviews/modelview.html
- https://doc.qt.io/qtforpython/overviews/sql-programming.html
