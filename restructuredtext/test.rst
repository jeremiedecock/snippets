========================
reStructuredText snippet
========================

:Authors:   Jérémie Decock
:Version:   1.0
:Date:      2015-08-01
:Contact:   jd.jdhp@gmail.com
:Copyright: Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

Online documentation
====================

See:

- http://docutils.sourceforge.net/rst.html
- http://docutils.sourceforge.net/docs/user/rst/quickstart.html
- http://docutils.sourceforge.net/docs/user/rst/quickref.html
- http://docutils.sourceforge.net/docs/user/rst/cheatsheet.txt
- https://aful.org/wikis/interop/ReStructuredText
- https://en.wikipedia.org/wiki/ReStructuredText
- https://docs.python.org/3.1/documenting/rest.html
- https://docs.python.org/devguide/documenting.html
- http://docutils.sourceforge.net/docs/user/links.html


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

   pandoc -o output.html input.md

Pandoc can be used to convert a Markdown document in reStructuredText::

   pandoc -o output.html input.md

More tools
~~~~~~~~~~

More tools are listed at http://docutils.sourceforge.net/docs/user/links.html


Paragraphs
==========

Paragraph 1, blablabla blablabla blablabla blablabla blablabla blablabla
blablabla blablabla blablabla blablabla blablabla blablabla blablabla
blablabla blablabla blablabla blablabla blablabla blablabla blablabla

Paragraph 2, blablabla blablabla blablabla blablabla blablabla blablabla
blablabla blablabla blablabla blablabla blablabla blablabla blablabla
blablabla blablabla blablabla blablabla blablabla blablabla blablabla

Links
=====

External links
--------------

`external link <https://help.github.com/articles/markdown-basics/>`__

Internal links and anchors
--------------------------

TODO...

Lists
=====

Unordered lists
---------------

-  item 1
-  item 2
-  item 3

-  item 1
-  item 2
-  item 3

Nested unordered lists
----------------------

-  item 1

   -  item 1.1
   -  item 1.2
   -  item 1.3

-  item 2

   -  item 2.1
   -  item 2.2
   -  item 2.3

-  item 3

   -  item 3.1
   -  item 3.2
   -  item 3.3

Ordered lists
-------------

1. item 1
2. item 2
3. item 3

Definition lists
----------------

Word1
  Definition of word1

*Word2*
  Definition of word2

Nested ordered lists
--------------------

1. item 1

   1. item 1.1
   2. item 1.2
   3. item 1.3

2. item 2

   1. item 2.1
   2. item 2.2
   3. item 2.3

3. item 3

   1. item 3.1
   2. item 3.2
   3. item 3.3

Nested ordered and unordered lists
----------------------------------

1. item 1

   1. item 1.1
   2. item 1.2
   3. item 1.3

2. item 2

   -  item 2.1
   -  item 2.2
   -  item 2.3

3. item 3

   -  item 3.1
   -  item 3.2
   -  item 3.3

Styling text
============

*Italic* or **bold** text.

*Italic* or **bold** text.

Images
======

.. image:: http://www.jdhp.org/medias/images/header.jpeg
   :alt: JDHP logo

Unformat
========

This is an example of ``<html>`` tag.

Blockquotes
===========

As Descartes said

    Cogito, ergo sum

Literal blocks
==============

As Descartes said::

    Cogito, ergo sum

Table
=====

+------------+------------+-----------+
| Header 1   | Header 2   | Header 3  |
+============+============+===========+
| (1,1)      | (1,2)      | (1,3)     |
+------------+------------+-----------+
| (2,1)      | Multi-column cell      |
+------------+------------+-----------+
| (3,1)      | Multi-row  | (3,3)     |
+------------+ cell       +-----------+
| (4,1)      |            | (4,3)     |
+------------+------------+-----------+
