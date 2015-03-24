/* 
 * Bullet OSG Framework.
 * The bullet environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BULLET_ENVIRONMENT_H
#define BULLET_ENVIRONMENT_H

#include "part.h"

#include <chrono>
#include <map>
#include <set>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class BulletEnvironment;

    class BulletTickObserver {
        public:
            virtual ~BulletTickObserver() {}; 

            virtual void update(BulletEnvironment * bullet_environment) = 0;
    };


    class TimeStepObserver {
        public:
            virtual ~TimeStepObserver() {}; 

            virtual void update(BulletEnvironment * bullet_environment) = 0;
    };


    class BulletEnvironment {
        private:
            /**
             * This is a workaround for btDynamicsWorld::setInternalTickCallback().
             */
            static std::map<btDynamicsWorld *, BulletEnvironment *> tickCallbackPointerMap;

            std::set<BulletTickObserver *> tickObserverSet;
            std::set<TimeStepObserver *> timeStepObserverSet;

            btDiscreteDynamicsWorld * dynamicsWorld;
            btDbvtBroadphase * broadphase;
            btDefaultCollisionConfiguration * collisionConfiguration;
            btCollisionDispatcher * collisionDispatcher;
            btSequentialImpulseConstraintSolver * constraintSolver;

            double gravity;

            /**
             * The time within the simulation.
             */
            double simulationTimeSec;
            double simulationTimeSecTickRes;

            /**
             * The actual user start time (i.e. outside the simulation).
             */
            std::chrono::time_point<std::chrono::system_clock> userStartTime;

            int bulletMaxSubSteps;

            double bulletFixedTimeSubStepSec;

        public:
            std::set<simulator::Part *> partsSet;


        private:
            /**
             * This is a workaround for btDynamicsWorld::setInternalTickCallback().
             */
            static void tickCallback(btDynamicsWorld * world, btScalar time_step);

            void notifyTick();

            void notifyTimeStep();

        public:
            BulletEnvironment(std::set<simulator::Part *> parts_set);

            ~BulletEnvironment();

            btDiscreteDynamicsWorld * getDynamicsWorld() const;

            void stepSimulation(const double time_step_sec);

            void stepSimulation();

            void resetSimulation();

            void attachTickObserver(BulletTickObserver * p_observer);

            void detachTickObserver(BulletTickObserver * p_observer);

            void attachTimeStepObserver(TimeStepObserver * p_observer);

            void detachTimeStepObserver(TimeStepObserver * p_observer);

            /**
             * Return the time within the simulation.
             */
            double getElapsedSimulationTimeSec() const;
            double getElapsedSimulationTimeSecTickRes() const;

            /**
             * Return the actual user time i.e. outside the simulation.
             */
            double getElapsedUserTimeSec() const;
    };

}

#endif // BULLET_ENVIRONMENT_H
