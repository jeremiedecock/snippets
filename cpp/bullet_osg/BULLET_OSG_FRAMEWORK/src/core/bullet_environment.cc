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


simulator::BulletEnvironment::BulletEnvironment(
        std::set<simulator::Object *> object_set,
        std::set<simulator::Part *> part_set,
        double bullet_time_step_duration_sec,
        double bullet_tick_duration_sec,
        int bullet_max_ticks_per_time_step,
        double simulation_duration_sec) :
            objectSet(object_set),
            partSet(part_set),
            bulletTimeStepDurationSec(bullet_time_step_duration_sec),
            bulletTickDurationSec(bullet_tick_duration_sec),
            bulletMaxTicksPerTimeStep(bullet_max_ticks_per_time_step),
            simulationDurationSec(simulation_duration_sec) {

    // Set bullet constants
    this->gravity = -10.;

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

    // Add rigid bodies ///////////////
    
    // Objects
    std::set<simulator::Object *>::iterator object_it;
    std::set<simulator::Part *>::iterator part_it;
    std::set<simulator::Joint *>::iterator joint_it;

    for(object_it = this->objectSet.begin() ; object_it != this->objectSet.end() ; object_it++) {
        std::set<simulator::Part *> part_set = (*object_it)->getPartSet();
        
        /*
         * Directly adding object's parts to this->dynamicsWorld from here is
         * probably a bad idea:
         * - there are a risk to have the same part multiple times in
         *   this->ObjectSet and this->partSet;
         * - requires to update other modules like osgEnvironment (requires to
         *   add another loop to get objects parts to display for instance).
         * Instead, see the alternative method below.
         */
        //for(part_it = part_set.begin() ; part_it != part_set.end() ; part_it++) {
        //    this->dynamicsWorld->addRigidBody((*part_it)->getRigidBody());
        //}

        /*
         * Take each part of the object and add it to this->partSet.
         * This method has multiple advantages:
         * - no risk to have the same part multiple times in this->ObjectSet
         *   and this->partSet ; this->partSet is the only set of parts
         *   considered by bullet, open scene graph, ...
         * - no needs to update other modules like osgEnvironment (no need to
         *   add another loop to get objects parts to display for instance).
         */
        this->partSet.insert(part_set.begin(), part_set.end());

        /*
         * Add object's joints (i.e. Bullet's constraints).
         */
        std::set<simulator::Joint *> joint_set = (*object_it)->getJointSet();
        for(joint_it = joint_set.begin() ; joint_it != joint_set.end() ; joint_it++) {
            this->dynamicsWorld->addConstraint((*joint_it)->getBulletTypedConstraint());
        }
    }

    // Parts
    for(part_it = this->partSet.begin() ; part_it != this->partSet.end() ; part_it++) {
        std::cout << "Add " << (*part_it)->getName() << std::endl;
        this->dynamicsWorld->addRigidBody((*part_it)->getRigidBody());
    }

    // Start the user clock
    this->userStartTime = std::chrono::system_clock::now();
    
    // Init the simulation clock
    this->elapsedSimulationTimeSec = 0.;
    this->elapsedSimulationTimeSecTickRes = 0.;
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
void simulator::BulletEnvironment::run() {

    // Check some variables ///////////////////////////////
    
    // assert this->getBulletTimeStepDurationSec() > 0.
    if(this->getBulletTimeStepDurationSec() <= 0.) {
        throw std::invalid_argument("BulletEnvironment::bulletTimeStepDurationSec received a negative value. Within \"healless\" mode, this variable must receive a positive value.");
    }

    // assert this->getSimulationDurationSec() > 0.
    if(this->getSimulationDurationSec() <= 0.) {
        throw std::invalid_argument("BulletEnvironment::simulationDurationSec received a negative value. Within \"healless\" mode, this variable must receive a positive value.");
    }
    
    // Main loop (simulation loop) ////////////////////////
    
    while( this->getElapsedSimulationTimeSec() < this->getSimulationDurationSec() ) {
        // Update the physics
        this->stepSimulation(this->getBulletTimeStepDurationSec());
    }
}


/**
 *
 */
void simulator::BulletEnvironment::stepSimulation(const double time_step_duration_sec) {
    this->elapsedSimulationTimeSec += time_step_duration_sec;

    btScalar bullet_time_step_duration_sec = btScalar(time_step_duration_sec);
    btScalar bullet_tick_duration_sec = this->bulletTickDurationSec;
    int bullet_max_ticks_per_time_step = this->bulletMaxTicksPerTimeStep;

    // Warn the user if timeStepDuration > maxTicksPerTimeStep * tickDuration
    // cf. http://bulletphysics.org/mediawiki-1.5.8/index.php/Stepping_The_World
    if(bullet_time_step_duration_sec > (bullet_max_ticks_per_time_step * bullet_tick_duration_sec)) {
        std::cerr << "Warning: simulation time will be lost (timeStepDuration > maxTicksPerTimeStep * tickDuration)" << std::endl; // TODO: improve this message...
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
     * time step], then you must increase the number of maxTicksPerTimeStep to
     * compensate for this, otherwise your simulation is "losing" time. 
     */
    this->getDynamicsWorld()->stepSimulation(bullet_time_step_duration_sec, bullet_max_ticks_per_time_step, bullet_tick_duration_sec);

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
    double time_step_duration_sec = elapsed_seconds_since_previous_step.count();

    // Update previous_user_time
    previous_user_time = std::chrono::system_clock::now();

    // Step simulation
    this->stepSimulation(time_step_duration_sec);
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
    this->elapsedSimulationTimeSecTickRes += this->bulletTickDurationSec;

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
    return this->elapsedSimulationTimeSec;
}


/**
 * return the simulation time (i.e. the time within the simulation) elapsed
 * since the beginning of the simulation.
 */
double simulator::BulletEnvironment::getElapsedSimulationTimeSecTickRes() const {
    return this->elapsedSimulationTimeSecTickRes;
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
double simulator::BulletEnvironment::getBulletTimeStepDurationSec() const {
    return this->bulletTimeStepDurationSec;
}

/**
 * 
 */
double simulator::BulletEnvironment::getBulletTickDurationSec() const {
    return this->bulletTickDurationSec;
}

/**
 * 
 */
double simulator::BulletEnvironment::getBulletMaxTicksPerTimeStep() const {
    return this->bulletMaxTicksPerTimeStep;
}

/**
 * 
 */
double simulator::BulletEnvironment::getSimulationDurationSec() const {
    return this->simulationDurationSec;
}
