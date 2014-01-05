/* 
 * OpenCV - Transform video
 *
 * Copyright (c) 2014 Jérémie Decock
 *
 * Required: opencv library (Debian: aptitude install libopencv-dev)
 * Usage: gcc demo.c $(pkg-config --cflags --libs opencv)
 *
 * See: Oreilly's book "Learning OpenCV" (first edition) p.22 and see chapter 6 for details about transformations
 *
 */

#include <stdio.h>
#include <cv.h>
#include <highgui.h>

static const int frame_delay_ms = 40; // (40ms -> 25fps)

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

    
    // INIT
    
    cvNamedWindow("Input", CV_WINDOW_AUTOSIZE);
    cvNamedWindow("Output", CV_WINDOW_AUTOSIZE);

    IplImage* in_frame = cvQueryFrame(capture);

    printf("In size: %dx%d\n", in_frame->width, in_frame->height);
    assert(in_frame->width%2 == 0 && in_frame->height%2 == 0);

    CvSize frame_size_half = cvSize(in_frame->width/2, in_frame->height/2);
    IplImage* out_frame_half = cvCreateImage(frame_size_half, IPL_DEPTH_8U, 3);

    printf("Out size: %dx%d\n", out_frame_half->width, out_frame_half->height);


    // MAIN LOOP
    
    while(1) {
        in_frame = cvQueryFrame(capture);
        if(in_frame == NULL) break;

        cvPyrDown(in_frame, out_frame_half, CV_GAUSSIAN_5x5); // reduce image (1:2)

        cvShowImage("Input", in_frame);         // display the frame
        cvShowImage("Output", out_frame_half);  // display the frame

        char c = cvWaitKey(frame_delay_ms); // wait for 40ms (40ms -> 25fps)
        if(c==27) break;                    // 27 = Esc key
    }


    // RELEASE POINTERS
    
    cvReleaseCapture(&capture);
    cvReleaseImage(&out_frame_half);
    cvDestroyWindow("Input");
    cvDestroyWindow("Output");

    return 0;
}
