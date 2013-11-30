/* 
 * OpenCV - Display image: display an image given in arguments
 *
 * Copyright (c) 2013 Jérémie Decock
 *
 * Required: opencv library (Debian: aptitude install libopencv-dev)
 * Usage: g++ display_img.cc $(pkg-config --cflags --libs opencv)
 *
 * See: http://docs.opencv.org/doc/tutorials/introduction/display_image/display_image.html#display-image
 *
 */

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

int main(int argc, char *argv[])
{
    if(argc != 2) {
        std::cout << "Usage: " << argv[0] << " FILENAME" << std::endl;
        return 1;
    }

    cv::Mat image;
    image = cv::imread(argv[1], CV_LOAD_IMAGE_COLOR);

    if(!image.data) {
        std::cout << "Could not open " << argv[1] << std::endl;
        return 2;
    }

    cv::namedWindow("Display window", CV_WINDOW_AUTOSIZE);
    cv::imshow("Display window", image);

    cv::waitKey(0);

    return 0;
}
