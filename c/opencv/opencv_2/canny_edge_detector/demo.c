/* 
 * OpenCV - Transform video
 *
 * Copyright (c) 2014 Jérémie Decock
 *
 * Required: opencv library (Debian: aptitude install libopencv-dev)
 * Usage: gcc demo.c $(pkg-config --cflags --libs opencv)
 *
 * See: Oreilly's book "Learning OpenCV" (first edition) p.24 and see chapter 6 for details about transformations
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
    CvSize frame_size = cvGetSize(in_frame);

    IplImage* in_frame_gray = cvCreateImage(frame_size, IPL_DEPTH_8U, 1);  // 1 channel (black and white)
    IplImage* out_frame_gray = cvCreateImage(frame_size, IPL_DEPTH_8U, 1); // 1 channel (black and white)


    // MAIN LOOP
    
    while(1) {
        in_frame = cvQueryFrame(capture);
        if(in_frame == NULL) break;

        // Canny edge detector
        cvCvtColor(in_frame, in_frame_gray, CV_BGR2GRAY); // RGB -> Gray
        cvCanny(in_frame_gray, out_frame_gray, 10, 120, 3);

        cvShowImage("Input", in_frame);       // display the frame
        cvShowImage("Output", out_frame_gray);  // display the frame

        char c = cvWaitKey(frame_delay_ms); // wait for 40ms (40ms -> 25fps)
        if(c==27) break;                    // 27 = Esc key
    }


    // RELEASE POINTERS
    
    cvReleaseCapture(&capture);
    cvReleaseImage(&in_frame_gray);
    cvReleaseImage(&out_frame_gray);
    cvDestroyWindow("Input");
    cvDestroyWindow("Output");

    return 0;
}
