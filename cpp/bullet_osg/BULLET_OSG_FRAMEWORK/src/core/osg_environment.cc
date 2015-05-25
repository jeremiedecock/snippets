/* 
 * Bullet OSG Framework.
 * The OSG environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "osg_environment.h"

#include <iostream>

#include <osg/Fog>
#include <osg/Group>
#include <osg/Material>
#include <osgGA/TrackballManipulator>
#include <osgShadow/ShadowedScene>
#include <osgShadow/ShadowMap>
#include <osgViewer/Viewer>
#include <osgViewer/ViewerEventHandlers>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

const std::string FILENAME("capture");
const std::string FILE_EXT("png");

const int CAPTURE_CHAR = 's';
const int CONTINUOUS_CAPTURE_CHAR = 'S';
const int RESET_CHAR = 'r';
const int PRINT_CAMERA_CHAR = 'c';

#define USE_SHADOW

// PhysicsCallback ////////////////////////////////////////////////////////////

botsim::PhysicsCallback::PhysicsCallback(BulletEnvironment * bullet_environment, OSGEnvironment * osg_environment) {
    this->bulletEnvironment = bullet_environment;
    this->osgEnvironment = osg_environment;
}

void botsim::PhysicsCallback::operator() (osg::Node * node, osg::NodeVisitor * nv) {
    // Quit ?
    double simulation_duration_sec = this->bulletEnvironment->getSimulationDurationSec();
    if((simulation_duration_sec > 0.) && (this->bulletEnvironment->getElapsedSimulationTimeSec() > simulation_duration_sec)) {
        // Quit
        this->osgEnvironment->getViewer()->setDone(true);
    }

    // Update the physics
    double time_step_duration_sec = this->bulletEnvironment->getBulletTimeStepDurationSec();
    if(time_step_duration_sec > 0.) {
        // Fixed time mode
        this->bulletEnvironment->stepSimulation(time_step_duration_sec);
    } else {
        // "Realtime" mode
        this->bulletEnvironment->stepSimulation();
    }

    // Update the position of each objects
    std::set<botsim::Part *>::iterator it;
    for(it = this->bulletEnvironment->partSet.begin() ; it != this->bulletEnvironment->partSet.end() ; it++) {
        // Bullet
        btTransform bulletTransform;
        (*it)->getRigidBody()->getMotionState()->getWorldTransform(bulletTransform);

        // OSG
        (*it)->getOSGPAT()->setPosition(osg::Vec3(bulletTransform.getOrigin().getX(),
                                                  bulletTransform.getOrigin().getY(),
                                                  bulletTransform.getOrigin().getZ()));
        (*it)->getOSGPAT()->setAttitude(osg::Quat(bulletTransform.getRotation().x(),
                                                  bulletTransform.getRotation().y(),
                                                  bulletTransform.getRotation().z(),
                                                  bulletTransform.getRotation().w()));

        // Debug
        //std::cout << (*it)->getPosition() << std::endl;
        //std::cout << (*it)->getAngle() << std::endl;
    }

    // Continue the traversal
    traverse(node, nv);
}


// KeyboardHandler ////////////////////////////////////////////////////////////

/* 
 * See "OpenSceneGraph 3.0" by Rui Wang and Xuelei Qian (ed. Packt publishing) p.232
 * and http://jeux.developpez.com/tutoriels/openscenegraph/evenements/
 */

botsim::KeyboardEventHandler::KeyboardEventHandler(BulletEnvironment * bullet_environment, OSGEnvironment * osg_environment) {
    this->bulletEnvironment = bullet_environment;
    this->osgEnvironment = osg_environment;
}

/**
 * osgGA::GUIEventAdapter  supplies the received events
 * osgGA::GUIActionAdapter parameter for feedback
 */
bool botsim::KeyboardEventHandler::handle(const osgGA::GUIEventAdapter& event_adapter,
                                             osgGA::GUIActionAdapter& action_adapter) {

    switch(event_adapter.getEventType()) {

        case(osgGA::GUIEventAdapter::KEYUP):  // KEYUP == key released
            {
                switch(event_adapter.getKey()) {
                    // See http://trac.openscenegraph.org/documentation/OpenSceneGraphReferenceDocs/a00359.html for the list of OSG key symbols
                    
                    case RESET_CHAR:
                        // TODO
                        this->bulletEnvironment->resetSimulation();
                        break;

                    case PRINT_CAMERA_CHAR:
                        osg::Vec3d eye;
                        osg::Vec3d center;
                        osg::Vec3d up;
                        this->osgEnvironment->getViewer()->getCamera()->getViewMatrixAsLookAt(eye, center, up);

                        std::cout << "Camera's settings" << std::endl;
                        std::cout << "eye: ("    << eye[0]    << ", " << eye[1]    << ", " << eye[2]    << ")" << std::endl;
                        std::cout << "center: (" << center[0] << ", " << center[1] << ", " << center[2] << ")" << std::endl;
                        std::cout << "up: ("     << up[0]     << ", " << up[1]     << ", " << up[2]     << ")" << std::endl;
                        break;
                } 
            }
            break;

        default: // To avoid a warning during compilation
            break;
    }

    return false;
}


// OSGEnvironment /////////////////////////////////////////////////////////////

const unsigned int botsim::OSGEnvironment::receivesShadowTraversalMask = 0x1;
const unsigned int botsim::OSGEnvironment::castsShadowTraversalMask = 0x2;

botsim::OSGEnvironment::OSGEnvironment(BulletEnvironment * bullet_environment, bool use_full_screen_mode) : useFullScreen(use_full_screen_mode) {

    // Note: the fog effect won't work if shader based shadow technique is used.
    // See http://trac.openscenegraph.org/projects/osg//wiki/Support/ProgrammingGuide/osgShadow
    // and http://forum.openscenegraph.org/viewtopic.php?t=6228&view=previous
    this->useFogEffect = true;


    // MAKE THE VIEWER //////////////////////////
    
    this->viewer = new osgViewer::Viewer();


    // MAKE THE SCENE GRAPH /////////////////////
    
#ifdef USE_SHADOW
        osg::ref_ptr<osgShadow::ShadowedScene> p_root = new osgShadow::ShadowedScene();  // To allow shadows, root must be a special group node named "ShadowedScene"
#else
        osg::ref_ptr<osg::Group> p_root = new osg::Group();
#endif // USE_SHADOW

    p_root->setUpdateCallback(new PhysicsCallback(bullet_environment, this)); // Physics is updated when root is traversed

    // Add objects
    std::set<botsim::Part *>::iterator it;
    for(it = bullet_environment->partSet.begin() ; it != bullet_environment->partSet.end() ; it++) {
        p_root->addChild((*it)->getOSGPAT());
    }

    this->viewer->setSceneData(p_root);


    // LIGHTS AND SHADOWS ///////////////////////

    osg::ref_ptr<osg::Light> p_light = new osg::Light();

    // OSG (as OpenGL) can handle up to 8 light sources.
    // Each light must have a unique number
    //
    // Light number 0 is the default one (integrated to the camera).
    //
    // We do not use light number 0, because we do not want to override the OSG
    // default headlights.
    p_light->setLightNum(1);

    p_light->setAmbient(osg::Vec4(1.0, 1.0, 1.0, 0.0));
    p_light->setDiffuse(osg::Vec4(1.0, 1.0, 1.0, 0.0));
    p_light->setSpecular(osg::Vec4(1.0, 1.0, 1.0, 1.0));

    // The light's position
    p_light->setPosition(osg::Vec4(10.0, -10.0, 40.0, 1.0)); // last param w = 0.0 directional light (direction)
                                                           // w = 1.0 point light (position)
    // Light source
    osg::ref_ptr<osg::LightSource> p_light_source = new osg::LightSource(); 
    p_light_source->setLight(p_light);
    p_root->addChild(p_light_source);

    osg::ref_ptr<osg::StateSet> p_state = p_root->getOrCreateStateSet();
    p_state->setMode(GL_LIGHT0, osg::StateAttribute::OFF); // GL_LIGHT0 is the default light
    p_state->setMode(GL_LIGHT1, osg::StateAttribute::ON);  // use GL_LIGHTN for light number N

    //// Default material
    //osg::ref_ptr<osg::Material> p_mat = new osg::Material();
    //p_mat->setDiffuse(osg::Material::FRONT, osg::Vec4(1.0f, 1.0f, 1.0f, 1.f)); // the diffuse color of the material
    //p_mat->setSpecular(osg::Material::FRONT, osg::Vec4(1.f, 1.f, 1.f, 0.f));   // the specular color of the material
    //p_mat->setShininess(osg::Material::FRONT, 96.f);
    //p_state->setAttribute(p_mat.get());

#ifdef USE_SHADOW
    // Set shadows
    osg::ref_ptr<osgShadow::ShadowMap> p_shadow_map = new osgShadow::ShadowMap();
    p_shadow_map->setLight(p_light_source);
    p_shadow_map->setTextureSize(osg::Vec2s(2048, 2048));
    p_shadow_map->setTextureUnit(1);

    p_root->setShadowTechnique(p_shadow_map.get());
    p_root->setReceivesShadowTraversalMask(botsim::OSGEnvironment::receivesShadowTraversalMask);
    p_root->setCastsShadowTraversalMask(botsim::OSGEnvironment::castsShadowTraversalMask);
#endif // USE_SHADOW


    // SET THE BACKGROUND COLOR /////////////////
    
    // Black background (0,0,0,0)
    this->viewer->getCamera()->setClearColor(osg::Vec4(0.0f, 0.0f, 0.0f, 0.0f));


    // MSAA (MULTI-SAMPLED ANTI-ALIASING) ///////

    // See http://gaming.stackexchange.com/questions/31801/what-are-the-differences-between-the-different-anti-aliasing-multisampling-set
    //     http://osghelp.com/?p=179
    osg::DisplaySettings::instance()->setNumMultiSamples(4); // MSAA: multi-sampled_anti-aliasing 

    
    // SETUP THE DEFAULT CAMERA /////////////////
    
    osg::Vec3d look_from(20.0, 20.0, 10.0); // point 3D qui définit la position de la caméra
    osg::Vec3d look_at(0.0, 0.0, 0.0);     // point 3D qui définit le point regardé par la caméra
    osg::Vec3d up(0.0, 0.0, 1.0);          // point 3D qui définit l'axe vertical de la caméra. En général il est défini selon l'axe vertical du repère.

    osg::ref_ptr<osgGA::TrackballManipulator> p_camera_manipulator = new osgGA::TrackballManipulator();
    p_camera_manipulator->setHomePosition(look_from, look_at, up, false);

    this->viewer->setCameraManipulator(p_camera_manipulator);


    // SETUP THE FOG EFFECT /////////////////////

    if(this->useFogEffect) {
        // Note: the fog effect won't work if shader based shadow technique is used.
        // See http://trac.openscenegraph.org/projects/osg//wiki/Support/ProgrammingGuide/osgShadow
        // and http://forum.openscenegraph.org/viewtopic.php?t=6228&view=previous
        
        // Set the fog effect
        osg::ref_ptr<osg::Fog> p_fog = new osg::Fog();
        p_fog->setMode(osg::Fog::LINEAR); // The fog opacity is linear from "start" to "end" (other modes available are exponential ones)
        p_fog->setStart(50.0f);           // The fog start at this distance to the camera
        p_fog->setEnd(150.0f);            // The fog is "complete" at this distance to the camera

        p_fog->setColor(this->viewer->getCamera()->getClearColor()); // The fog color is the same than the one used for the background

        // Enable the fog effect
        p_state->setAttributeAndModes(p_fog.get());
    }


    // SETUP WINDOW MODE ////////////////////////

    if(!this->useFullScreen) {
        // Set the window mode (512x512 at position (32,32))
        this->viewer->setUpViewInWindow(32, 32, 512, 512);
    }


    // SETUP SCREEN CAPTURE HANDLER /////////////
    
    // Setup the screen capture handler
    osg::ref_ptr<osgViewer::ScreenCaptureHandler::WriteToFile> p_write_to_file = new osgViewer::ScreenCaptureHandler::WriteToFile(FILENAME, FILE_EXT, osgViewer::ScreenCaptureHandler::WriteToFile::SEQUENTIAL_NUMBER);

    // Make the screen capture handler
    osg::ref_ptr<osgViewer::ScreenCaptureHandler> p_screen_capture_handler = new osgViewer::ScreenCaptureHandler(p_write_to_file, 1);
    //osg::ref_ptr<osgViewer::ScreenCaptureHandler> p_screen_capture_handler = new osgViewer::ScreenCaptureHandler();

    // Change the default settings of the screen capture handler
    p_screen_capture_handler->setKeyEventTakeScreenShot(CAPTURE_CHAR);
    p_screen_capture_handler->setKeyEventToggleContinuousCapture(CONTINUOUS_CAPTURE_CHAR);
    
    // Add the screen capture handler to the viewer
    this->viewer->addEventHandler(p_screen_capture_handler);

    // Print some messages
    std::cout << "Press '" << (char) p_screen_capture_handler->getKeyEventTakeScreenShot() << "' to take a screenshot ";
    std::cout << "(" << p_screen_capture_handler->getFramesToCapture() << " frames will be captured)." << std::endl;

    std::cout << "Press '" << (char) p_screen_capture_handler->getKeyEventToggleContinuousCapture() << "' to start or stop continuous capture." << std::endl;


    // KEYBOARD HANDLER /////////////////////////
    
    // Set the keyboard handler
    osg::ref_ptr<KeyboardEventHandler> p_keyboard_event_handler = new KeyboardEventHandler(bullet_environment, this);
    this->viewer->addEventHandler(p_keyboard_event_handler);
}

osgViewer::Viewer * botsim::OSGEnvironment::getViewer() const {
    return this->viewer;
}

void botsim::OSGEnvironment::run() {
    this->viewer->run();
}

botsim::OSGEnvironment::~OSGEnvironment() {
    delete this->viewer;
}
