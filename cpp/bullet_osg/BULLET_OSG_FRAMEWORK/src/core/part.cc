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


btRigidBody * botsim::Part::getRigidBody() const {
    return this->rigidBody;
}

osg::Node * botsim::Part::getOSGGroup() const {
    return this->osgGroup;
}

osg::PositionAttitudeTransform * botsim::Part::getOSGPAT() const {
    return this->osgPAT;
}

//std::map<std::string, botsim::JointSlot *> botsim::Part::getJointSlotMap() const {
//    return this->jointSlotMap;
//}

Eigen::Vector3d botsim::Part::getPosition() const {
    btTransform bulletTransform;
    this->rigidBody->getMotionState()->getWorldTransform(bulletTransform);

    Eigen::Vector3d position(bulletTransform.getOrigin().getX(),
                             bulletTransform.getOrigin().getY(),
                             bulletTransform.getOrigin().getZ());
    return position;
}

Eigen::Vector4d botsim::Part::getAngle() const {
    btTransform bulletTransform;
    this->rigidBody->getMotionState()->getWorldTransform(bulletTransform);

    Eigen::Vector4d angle(bulletTransform.getRotation().x(),
                          bulletTransform.getRotation().y(),
                          bulletTransform.getRotation().z(),
                          bulletTransform.getRotation().w());
    return angle;
}

Eigen::Vector3d botsim::Part::getLinearVelocity() const {
    const btVector3 bullet_vector = this->rigidBody->getLinearVelocity();
    Eigen::Vector3d eigen_vector = botsim::vec3_bullet_to_eigen(bullet_vector);
    return eigen_vector;
}

Eigen::Vector3d botsim::Part::getAngularVelocity() const {
    const btVector3 bullet_vector = this->rigidBody->getAngularVelocity();
    Eigen::Vector3d eigen_vector = botsim::vec3_bullet_to_eigen(bullet_vector);
    return eigen_vector;
}

Eigen::Vector3d botsim::Part::getTotalForce() const {
    const btVector3 bullet_vector = this->rigidBody->getTotalForce();
    Eigen::Vector3d eigen_vector = botsim::vec3_bullet_to_eigen(bullet_vector);
    return eigen_vector;
}

Eigen::Vector3d botsim::Part::getTotalTorque() const {
    const btVector3 bullet_vector = this->rigidBody->getTotalTorque();
    Eigen::Vector3d eigen_vector = botsim::vec3_bullet_to_eigen(bullet_vector);
    return eigen_vector;
}

double botsim::Part::getMass() const {
    return this->mass;
}

double botsim::Part::getFriction() const {
    return this->friction;
}

double botsim::Part::getRollingFriction() const {
    return this->rollingFriction;
}

double botsim::Part::getRestitution() const {
    return this->restitution;
}

void botsim::Part::addJointSlot(std::string key, botsim::JointSlot * value) {
    this->jointSlotMap[key] = value;
}

botsim::JointSlot * botsim::Part::getJointSlot(std::string key) {
    std::map<std::string, botsim::JointSlot *>::iterator it;
    botsim::JointSlot * p_joint_slot;

    it = this->jointSlotMap.find(key); 
    if(it != this->jointSlotMap.end()) {
        p_joint_slot = it->second;
        if(p_joint_slot == NULL) {
            throw std::invalid_argument(key + " has a null value.");
        }
    } else {
        throw std::invalid_argument(key + " is not a valid key.");
    }

    return p_joint_slot;
}

