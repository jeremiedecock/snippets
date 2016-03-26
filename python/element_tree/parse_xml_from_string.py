#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

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
See also https://docs.python.org/3/library/xml.etree.elementtree.html
"""

import xml.etree.ElementTree as et

DATA = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>

<library>
	<book date="1998-03-01" isbn="0262193981">
		<title><![CDATA[Reinforcement Learning: An Introduction]]></title>
		<author>Richard S. Sutton</author>
		<author>Andrew G. Barto</author>
        <tag>Computer Science</tag>
        <tag>Artificial Intelligence</tag>
        <tag>Reinforcement Learning</tag>
    </book>
	<book date="2009-12-11" isbn="0136042594">
		<title><![CDATA[Artificial Intelligence: A Modern Approach]]></title>
		<author>Stuart Russell</author>
		<author>Peter Norvig</author>
        <tag>Computer Science</tag>
        <tag>Artificial Intelligence</tag>
    </book>
</library>
"""

root = et.fromstring(DATA)

print(root.tag, root.attrib)

for child in root:
    print(child.tag, child.attrib)
