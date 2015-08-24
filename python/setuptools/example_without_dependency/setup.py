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

from setuptools import setup, find_packages

from nursery_rhymes import __version__ as VERSION

# See :  http://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries']

#PACKAGES = ['nursery_rhymes']

README_FILE = 'README.rst'

def get_long_description():
    with open(README_FILE, 'r') as fd:
        desc = fd.read()
    return desc

setup(author='Jeremie DECOCK',
      author_email='jd.jdhp@gmail.com',

      name='nursery_rhymes',
      description='A snippet to show how to install a project with setuptools',
      long_description=get_long_description(),
      url='http://www.jdhp.org/',

      classifiers=CLASSIFIERS,
      license='MIT license',     # Useless if license is already in CLASSIFIERS

      # You can either specify manually the list of packages to include in the
      # distribution or use "setuptools.find_packages()" to include them
      # automatically with a recursive search (from the root directory of the
      # project).
      packages=find_packages(),
      #packages=PACKAGES,

      include_package_data=True,   # Use the MANIFEST.in file

      # The following list contains all dependencies that Python will try to
      # install with this project
      #install_requires= ['pyserial >= 2.6', 'docutils >= 0.3'],

      # Entry point can be used to create plugins or to automatically generate
      # system commands to call specific functions.
      # Syntax: "name_of_the_command_to_make = package.module:function".
      #
      # For instance, here it will automatically make the "rowyourboat" system
      # command (when this package is installed) which calls
      # nursery_rhymes.row_your_boat.sing().
      entry_points = {
          'console_scripts': [
              'rowyourboat = nursery_rhymes.row_your_boat:sing',
          ],
      },

      version=VERSION)
