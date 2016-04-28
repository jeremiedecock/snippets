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

import argparse

def main():
    """Main function"""

    parser = argparse.ArgumentParser(description='An argparse snippet.')

    # add_argument (see http://docs.python.org/2/library/argparse.html#the-add-argument-method)
    # - name or flags: Either a name or a list of option strings, e.g. foo or -f, --foo.
    # - action: The basic type of action to be taken when this argument is encountered at the command line
    #     - 'store': This just stores the argument’s value. This is the default action.
    #     - 'store_const': This stores the value specified by the const keyword argument.
    #     - 'store_true': This is a special cases of 'store_const' using for storing the value True.
    #     - 'store_false': This is a special cases of 'store_const' using for storing the value False.
    #     - 'append': This stores a list, and appends each argument value to the list. This is useful to allow an option to be specified multiple times.
    #     - 'append_const': This stores a list, and appends the value specified by the const keyword argument to the list.
    #     - 'count': This counts the number of times a keyword argument occurs.
    #     - 'help': This prints a complete help message for all the options in the current parser and then exits.
    #     - 'version': This expects a version= keyword argument in the add_argument() call, and prints version information and exits.
    # - nargs: The number of command-line arguments that should be consumed.
    # - const: A constant value required by some action and nargs selections.
    # - default: The value produced if the argument is absent from the command line.
    # - type: The type to which the command-line argument should be converted.
    # - choices: A container of the allowable values for the argument.
    # - required: Whether or not the command-line option may be omitted (optionals only).
    # - help: A brief description of what the argument does.
    # - metavar: A name for the argument in usage messages.
    # - dest: The name of the attribute to be added to the object returned by parse_args().
    parser.add_argument("--stropt", "-s", required=True, metavar="STRING",
            help="an example of str option")

    parser.add_argument("--intopt", "-i", type=int, default=3, metavar="INTEGER",
            help="an example of int option (default: 3)")

    parser.add_argument("--floatopt", "-f", type=float, default=3.14, metavar="FLOAT",
            help="an example of float option (default: 3.14)")

    parser.add_argument("--boolopt", "-b", action="store_true",
            help="an example of flag (boolean option)")

    parser.add_argument("fileargs", nargs="*", type=file, metavar="FILE",
            help="an example of file arguments")

    args = parser.parse_args()

    print "args.stropt:", args.stropt
    print "args.intopt:", args.intopt
    print "args.floatopt:", args.floatopt
    print "args.boolopt:", args.boolopt
    print "args.fileargs:", args.fileargs

if __name__ == '__main__':
    main()

