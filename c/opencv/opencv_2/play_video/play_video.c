/* 
 * OpenCV - Play video: play a video file given in arguments
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Required: opencv library (Debian: aptitude install libopencv-dev)
 * Usage: gcc play_video.c $(pkg-config --cflags --libs opencv)
 *
 * See: Oreilly's book "Learning OpenCV" (first edition) p.18
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

    CvCapture* capture = cvCreateFileCapture(argv[1]);

    if(capture == NULL) {
        fprintf(stderr, "Error: cannot play the file.\n");
        exit(1);
    } else {
        fprintf(stdout, "Press Esc to close the window.\n");
    }

    cvNamedWindow("Play video snippet", CV_WINDOW_AUTOSIZE);

    IplImage* frame;

    while(1) {
        frame = cvQueryFrame(capture);
        if(!frame) break;

        cvShowImage("Play video snippet", frame);

        char c = cvWaitKey(40); // wait for 40ms (40ms -> 25fps)
        if(c==27) break;        // 27 = Esc key
    }

    cvReleaseCapture(&capture);
    cvDestroyWindow("Play video snippet");

    return 0;
}
