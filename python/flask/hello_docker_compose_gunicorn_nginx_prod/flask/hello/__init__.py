"""Accenta.ai prediction library

Note:

    This project is in beta stage.

Viewing documentation using IPython
-----------------------------------
To see which functions are available in `aipred`, type ``aipred.<TAB>`` (where
``<TAB>`` refers to the TAB key), or use ``aipred.*get_version*?<ENTER>`` (where
``<ENTER>`` refers to the ENTER key) to narrow down the list.  To view the
docstring for a function, use ``aipred.get_version?<ENTER>`` (to view the
docstring) and ``aipred.get_version??<ENTER>`` (to view the source code).
"""

import hello.core
from hello.core import app

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
# X.Y
# X.Y.Z # For bugfix releases  
# 
# Admissible pre-release markers:
# X.YaN # Alpha release
# X.YbN # Beta release         
# X.YrcN # Release Candidate   
# X.Y # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = '0.1.dev0'

def get_version():
    return __version__

__all__ = []
