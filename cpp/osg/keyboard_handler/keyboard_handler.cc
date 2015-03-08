/* 
 * OSG Keyboard handler
 *
 * Copyright (c) 2015 Jérémie Decock
 *
 * See "OpenSceneGraph 3.0" by Rui Wang and Xuelei Qian (ed. Packt publishing) p.232
 * and http://jeux.developpez.com/tutoriels/openscenegraph/evenements/
 */

#include <osgViewer/Viewer>
#include <iostream>

#include <osgGA/GUIEventHandler>

class KeyboardEventHandler : public osgGA::GUIEventHandler {
    public:
        KeyboardEventHandler() {
            // Put here the data to manipulate...
        }

        /**
         * osgGA::GUIEventAdapter  supplies the received events
         * osgGA::GUIActionAdapter parameter for feedback
         */
        virtual bool handle(const osgGA::GUIEventAdapter& event_adapter, osgGA::GUIActionAdapter& action_adapter) {

            switch(event_adapter.getEventType()) {

                case(osgGA::GUIEventAdapter::KEYDOWN):  // KEYDOWN == key pressed
                    {
                        switch(event_adapter.getKey()) {
                            // See http://trac.openscenegraph.org/documentation/OpenSceneGraphReferenceDocs/a00359.html for the list of OSG key symbols
                            
                            case 'q':
                                std::cout << "q key pressed (KEYDOWN)" << std::endl;
                                break;

                            case osgGA::GUIEventAdapter::KEY_Escape:
                                std::cout << "Escape key pressed (KEYDOWN)" << std::endl;
                                break;

                            case osgGA::GUIEventAdapter::KEY_Space:
                                std::cout << "Space key pressed (KEYDOWN)" << std::endl;
                                break;

                            case osgGA::GUIEventAdapter::KEY_Up:
                                std::cout << "Up key pressed (KEYDOWN)" << std::endl;
                                break;

                            case osgGA::GUIEventAdapter::KEY_Down:
                                std::cout << "Down key pressed (KEYDOWN)" << std::endl;
                                break;

                            case osgGA::GUIEventAdapter::KEY_Left:
                                std::cout << "Left key pressed (KEYDOWN)" << std::endl;
                                break;

                            case osgGA::GUIEventAdapter::KEY_Right:
                                std::cout << "Right key pressed (KEYDOWN)" << std::endl;
                                break;
                        } 
                    }
                    break;

                case(osgGA::GUIEventAdapter::KEYUP):  // KEYUP == key released
                    {
                        switch(event_adapter.getKey()) {
                            case 'q':
                                std::cout << "q key pressed (KEYUP)" << std::endl;
                                break;
                        } 
                    }
                    break;

                default: // To avoid a warning during compilation
                    break;
            }

            return false;
        }
};

int main(int, char **) {

    // Create an empty scene
    osg::ref_ptr<osg::Group> root = new osg::Group;

    // Viewer
    osgViewer::Viewer viewer;
    viewer.setSceneData(root);

    // Set the keyboard handler
    osg::ref_ptr<KeyboardEventHandler> keyboard_event_handler = new KeyboardEventHandler();
    viewer.addEventHandler(keyboard_event_handler);

    // Make the viewer create a 512x512 window and position it at 32, 32
    viewer.setUpViewInWindow(32, 32, 512, 512);

    // Run the viewer
    viewer.run();

    return 0;
}
