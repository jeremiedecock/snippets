=========================
IPython/Jupyter notebooks
=========================

Usage
=====

Open a terminal, go to the directory containing the `*.ipynb` files, then type::

    $ jupyter notebook

or::

    $ ipython notebook

or::

    $ ipython3 notebook

with old versions of IPython.

It open a notebook in your web browser.

Note: in my case, it's `ipython3` thus I will use it in the rest of this
document...

Nbviewer
========

Go there: http://nbviewer.ipython.org/, and put the URL of your `*.ipynb` files.

Slides
======

To view notebooks as slides::

    $ ipython3 nbconvert FILENAME.ipynb --to slides --post serve


