/* 
 * Bullet OSG Framework.
 * The bullet environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "bullet_environment.h"

#include <iostream>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

std::map<btDynamicsWorld *, simulator::BulletEnvironment *> simulator::BulletEnvironment::tickCallbackPointerMap;

/*
 * TODO
 * Well... it sucks; because of the way it has been designed in Bullet, this
 * callback *must* be a static function...
 * This is dirty and not convenient at all...
 */
void simulator::BulletEnvironment::tickCallback(btDynamicsWorld * world, btScalar time_step) {
    //std::cout << "The world just ticked by " << static_cast<float>(time_step) << " seconds" << std::endl;

    std::map<btDynamicsWorld *, BulletEnvironment *>::iterator it;
    it = simulator::BulletEnvironment::tickCallbackPointerMap.find(world);

    if(it != simulator::BulletEnvironment::tickCallbackPointerMap.end()) {
        // Element found;
        it->second->notifyTick();
    }
}


simulator::BulletEnvironment::BulletEnvironment(std::set<simulator::Part *> parts_set) : partsSet(parts_set) {
    // Set bullet constants
    this->gravity = -10.;
    this->bulletMaxSubSteps = 1000;                                  // TODO
    this->bulletFixedTimeSubStepSec = btScalar(1.) / btScalar(300.); // TODO

    // Setup bullet
    this->broadphase = new btDbvtBroadphase();

    this->collisionConfiguration = new btDefaultCollisionConfiguration();
    this->collisionDispatcher = new btCollisionDispatcher(this->collisionConfiguration);

    this->constraintSolver = new btSequentialImpulseConstraintSolver();

    this->dynamicsWorld = new btDiscreteDynamicsWorld(this->collisionDispatcher,
            this->broadphase,
            this->constraintSolver,
            this->collisionConfiguration);
    this->dynamicsWorld->setGravity(btVector3(0, 0, this->gravity));

    // This is a workaround for btDynamicsWorld::setInternalTickCallback().
    simulator::BulletEnvironment::tickCallbackPointerMap[this->dynamicsWorld] = this;

    // setInternalTickCallback() attachs a callback for internal ticks (substeps).
    // Only one callback can be attached (this is not an "observer pattern").
    // See: http://bulletphysics.org/mediawiki-1.5.8/index.php/Simulation_Tick_Callbacks
    this->dynamicsWorld->setInternalTickCallback(simulator::BulletEnvironment::tickCallback);

    // Add rigid bodies
    std::set<simulator::Part *>::iterator it;
    for(it = this->partsSet.begin() ; it != this->partsSet.end() ; it++) {
        this->dynamicsWorld->addRigidBody((*it)->getRigidBody());
    }

    // Start the user clock
    this->userStartTime = std::chrono::system_clock::now();
    
    // Init the simulation clock
    this->simulationTimeSec = 0.;
    this->simulationTimeSecTickRes = 0.;
}

simulator::BulletEnvironment::~BulletEnvironment() {
    simulator::BulletEnvironment::tickCallbackPointerMap.erase(this->dynamicsWorld);

    delete this->dynamicsWorld;

    delete this->constraintSolver;
    delete this->collisionConfiguration;
    delete this->collisionDispatcher;
    delete this->broadphase;
}

btDiscreteDynamicsWorld * simulator::BulletEnvironment::getDynamicsWorld() const {
    return this->dynamicsWorld;
}


/**
 *
 */
void simulator::BulletEnvironment::stepSimulation(const double time_step_sec) {
    this->simulationTimeSec += time_step_sec;

    btScalar bullet_time_step = btScalar(time_step_sec);
    int bullet_max_sub_steps = this->bulletMaxSubSteps;
    btScalar bullet_fixed_time_sub_step = this->bulletFixedTimeSubStepSec;

    // Warn the user if timeStep > maxSubSteps * fixedTimeStep
    // cf. http://bulletphysics.org/mediawiki-1.5.8/index.php/Stepping_The_World
    if(bullet_time_step > (bullet_max_sub_steps * bullet_fixed_time_sub_step)) {
        std::cerr << "Warning: simulation time will be lost (timeStep > maxSubSteps * fixedTimeStep)" << std::endl; // TODO: improve this message...
    }

    /*
     * getDynamicsWorld()->stepSimulation()
     * (cf. http://bulletphysics.org/mediawiki-1.5.8/index.php/Stepping_The_World)
     *
     * The first parameter is the easy one. It's simply the amount of time to
     * step the simulation by. Typically you're going to be passing it the time
     * since you last called it
     *
     * Bullet maintains an internal clock, in order to keep the actual length
     * of ticks constant. This is pivotally important for framerate
     * independence. The third parameter is the size of that internal step.
     *
     * The second parameter is the maximum number of steps that Bullet is
     * allowed to take each time you call it. If you pass a very large timeStep
     * as the first parameter [say, five times the size of the fixed internal
     * time step], then you must increase the number of maxSubSteps to
     * compensate for this, otherwise your simulation is "losing" time. 
     */
    this->getDynamicsWorld()->stepSimulation(bullet_time_step, bullet_max_sub_steps, bullet_fixed_time_sub_step);

    //// TODO: log this
    //std::cout << "Simulation time = " << this->getElapsedSimulationTimeSec() << " - ";
    //std::cout << "User time = " << this->getElapsedUserTimeSec() << " - ";
    //std::cout << "Time step = " << bullet_time_step << " - ";
    //std::cout << "Fixed sub time step = " << bullet_fixed_time_sub_step << " - ";
    //std::cout << "Sub steps = " << bullet_time_step / bullet_fixed_time_sub_step << " - ";
    //std::cout << "Max sub steps = " << bullet_max_sub_steps << std::endl;
    this->notifyTimeStep();
}


/**
 * Realtime case.
 */
void simulator::BulletEnvironment::stepSimulation() {
    // Define the static variable previous_user_time: the previous actual user time (i.e. outside the simulation).
    static std::chrono::time_point<std::chrono::system_clock> previous_user_time = std::chrono::system_clock::now();

    // Get the elapsed user time (in seconds) since the previous time step.
    std::chrono::time_point<std::chrono::system_clock> current_user_time = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds_since_previous_step = current_user_time - previous_user_time;
    double time_step_sec = elapsed_seconds_since_previous_step.count();

    // Update previous_user_time
    previous_user_time = std::chrono::system_clock::now();

    // Step simulation
    this->stepSimulation(time_step_sec);
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


void simulator::BulletEnvironment::attachTickObserver(simulator::BulletTickObserver * p_observer) {
    this->tickObserverSet.insert(p_observer);
}


void simulator::BulletEnvironment::detachTickObserver(simulator::BulletTickObserver * p_observer) {
    this->tickObserverSet.erase(p_observer);
}


void simulator::BulletEnvironment::attachTimeStepObserver(simulator::TimeStepObserver * p_observer) {
    this->timeStepObserverSet.insert(p_observer);
}


void simulator::BulletEnvironment::detachTimeStepObserver(simulator::TimeStepObserver * p_observer) {
    this->timeStepObserverSet.erase(p_observer);
}


void simulator::BulletEnvironment::notifyTick() {
    this->simulationTimeSecTickRes += this->bulletFixedTimeSubStepSec;

    std::set<simulator::BulletTickObserver *>::iterator it;
    for(it = this->tickObserverSet.begin() ; it != this->tickObserverSet.end() ; it++) {
        (*it)->update(this);
    }
}


void simulator::BulletEnvironment::notifyTimeStep() {
    std::set<simulator::TimeStepObserver *>::iterator it;
    for(it = this->timeStepObserverSet.begin() ; it != this->timeStepObserverSet.end() ; it++) {
        (*it)->update(this);
    }
}


/**
 * return the simulation time (i.e. the time within the simulation) elapsed
 * since the beginning of the simulation.
 */
double simulator::BulletEnvironment::getElapsedSimulationTimeSec() const {
    return this->simulationTimeSec;
}


/**
 * return the simulation time (i.e. the time within the simulation) elapsed
 * since the beginning of the simulation.
 */
double simulator::BulletEnvironment::getElapsedSimulationTimeSecTickRes() const {
    return this->simulationTimeSecTickRes;
}


/**
 * return the actual time (i.e. the time outside the simulation) elapsed since
 * the beginning of the simulation.
 */
double simulator::BulletEnvironment::getElapsedUserTimeSec() const {
    std::chrono::time_point<std::chrono::system_clock> current_user_time = std::chrono::system_clock::now();
    std::chrono::duration<double> elapsed_seconds = current_user_time - this->userStartTime;
    return elapsed_seconds.count();
}

/**
 * 
 */
double simulator::BulletEnvironment::getBulletFixedTimeSubStepSec() const {
    return this->bulletFixedTimeSubStepSec;
}

/**
 * 
 */
double simulator::BulletEnvironment::getBulletMaxSubSteps() const {
    return this->bulletMaxSubSteps;
}
