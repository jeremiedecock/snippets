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
#include <cv.h>
#include <highgui.h>

int main(int argc, char *argv[])
{
    if(argc != 2) {
        fprintf(stderr, "Usage: %s INPUT_FILENAME\n", argv[0]);
        return 1;
    }

    CvCapture* capture = cvCreateFileCapture(argv[1]);

    if(capture == NULL) {
        fprintf(stderr, "Error: cannot play the file.\n");
        exit(1);
    }


    // INIT CAPTURE
    
    IplImage* in_frame = cvQueryFrame(capture);   // Required prior to read the video properties on some systems


    // CREATE VIDEO WRITER

    char * output_filename = "out.avi";
    int video_codec = CV_FOURCC('M', 'J', 'P', 'G');  // The four character code of the codec
    double fps = cvGetCaptureProperty(capture, CV_CAP_PROP_FPS);
    CvSize frame_size = cvGetSize(in_frame);
    int is_color = 1;

    CvVideoWriter* writer = cvCreateVideoWriter(output_filename, video_codec, fps, frame_size, is_color);


    // MAIN LOOP
    
    IplImage* out_frame = cvCreateImage(frame_size, IPL_DEPTH_8U, 3);

    while(1) {
        in_frame = cvQueryFrame(capture);
        if(in_frame == NULL) break;

        // TRANSFORM THE IMAGE AND WRITE IT
        cvSmooth(in_frame, out_frame, CV_GAUSSIAN, 5, 5, 0, 0);  // Gaussian smooth over a 5x5 area centred on each pixel
        cvWriteFrame(writer, out_frame);
    }


    // RELEASE POINTERS
    
    cvReleaseVideoWriter(&writer);
    cvReleaseImage(&out_frame);
    cvReleaseCapture(&capture);

    return 0;
}
