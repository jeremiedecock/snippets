/* 
 * OpenCV - Display image: display an image given in arguments
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Required: opencv library (Debian: aptitude install libopencv-dev)
 * Usage: gcc display_img.c $(pkg-config --cflags --libs opencv)
 *
 * See: Oreilly's book "Learning OpenCV" (first edition) p.17
 *
 */

#include <stdio.h>
#include <highgui.h>

int main(int argc, char *argv[])
{
    if(argc != 2) {
        fprintf(stderr, "Usage: %s FILENAME\n", argv[0]);
        return 1;
    }

    IplImage* img = cvLoadImage(argv[1], CV_LOAD_IMAGE_COLOR);

    cvNamedWindow("Display picture snippet", CV_WINDOW_AUTOSIZE);
    cvShowImage("Display picture snippet", img);
    cvWaitKey(0);

    cvReleaseImage(&img);
    cvDestroyWindow("Display picture snippet");

    return 0;
}
