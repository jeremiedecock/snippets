/* 
 * Bullet OSG Framework.
 * The bullet environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_BULLET_ENVIRONMENT_H
#define BOTSIM_BULLET_ENVIRONMENT_H

#include "controller.h"
#include "joint.h"
#include "object.h"
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

            const double simulationDurationSec;

            /**
             * The time within the simulation.
             */
            double elapsedSimulationTimeSec;
            double elapsedSimulationTimeSecTickRes;

            /**
             * The actual user start time (i.e. outside the simulation).
             */
            std::chrono::time_point<std::chrono::system_clock> userStartTime;

            const double bulletTimeStepDurationSec;
            const double bulletTickDurationSec;
            const int bulletMaxTicksPerTimeStep;

        public:
            std::set<simulator::Object *> objectSet;
            std::set<simulator::Part *> partSet;
            std::set<simulator::Controller *> controllerSet;

        private:
            /**
             * This is a workaround for btDynamicsWorld::setInternalTickCallback().
             */
            static void tickCallback(btDynamicsWorld * world, btScalar time_step);

            /**
             * This function is called at each tick of this instance.
             */
            void notifyTick();

            void notifyTimeStep();

        public:
            BulletEnvironment(std::set<simulator::Object *> object_set,
                              std::set<simulator::Part *> part_set,
                              std::set<simulator::Controller *> controller_set,
                              double bullet_time_step_duration_sec=-1.0,
                              double bullet_tick_duration_sec=0.003,
                              int bullet_max_ticks_per_time_step=1000,
                              double simulation_duration_sec=-1.0);

            ~BulletEnvironment();

            btDiscreteDynamicsWorld * getDynamicsWorld() const;

            void run();

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

            /**
             * 
             */
            double getBulletTimeStepDurationSec() const;

            /**
             * 
             */
            double getBulletTickDurationSec() const;

            /**
             * 
             */
            double getBulletMaxTicksPerTimeStep() const;

            /**
             * 
             */
            double getSimulationDurationSec() const;

        private:
            /**
             * Forbid copy of instances.
             */
            BulletEnvironment(const BulletEnvironment &);

            /**
             * Forbid assignment.
             */
            BulletEnvironment & operator = (const BulletEnvironment &);
    };

}

#endif // BOTSIM_BULLET_ENVIRONMENT_H
