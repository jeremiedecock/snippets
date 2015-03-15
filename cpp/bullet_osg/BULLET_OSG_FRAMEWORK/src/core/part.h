/* 
 * Bullet OSG Framework.
 * Part module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef PART_H
#define PART_H

#include <string>

#include <osg/Group>
#include <osg/PositionAttitudeTransform>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class Part {
        protected:
            // Bullet
            btRigidBody * rigidBody;

            // OSG
            osg::Group * osgGroup;
            osg::PositionAttitudeTransform * osgPAT;

        public:
            virtual std::string getName() const = 0;

            btRigidBody * getRigidBody() const;

            osg::Node * getOSGGroup() const;

            Eigen::Vector3d getPosition() const;

            Eigen::Vector4d getAngle() const;

            osg::PositionAttitudeTransform * getOSGPAT() const;
    };

}

#endif // PART_H
