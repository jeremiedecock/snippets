#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (jd.jdhp@gmail.com)

import numpy as np
import matplotlib.pyplot as plt
import math

import argparse
import json

def main():
    """Main function"""

    # PARSE OPTIONS ###################

    parser = argparse.ArgumentParser(description='Plot one or several part(s).')
    parser.add_argument('filename', nargs=1, metavar='FILE', help='DAT file to read')
    parser.add_argument("--title", "-t", help="set the title of the figure", metavar="STRING")
    args = parser.parse_args()

    title = args.title

    # PLOT DATA #######################

    fig = plt.figure(figsize=(16.0, 10.0))
    #fig = plt.figure()
    ax = fig.add_subplot(111)

    #ax.grid(True)

    # PARSE
    fd = open(args.filename[0], "r")
    data_dict = json.load(fd)

    # PLOT
    keys_to_plot_set = {key for key in data_dict.keys() if key.endswith("_position_z")}
    for key in keys_to_plot_set:
        ax.plot(data_dict["elapsed_simulation_time_sec"], data_dict[key], label=key)

    # TITLE AND LABELS ################

    FONTSIZE = 26
    FONTSIZE_S = 22

    if title is None:
        title = "Parts position with respect to time."

    ax.set_title(title, fontsize=FONTSIZE)
    ax.set_xlabel("Time (sec)",  fontsize=FONTSIZE)
    ax.set_ylabel("Position", fontsize=FONTSIZE)

    ax.legend(loc='best', fontsize=FONTSIZE_S)

    # SAVE FILES ######################

    fig_filename = "parts.pdf"
    plt.savefig(fig_filename)

    # PLOT ############################

    plt.show()

if __name__ == '__main__':
    main()
