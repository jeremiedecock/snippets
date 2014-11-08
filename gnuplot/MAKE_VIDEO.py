#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import math

"""    
Crée une représentation animée de données avec gnuplot.
"""

def main():

    outfile = 'video'
    angle_x = 45
    num_frames = 360

    # Make video ####################################################

    for frame_index in range(num_frames):
        
        print('{:.2f}%'.format(float(frame_index) / float(num_frames) * 100.0))

        # Write gnuplot file #########################################
        with open('/tmp/tmp.gp', 'w') as fd:
            print('set zeroaxis', file=fd)
            print('set view {},{}'.format(angle_x, frame_index%360), file=fd)
            print('set isosamples 100', file=fd)
            print('set hidden3d', file=fd)

            print("set term pngcairo size 1920,1080 enhanced font 'Verdana,10'", file=fd)
            print('set output "/tmp/frame_{:04d}.png"'.format(frame_index), file=fd)
            #print('splot [-pi:pi][-pi:pi] sin(x**2+y**2)/(x**2+y**2)', file=fd)
            print('splot [-2*pi:2*pi][-2*pi:2*pi] sin((x+{0})**2+(y)**2)/((x+{0})**2+(y)**2)'.format(frame_index/100.), file=fd)
            print('set output', file=fd)
            print('set term X11', file=fd)

        # Plot datas ################################################
        os.system('gnuplot /tmp/tmp.gp')

    os.remove('/tmp/tmp.gp')

    # Write video file ##############################################

    #os.system('ffmpeg2theora -f image2 /tmp/frame_%04d.png -o {}.ogv'.format(outfile))
    os.system('avconv -f image2 -i /tmp/frame_%04d.png {}.mp4'.format(outfile))


if __name__ == "__main__":
    main()
