#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# See: http://scikit-learn.org/stable/tutorial/basic/tutorial.html#loading-an-example-dataset
#      http://scikit-learn.org/stable/datasets/index.html#datasets

from __future__ import print_function

from sklearn import datasets

import matplotlib.pyplot as plt

def main():

    # http://scikit-learn.org/stable/tutorial/basic/tutorial.html#loading-an-example-dataset
    # "A dataset is a dictionary-like object that holds all the data and some
    # metadata about the data. This data is stored in the .data member, which
    # is a n_samples, n_features array. In the case of supervised problem, one
    # or more response variables are stored in the .target member."

    # Toy datasets

    iris = datasets.load_iris()         # The iris dataset (classification)
    digits = datasets.load_digits()     # The digits dataset (classification)

    #boston = datasets.load_boston()     # The boston house-prices dataset (regression)
    #diabetes = datasets.load_diabetes() # The diabetes dataset (regression)
    #linnerud = datasets.load_linnerud() # The linnerud dataset (multivariate regression)

    print(iris.feature_names)
    print(iris.data)
    print(iris.target_names)
    print(iris.target)

    print(digits.images[0])
    print(digits.target_names)
    print(digits.target)

    plt.imshow(digits.images[0], cmap='gray', interpolation='nearest')
    plt.show()

    # Others datasets
    
    # See: http://scikit-learn.org/stable/datasets/index.html#datasets



if __name__ == '__main__':
    main()

