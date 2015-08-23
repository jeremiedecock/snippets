#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PyNurseryRhymesDemo

# The MIT License
#
# Copyright (c) 2010,2015 Jeremie DECOCK (http://www.jdhp.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from nursery_rhymes import __version__ as VERSION
from distutils.core import setup

# See :  http://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Operating System :: POSIX :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries']

PACKAGES = ['nursery_rhymes']

README_FILE = 'README.rst'

def get_long_description():
    with open(README_FILE, 'r') as fd:
        desc = fd.read()
    return desc

# Don't use unicode strings in setup arguments or bdist_rpm will fail.
setup(author='Jeremie DECOCK',
      author_email='jd.jdhp@gmail.com',
      classifiers=CLASSIFIERS,
      description='A snippet to show how to install a project with setuptools',
      license='MIT license',
      long_description=get_long_description(),
      maintainer='Jeremie DECOCK',
      maintainer_email='jd.jdhp@gmail.com',
      name='nursery_rhymes',
      packages=PACKAGES,
      url='http://www.jdhp.org/',
      version=VERSION)
