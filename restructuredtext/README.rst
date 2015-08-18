================
ReStructuredText
================

:Authors:   Jérémie Decock
:Version:   1.0
:Date:      2015-08-01
:Contact:   jd.jdhp@gmail.com
:Copyright: Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

What is ReStructuredText ?
==========================

    "reStructuredText is an easy-to-read, what-you-see-is-what-you-get
    plaintext markup syntax and parser system. It is useful for in-line program
    documentation (such as Python docstrings), for quickly creating simple web
    pages, and for standalone documents. reStructuredText is designed for
    extensibility for specific application domains. The reStructuredText parser
    is a component of Docutils. reStructuredText is a revision and
    reinterpretation of the StructuredText and Setext lightweight markup
    systems." (http://docutils.sourceforge.net/rst.html)

Online documentation
====================

- Official web site: http://docutils.sourceforge.net/rst.html
- Reference: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
- Quickref: http://docutils.sourceforge.net/docs/user/rst/quickref.html
- Quickstart: http://docutils.sourceforge.net/docs/user/rst/quickstart.html
- Cheatsheet: http://docutils.sourceforge.net/docs/user/rst/cheatsheet.txt
- Wikipedia: https://en.wikipedia.org/wiki/ReStructuredText
- AFUL (french) tutorial: https://aful.org/wikis/interop/ReStructuredText
- Python:
    - https://docs.python.org/3.1/documenting/rest.html
    - https://docs.python.org/devguide/documenting.html
- Links: http://docutils.sourceforge.net/docs/user/links.html


Tools (on Debian Gnu/Linux)
===========================

Docutils
--------

The main distribution of reStructuredText is the python-docutils package. It
contains several conversion tools:

- rst2html
- rst2latex
- rst2man
- rst2odt
- rst2s5 (S5, a Simple Standards-based Slide Show System)
- rst2beamer (generates a LaTeX source that uses the Beamer document class) http://docutils.sourceforge.net/sandbox/rst2beamer/

Other tools
-----------

rst2pdf
~~~~~~~

Usage::

  rst2pdf test.rst

Pandoc
~~~~~~

Pandoc is a document converter that can write Markdown, reStructuredText, HTML,
LaTeX, RTF, DocBook XML, and S5::

   pandoc -o output.html input.rst

Pandoc can be used to convert a Markdown document in reStructuredText::

   pandoc -o output.rst input.md

More tools
~~~~~~~~~~

More tools are listed at http://docutils.sourceforge.net/docs/user/links.html

