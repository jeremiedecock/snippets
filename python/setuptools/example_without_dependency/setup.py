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

# Here is the procedure to submit updates to PyPI
# ===============================================
#
# 1. Register to PyPI:
#
#    $ python3 setup.py register
#
# 2. Upload the source distribution:
#
#    $ python3 setup.py sdist upload

from jdhp_setuptools_demo import __version__ as VERSION
from setuptools import setup, find_packages

# See :  http://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries']


# You can either specify manually the list of packages to include in the
# distribution or use "setuptools.find_packages()" to include them
# automatically with a recursive search (from the root directory of the
# project).
PACKAGES = find_packages()
#PACKAGES = ['jdhp_setuptools_demo']


# The following list contains all dependencies that Python will try to
# install with this project
#INSTALL_REQUIRES = ['pyserial >= 2.6', 'docutils >= 0.3']
INSTALL_REQUIRES = []


# Entry point can be used to create plugins or to automatically generate
# system commands to call specific functions.
# Syntax: "name_of_the_command_to_make = package.module:function".
#
# For instance, here it will automatically make the "rowyourboat" system
# command (when this package is installed) which calls
# nursery_rhymes.row_your_boat.sing().
#
# For more information: http://www.pythonhosted.org/setuptools/setuptools.html#automatic-script-creation
ENTRY_POINTS = {
  'console_scripts': [
      'setuptools-demo-nox = jdhp_setuptools_demo.row_your_boat:sing',
  ],
  'gui_scripts': [
      'setuptools-demo = jdhp_setuptools_demo.row_your_boat:gui',
  ]
}


README_FILE = 'README.rst'

def get_long_description():
    with open(README_FILE, 'r') as fd:
        desc = fd.read()
    return desc


setup(author='Jeremie DECOCK',
      author_email='jd.jdhp@gmail.com',
      maintainer='Jeremie DECOCK',
      maintainer_email='jd.jdhp@gmail.com',

      name='jdhp-setuptools-demo',
      description='A snippet to test setuptools and PyPI',
      long_description=get_long_description(),
      url='http://www.jdhp.org/',
      download_url='http://www.jdhp.org/',# Where the package can be downloaded

      entry_points=ENTRY_POINTS,
      include_package_data=True, # Use the MANIFEST.in file
      install_requires=INSTALL_REQUIRES,

      classifiers=CLASSIFIERS,
      #license='MIT license',    # Useless if license is already in CLASSIFIERS
      packages=PACKAGES,
      version=VERSION)
