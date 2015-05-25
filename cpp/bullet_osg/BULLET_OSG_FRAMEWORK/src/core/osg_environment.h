/* 
 * Bullet OSG Framework.
 * The OSG environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_OSG_ENVIRONMENT_H
#define BOTSIM_OSG_ENVIRONMENT_H

#include "bullet_environment.h"
#include "part.h"

#include <set>

#include <osg/Group>
#include <osg/Material>
#include <osgGA/GUIEventHandler>
#include <osgViewer/Viewer>

#include <Eigen/Dense>

namespace botsim {

    class OSGEnvironment {

        // TODO: cette classe devrait être un singleton ?!

        private:
            osgViewer::Viewer * viewer;
            bool useFogEffect; // TODO: const
            const bool useFullScreen;

        public:
            static const unsigned int receivesShadowTraversalMask;
            static const unsigned int castsShadowTraversalMask;

            OSGEnvironment(BulletEnvironment * bullet_environment, bool use_full_screen_mode = false);
            
            osgViewer::Viewer * getViewer() const;

            void run();

            ~OSGEnvironment();

        private:
            /**
             * Forbid copy of instances.
             */
            OSGEnvironment(const OSGEnvironment &);

            /**
             * Forbid assignment.
             */
            OSGEnvironment & operator = (const OSGEnvironment &);
    };


    class PhysicsCallback : public osg::NodeCallback {
        // This callback should be applied only to the root osgNode as physics
        // should be updated once per traversal.
        
        private:
            BulletEnvironment * bulletEnvironment;
            OSGEnvironment * osgEnvironment;

        public:
            PhysicsCallback(BulletEnvironment * bullet_environment, OSGEnvironment * osg_environment);

            virtual void operator() (osg::Node * node, osg::NodeVisitor * nv);

        private:
            /**
             * Forbid copy of instances.
             */
            PhysicsCallback(const PhysicsCallback &);

            /**
             * Forbid assignment.
             */
            PhysicsCallback & operator = (const PhysicsCallback &);
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

        private:
            /**
             * Forbid copy of instances.
             */
            KeyboardEventHandler(const KeyboardEventHandler &);

            /**
             * Forbid assignment.
             */
            KeyboardEventHandler & operator = (const KeyboardEventHandler &);
    };

}

#endif // BOTSIM_OSG_ENVIRONMENT_H
