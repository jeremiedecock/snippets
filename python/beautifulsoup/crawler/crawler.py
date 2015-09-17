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

# Required package (on Debian8):
# - BeautifulSoup4: python3-bs4

# Online documentation:
# - BeautifulSoup4: http://www.crummy.com/software/BeautifulSoup/bs4/doc/
# - Urllib:         https://docs.python.org/3/library/internet.html
#                   https://docs.python.org/3/library/urllib.request.html

import argparse
from bs4 import BeautifulSoup
import urllib.request
import time
from urllib.parse import urljoin

TIME_SLEEP = 1

class Node:
    """Node class"""

    traversed_nodes = []

    def __init__(self, url, depth=0):
        self.url = url
        self.html = urllib.request.urlopen(self.url).read()
        self.depth = depth

    @property
    def child_nodes(self):
        child_nodes_set = set()

        if not self.is_final:
            #html = urllib.request.urlopen(self.url).read()
            soup = BeautifulSoup(self.html)

            for anchor in soup.find_all('a'):
                relative_url = anchor.get('href')
                absolute_url = urljoin(self.url, relative_url)
                child_node = Node(absolute_url, self.depth + 1)
                #print(id(child_node))
                child_nodes_set.add(child_node)

        return child_nodes_set

    def visit(self):
        """Do something with node value."""
        print("Visiting {}...".format(self.url))

        # Wait a litte bit
        time.sleep(TIME_SLEEP)      # TODO: randomize time sleep

    @property
    def is_final(self):
        return False

    def __str__(self):
        return "%s" % self.url

    def __eq__(self, other):
        """
        TODO: doctest

            node1 = Node("http://www.google.com")
            node2 = Node("http://www.google.com")
            traversed_nodes = [node1]
            node2 in traversed_nodes
            >>> True
        """

        return self.url == other.url

    def __hash__(self):
        # See http://stackoverflow.com/questions/1608842/types-that-define-eq-are-unhashable-in-python-3-x
        return id(self)


# TODO: make a subclass of Node for each website to crawl and redefine
# "visit", "child_nodes" and "is_final".



def walk(node):
    """The graph traversal function"""

    Node.traversed_nodes.append(node)
    
    # Do something with node value...
    node.visit()

    # Recurse on each child node
    for child_node in node.child_nodes:
        if child_node not in Node.traversed_nodes:
            walk(child_node)


def main():
    """Main function"""

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description='A BeautifulSoup snippet.')
    parser.add_argument("url", nargs=1, metavar="URL",
                        help="The URL of the webpage to parse.")
    args = parser.parse_args()

    url = args.url[0]

    # TRAVERSE THE GRAPH ######################################################

    start_node = Node(url)
    walk(start_node)

    # PRINT TRAVERSED NODES ###################################################

    print("Traversed nodes:")
    for node in Node.traversed_nodes:
        print(" ", node)


if __name__ == '__main__':
    main()
