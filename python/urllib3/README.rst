=======
Urllib3
=======

Urllib vs urllib2 vs urllib3 (WTF!)
-----------------------------------

Urllib is part of the Python3 standard library but this is **not the case** for
urllib2 and urllib3 ! (and yes, this is quite confusing)

    "urllib and urllib2 have little to do with each other. They were designed
    to be independent and standalone, each solving a different scope of
    problems, and urllib3 follows in a similar vein."
    https://pypi.python.org/pypi/urllib3

To sum up, if you just want to get HTML from a basic HTTP source, urllib
is probably enough (moreover it's already in the standard library).
If you wand advanced features, urllib2/urllib3 may be more adequate.


Required package (on Debian8)
-----------------------------

    python3-urllib3

Online documentation
--------------------

https://urllib3.readthedocs.org/en/latest/
