/* 
 * OpenCV - Write video: write to a video file
 *
 * Copyright (c) 2014 Jérémie Decock
 *
 * Required: opencv library (Debian: aptitude install libopencv-dev)
 * Usage: gcc write_video.c $(pkg-config --cflags --libs opencv)
 *
 * See: Oreilly's book "Learning OpenCV" (first edition) p.27
 *
 */

#include <stdio.h>
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


    // INIT CAPTURE
    
    IplImage* frame = cvQueryFrame(capture);   // Required prior to read the video properties on some systems


    // CREATE VIDEO WRITER

    char * output_filename = "out.avi";
    int video_codec = CV_FOURCC('M', 'J', 'P', 'G');  // The four character code of the codec
    double fps = 1000 / frame_delay_ms; // (40ms -> 25fps)
    CvSize frame_size = cvGetSize(frame);
    int is_color = 1;

    CvVideoWriter* writer = cvCreateVideoWriter(output_filename, video_codec, fps, frame_size, is_color);


    // MAIN LOOP
    
    cvNamedWindow("Capture video snippet", CV_WINDOW_AUTOSIZE);

    while(1) {
        frame = cvQueryFrame(capture);
        if(frame == NULL) break;

        cvShowImage("Capture video snippet", frame);  // display the frame
        cvWriteFrame(writer, frame);                  // write the frame to the output file

        char c = cvWaitKey(frame_delay_ms); // wait for 40ms (40ms -> 25fps)
        if(c==27) break;                    // 27 = Esc key
    }


    // RELEASE POINTERS
    
    cvReleaseCapture(&capture);
    cvReleaseVideoWriter(&writer);
    cvDestroyWindow("Capture video snippet");

    return 0;
}
