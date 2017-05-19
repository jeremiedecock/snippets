#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

import sys

SCRIPT_NAME = os.path.basename(sys.argv[0])
OUTPUT_FILE_PATH = "matplotlib_snippets.ipynb"
NB_TITLE = "Matplotlib snippets"

# DIRECTORY PARSER ############################################################

def get_file_list(directory_path='.'):
    """
    Return the list of all python file's path in `directory_path`.
    """

    # Parse the input directory
    print("Parsing", directory_path)

    file_name_list = [os.path.join(directory_path, file_name)
                      for file_name
                      in os.listdir(directory_path)
                      if os.path.isfile(os.path.join(directory_path, file_name))
                      and file_name.endswith(".py")
                      and not os.path.islink(os.path.join(directory_path, file_name))
                      and file_name != SCRIPT_NAME]  # Ignore this script

    return file_name_list


# FILE PARSER #################################################################

def rst_to_markdown(docstring):
    markdown_code = docstring                    # TODO
    return markdown_code

def get_file_content(python_file_path):
    """
    Return the list of all python file's path in `directory_path`.
    """

    title = "Unknown"    # Snippet title
    docstring = []       # Module docstring
    python_code = []     # Python code

    # status=0 means the module docstring hasn't been reached yet
    # status=1 means the current line is in the module docstring
    # status=2 means the current line is in the module python code
    status = 0

    with open(python_file_path, 'rU') as fd:
        for line in fd.readlines():
            if line in ("'''\n", '"""\n'):
                status += 1
            else:
                if status == 1:
                    docstring.append(line)
                elif status == 2:
                    python_code.append(line)

    markdown_code = rst_to_markdown(docstring)

    return title, markdown_code, python_code


# NOTEBOOK ####################################################################

def init_notebook():

    ipynb_dict = {"cells": [
                   {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                     "# {}".format(NB_TITLE)
                    ]
                   },
                   {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {
                     "collapsed": True
                    },
                    "outputs": [],
                    "source": [
                     "%matplotlib inline"
                    ]
                   }
                  ],
                  "metadata": {
                   "anaconda-cloud": {},
                   "kernelspec": {
                    "display_name": "Python [default]",
                    "language": "python",
                    "name": "python3"
                   },
                   "language_info": {
                    "codemirror_mode": {
                     "name": "ipython",
                     "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.5.2"
                   }
                  },
                  "nbformat": 4,
                  "nbformat_minor": 1
                 }

    return ipynb_dict


def add_cells(ipynb_dict, title, file_path, markdown_code, python_code):

    file_name = os.path.basename(file_path)

    markdown_cell = {
                     "cell_type": "markdown",
                     "metadata": {},
                     "source": [
                      "## {}\n".format(title),
                      "Source: {}\n\n".format(file_name)
                     ] + markdown_code
                    }

    code_cell = {
                 "cell_type": "code",
                 "execution_count": None,
                 "metadata": {
                  "collapsed": True
                 },
                 "outputs": [],
                 "source": python_code
                }

    ipynb_dict["cells"].append(markdown_cell)
    ipynb_dict["cells"].append(code_cell)



if __name__ == '__main__':

    ipynb_dict = init_notebook()

    file_path_list = get_file_list()

    for file_path in file_path_list:
        print("Parsing", file_path)
        title, markdown_code, python_code = get_file_content(file_path)
        add_cells(ipynb_dict, title, file_path, markdown_code, python_code)

    # Save the notebook
    with open(OUTPUT_FILE_PATH, "w") as fd:
        #json.dump(ipynb_dict, fd)                           # no pretty print
        json.dump(ipynb_dict, fd, sort_keys=True, indent=1)  # pretty print format

