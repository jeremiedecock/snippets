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

int main(int, char **) {

    // Make the scene
    osg::ref_ptr<osg::Node> model = osgDB::readNodeFile("cessna.osg"); // could be also .obj files, ...

    osgViewer::Viewer viewer;
    viewer.setSceneData(model);

    // Make the screen capture handler
    osg::ref_ptr<osgViewer::ScreenCaptureHandler> p_screen_capture_handler = new osgViewer::ScreenCaptureHandler();

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

    return 0;
}
