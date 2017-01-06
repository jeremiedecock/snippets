#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt


def get_pixel_value(image, x, y, type_border):
    if type_border == 0:
        try:
            pixel_value = image[x, y]
            return pixel_value
        except IndexError as e:
            return 0
    elif type_border == 1:
        num_lines, num_col = image.shape    # TODO
        x = x % num_lines
        y = y % num_col
        pixel_value = image[x, y]
        return pixel_value
    elif type_border == 2:
        num_lines, num_col = image.shape    # TODO

        if x >= num_lines:
            x = num_lines - 2 - x
        elif x < 0:
            x = abs(x)

        if y >= num_col:
            y = num_col - 2 - y
        elif y < 0:
            y = abs(y)

        pixel_value = image[x, y]
        return pixel_value
    elif type_border == 3:
        num_lines, num_col = image.shape    # TODO

        if x >= num_lines:
            x = num_lines - 1 - x
        elif x < 0:
            x = abs(x) - 1

        if y >= num_col:
            y = num_col - 1 - y
        elif y < 0:
            y = abs(y) - 1

        pixel_value = image[x, y]
        return pixel_value
    else:
        raise ValueError()



#def smooth_bspline(img_in, img_out, type_border, step_trou):
#
#    int num_lines = img_in.nl();  // num lines in the image
#    int num_col = img_in.nc();  // num columns in the image
#
#    int i, j, step;
#
#    float coeff_h0 = 3. / 8.;
#    float coeff_h1 = 1. / 4.;
#    float coeff_h2 = 1. / 16.;
#
#    Ifloat buff(num_lines, num_col, "buff smooth_bspline");
#
#    step = (int)(pow((double)2., (double) step_trou) + 0.5);
#
#    for (i = 0; i < num_lines; i ++)
#    for (j = 0; j < num_col; j ++)
#       buff(i,j) = coeff_h0 * img_in(i,j)
#                 + coeff_h1 * (  img_in(i, j-step, type_border)
#                               + img_in(i, j+step, type_border))
#                 + coeff_h2 * (  img_in(i, j-2*step, type_border)
#                               + img_in(i, j+2*step, type_border));
#
#    for (i = 0; i < num_lines; i ++)
#    for (j = 0; j < num_col; j ++)
#       img_out(i,j) = coeff_h0 * buff(i,j)
#                    + coeff_h1 * (  buff(i-step, j, type_border)
#                                  + buff(i+step, j, type_border))
#                    + coeff_h2 * (  buff(i-2*step, j, type_border)
#                                  + buff(i+2*step, j, type_border));


def smooth_bspline(input_image, type_border, step_trou):

    input_image = input_image.astype('float64', copy=True)

    coeff_h0 = 3. / 8.
    coeff_h1 = 1. / 4.
    coeff_h2 = 1. / 16.

    num_lines, num_col = input_image.shape    # TODO

    buff = np.zeros(input_image.shape, dtype='float64')
    img_out = np.zeros(input_image.shape, dtype='float64')

    step = int(pow(2., step_trou) + 0.5)

    print("step =", step)

    for i in range(num_lines):
        for j in range(num_col):
            buff[i,j]  = coeff_h0 *    get_pixel_value(input_image, i, j,        type_border) 
            buff[i,j] += coeff_h1 * (  get_pixel_value(input_image, i, j-step,   type_border) \
                                     + get_pixel_value(input_image, i, j+step,   type_border))
            buff[i,j] += coeff_h2 * (  get_pixel_value(input_image, i, j-2*step, type_border) \
                                     + get_pixel_value(input_image, i, j+2*step, type_border))

#    for (i = 0; i < num_lines; i ++)
#    for (j = 0; j < num_col; j ++)
#       img_out(i,j) = coeff_h0 * buff(i,j)
#                    + coeff_h1 * (  buff(i-step, j, type_border)
#                                  + buff(i+step, j, type_border))
#                    + coeff_h2 * (  buff(i-2*step, j, type_border)
#                                  + buff(i+2*step, j, type_border));
    for i in range(num_lines):
        for j in range(num_col):
            img_out[i,j]  = coeff_h0 *    get_pixel_value(buff, i,        j, type_border) 
            img_out[i,j] += coeff_h1 * (  get_pixel_value(buff, i-step,   j, type_border) \
                                        + get_pixel_value(buff, i+step,   j, type_border))
            img_out[i,j] += coeff_h2 * (  get_pixel_value(buff, i-2*step, j, type_border) \
                                        + get_pixel_value(buff, i+2*step, j, type_border))

    return img_out



def transform(image, num_scales):
    # MR_Transf.band(0) = Image;
    # for (s = 0; s < Nbr_Plan -1; s++)
    # {
    #     smooth_bspline (MR_Transf.band(s),MR_Transf.band(s+1),Border,s);
    #     if  (Details == True) MR_Transf.band(s) -= MR_Transf.band(s+1);
    # }

    image = image.astype('float64', copy=True)

    scale_list = []
    scale_list.append(image)

    for scale_index in range(num_scales - 1):
        previous_scale = scale_list[scale_index]

        next_scale = smooth_bspline(previous_scale, 3, scale_index)

        previous_scale -= next_scale

        scale_list.append(next_scale)

    return scale_list



def read_fits_file(file_path):
    # Open the FITS file
    hdu_list = fits.open(file_path)

    data = hdu_list[0].data

    # Close the FITS file
    hdu_list.close()

    return data


def save_image(data, file_path):
    interp='nearest'     # "raw" (non smooth) map

    fig = plt.figure()
    ax = fig.add_subplot(111)

    im = ax.imshow(data, interpolation=interp, origin='lower', cmap="gnuplot2")   # cmap=cm.inferno and cmap="inferno" are both valid

    plt.colorbar(im) # draw the colorbar

    plt.savefig(file_path)
    plt.show()


# PARSE OPTIONS ###############################################################

parser = argparse.ArgumentParser(description="Bspline wavelet transform")
parser.add_argument("filearg", nargs=1, metavar="FILE", help="the FITS file to process")
args = parser.parse_args()
file_path = args.filearg[0]

# PROCESS DATA ################################################################

# Read data
data = read_fits_file(file_path)

num_scales = 4
transformed_image = transform(data, num_scales)

print(transformed_image)

# Write data
for scale_index, scale in enumerate(transformed_image):
    save_image(scale, file_path + "." + str(scale_index) + ".out.png")

