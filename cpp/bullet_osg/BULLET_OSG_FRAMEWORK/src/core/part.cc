/* 
 * Bullet OSG Framework.
 * Part module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "part.h"
#include "tools/tools.h"

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

osg::PositionAttitudeTransform * simulator::Part::getOSGPAT() const {
    return this->osgPAT;
}

//std::map<std::string, simulator::JointSlot *> simulator::Part::getJointSlotMap() const {
//    return this->jointSlotMap;
//}

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

Eigen::Vector3d simulator::Part::getLinearVelocity() const {
    const btVector3 bullet_vector = this->rigidBody->getLinearVelocity();
    Eigen::Vector3d eigen_vector = simulator::vec3_bullet_to_eigen(bullet_vector);
    return eigen_vector;
}

Eigen::Vector3d simulator::Part::getAngularVelocity() const {
    const btVector3 bullet_vector = this->rigidBody->getAngularVelocity();
    Eigen::Vector3d eigen_vector = simulator::vec3_bullet_to_eigen(bullet_vector);
    return eigen_vector;
}

Eigen::Vector3d simulator::Part::getTotalForce() const {
    const btVector3 bullet_vector = this->rigidBody->getTotalForce();
    Eigen::Vector3d eigen_vector = simulator::vec3_bullet_to_eigen(bullet_vector);
    return eigen_vector;
}

Eigen::Vector3d simulator::Part::getTotalTorque() const {
    const btVector3 bullet_vector = this->rigidBody->getTotalTorque();
    Eigen::Vector3d eigen_vector = simulator::vec3_bullet_to_eigen(bullet_vector);
    return eigen_vector;
}

double simulator::Part::getMass() const {
    return this->mass;
}

double simulator::Part::getFriction() const {
    return this->friction;
}

double simulator::Part::getRollingFriction() const {
    return this->rollingFriction;
}

double simulator::Part::getRestitution() const {
    return this->restitution;
}

