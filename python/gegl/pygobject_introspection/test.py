#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

"""
A simple GEGL snippet with the Gobject automatic introspection method.

This inverts the colors of a PNG file.

BUG: GEGL has been built without introspection on Debian 8.
     See https://github.com/jsbueno/python-gegl/issues/2

See: http://linuxfr.org/news/gegl-0-3-0-et-babl-0-1-12-sont-de-sortie
     http://gegl.org/operations.html#Gegl
     http://gegl.org/operations.html#GEGL%20operations
     https://github.com/jsbueno/python-gegl/blob/master/snippets.py
     https://github.com/jsbueno/python-gegl

Debian dependencies: libgegl-dev (?)
"""

import argparse

from gi.repository import Gegl as gegl

def main():

    # Parse options

    parser = argparse.ArgumentParser(description='An argparse snippet.')

    parser.add_argument("--infile",  "-i",  help="the input file",  required=True, metavar="STRING")
    parser.add_argument("--outfile", "-o",  help="the output file", required=True, metavar="STRING")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile

    # GEGL ######################################

    gegl.init([])

    #print(gegl.list_operations())

    # Make nodes

    node1 = gegl.Node()
    node2 = gegl.Node() # png-load
    node3 = gegl.Node() # invert
    node4 = gegl.Node() # png-save

    # Set properties

    node2.set_property("operation", "gegl:png-load")
    node2.set_property("path", infile)

    node3.set_property("operation", "gegl:invert")

    node4.set_property("operation", "gegl:png-save")
    node4.set_property("path", outfile)

    # Make the graph

    node1.add_child(node2)
    node1.add_child(node3)
    node1.add_child(node4)

    node2.connect_to("output", node3, "input")
    node3.connect_to("output", node4, "input")

    # Process

    node4.process()

if __name__ == '__main__':
    main()

