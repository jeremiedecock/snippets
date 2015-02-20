/* 
 * Bullet OSG Framework.
 * The bullet environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "bullet_environment.h"

#include <vector>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>


simulator::BulletEnvironment::BulletEnvironment(std::vector<simulator::Part *> * objects_vec) {
    this->gravity = -10.;

    this->broadphase = new btDbvtBroadphase();

    this->collisionConfiguration = new btDefaultCollisionConfiguration();
    this->collisionDispatcher = new btCollisionDispatcher(this->collisionConfiguration);

    this->constraintSolver = new btSequentialImpulseConstraintSolver();

    this->dynamicsWorld = new btDiscreteDynamicsWorld(this->collisionDispatcher,
            this->broadphase,
            this->constraintSolver,
            this->collisionConfiguration);
    this->dynamicsWorld->setGravity(btVector3(0, 0, this->gravity));

    this->objectsVec = objects_vec;

    // Add rigid bodies
    std::vector<simulator::Part *>::iterator it;
    for(it = this->objectsVec->begin() ; it != this->objectsVec->end() ; it++) {
        this->dynamicsWorld->addRigidBody((*it)->getRigidBody());
    }
}


btDiscreteDynamicsWorld * simulator::BulletEnvironment::getDynamicsWorld() const {
    return this->dynamicsWorld;
}


simulator::BulletEnvironment::~BulletEnvironment() {
    std::vector<simulator::Part *>::iterator it;
    for(it = this->objectsVec->begin() ; it != this->objectsVec->end() ; it++) {
        delete (*it);
    }

    delete this->dynamicsWorld;

    delete this->constraintSolver;
    delete this->collisionConfiguration;
    delete this->collisionDispatcher;
    delete this->broadphase;
}

