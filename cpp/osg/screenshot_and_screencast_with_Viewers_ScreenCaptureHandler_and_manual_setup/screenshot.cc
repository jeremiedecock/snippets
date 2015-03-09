/* 
 * OSG Screenshot
 *
 * Copyright (c) 2015 Jérémie Decock
 *
 * See:
 * - the applications/osgviewer/osgviewer.cpp file in OSG source code
 * - http://trac.openscenegraph.org/documentation/OpenSceneGraphReferenceDocs/a00724.html#details
 * - http://forum.openscenegraph.org/viewtopic.php?t=3240
 */

#include <osgViewer/Viewer>
#include <osgViewer/ViewerEventHandlers>

#include <osgDB/ReadFile>

#include <iostream>

const std::string FILENAME("capture");
const std::string FILE_EXT("png");

const int CAPTURE_CHAR = 's';
const int CONT_CAPTURE_CHAR = 'S';

// How to react to the KeyEventTakeScreenShot
const int NUM_FRAMES = 1;     // Capture 1 frame (default)
//const int NUM_FRAMES = 3;   // Capture 3 successive frames
//const int NUM_FRAMES = 0;   // Disable screen capture
//const int NUM_FRAMES = -1;  // Continuous capture ("screencast")

int main(int, char **) {

    // Make the scene
    osg::ref_ptr<osg::Node> model = osgDB::readNodeFile("cessna.osg"); // could be also .obj files, ...

    osgViewer::Viewer viewer;
    viewer.setSceneData(model);

    // Setup the screen capture handler
    osg::ref_ptr<osgViewer::ScreenCaptureHandler::WriteToFile> p_write_to_file = new osgViewer::ScreenCaptureHandler::WriteToFile(FILENAME, FILE_EXT, osgViewer::ScreenCaptureHandler::WriteToFile::SEQUENTIAL_NUMBER);

    // Make the screen capture handler
    osg::ref_ptr<osgViewer::ScreenCaptureHandler> p_screen_capture_handler = new osgViewer::ScreenCaptureHandler(p_write_to_file, NUM_FRAMES);
    //osg::ref_ptr<osgViewer::ScreenCaptureHandler> p_screen_capture_handler = new osgViewer::ScreenCaptureHandler();

    // Change the default settings of the screen capture handler
    p_screen_capture_handler->setKeyEventTakeScreenShot(CAPTURE_CHAR);
    p_screen_capture_handler->setKeyEventToggleContinuousCapture(CONT_CAPTURE_CHAR);
    p_screen_capture_handler->setFramesToCapture(NUM_FRAMES);

    // Add the screen capture handler to the viewer
    viewer.addEventHandler(p_screen_capture_handler);

    // Set the window mode (512x512 at position (32,32))
    viewer.setUpViewInWindow(32, 32, 512, 512);

    // Print some messages
    std::cout << "Press '" << (char) p_screen_capture_handler->getKeyEventTakeScreenShot() << "' to take a screenshot ";
    std::cout << "(" << p_screen_capture_handler->getFramesToCapture() << " frames will be captured)." << std::endl;

    std::cout << "Press '" << (char) p_screen_capture_handler->getKeyEventToggleContinuousCapture() << "' to start or stop continuous capture." << std::endl;

    // Run the viewer
    viewer.run();

    // To manually start capture...
    //p_screen_capture_handler->startCapture();
    //...
    //p_screen_capture_handler->stopCapture();

    return 0;
}
