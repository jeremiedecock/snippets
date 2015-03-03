/* 
 * Bullet OSG Framework.
 * The OSG environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "osg_environment.h"

#include <vector>

#include <osg/Group>
#include <osg/Material>
#include <osgGA/TrackballManipulator>
#include <osgShadow/ShadowedScene>
#include <osgShadow/ShadowMap>
#include <osgViewer/Viewer>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>


// PhysicsCallback ////////////////////////////////////////////////////////////

simulator::PhysicsCallback::PhysicsCallback(BulletEnvironment * bullet_environment,
                                            std::vector<simulator::Part *> * objects_vec) {
    this->bulletEnvironment = bullet_environment;
    this->objectsVec = objects_vec;
}

void simulator::PhysicsCallback::operator() (osg::Node * node, osg::NodeVisitor * nv) {
    // Update the physics
    this->bulletEnvironment->stepSimulation(1. / 60.);

    // Update the position of each objects
    std::vector<simulator::Part *>::iterator it;
    for(it = this->objectsVec->begin() ; it != this->objectsVec->end() ; it++) {
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


// OSGEnvironment /////////////////////////////////////////////////////////////

const unsigned int simulator::OSGEnvironment::receivesShadowTraversalMask = 0x1;
const unsigned int simulator::OSGEnvironment::castsShadowTraversalMask = 0x2;

simulator::OSGEnvironment::OSGEnvironment(BulletEnvironment * bullet_environment,
                                          std::vector<simulator::Part *> * objects_vec) {

    // Make the scene graph
    //osg::Group * root = new osg::Group();
    osg::ref_ptr<osgShadow::ShadowedScene> root = new osgShadow::ShadowedScene();  // To allow shadows, root must be a special group node named "ShadowedScene"

    root->setUpdateCallback(new PhysicsCallback(bullet_environment, objects_vec)); // Physics is updated when root is traversed

    // Add objects
    std::vector<simulator::Part *>::iterator it;
    for(it = objects_vec->begin() ; it != objects_vec->end() ; it++) {
        root->addChild((*it)->getOSGPAT());
    }

    // LIGHT ////////////////

    osg::ref_ptr<osg::Light> light = new osg::Light;

    // OSG (as OpenGL) can handle up to 8 light sources.
    // Each light must have a unique number
    //
    // Light number 0 is the default one (integrated to the camera).
    //
    // We do not use light number 0, because we do not want to override the OSG
    // default headlights.
    light->setLightNum(1);

    light->setAmbient(osg::Vec4(1.0, 1.0, 1.0, 0.0));
    light->setDiffuse(osg::Vec4(1.0, 1.0, 1.0, 0.0));
    light->setSpecular(osg::Vec4(1.0, 1.0, 1.0, 1.0));

    // The light's position
    light->setPosition(osg::Vec4(10.0, -10.0, 20.0, 1.0)); // last param w = 0.0 directional light (direction)
                                                           // w = 1.0 point light (position)
    // Light source
    osg::ref_ptr<osg::LightSource> light_source = new osg::LightSource;    
    light_source->setLight(light);
    root->addChild(light_source);

    osg::ref_ptr<osg::StateSet> state = root->getOrCreateStateSet();
    state->setMode(GL_LIGHT0, osg::StateAttribute::OFF); // GL_LIGHT0 is the default light
    state->setMode(GL_LIGHT1, osg::StateAttribute::ON);  // use GL_LIGHTN for light number N

    // Material
    osg::ref_ptr<osg::Material> p_mat = new osg::Material;
    p_mat->setDiffuse(osg::Material::FRONT, osg::Vec4(1.0f, 1.0f, 1.0f, 1.f)); // the diffuse color of the material
    p_mat->setSpecular(osg::Material::FRONT, osg::Vec4(1.f, 1.f, 1.f, 0.f));   // the specular color of the material
    p_mat->setShininess(osg::Material::FRONT, 96.f);
    state->setAttribute(p_mat.get());

    // Set shadows
    osg::ref_ptr<osgShadow::ShadowMap> p_shadow_map = new osgShadow::ShadowMap();
    p_shadow_map->setLight(light_source);
    p_shadow_map->setTextureSize(osg::Vec2s(2048, 2048));
    p_shadow_map->setTextureUnit(1);

    root->setShadowTechnique(p_shadow_map.get());
    root->setReceivesShadowTraversalMask(simulator::OSGEnvironment::receivesShadowTraversalMask);
    root->setCastsShadowTraversalMask(simulator::OSGEnvironment::castsShadowTraversalMask);

    // MAKE THE VIEWER ////////
    this->viewer = new osgViewer::Viewer();
    this->viewer->setSceneData(root);

    // Set the background color (black here -> (0,0,0,0))
    this->viewer->getCamera()->setClearColor(osg::Vec4(0.0f, 0.0f, 0.0f, 0.0f));

    // MSAA: multi-sampled_anti-aliasing 
    // See http://gaming.stackexchange.com/questions/31801/what-are-the-differences-between-the-different-anti-aliasing-multisampling-set
    //     http://osghelp.com/?p=179
    osg::DisplaySettings::instance()->setNumMultiSamples(4); // MSAA: multi-sampled_anti-aliasing 

    // Setup the default camera
    osg::Vec3d look_from(20.0, 20.0, 10.0); // point 3D qui définit la position de la caméra
    osg::Vec3d look_at(0.0, 0.0, 0.0);     // point 3D qui définit le point regardé par la caméra
    osg::Vec3d up(0.0, 0.0, 1.0);          // point 3D qui définit l'axe vertical de la caméra. En général il est défini selon l'axe vertical du repère.

    osg::ref_ptr<osgGA::TrackballManipulator> p_camera_manipulator = new osgGA::TrackballManipulator();
    p_camera_manipulator->setHomePosition(look_from, look_at, up, false);

    this->viewer->setCameraManipulator(p_camera_manipulator);
}

void simulator::OSGEnvironment::run() {
    this->viewer->run();
}

simulator::OSGEnvironment::~OSGEnvironment() {
    delete this->viewer;
}
