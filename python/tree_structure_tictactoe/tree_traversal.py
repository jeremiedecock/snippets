#!/usr/bin/env python
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

import pdb

class Node:
    """Node class"""

    _value = None
    _child_nodes = []

    def __init__(self, value):
        self._value = tuple(value)
        self._child_nodes = []      # WARNING: without this line, all "Node" objects share the same list "_child_nodes" !!!

        if not self.isFinal():
            player_id = self._value[-1]

            # Get the list index of empty squares (that is to say self._value[index]==0)
            empty_indices = [index for index, value in enumerate(self._value[:-1]) if value==0]
            for index in empty_indices:
                child_node_value = list(self._value)  # *copy* the list
                child_node_value[index] = player_id
                child_node_value[-1] = player_id * -1
                
                self._child_nodes.append(Node(child_node_value))

    def isFinal(self):
        is_final = False

        # Check lines
        if abs(sum(self._value[0:3])==3) or abs(sum(self._value[3:6])==3) or abs(sum(self._value[6:9])==3):
            is_final = True

        # Check columns
        if abs(sum(self._value[0::3])==3) or abs(sum(self._value[1::3])==3) or abs(sum(self._value[2::3])==3):
            is_final = True

        # Check diagonals
        if abs(sum(self._value[0::4])==3) or abs(sum(self._value[2:6:2])==3):
            is_final = True

        return is_final

    def getValue(self):
        return self._value

    def getChildNodes(self):
        return self._child_nodes


def walk(node):
    """The tree traversal function"""

    # Do something with node value...
    print node.getValue()

    # Recurse on each child node
    for child_node in node.getChildNodes():
        walk(child_node)


def main():
    """Main function

    Build the tic-tac-toe game tree and traverse it.
    """

    # Build the game tree
    root = Node([1, 0, 1,  -1, 0, -1,  0, 0, 0,  1])

    # Traverse the tree
    walk(root)


if __name__ == '__main__':
    main()

