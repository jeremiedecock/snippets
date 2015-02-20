/* 
 * Bullet OSG Framework.
 * Part module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "part.h"

#include <osg/Group>
#include <osg/PositionAttitudeTransform>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>


btRigidBody * simulator::Part::getRigidBody() const {
    return this->rigidBody;
}

osg::Node * simulator::Part::getOSGGroup() const {
    return this->osgGroup;
}

Eigen::Vector3d simulator::Part::getPosition() const {
    btTransform bulletTransform;
    this->rigidBody->getMotionState()->getWorldTransform(bulletTransform);

    Eigen::Vector3d position(bulletTransform.getOrigin().getX(),
                             bulletTransform.getOrigin().getY(),
                             bulletTransform.getOrigin().getZ());
    return position;
}

Eigen::Vector4d simulator::Part::getAngle() const {
    btTransform bulletTransform;
    this->rigidBody->getMotionState()->getWorldTransform(bulletTransform);

    Eigen::Vector4d angle(bulletTransform.getRotation().x(),
                          bulletTransform.getRotation().y(),
                          bulletTransform.getRotation().z(),
                          bulletTransform.getRotation().w());
    return angle;
}

osg::PositionAttitudeTransform * simulator::Part::getOSGPAT() const {
    return this->osgPAT;
}

