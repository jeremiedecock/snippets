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

            double mass;                              // which unit ? Kg ?

//        protected:
//            Part() {};

        public:
            virtual ~Part() {};


            // Bullet accessors (return bullet objects) ///////////////////////////////////////////

            btRigidBody * getRigidBody() const; // TODO: should be protected...


            // OSG accessors (return OSG objects) /////////////////////////////////////////////////

            osg::Node * getOSGGroup() const;

            osg::PositionAttitudeTransform * getOSGPAT() const;


            // General accessors (return scalars, stl objects or eigen matrices) //////////////////

            virtual std::string getName() const = 0;

            Eigen::Vector3d getPosition() const;

            Eigen::Vector4d getAngle() const;

            Eigen::Vector3d getLinearVelocity() const;

            Eigen::Vector3d getAngularVelocity() const;

            /**
             * TotalForce is always equals to 0 outside the Bullet's "internalTickCallback".
             * See http://bulletphysics.org/Bullet/phpBB3/viewtopic.php?t=9688 :
             * "[...] one of the last lines of StepSim is ClearForces [...]."
             */
            Eigen::Vector3d getTotalForce() const;

            /**
             * TotalTorque is always equals to 0 outside the Bullet's "internalTickCallback".
             * See http://bulletphysics.org/Bullet/phpBB3/viewtopic.php?t=9688 :
             * "[...] one of the last lines of StepSim is ClearForces [...]."
             */
            Eigen::Vector3d getTotalTorque() const;

            double getMass() const;
    };

}

#endif // PART_H
