/* 
 * Bullet OSG Framework.
 * The OSG environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef OSG_ENVIRONMENT_H
#define OSG_ENVIRONMENT_H

#include "bullet_environment.h"
#include "part.h"

#include <set>

#include <osg/Group>
#include <osg/Material>
#include <osgGA/GUIEventHandler>
#include <osgViewer/Viewer>

#include <Eigen/Dense>

namespace simulator {

    class OSGEnvironment {

        // TODO: cette classe devrait être un singleton ?!

        private:
            osgViewer::Viewer * viewer;
            bool useFogEffect;
            bool useFullScreen;

        public:
            static const unsigned int receivesShadowTraversalMask;
            static const unsigned int castsShadowTraversalMask;

            OSGEnvironment(BulletEnvironment * bullet_environment);
            
            osgViewer::Viewer * getViewer() const;

            void run();

            ~OSGEnvironment();
    };


    class PhysicsCallback : public osg::NodeCallback {
        // This callback should be applied only to the root osgNode as physics
        // should be updated once per traversal.
        
        private:
            BulletEnvironment * bulletEnvironment;

        public:
            PhysicsCallback(BulletEnvironment * bullet_environment);

            virtual void operator() (osg::Node * node, osg::NodeVisitor * nv);
    };


    class KeyboardEventHandler : public osgGA::GUIEventHandler {
        
        private:
            BulletEnvironment * bulletEnvironment;
            OSGEnvironment * osgEnvironment;

        public:
            KeyboardEventHandler(BulletEnvironment * bullet_environment, OSGEnvironment * osg_environment);

            /**
             * osgGA::GUIEventAdapter  supplies the received events
             * osgGA::GUIActionAdapter parameter for feedback
             */
            virtual bool handle(const osgGA::GUIEventAdapter& event_adapter, osgGA::GUIActionAdapter& action_adapter);
    };

}

#endif // OSG_ENVIRONMENT_H
