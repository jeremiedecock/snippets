#!/bin/sh

# For optimal parameters, see:
# - https://support.google.com/youtube/answer/1722171?hl=en
# - https://trac.ffmpeg.org/wiki/Encode/H.264
#
# Video codec: H.264
# - Progressive scan (no interlacing)
# - High Profile
# - 2 consecutive B frames
# - Closed GOP. GOP of half the frame rate.
# - CABAC
# - Variable bitrate. No bitrate limit required, though we offer recommended bit rates below for reference
# - Chroma subsampling: 4:2:0

avconv -f image2 -i ./capture_%04d.png -c:v libx264 -profile:v high -pix_fmt yuv420p -b:v 5000k -pass 1 video.mp4 && \
avconv -f image2 -i ./capture_%04d.png -c:v libx264 -profile:v high -pix_fmt yuv420p -b:v 5000k -pass 2 video.mp4

#avconv -f image2 -i ./capture_%04d.png video.mp4
