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

#include <vector>

#include <osg/Group>
#include <osg/Material>
#include <osgViewer/Viewer>

#include <Eigen/Dense>

namespace simulator {

    class PhysicsCallback : public osg::NodeCallback {
        // This callback should be applied only to the root osgNode as physics
        // should be updated once per traversal.
        
        private:
            BulletEnvironment * bulletEnvironment;
            std::vector<simulator::Part *> * objectsVec; //

        public:
            PhysicsCallback(BulletEnvironment * bullet_environment,
                            std::vector<simulator::Part *> * objects_vec);

            virtual void operator() (osg::Node * node, osg::NodeVisitor * nv);
    };

    class OSGEnvironment {

        // TODO: cette classe devrait être un singleton ?!

        private:
            osgViewer::Viewer * viewer;

        public:
            OSGEnvironment(BulletEnvironment * bullet_environment,
                           std::vector<simulator::Part *> * objects_vec);
            
            void run();

            ~OSGEnvironment();
    };

}

#endif // OSG_ENVIRONMENT_H
