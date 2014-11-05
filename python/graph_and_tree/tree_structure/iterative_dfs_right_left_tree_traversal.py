#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)

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

class Node:
    """Node class"""

    def __init__(self, value, child_nodes=[]):
        self._value = value
        self._child_nodes = child_nodes

    def getValue(self):
        return self._value

    def getChildNodes(self):
        return self._child_nodes


def walk(start_node):
    """The tree traversal function."""

    stack = [start_node]

    while len(stack) > 0:
        # Retrive the last element
        node = stack.pop()

        # Do something with node value...
        print(node.getValue())

        # Add child node into the stack
        stack.extend(node.getChildNodes())

        #print([n.getValue() for n in stack])


def main():
    """Main function

    Build the following test tree and traverse it.

           1
          /|\ 
         2 3 4
            / \
           5   6

    Top-down (right-left) traversal should print: 1, 4, 6, 5, 3, 2.
    """

    # Build the test tree
    n5 = Node(5)
    n6 = Node(6)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4, [n5, n6])
    n1 = Node(1, [n2, n3, n4])

    # Traverse the tree
    walk(n1)


if __name__ == '__main__':
    main()
