#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Jérémie DECOCK (http://www.jdhp.org)

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

"""
Depth-first search.
"""

from node import Node as Node
#from node import GraphvizNode as Node

def walk(node, preorder):
    """The tree traversal function."""

    # Pre-order visit (top down)
    if preorder:
        print(node.getValue())

    # Recurse on each child node
    for child_node in node.getChildNodes():
        walk(child_node, preorder)

    # Post-order visit (bottom up)
    if not preorder:
        print(node.getValue())


def test():
    r"""Main function

    Build the following test tree and traverse it.

           1
          /|\ 
         2 3 4
        / \
       5   6

    Top-down traversal should print: 1, 2, 5, 6, 3, 4.
    """

    # Build the test tree
    n5 = Node(5)
    n6 = Node(6)
    n2 = Node(2, [n5, n6])
    n3 = Node(3)
    n4 = Node(4)
    n1 = Node(1, [n2, n3, n4])

    print(r"""
           1
          /|\ 
         2 3 4
        / \
       5   6
    """)

    # Pre-order walk
    print("Pre-order walk (top down)")
    walk(n1, True)

    # Post-order walk
    print("\nPost-order walk (bottom up)")
    walk(n1, False)


if __name__ == '__main__':
    test()
