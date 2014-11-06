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

"""
Provides Node classes for graph and tree traversal snippets.
"""

class Node:
    """
    A basic node class for graph and tree traversal snippets.
    
    Attributes:
      _value: the value of the node.
      _child_nodes: a list of node's children.
    """

    def __init__(self, value, child_nodes=[]):
        self._value = value
        self._child_nodes = child_nodes

    def getValue(self):
        return self._value

    def getChildNodes(self):
        return self._child_nodes


class GraphvizNode:
    """A node class using Graphviz for display"""

    node_list = []
    iteration_counter = 0
    id_counter = 0

    def __init__(self, value, child_nodes=[]):
        self._value = value
        self._child_nodes = child_nodes

        GraphvizNode.id_counter += 1
        self._id_str = "node_{}".format(GraphvizNode.id_counter)

        self.status = "not_visited"

        GraphvizNode.node_list.append(self)

    def getValue(self):
        GraphvizNode.iteration_counter += 1
        file_name = "{}.dot".format(GraphvizNode.iteration_counter)
        self.writeGraphvizFile(file_name)

        self.status = "visited"

        return self._value

    def getChildNodes(self):
        return self._child_nodes

    def writeGraphvizFile(self, file_name):
        """Write graphviz file"""
        with open(file_name, 'w') as fd:
            fd.write("digraph G {\n")

            for node in GraphvizNode.node_list:
                if node is self:
                    fd.write('\t{str_id}[label="{label}", color=red, style=filled, shape=circle];\n'.format(str_id=node._id_str, label=node._value))
                elif node.status == "visited":
                    fd.write('\t{str_id}[label="{label}", color=lightgray, style=filled, shape=circle];\n'.format(str_id=node._id_str, label=node._value))
                else:
                    fd.write('\t{str_id}[label="{label}", shape=circle];\n'.format(str_id=node._id_str, label=node._value))

            for node in GraphvizNode.node_list:
                if len(node._child_nodes) > 0:
                    children_str = ", ".join([child_node._id_str for child_node in node._child_nodes])
                    fd.write("\t{} -> {};\n".format(node._id_str, children_str))

            fd.write("}")
