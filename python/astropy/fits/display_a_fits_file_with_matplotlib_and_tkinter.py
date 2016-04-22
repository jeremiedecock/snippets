#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation: http://docs.astropy.org/en/stable/io/fits/index.html

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib import cm

import tkinter as tk

import argparse

from astropy.io import fits


def get_image_array_from_fits_file(file_path):
    
    hdu_list = fits.open(file_path)   # open the FITS file

    if len(hdu_list) != 1:
        raise Exception("The FITS file should contain only one HDU.")

    image_array = hdu_list[0].data    # "hdu.data" is a Numpy Array

    hdu_list.close()

    return image_array


def main():

    # PARSE OPTIONS ###############################################################

    parser = argparse.ArgumentParser(description="Display a FITS file with Tkinter.")
    parser.add_argument("filearg", nargs=1, metavar="FILE",
                        help="the FITS file to process")
    args = parser.parse_args()
    input_file_path = args.filearg[0]


    # READ THE INPUT FILE #########################################################

    input_img = get_image_array_from_fits_file(input_file_path)

    if input_img.ndim != 2:
        raise Exception("Unexpected error: the input FITS file should contain a 2D array.")


    # MATPLOTLIB ##################################################################

    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title(input_file_path)
    ax.imshow(input_img, interpolation='nearest', cmap=cm.gray)


    # TKINTER #####################################################################

    root = tk.Tk()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    button = tk.Button(master=root, text='Quit', command=_quit)
    button.pack(fill="x", expand=True)

    # Add a callback on WM_DELETE_WINDOW event
    root.protocol("WM_DELETE_WINDOW", _quit)

    root.mainloop()

if __name__ == "__main__":
    main()


