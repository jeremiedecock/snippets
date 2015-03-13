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
#include <iostream>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>


simulator::BulletEnvironment::BulletEnvironment(std::vector<simulator::Part *> * objects_vec) {
    this->gravity = -10.;
    this->simulationTime = 0.;

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


void simulator::BulletEnvironment::stepSimulation(const double time_step) {
    this->simulationTime += time_step;
    this->getDynamicsWorld()->stepSimulation(time_step, 10); // TODO http://bulletphysics.org/mediawiki-1.5.8/index.php/Stepping_The_World
    //std::cout << this->simulationTime << std::endl;
}

void simulator::BulletEnvironment::resetSimulation() {
    std::cout << "Reset simulation" << std::endl;

    // TODO

    //this->constraintSolver->reset();
    //this->dynamicsWorld->clearForces();
    //this->broadphase->resetPool(this->collisionDispatcher);
    ////m_clock.reset();

    //btOverlappingPairCache* pair_cache = this->dynamicsWorld->getBroadphase()->getOverlappingPairCache();
    //btBroadphasePairArray& pair_array = pair_cache->getOverlappingPairArray();
    //for(int i = 0; i < pair_array.size(); i++) {
    //    pair_cache->cleanOverlappingPair(pair_array[i], this->dynamicsWorld->getDispatcher());
    //}
    // TODO: reset the initial position, angle, velocity, mass, ... of each parts.
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

