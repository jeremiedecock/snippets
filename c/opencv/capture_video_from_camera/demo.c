/* 
 * OpenCV - Capture video from camera (V4L): capture a video from a camera
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Required: opencv library (Debian: aptitude install libopencv-dev)
 * Usage: gcc demo.c $(pkg-config --cflags --libs opencv)
 *
 * See: Oreilly's book "Learning OpenCV" (first edition) p.26
 *
 */

#include <stdio.h>
#include <highgui.h>

int main(int argc, char *argv[])
{
    int camera_id = -1;

    if(argc == 2) {
        if(0 == strcmp(argv[1], "-h")) {
            fprintf(stderr, "Usage: %s [CAMERA_ID]\n", argv[0]);
            exit(0);
        } else {
            camera_id = atoi(argv[1]);
        }
    }

    CvCapture* capture = cvCreateCameraCapture(camera_id);  // camera id number (-1=any camera)

    if(capture == NULL) {
        fprintf(stderr, "Error: cannot find any camera.\n");
        exit(1);
    } else {
        fprintf(stdout, "Press Esc to close the window.\n");
    }

    cvNamedWindow("Capture video snippet", CV_WINDOW_AUTOSIZE);

    IplImage* frame;

    while(1) {
        frame = cvQueryFrame(capture);
        if(!frame) break;

        cvShowImage("Capture video snippet", frame);

        char c = cvWaitKey(40); // wait for 40ms (40ms -> 25fps)
        if(c==27) break;        // 27 = Esc key
    }

    cvReleaseCapture(&capture);
    cvDestroyWindow("Capture video snippet");

    return 0;
}
