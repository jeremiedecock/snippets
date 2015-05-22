/* 
 * Bullet OSG Framework.
 * Part module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_PART_H
#define BOTSIM_PART_H

#include "joint_slot.h"

#include <map>
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

            double friction;                          // Resistance of the part to movement
            double rollingFriction;                   // Resistance of the part to movement. It prevents rounded shapes, such as spheres, cylinders and capsules from rolling forever.
            double restitution;                       // Tendency of the part to bounce after colliding with another (0=stays still, 1=perfectly elastic)
            
        public:
            std::map<std::string, simulator::JointSlot *> jointSlotMap;

        public:
            virtual ~Part() {};


            // Bullet accessors (return bullet objects) ///////////////////////////////////////////

            btRigidBody * getRigidBody() const; // TODO: should be protected...


            // OSG accessors (return OSG objects) /////////////////////////////////////////////////

            osg::Node * getOSGGroup() const;

            osg::PositionAttitudeTransform * getOSGPAT() const;


            // General accessors (return scalars, stl objects or eigen matrices) //////////////////

            //std::map<std::string, simulator::JointSlot *> getJointSlotMap() const;

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

            double getFriction() const;

            double getRollingFriction() const;

            double getRestitution() const;

        protected:
            /**
             * Forbid instantiation.
             */
            Part() {};  // TODO !!!

        private:
            /**
             * Forbid copy of instances.
             */
            Part(const Part &);

            /**
             * Forbid assignment.
             */
            Part & operator = (const Part &);
    };

}

#endif // BOTSIM_PART_H
