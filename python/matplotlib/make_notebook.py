#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os

import sys

'''
Snippets should have the following structure:

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SNIPPET_TITLE

SNIPPET DESCRIPTION
"""

SNIPPET CODE
'''

SCRIPT_NAME = os.path.basename(sys.argv[0])
OUTPUT_FILE_PATH = "../../../../jdhp-docs/notebooks/matplotlib_snippets.ipynb"
NB_TITLE = "Matplotlib snippets"
GIT_BASE_URL = "https://github.com/jeremiedecock/snippets/blob/master/python/matplotlib/"
FILES_TO_IGNORE = [
    SCRIPT_NAME,                # Ignore this script
    "animation.py",
    "animation_alt.py",
    # TODO
    "hist2d_contour.py",
    "hist2d_contour_sigmas.py",
    "hist2d_hexa.py",
    "hist2d_hexa_logscale_xy.py",
    "hist2d_logscale_xy.py",
    "hist2d_logscale_z.py",
    "hist2d_scatter_plot.py",
    "hist2d_scatter_plot_logscale_xy.py",
    "hist_logscale_x.py",
    "hist_logscale_xy.py",
    "hist_logscale_y.py",
    "hist_with_weighted_values.py",
    "imshow_ax.py",
    "imshow_colour_map_ax.py",
    "imshow_colour_map_plt.py",
    "imshow_plt.py",
    "imshow_with_histogram_ax.py",
    "log_scale.py",
    "log_scale2.py",
    "make_notebook.py",
    "matplotlib_gtk3_widget.py",
    "multiple_y_axis.py",
    "no_axis.py",
    "no_ticks_and_labels.py",
    "parametric_curve.py",
    "plot2d.py",
    "plot_style_availables.py",
    "plot_style_seaborn_paper.py",
    "plot_style_seaborn_poster.py",
    "plot_style_seaborn_talk.py",
    "ratio_of_two_histograms.py",
    "realtime_plot.py",
    "realtime_plot_alt.py",
    "save_without_borders.py",
    "subplots_full_example.py",
    "subplots_meth1.py",
    "subplots_meth2.py",
    "subplots_meth3.py",
    "subplots_meth4.py",
    "subplots_meth5.py",
    "text_box.py",
    "tkinter.py",
    "tkinter_using_class.py",
    "tkinter_using_class_and_toolbar.py",
    "tkinter_using_class_and_toolbar_and_keyboard_events.py",
    "tkinter_with_animation.py",
    "tkinter_with_navigation_toolbar.py",
    "tkinter_with_widgets_interactions.py",
    "tkinter_without_navigation_toolbar.py",
    "twinx.py",
    "zorder.py"
]

# DIRECTORY PARSER ############################################################

def get_file_list(directory_path='.'):
    """
    Return the list of all python file's path in `directory_path`.
    """

    # Parse the input directory
    file_name_list = [os.path.join(directory_path, file_name)
                      for file_name
                      in os.listdir(directory_path)
                      if os.path.isfile(os.path.join(directory_path, file_name))
                      and file_name.endswith(".py")
                      and not os.path.islink(os.path.join(directory_path, file_name))
                      and file_name not in FILES_TO_IGNORE]

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
    # status=1 means the current line is the title
    # status=2 means the current line is in the module docstring
    # status=3 means the current line is in the module python code
    status = 0

    with open(python_file_path, 'rU') as fd:
        for line in fd.readlines():
            if line.strip() in ("'''", '"""'):
                status += 1
            else:
                if status == 1:
                    title = line
                    status += 1
                elif status == 2:
                    if not(len(docstring) == 0 and len(line.strip()) == 0):
                        docstring.append(line)
                elif status == 3:
                    if not(len(python_code) == 0 and len(line.strip()) == 0):
                        if not line.strip().startswith("plt.savefig("):
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
                     "# {}\n\n".format(NB_TITLE),
                     "Author: Jérémie Decock (http://www.jdhp.org)\n",
                     "\n",
                     "Last update: {}\n".format(datetime.date.isoformat(datetime.date.today())),
                     "\n",
                     "This document has been made from snippets using {}make_notebook.py".format(GIT_BASE_URL)
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
                      "Source: {}{}\n\n".format(GIT_BASE_URL, file_name)
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
    print("Writing", OUTPUT_FILE_PATH)

    with open(OUTPUT_FILE_PATH, "w") as fd:
        #json.dump(ipynb_dict, fd)                           # no pretty print
        json.dump(ipynb_dict, fd, sort_keys=True, indent=1)  # pretty print format
