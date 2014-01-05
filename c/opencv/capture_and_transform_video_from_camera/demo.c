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

static const int demo_id = 3;

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

    IplImage* out_frame = cvCreateImage(frame_size, IPL_DEPTH_8U, 3);


    // MAIN LOOP
    
    while(1) {
        in_frame = cvQueryFrame(capture);
        if(in_frame == NULL) break;

        // VARIOUS TRANSFORMS
        switch(demo_id) {
            case 1:
                cvSmooth(in_frame, out_frame, CV_GAUSSIAN, 11, 11, 0, 0);  // Gaussian smooth over a 11x11 area centred on each pixel
                break;
            case 2:
                cvSobel(in_frame, out_frame, 1, 1, 3);
                break;
            case 3:
                cvLaplace(in_frame, out_frame, 3);
                break;
            default:
                printf("Unknown tranform id\n");
                return 1;
        }

        cvShowImage("Input", in_frame);  // display the frame
        cvShowImage("Output", out_frame);  // display the frame

        char c = cvWaitKey(frame_delay_ms); // wait for 40ms (40ms -> 25fps)
        if(c==27) break;                    // 27 = Esc key
    }


    // RELEASE POINTERS
    
    cvReleaseCapture(&capture);
    cvReleaseImage(&out_frame);
    cvDestroyWindow("Input");
    cvDestroyWindow("Output");

    return 0;
}
