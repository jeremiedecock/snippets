#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (jd.jdhp@gmail.com)

import numpy as np
import matplotlib.pyplot as plt
import math

import argparse

def parse_part_log_file(filename):
    log_data = np.loadtxt(filename)

    data_dict = {}
    data_dict["time_sec"]           = log_data[:, 0]
    data_dict["position_x"]         = log_data[:, 1]
    data_dict["position_y"]         = log_data[:, 2]
    data_dict["position_z"]         = log_data[:, 3]
    data_dict["angle_x"]            = log_data[:, 4]
    data_dict["angle_y"]            = log_data[:, 5]
    data_dict["angle_z"]            = log_data[:, 6]
    data_dict["angle_w"]            = log_data[:, 7]
    data_dict["linear_velocity_x"]  = log_data[:, 8]
    data_dict["linear_velocity_y"]  = log_data[:, 9]
    data_dict["linear_velocity_z"]  = log_data[:,10]
    data_dict["angular_velocity_x"] = log_data[:,11]
    data_dict["angular_velocity_y"] = log_data[:,12]
    data_dict["angular_velocity_z"] = log_data[:,13]
    data_dict["total_force_x"]      = log_data[:,14]
    data_dict["total_force_y"]      = log_data[:,15]
    data_dict["total_force_z"]      = log_data[:,16]
    data_dict["total_torque_x"]     = log_data[:,17]
    data_dict["total_torque_y"]     = log_data[:,18]
    data_dict["total_torque_z"]     = log_data[:,19]

    return data_dict


def main():
    """Main function"""

    # PARSE OPTIONS ###################

    parser = argparse.ArgumentParser(description='Plot one or several part(s).')
    parser.add_argument('filenames', nargs='+', metavar='FILE', help='DAT file to read')
    parser.add_argument("--title", "-t", help="set the title of the figure", metavar="STRING")
    args = parser.parse_args()

    title = args.title

    # PLOT DATA #######################

    fig = plt.figure(figsize=(16.0, 10.0))
    #fig = plt.figure()
    ax = fig.add_subplot(111)

    #ax.grid(True)

    for index, filename in enumerate(args.filenames):
        print(index, filename)

        data_dict = parse_part_log_file(filename)

        ax.plot(data_dict["time_sec"], data_dict["position_z"], label=filename)

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
