/* 
 * Bullet OSG Framework.
 * The ground module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef GROUND_H
#define GROUND_H

#include "part.h"

#include <osg/Geode>
#include <osg/Group>
#include <osg/Material>
#include <osg/PositionAttitudeTransform>
#include <osg/ShapeDrawable>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class Ground: public simulator::Part {
        private:
            // Bullet
            btCollisionShape * groundShape;
            btDefaultMotionState * groundMotionState;

        public:
            Ground(double friction=0.5,
                   double rolling_friction=0.,
                   double restitution=0.);

            ~Ground();

            std::string getName() const;
    };
}

#endif // GROUND_H
